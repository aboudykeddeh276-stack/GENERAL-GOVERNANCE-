#!/usr/bin/env python3
"""launch.py — BRAINK live terminal interface.

Boots the full BRAINK system, runs every ops process with a live
panel display, commits results, and shows the final system dashboard.

Usage:
    python scripts/launch.py [--tick-id N]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

from virtual_brain_pc.ops_processes import PROCESS_CATALOGUE, run_single_process

console = Console()

PALETTE = {
    "PASS":    "bold green",
    "FAIL":    "bold red",
    "RUNNING": "bold yellow",
    "IDLE":    "dim white",
    "head":    "bold cyan",
    "hash":    "dim magenta",
    "lane":    "bold blue",
    "title":   "bold white",
}

OS_INFO = subprocess.check_output(["uname", "-srm"], text=True).strip()
GIT_SHA = subprocess.check_output(
    ["git", "-C", str(REPO_ROOT), "rev-parse", "--short", "HEAD"], text=True
).strip()
GIT_BRANCH = subprocess.check_output(
    ["git", "-C", str(REPO_ROOT), "rev-parse", "--abbrev-ref", "HEAD"], text=True
).strip()


# ── Banner ─────────────────────────────────────────────────────────────────

def _banner(tick_id: int) -> Panel:
    lines = Text(justify="center")
    lines.append("  B R A I N K   O P S   I N T E R F A C E  \n", style="bold cyan")
    lines.append(f"  OS        : {OS_INFO}\n", style="dim white")
    lines.append(f"  Branch    : {GIT_BRANCH}  @  {GIT_SHA}\n", style="dim white")
    lines.append(f"  Tick ID   : {tick_id}\n", style="bold white")
    lines.append(f"  Processes : {len(PROCESS_CATALOGUE)}\n", style="dim white")
    lines.append(
        f"  Time      : {datetime.now(timezone.utc).strftime('%Y-%m-%d  %H:%M:%S UTC')}",
        style="dim white",
    )
    return Panel(Align.center(lines), border_style="cyan", box=box.DOUBLE_EDGE)


# ── Process status table ────────────────────────────────────────────────────

def _build_table(results: list[dict], running_id: str | None) -> Table:
    tbl = Table(box=box.SIMPLE_HEAVY, expand=True, show_header=True)
    tbl.add_column("#",           style="dim white",  width=3,  no_wrap=True)
    tbl.add_column("PROCESS",     style="bold white",  width=32, no_wrap=True)
    tbl.add_column("LANE",        style="bold blue",   width=22, no_wrap=True)
    tbl.add_column("VER",         style="dim white",   width=6,  no_wrap=True)
    tbl.add_column("STATUS",      style="bold green",  width=9,  no_wrap=True)
    tbl.add_column("HASH",        style="dim magenta", width=16, no_wrap=True)

    result_map = {r["process_id"]: r for r in results}

    for i, proc in enumerate(PROCESS_CATALOGUE, 1):
        pid = proc.process_id
        if pid in result_map:
            r = result_map[pid]
            ok = r.get("ok", False)
            status_txt = Text("PASS" if ok else "FAIL", style=PALETTE["PASS"] if ok else PALETTE["FAIL"])
            hash_txt   = Text(r.get("process_hash", "")[:14], style=PALETTE["hash"])
        elif pid == running_id:
            status_txt = Text("RUNNING…", style=PALETTE["RUNNING"])
            hash_txt   = Text("—", style="dim white")
        else:
            status_txt = Text("IDLE",    style=PALETTE["IDLE"])
            hash_txt   = Text("—", style="dim white")

        tbl.add_row(str(i), pid, proc.lane, proc.version, status_txt, hash_txt)

    return tbl


# ── Live run ────────────────────────────────────────────────────────────────

def run_interface(tick_id: int) -> list[dict]:
    results: list[dict] = []

    with Live(console=console, refresh_per_second=12, screen=False) as live:

        def _refresh(running_id: str | None = None) -> None:
            layout = Table.grid(padding=0)
            layout.add_row(_banner(tick_id))
            layout.add_row(Rule(style="dim cyan"))
            layout.add_row(_build_table(results, running_id))
            live.update(layout)

        _refresh()
        time.sleep(0.4)

        for proc in PROCESS_CATALOGUE:
            _refresh(running_id=proc.process_id)
            time.sleep(0.15)
            result = run_single_process(proc.process_id, tick_id=tick_id)
            results.append(result)
            _refresh(running_id=None)
            time.sleep(0.1)

        # Final frame — all done
        _refresh(running_id=None)
        time.sleep(0.3)

    return results


# ── Commit results ──────────────────────────────────────────────────────────

def commit_results(results: list[dict], tick_id: int) -> None:
    OPS_DIR = REPO_ROOT / "docs" / "ops"
    OPS_DIR.mkdir(parents=True, exist_ok=True)

    GIT = ["git", "-C", str(REPO_ROOT)]

    # Ensure identity
    try:
        subprocess.check_output(GIT + ["config", "user.email"], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        subprocess.run(GIT + ["config", "user.email", "ops-bot@braink.local"], check=True)
        subprocess.run(GIT + ["config", "user.name",  "BRAINK OPS BOT"],       check=True)

    console.print()
    console.print(Rule("[bold cyan]COMMITTING PER-PROCESS RESULTS[/bold cyan]"))
    console.print()

    for r in results:
        pid   = r["process_id"]
        ok    = r.get("ok", False)
        phash = r.get("process_hash", "")[:12]
        path  = OPS_DIR / f"{pid}.json"
        path.write_text(json.dumps(r, indent=2))

        rel = str(path.relative_to(REPO_ROOT))
        subprocess.run(GIT + ["add", rel], check=True, capture_output=True)
        msg = (
            f"ops[{pid}]: tick={tick_id} status={'PASS' if ok else 'FAIL'} hash={phash}\n\n"
            f"Lane    : {r.get('lane','?')}\n"
            f"Version : {r.get('version','?')}\n"
            f"Title   : {r.get('process_title', pid)}\n"
            f"Hash    : {r.get('process_hash','')}"
        )
        subprocess.run(GIT + ["commit", "-m", msg], check=True, capture_output=True)
        sha = subprocess.check_output(GIT + ["rev-parse", "--short", "HEAD"], text=True).strip()
        status_style = "bold green" if ok else "bold red"
        console.print(
            f"  [{status_style}]{'PASS' if ok else 'FAIL'}[/{status_style}]  "
            f"[bold white]{pid:<36}[/bold white]  "
            f"[dim magenta]{phash}[/dim magenta]  "
            f"[dim]→ {sha}[/dim]"
        )

    # Manifest
    passed = [r["process_id"] for r in results if r.get("ok")]
    failed = [r["process_id"] for r in results if not r.get("ok")]
    ts = datetime.now(timezone.utc).isoformat()
    manifest = {
        "manifest_version": "OPS_MANIFEST_v1.0",
        "tick_id": tick_id,
        "timestamp": ts,
        "processes_total": len(results),
        "processes_passed": len(passed),
        "processes_failed": len(failed),
        "passed": passed,
        "failed": failed,
        "all_ok": len(failed) == 0,
        "process_hashes": {r["process_id"]: r.get("process_hash", "") for r in results},
    }
    raw = json.dumps(manifest, sort_keys=True).encode()
    manifest["manifest_hash"] = hashlib.sha256(raw).hexdigest()

    manifest_path = OPS_DIR / "OPS_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    rel_m = str(manifest_path.relative_to(REPO_ROOT))
    subprocess.run(GIT + ["add", rel_m], check=True, capture_output=True)
    msg_m = (
        f"ops[OPS_MANIFEST]: tick={tick_id} passed={len(passed)}/{len(results)}\n\n"
        f"Manifest hash : {manifest['manifest_hash']}\n"
        f"All OK        : {manifest['all_ok']}"
    )
    subprocess.run(GIT + ["commit", "-m", msg_m], check=True, capture_output=True)
    sha_m = subprocess.check_output(GIT + ["rev-parse", "--short", "HEAD"], text=True).strip()
    console.print()
    console.print(f"  [bold cyan]MANIFEST[/bold cyan]  {manifest['manifest_hash'][:16]}  [dim]→ {sha_m}[/dim]")


# ── Dashboard ───────────────────────────────────────────────────────────────

def _dashboard(results: list[dict], tick_id: int) -> None:
    console.print()
    console.print(Rule("[bold cyan]BRAINK OPS DASHBOARD[/bold cyan]"))
    console.print()

    passed = sum(1 for r in results if r.get("ok"))
    failed = len(results) - passed
    all_ok = failed == 0

    # Summary row
    summary = Table.grid(padding=(0, 4))
    summary.add_row(
        Panel(f"[bold cyan]{len(results)}[/bold cyan]\n[dim]TOTAL[/dim]",    width=18),
        Panel(f"[bold green]{passed}[/bold green]\n[dim]PASSED[/dim]",       width=18),
        Panel(f"[bold {'red' if failed else 'green'}]{failed}[/bold {'red' if failed else 'green'}]\n[dim]FAILED[/dim]", width=18),
        Panel(
            f"[bold {'green' if all_ok else 'red'}]{'ALL PASS' if all_ok else 'FAILURES'}[/bold {'green' if all_ok else 'red'}]",
            width=18,
        ),
    )
    console.print(Align.center(summary))

    # Process detail
    console.print()
    detail = Table(box=box.ROUNDED, expand=True)
    detail.add_column("PROCESS",  style="bold white",  no_wrap=True)
    detail.add_column("LANE",     style="bold blue",   no_wrap=True)
    detail.add_column("STATUS",   no_wrap=True)
    detail.add_column("HASH",     style="dim magenta", no_wrap=True)

    for r in results:
        ok = r.get("ok", False)
        detail.add_row(
            r["process_id"],
            r.get("lane", "?"),
            Text("PASS", style="bold green") if ok else Text("FAIL", style="bold red"),
            r.get("process_hash", "")[:16],
        )
    console.print(detail)

    # Git state
    git_log = subprocess.check_output(
        ["git", "-C", str(REPO_ROOT), "log", "--oneline", "-5"],
        text=True,
    ).strip()
    console.print()
    console.print(Panel(git_log, title="[bold cyan]RECENT COMMITS[/bold cyan]", border_style="cyan"))

    console.print()
    console.print(Rule(style="dim cyan"))
    console.print(
        Align.center(
            Text(
                f"TICK {tick_id} COMPLETE  ·  {passed}/{len(results)} PASSED  ·  "
                f"{datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}",
                style="bold cyan",
            )
        )
    )
    console.print()


# ── Main ────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="BRAINK live ops interface")
    parser.add_argument("--tick-id", type=int, default=2)
    args = parser.parse_args()

    console.clear()
    results = run_interface(args.tick_id)
    commit_results(results, args.tick_id)
    _dashboard(results, args.tick_id)
    return 0 if all(r.get("ok") for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
