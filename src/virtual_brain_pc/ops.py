from __future__ import annotations

import hashlib
import json
from typing import Any, Dict

from .braink_runtime import run_full_braink_lane
from .cognition import BrainInspiredController
from .core import VirtualComputer
from .material_calibration import run_material_failure_calibration
from .organism import run_organism_process
from .orchestrator import UniformBuildOrchestrator
from .registry import REGISTRY_BLOCKS
from .spike_calibration import run_spike_boundary_calibration
from .zero_classifier import (
    CALL_SYMBOLIC_ZERO_GATE,
    CALL_ZERO_CLASSIFY,
    CALL_ZERO_RELATION_RESOLVE,
)
from .naming_protocol import (
    FUNCTION_NAMING_PROTOCOL_EXECUTE_SYSTEM_WIDE_IDENTIFIER_SWEEP_AND_EMIT_PROOF_RECORD,
)
from .iterative_resolution_engine import (
    FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_BUILT_IN_SELF_TEST_WITH_CONTROLLED_SCENARIO,
)
from .agent_directive_dispatcher import (
    FUNCTION_AGENT_DIRECTIVE_DISPATCHER_BUILD_STANDARD_DIRECTIVE_ASSIGNMENTS_FOR_ALL_SEVEN_AGENTS,
    FUNCTION_AGENT_DIRECTIVE_DISPATCHER_EXECUTE_ALL_AGENT_DIRECTIVES_IN_SEQUENCE,
)
from .automation_protocol import (
    FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_COMPLETE_GOVERNANCE_CYCLE,
    FUNCTION_AUTOMATION_PROTOCOL_SERIALIZE_GOVERNANCE_CYCLE_RESULT_TO_DICT,
)

# ---------------------------------------------------------------------------
# Internal Ops Runner  — executes every lane in sequence and produces a
# single comprehensive status report for the BRAINK system.
# ---------------------------------------------------------------------------

OPS_VERSION = "INTERNAL_OPS_v1.0"


def _run_vm_lane(tick_id: int) -> Dict[str, Any]:
    vm = VirtualComputer()
    vm.load_program([1, 1, 2, 255])
    cycles = vm.run(max_cycles=16)
    brain = BrainInspiredController()
    directive = brain.evaluate_load(cpu_signal=0.55, mem_signal=0.40)
    return {
        "lane": "VM_BRAIN",
        "cycles": cycles,
        "halted": vm.snapshot()["halted"],
        "register_A": vm.snapshot()["A"],
        "directive": directive["directive"],
        "trace": vm.trace_log,
        "ok": vm.snapshot()["halted"],
    }


def _run_braink_lane(tick_id: int) -> Dict[str, Any]:
    result = run_full_braink_lane(
        tick_id=tick_id,
        system="cpu_runtime",
        environment="production",
        spike_kind="temperature",
        observed_value=97.0,
        safe_boundary=90.0,
        failure_boundary=100.0,
    )
    return {
        "lane": "BRAINK_RUNTIME",
        "output_state": result["output_state"],
        "whole_state_preserved": result["whole_state_preserved"],
        "proof_hash": result["proof_ledger"]["proof_hash"],
        "steps_executed": len(result["runtime_lane"]),
        "ok": result["whole_state_preserved"],
    }


def _run_organism_lane(tick_id: int) -> Dict[str, Any]:
    result = run_organism_process(
        input_signal={"signal_strength": 0.88, "env": "production", "load": 0.72},
        tick_id=tick_id,
    )
    return {
        "lane": "ORGANISM_CORE",
        "organism_alive": result["organism_alive"],
        "learning_committed": result["learning_committed"],
        "theorem_compliant": result["theorem_compliant"],
        "output_state": result["output_state"],
        "steps_executed": len(result["organism_lane"]),
        "ok": result["organism_alive"] and result["theorem_compliant"],
    }


def _run_spike_lane(tick_id: int) -> Dict[str, Any]:
    result = run_spike_boundary_calibration(
        spike_kind="cpu_load",
        observed_value=82.0,
        safe_boundary=75.0,
        failure_boundary=95.0,
        environment="production",
        target_system="cpu_runtime",
    )
    return {
        "lane": "SPIKE_CALIBRATION",
        "spike_type": result["classification"]["spike_type"],
        "boundary_3_achieved": result["classification"]["boundary_3_achieved"],
        "proof_status": result["proof_ledger"]["proof_status"],
        "proof_hash": result["proof_ledger"]["proof_hash"],
        "ok": result["proof_ledger"]["proof_status"] == "committed",
    }


def _run_material_lane(tick_id: int) -> Dict[str, Any]:
    result = run_material_failure_calibration(
        material="alloy_frame",
        environment="production",
        whole_identity="frame_integrity",
        force_value=88.5,
        lower_boundary=-100.0,
        upper_boundary=100.0,
        force_kind="stress",
    )
    return {
        "lane": "MATERIAL_CALIBRATION",
        "whole_state_before": result["failure_event"]["whole_state_before"],
        "proof_status": result["proof_ledger"]["proof_status"],
        "proof_hash": result["proof_ledger"]["event_hash"],
        "ok": result["proof_ledger"]["proof_status"] == "committed",
    }


def _run_zero_classifier_lane() -> Dict[str, Any]:
    classify = CALL_ZERO_CLASSIFY(symbol=0, context="boundary threshold origin")
    relation = CALL_ZERO_RELATION_RESOLVE(left_value=1.0, right_value=-1.0)
    gate = CALL_SYMBOLIC_ZERO_GATE(zero_frame=classify)
    return {
        "lane": "ZERO_CLASSIFIER",
        "zero_class": classify["zero_class"],
        "gate_passed": gate["gate_passed"],
        "zero_produced": relation["produced_zero"],
        "power_one_preserved": relation["power_one_preserved"],
        "ok": gate["gate_passed"] and relation["power_one_preserved"] == 1,
    }


