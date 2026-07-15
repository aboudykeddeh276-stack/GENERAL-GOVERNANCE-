#!/usr/bin/env python3
"""KEX-BRAINK V5 sector compiler and receipt-driven evolution engine."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


class CompileError(ValueError):
    pass


@dataclass(frozen=True)
class Seed:
    seed_id: str
    seed_version: str
    architect: str
    system: str
    calculus: str
    order: int
    purpose: str
    fragment: str
    word_count: int
    required: bool
    typed_state: str

    @classmethod
    def load(cls, path: Path) -> "Seed":
        data = json.loads(path.read_text(encoding="utf-8"))
        required = {
            "seed_id", "seed_version", "architect", "system", "calculus",
            "order", "purpose", "fragment", "word_count", "required", "typed_state"
        }
        missing = sorted(required - set(data))
        if missing:
            raise CompileError(f"{path}: missing seed fields {missing}")
        seed = cls(**data)
        actual = len(seed.fragment.split())
        if seed.word_count != actual:
            raise CompileError(
                f"{seed.seed_id}: declared word_count={seed.word_count}, actual={actual}"
            )
        if seed.typed_state != "Present":
            raise CompileError(f"{seed.seed_id}: typed_state must be Present")
        return seed


def load_profile(root: Path, sector_id: str) -> dict[str, Any]:
    path = root / "sectors" / sector_id / "profile.json"
    if not path.is_file():
        raise CompileError(f"profile not found for {sector_id}")
    return json.loads(path.read_text(encoding="utf-8"))


def selected_seeds(root: Path, sector_id: str) -> list[Seed]:
    profile = load_profile(root, sector_id)
    seeds = [Seed.load(root / Path(item)) for item in profile["seed_paths"]]
    ids = [seed.seed_id for seed in seeds]
    if len(ids) != len(set(ids)):
        raise CompileError(f"{sector_id}: duplicate seed IDs")
    seeds.sort(key=lambda item: (item.order, item.seed_id))
    for seed in seeds:
        if (seed.architect, seed.system, seed.calculus) != (
            profile["architect"], profile["system"], profile["calculus"]
        ):
            raise CompileError(f"{sector_id}: anchor mismatch in {seed.seed_id}")
    return seeds


def compile_sector(root: Path, sector_id: str) -> tuple[str, dict[str, Any], dict[str, Any]]:
    profile = load_profile(root, sector_id)
    seeds = selected_seeds(root, sector_id)
    instruction = "\n\n".join(seed.fragment.strip() for seed in seeds).strip() + "\n"
    actual_words = len(instruction.split())
    if actual_words != int(profile["target_words"]):
        raise CompileError(
            f"{sector_id}: compiled words={actual_words}, target={profile['target_words']}"
        )
    missing = [term for term in profile.get("required_terms", []) if term not in instruction]
    if missing:
        raise CompileError(f"{sector_id}: required terms missing {missing}")

    receipt = {
        "receipt_id": f"{sector_id}-COMPILE-V5-G1",
        "sector_id": sector_id,
        "profile_id": profile["profile_id"],
        "profile_version": profile["profile_version"],
        "parent_profile": profile["parent_profile"],
        "architect": profile["architect"],
        "system": profile["system"],
        "calculus": profile["calculus"],
        "generation": 1,
        "seed_ids": [seed.seed_id for seed in seeds],
        "seed_orders": [seed.order for seed in seeds],
        "target_words": profile["target_words"],
        "actual_words": actual_words,
        "repo_bindings": profile["repo_bindings"],
        "conceptual_systems": profile["conceptual_systems"],
        "deterministic_order": True,
        "required_terms_passed": True,
        "polygon": {
            "anchor": "1/1", "factor": "1/1", "translation": "1/1",
            "action": "1/1", "validation": "1/1", "continuity": "1/1",
            "mean": "1/1", "baseline": "49/60", "bilateral_residual": "0/1"
        },
        "promotion": "PASS",
        "status": "COMPLETED",
    }
    bundle = {
        "profile": profile,
        "instruction": instruction,
        "description": profile["description"],
        "receipt": receipt,
    }
    return instruction, receipt, bundle


def clip(value: Fraction, lower: Fraction, upper: Fraction) -> Fraction:
    return min(upper, max(lower, value))


def parse_fraction(value: str | int | float) -> Fraction:
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, float):
        return Fraction(str(value))
    return Fraction(value)


def evolve_state(state: dict[str, Any], execution_receipt: dict[str, Any]) -> dict[str, Any]:
    baseline = Fraction(49, 60)
    axes_order = ["anchor", "factor", "translation", "action", "validation", "continuity"]
    axes = {name: parse_fraction(execution_receipt["axes"][name]) for name in axes_order}
    residual = parse_fraction(execution_receipt.get("bilateral_residual", "0/1"))
    proof_product = int(execution_receipt.get("proof_product", 0))
    mean = sum(axes.values(), Fraction(0, 1)) / len(axes)
    hard_pass = (
        axes["anchor"] == 1
        and axes["validation"] == 1
        and axes["continuity"] == 1
        and mean >= baseline
        and residual == 0
        and proof_product == 1
    )

    prior_bias = {
        name: parse_fraction(state.get("bias", {}).get(name, "0/1"))
        for name in axes_order
    }
    lower, upper = Fraction(-3, 20), Fraction(3, 20)
    updated_bias = {}
    for name in axes_order:
        updated = Fraction(19, 20) * prior_bias[name] + Fraction(1, 5) * (axes[name] - baseline)
        updated_bias[name] = clip(updated, lower, upper)

    applied_bias = (
        {name: Fraction(0, 1) for name in axes_order}
        if len(set(axes.values())) == 1
        else updated_bias
    )

    result = dict(state)
    result["last_receipt_id"] = execution_receipt.get("receipt_id")
    result["last_polygon"] = {name: str(value) for name, value in axes.items()}
    result["last_polygon"].update({
        "mean": str(mean),
        "baseline": str(baseline),
        "bilateral_residual": str(residual),
    })
    result["bias"] = {name: str(value) for name, value in applied_bias.items()}

    if hard_pass:
        result["generation"] = int(state.get("generation", 1)) + 1
        result["parent_generation"] = int(state.get("generation", 1))
        result["promotion"] = "PASS"
        result["status"] = "COMPLETED"
    else:
        result["generation"] = int(state.get("generation", 1))
        result["parent_generation"] = int(state.get("parent_generation", 0))
        result["promotion"] = "REJECTED_PARENT_PRESERVED"
        result["status"] = "FAILED"
        result["correction_vector"] = {
            "anchor_gap": str(Fraction(1, 1) - axes["anchor"]),
            "validation_gap": str(Fraction(1, 1) - axes["validation"]),
            "continuity_gap": str(Fraction(1, 1) - axes["continuity"]),
            "baseline_gap": str(max(Fraction(0, 1), baseline - mean)),
            "residual": str(residual),
            "proof_gap": 1 - proof_product,
        }
    return result


def compile_all(root: Path) -> dict[str, Any]:
    registry = json.loads((root / "sector_registry.json").read_text(encoding="utf-8"))
    receipts = []
    for sector in registry["sectors"]:
        sector_id = sector["sector_id"]
        instruction, receipt, bundle = compile_sector(root, sector_id)
        compiled_dir = root / "sectors" / sector_id / "compiled"
        compiled_dir.mkdir(parents=True, exist_ok=True)
        safe = re.sub(r"[^A-Za-z0-9]+", "_", sector_id).strip("_")
        (compiled_dir / f"{safe}_AGENT_INSTRUCTION.txt").write_text(instruction, encoding="utf-8")
        (compiled_dir / "compile_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        (compiled_dir / "sector_bundle.json").write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
        (compiled_dir / "description.txt").write_text(bundle["description"].strip() + "\n", encoding="utf-8")
        receipts.append(receipt)
    result = {
        "compiler": "KEX-BRAINK-SECTOR-EVOLUTION-COMPILER-V5",
        "sector_count": len(receipts),
        "compiled": len(receipts),
        "failed": 0,
        "status": "COMPLETED",
        "receipts": receipts,
    }
    (root / "receipts" / "compile_all_receipt.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile and evolve KEX-BRAINK sector packages.")
    parser.add_argument("--root", default=".")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("compile-all")
    compile_one = sub.add_parser("compile-sector")
    compile_one.add_argument("sector_id")
    evolve = sub.add_parser("evolve-sector")
    evolve.add_argument("sector_id")
    evolve.add_argument("--receipt", required=True)
    args = parser.parse_args()
    root = Path(args.root).resolve()

    if args.command == "compile-all":
        print(json.dumps(compile_all(root), indent=2))
        return 0
    if args.command == "compile-sector":
        instruction, receipt, bundle = compile_sector(root, args.sector_id)
        compiled_dir = root / "sectors" / args.sector_id / "compiled"
        compiled_dir.mkdir(parents=True, exist_ok=True)
        (compiled_dir / "AGENT_INSTRUCTION.txt").write_text(instruction, encoding="utf-8")
        (compiled_dir / "compile_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        (compiled_dir / "sector_bundle.json").write_text(json.dumps(bundle, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(receipt, indent=2))
        return 0

    state_path = root / "sectors" / args.sector_id / "evolution_state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    receipt = json.loads(Path(args.receipt).read_text(encoding="utf-8"))
    evolved = evolve_state(state, receipt)
    state_path.write_text(json.dumps(evolved, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(evolved, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
