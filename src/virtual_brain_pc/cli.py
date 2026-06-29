from __future__ import annotations

import argparse
import json
from typing import List

from .cognition import BrainInspiredController
from .core import VirtualComputer
from .material_calibration import run_material_failure_calibration
from .orchestrator import SUPPORTED_TARGETS, UniformBuildOrchestrator
from .registry import REGISTRY_BLOCKS
from .spike_calibration import run_spike_boundary_calibration


def _run_virtual_machine(cycles: int) -> dict:
    vm = VirtualComputer()
    brain = BrainInspiredController()

    # Program: INC A, INC A, DEC A, HALT
    vm.load_program([1, 1, 2, 255])
    completed = vm.run(max_cycles=cycles)
    stats = brain.evaluate_load(cpu_signal=0.55, mem_signal=0.40)

    return {
        "cycles": completed,
        "vm_snapshot": vm.snapshot(),
        "brain_directive": stats,
        "trace": vm.trace_log,
    }


def _build(target: str) -> dict:
    orchestrator = UniformBuildOrchestrator()
    return orchestrator.build_target(target)


def _build_all() -> dict:
    orchestrator = UniformBuildOrchestrator(targets=SUPPORTED_TARGETS)
    return orchestrator.build_all()


def _material_calibrate(
    material: str,
    environment: str,
    whole_identity: str,
    force: float,
    lower: float,
    upper: float,
    force_kind: str,
) -> dict:
    return run_material_failure_calibration(
        material=material,
        environment=environment,
        whole_identity=whole_identity,
        force_value=force,
        lower_boundary=lower,
        upper_boundary=upper,
        force_kind=force_kind,
    )


def _registry() -> dict:
    return {"registry": REGISTRY_BLOCKS}


def _spike_calibrate(
    spike_kind: str,
    observed_value: float,
    safe_boundary: float,
    failure_boundary: float,
    environment: str,
    target_system: str,
) -> dict:
    return run_spike_boundary_calibration(
        spike_kind=spike_kind,
        observed_value=observed_value,
        safe_boundary=safe_boundary,
        failure_boundary=failure_boundary,
        environment=environment,
        target_system=target_system,
    )


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Virtual Brain PC CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    run_cmd = sub.add_parser("run", help="Run the virtualized computer")
    run_cmd.add_argument("--cycles", type=int, default=16)

    build_cmd = sub.add_parser("build", help="Run agent pipeline for one target")
    build_cmd.add_argument("--target", choices=SUPPORTED_TARGETS + ["local"], default="local")

    sub.add_parser("build-all", help="Run uniform agent pipeline for all targets")

    material_cmd = sub.add_parser(
        "material-calibrate",
        help="Run BRAINK material failure calibration runtime lane",
    )
    material_cmd.add_argument("--material", default="steel_beam")
    material_cmd.add_argument("--environment", default="ambient_lab")
    material_cmd.add_argument("--whole-identity", default="beam_integrity")
    material_cmd.add_argument("--force", type=float, default=97.0)
    material_cmd.add_argument("--lower", type=float, default=-100.0)
    material_cmd.add_argument("--upper", type=float, default=100.0)
    material_cmd.add_argument("--force-kind", default="stress")

    spike_cmd = sub.add_parser(
        "spike-calibrate",
        help="Run BRAINK spike boundary calibration lane",
    )
    spike_cmd.add_argument(
        "--spike-kind",
        choices=["temperature", "voltage", "stress", "runtime", "signal"],
        default="temperature",
    )
    spike_cmd.add_argument("--observed-value", type=float, default=97.0)
    spike_cmd.add_argument("--safe-boundary", type=float, default=90.0)
    spike_cmd.add_argument("--failure-boundary", type=float, default=100.0)
    spike_cmd.add_argument("--environment", default="ambient_lab")
    spike_cmd.add_argument("--target-system", default="cpu_runtime")

    sub.add_parser("registry", help="Print BRAINK registry blocks")

    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "run":
        result = _run_virtual_machine(args.cycles)
    elif args.command == "build":
        result = _build(args.target)
    elif args.command == "build-all":
        result = _build_all()
    elif args.command == "material-calibrate":
        result = _material_calibrate(
            material=args.material,
            environment=args.environment,
            whole_identity=args.whole_identity,
            force=args.force,
            lower=args.lower,
            upper=args.upper,
            force_kind=args.force_kind,
        )
    elif args.command == "registry":
        result = _registry()
    elif args.command == "spike-calibrate":
        result = _spike_calibrate(
            spike_kind=args.spike_kind,
            observed_value=args.observed_value,
            safe_boundary=args.safe_boundary,
            failure_boundary=args.failure_boundary,
            environment=args.environment,
            target_system=args.target_system,
        )
    else:
        raise ValueError(f"Unknown command: {args.command}")

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