def _run_build_matrix_lane() -> Dict[str, Any]:
    orchestrator = UniformBuildOrchestrator()
    result = orchestrator.build_all()
    targets = [m["target"] for m in result["matrix"]]
    statuses = [
        r["status"]
        for m in result["matrix"]
        for r in m["reports"]
    ]
    all_ok = all(s == "ok" for s in statuses)
    return {
        "lane": "BUILD_MATRIX",
        "targets": targets,
        "report_count": len(statuses),
        "all_agents_ok": all_ok,
        "ok": all_ok,
    }


def _run_registry_check() -> Dict[str, Any]:
    count = len(REGISTRY_BLOCKS)
    return {
        "lane": "REGISTRY_CHECK",
        "block_count": count,
        "expected": 39,
        "ok": count >= 39,
    }


def _run_naming_protocol_sweep() -> Dict[str, Any]:
    result = FUNCTION_NAMING_PROTOCOL_EXECUTE_SYSTEM_WIDE_IDENTIFIER_SWEEP_AND_EMIT_PROOF_RECORD()
    return {
        "lane": "NAMING_PROTOCOL",
        "sweep_state": result["state"],
        "compliant_count": result["compliant_identifier_count"],
        "non_compliant_count": result["non_compliant_identifier_count"],
        "aggregate_proof_hash": result["aggregate_proof_hash"],
        "ok": result["state"] == "STATE_COMPLETED",
    }


def _run_iterative_resolution_self_test() -> Dict[str, Any]:
    result = (
        FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_BUILT_IN_SELF_TEST_WITH_CONTROLLED_SCENARIO()
    )
    return {
        "lane": "ITERATIVE_RESOLUTION",
        "test_passed": result["test_passed"],
        "protocol_state": result["protocol_state"],
        "total_steps_executed": result["total_steps_executed"],
        "aggregate_proof_hash": result["aggregate_proof_hash"],
        "ok": result["ok"],
    }


def _run_agent_directive_sweep() -> Dict[str, Any]:
    assignments = (
        FUNCTION_AGENT_DIRECTIVE_DISPATCHER_BUILD_STANDARD_DIRECTIVE_ASSIGNMENTS_FOR_ALL_SEVEN_AGENTS(
            target_platform="linux"
        )
    )
    dispatch_result = FUNCTION_AGENT_DIRECTIVE_DISPATCHER_EXECUTE_ALL_AGENT_DIRECTIVES_IN_SEQUENCE(
        assignments
    )
    return {
        "lane": "AGENT_DISPATCHER",
        "total_dispatched": dispatch_result.total_directives_dispatched,
        "total_completed": dispatch_result.total_directives_completed,
        "failover_activations": dispatch_result.total_failover_activations,
        "ok": dispatch_result.all_directives_completed,
    }


def _run_automation_protocol_cycle(tick_id: int) -> Dict[str, Any]:
    cycle_result = FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_COMPLETE_GOVERNANCE_CYCLE(
        tick_id=tick_id,
        target_platform="linux",
    )
    serialised = FUNCTION_AUTOMATION_PROTOCOL_SERIALIZE_GOVERNANCE_CYCLE_RESULT_TO_DICT(
        cycle_result
    )
    return {
        "lane": "AUTOMATION_PROTOCOL",
        "cycle_state": serialised["cycle_state"],
        "cycle_all_subsystems_passed": serialised["cycle_all_subsystems_passed"],
        "aggregate_cycle_proof_hash": serialised["aggregate_cycle_proof_hash"],
        "ok": serialised["ok"],
    }


def run_internal_ops(tick_id: int = 0) -> Dict[str, Any]:
    """Execute every internal operational lane in sequence.

    Returns a comprehensive status report covering all BRAINK system lanes.
    The `ops_hash` is a deterministic SHA-256 fingerprint of the core results.
    """
    lanes: Dict[str, Any] = {}

    lanes["vm_brain"] = _run_vm_lane(tick_id)
    lanes["braink_runtime"] = _run_braink_lane(tick_id)
    lanes["organism_core"] = _run_organism_lane(tick_id)
    lanes["spike_calibration"] = _run_spike_lane(tick_id)
    lanes["material_calibration"] = _run_material_lane(tick_id)
    lanes["zero_classifier"] = _run_zero_classifier_lane()
    lanes["build_matrix"] = _run_build_matrix_lane()
    lanes["registry_check"] = _run_registry_check()
    lanes["naming_protocol"] = _run_naming_protocol_sweep()
    lanes["iterative_resolution"] = _run_iterative_resolution_self_test()
    lanes["agent_dispatcher"] = _run_agent_directive_sweep()
    lanes["automation_protocol"] = _run_automation_protocol_cycle(tick_id)

    passed = [k for k, v in lanes.items() if v.get("ok")]
    failed = [k for k, v in lanes.items() if not v.get("ok")]

    summary = {
        "ops_version": OPS_VERSION,
        "tick_id": tick_id,
        "lanes_total": len(lanes),
        "lanes_passed": len(passed),
        "lanes_failed": len(failed),
        "passed": passed,
        "failed": failed,
        "all_ok": len(failed) == 0,
    }

    # deterministic fingerprint over the summary
    raw = json.dumps(summary, sort_keys=True).encode()
    summary["ops_hash"] = hashlib.sha256(raw).hexdigest()

    return {
        "summary": summary,
        "lanes": lanes,
    }
