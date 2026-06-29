#!/usr/bin/env python3
"""auto_ops_commit.py — Automated per-process ops runner and git committer.

Runs every process in PROCESS_CATALOGUE individually, saves its result JSON
to docs/ops/<process_id>.json, then issues a dedicated git commit for each.
After all per-process commits, writes docs/ops/OPS_MANIFEST.json and commits
that as the final merge record.

Usage:
    python scripts/auto_ops_commit.py [--tick-id N] [--dry-run]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

# Ensure src/ is on sys.path when run as a script
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from virtual_brain_pc.ops_processes import PROCESS_CATALOGUE, run_single_process  # noqa: E402

OPS_DIR = REPO_ROOT / "docs" / "ops"
GIT = ["git", "-C", str(REPO_ROOT)]


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def _git(*args: str, dry_run: bool = False) -> str:
    cmd = GIT + list(args)
    if dry_run:
        print(f"  [DRY-RUN] {' '.join(cmd)}")
        return ""
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()


def _git_config_identity() -> None:
    """Ensure git author identity is set (needed in CI/codespace)."""
    try:
        _git("config", "user.email")
    except subprocess.CalledProcessError:
        subprocess.run(
            GIT + ["config", "user.email", "ops-bot@braink.local"],
            check=True,
        )
        subprocess.run(
            GIT + ["config", "user.name", "BRAINK OPS BOT"],
            check=True,
        )


# ---------------------------------------------------------------------------
# Per-process commit
# ---------------------------------------------------------------------------

def run_and_commit_process(
    process_id: str,
    tick_id: int,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Run one process, save its output, and commit it individually."""
    print(f"\n{'─'*60}")
    print(f"  PROCESS  : {process_id}")

    result = run_single_process(process_id, tick_id=tick_id)
    status = "PASS" if result.get("ok") else "FAIL"
    proc_hash = result["process_hash"][:12]

    print(f"  STATUS   : {status}")
    print(f"  HASH     : {proc_hash}")
    print(f"  LANE     : {result.get('lane', '?')}")
    print(f"  VERSION  : {result.get('version', '?')}")

    # Save to docs/ops/
    OPS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OPS_DIR / f"{process_id}.json"
    out_path.write_text(json.dumps(result, indent=2))
    print(f"  SAVED    : {out_path.relative_to(REPO_ROOT)}")

    # Stage and commit
    _git("add", str(out_path.relative_to(REPO_ROOT)), dry_run=dry_run)

    commit_msg = (
        f"ops[{process_id}]: tick={tick_id} status={status} hash={proc_hash}\n\n"
        f"Lane    : {result.get('lane', '?')}\n"
        f"Version : {result.get('version', '?')}\n"
        f"Title   : {result.get('process_title', process_id)}\n"
        f"Hash    : {result['process_hash']}"
    )
    _git("commit", "-m", commit_msg, dry_run=dry_run)
    if not dry_run:
        sha = _git("rev-parse", "--short", "HEAD")
        print(f"  COMMIT   : {sha}")

    return result


# ---------------------------------------------------------------------------
# OPS manifest (final commit)
# ---------------------------------------------------------------------------

def write_ops_manifest(
    results: List[Dict[str, Any]],
    tick_id: int,
    dry_run: bool = False,
) -> None:
    passed = [r["process_id"] for r in results if r.get("ok")]
    failed = [r["process_id"] for r in results if not r.get("ok")]
    ts = datetime.now(timezone.utc).isoformat()

    manifest: Dict[str, Any] = {
        "manifest_version": "OPS_MANIFEST_v1.0",
        "tick_id": tick_id,
        "timestamp": ts,
        "processes_total": len(results),
        "processes_passed": len(passed),
        "processes_failed": len(failed),
        "passed": passed,
        "failed": failed,
        "all_ok": len(failed) == 0,
        "process_hashes": {r["process_id"]: r["process_hash"] for r in results},
    }
    raw = json.dumps(manifest, sort_keys=True).encode()
    manifest["manifest_hash"] = hashlib.sha256(raw).hexdigest()

    OPS_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = OPS_DIR / "OPS_MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))

    print(f"\n{'═'*60}")
    print(f"  MANIFEST : {manifest_path.relative_to(REPO_ROOT)}")
    print(f"  TICK_ID  : {tick_id}")
    print(f"  PASSED   : {len(passed)}/{len(results)}")
    print(f"  HASH     : {manifest['manifest_hash'][:16]}")

    _git("add", str(manifest_path.relative_to(REPO_ROOT)), dry_run=dry_run)
    commit_msg = (
        f"ops[OPS_MANIFEST]: tick={tick_id} passed={len(passed)}/{len(results)}\n\n"
        f"Manifest hash : {manifest['manifest_hash']}\n"
        f"Timestamp     : {ts}\n"
        f"All OK        : {manifest['all_ok']}"
    )
    _git("commit", "-m", commit_msg, dry_run=dry_run)
    if not dry_run:
        sha = _git("rev-parse", "--short", "HEAD")
        print(f"  COMMIT   : {sha}")


# ---------------------------------------------------------------------------
# CLI entry
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="BRAINK automated ops commit runner")
    parser.add_argument("--tick-id", type=int, default=0, help="Ops tick identifier")
    parser.add_argument("--dry-run", action="store_true", help="Run without committing")
    args = parser.parse_args()

    print(f"\n{'═'*60}")
    print(f"  BRAINK AUTO-OPS COMMIT — tick_id={args.tick_id}")
    print(f"  Processes : {len(PROCESS_CATALOGUE)}")
    print(f"  Dry-run   : {args.dry_run}")
    print(f"{'═'*60}")

    if not args.dry_run:
        _git_config_identity()

    results: List[Dict[str, Any]] = []
    for proc in PROCESS_CATALOGUE:
        result = run_and_commit_process(proc.process_id, args.tick_id, dry_run=args.dry_run)
        results.append(result)

    write_ops_manifest(results, args.tick_id, dry_run=args.dry_run)

    all_ok = all(r.get("ok") for r in results)
    print(f"\n  FINAL STATUS: {'ALL PASS' if all_ok else 'FAILURES DETECTED'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
