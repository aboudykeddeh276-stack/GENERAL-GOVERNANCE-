from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Callable, Dict, List

import pathlib

from .braink_runtime import run_full_braink_lane
from .cognition import BrainInspiredController
from .core import VirtualComputer
from .governance_automation import run_governance_automation
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

# ---------------------------------------------------------------------------
# OPS PROCESS REGISTRY
# Each internal process is individually declared with:
#   - process_id   : machine-readable slug
#   - title        : human-readable name
#   - lane         : BRAINK lane classification
#   - version      : doctrine version string
#   - description  : single-sentence purpose
#   - run          : zero-argument callable, returns Dict result
# ---------------------------------------------------------------------------


@dataclass
class OpsProcess:
    process_id: str
    title: str
    lane: str
    version: str
    description: str
    run: Callable[[], Dict[str, Any]]


# ---------------------------------------------------------------------------
# Process 1 — VM_BRAIN
# Boots the VirtualComputer, loads a deterministic program, steps through
# the instruction cycle and returns the halted register snapshot together
# with a BrainInspiredController directive.
# ---------------------------------------------------------------------------
def _proc_vm_brain(tick_id: int = 0) -> Dict[str, Any]:
    vm = VirtualComputer()
    vm.load_program([1, 1, 2, 255])          # INC A, INC A, DEC A, HALT
    cycles = vm.run(max_cycles=16)
    brain = BrainInspiredController()
    directive = brain.evaluate_load(cpu_signal=0.55, mem_signal=0.40)
    snap = vm.snapshot()
    return {
        "process_id": "VM_BRAIN",
        "tick_id": tick_id,
        "cycles": cycles,
        "halted": snap["halted"],
        "register_A": snap["A"],
        "directive": directive["directive"],
        "signal": directive["signal"],
        "trace": vm.trace_log,
        "ok": snap["halted"],
    }


# ---------------------------------------------------------------------------
# Process 2 — BRAINK_RUNTIME_LANE
# Executes the full 14-step §69 BRAINK runtime lane:
# HEARTBEAT → INGESTION → SPIKE_CLASSIFY → TEMPERATURE_SPIKE →
# VOLTAGE_SPIKE → WHOLE_BIND → ACTIVE_PRESERVE → 297_BAND →
# BOUNDARY_3 → RUNTIME_TRACE → DETRIMENTAL_SPIKE →
# REALIGNMENT → PROOF_LEDGER → SIGNAL_OUTPUT
# ---------------------------------------------------------------------------
def _proc_braink_runtime(tick_id: int = 0) -> Dict[str, Any]:
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
        "process_id": "BRAINK_RUNTIME_LANE",
        "tick_id": tick_id,
        "steps_executed": len(result["runtime_lane"]),
        "steps": result["runtime_lane"],
        "output_state": result["output_state"],
        "whole_state_preserved": result["whole_state_preserved"],
        "proof_hash": result["proof_ledger"]["proof_hash"],
        "near_boundary_297": result["classification"]["near_boundary_297"],
        "boundary_3_achieved": result["classification"]["boundary_3_achieved"],
        "ok": result["whole_state_preserved"],
    }


# ---------------------------------------------------------------------------
# Process 3 — ORGANISM_CORE_PROCESS
# Runs the BRAINK organism core loop (§34):
# POWER_CORE_READ → ACTIVE_STATE_2_CROSS → INGESTION →
# CALIBRATION_RUN → THINKING_PROCESS → MIRROR_UPDATE →
# LEARNING_MIRROR_UPDATE → PROOF_LEDGER → KEDDEH_THEOREM_LEDGER →
# SIGNAL_OUTPUT
# Learning is committed only through the mirror validation lane.
# ---------------------------------------------------------------------------
def _proc_organism_core(tick_id: int = 0) -> Dict[str, Any]:
    result = run_organism_process(
        input_signal={"signal_strength": 0.88, "env": "production", "load": 0.72},
        tick_id=tick_id,
    )
    return {
        "process_id": "ORGANISM_CORE_PROCESS",
        "tick_id": tick_id,
        "steps_executed": len(result["organism_lane"]),
        "steps": result["organism_lane"],
        "organism_alive": result["organism_alive"],
        "learning_committed": result["learning_committed"],
        "theorem_compliant": result["theorem_compliant"],
        "output_state": result["output_state"],
        "ok": result["organism_alive"] and result["theorem_compliant"],
    }


# ---------------------------------------------------------------------------
# Process 4 — SPIKE_BOUNDARY_CALIBRATION
# Classifies a cpu_load spike against the safe/failure boundaries:
# SPIKE_EVENT_CLASSIFY → TEMPERATURE_SPIKE_BOUNDARY →
# VOLTAGE_SPIKE_BOUNDARY → RUNTIME_EXISTENCE_TRACE →
# DETRIMENTAL_FAILURE_SPIKE → BOUNDARY_REALIGNMENT_ENGINE →
# PROOF_LEDGER_COMMIT
# ---------------------------------------------------------------------------
def _proc_spike_calibration(tick_id: int = 0) -> Dict[str, Any]:
    result = run_spike_boundary_calibration(
        spike_kind="cpu_load",
        observed_value=82.0,
        safe_boundary=75.0,
        failure_boundary=95.0,
        environment="production",
        target_system="cpu_runtime",
    )
    return {
        "process_id": "SPIKE_BOUNDARY_CALIBRATION",
        "tick_id": tick_id,
        "spike_type": result["classification"]["spike_type"],
        "near_boundary_297": result["classification"]["near_boundary_297"],
        "boundary_3_achieved": result["classification"]["boundary_3_achieved"],
        "proof_status": result["proof_ledger"]["proof_status"],
        "proof_hash": result["proof_ledger"]["proof_hash"],
        "ok": result["proof_ledger"]["proof_status"] == "committed",
    }


# ---------------------------------------------------------------------------
# Process 5 — MATERIAL_FAILURE_CALIBRATION
# Runs the BRAINK material failure calibration lane:
# MATERIAL_WHOLE_BIND → ACTIVE_STRESS_CROSSING → BOUNDARY_PAIR_DETECT →
# NEAR_FAILURE_297_BAND → BOUNDARY_3_ACHIEVEMENT →
# FAILURE_CALIBRATION_LEDGER
# ---------------------------------------------------------------------------
def _proc_material_calibration(tick_id: int = 0) -> Dict[str, Any]:
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
        "process_id": "MATERIAL_FAILURE_CALIBRATION",
        "tick_id": tick_id,
        "whole_state_before": result["failure_event"]["whole_state_before"],
        "near_boundary_band": result["failure_event"]["near_boundary_band"],
        "achieved_boundary": result["failure_event"]["achieved_boundary"],
        "proof_status": result["proof_ledger"]["proof_status"],
        "proof_hash": result["proof_ledger"]["event_hash"],
        "ok": result["proof_ledger"]["proof_status"] == "committed",
    }


# ---------------------------------------------------------------------------
# Process 6 — ZERO_CLASSIFIER_GATE
# Exercises the zero doctrine classification pipeline:
# ZERO_CLASSIFY → ZERO_RELATION_RESOLVE → SYMBOLIC_ZERO_GATE
# Zero must be typed before it is allowed into weighted calculation.
# ---------------------------------------------------------------------------
def _proc_zero_classifier(tick_id: int = 0) -> Dict[str, Any]:
    classify = CALL_ZERO_CLASSIFY(symbol=0, context="boundary threshold origin")
    relation = CALL_ZERO_RELATION_RESOLVE(left_value=1.0, right_value=-1.0)
    gate = CALL_SYMBOLIC_ZERO_GATE(zero_frame=classify)
    return {
        "process_id": "ZERO_CLASSIFIER_GATE",
        "tick_id": tick_id,
        "zero_class": classify["zero_class"],
        "valid_for_use": classify["valid_for_use"],
        "gate_passed": gate["gate_passed"],
        "zero_produced_by_relation": relation["produced_zero"],
        "power_one_preserved": relation["power_one_preserved"],
        "ok": gate["gate_passed"] and relation["power_one_preserved"] == 1,
    }


# ---------------------------------------------------------------------------
# Process 7 — BUILD_MATRIX_PIPELINE
# Runs the uniform agent build pipeline across all three OS targets:
# linux → BuildAgent → ValidationAgent → PackagingAgent
# windows → BuildAgent → ValidationAgent → PackagingAgent
# macos → BuildAgent → ValidationAgent → PackagingAgent
# ---------------------------------------------------------------------------
def _proc_build_matrix(tick_id: int = 0) -> Dict[str, Any]:
    orchestrator = UniformBuildOrchestrator()
    result = orchestrator.build_all()
    targets = [m["target"] for m in result["matrix"]]
    statuses = [r["status"] for m in result["matrix"] for r in m["reports"]]
    all_ok = all(s == "ok" for s in statuses)
    return {
        "process_id": "BUILD_MATRIX_PIPELINE",
        "tick_id": tick_id,
        "targets": targets,
        "agents_per_target": 3,
        "reports_total": len(statuses),
        "all_agents_ok": all_ok,
        "ok": all_ok,
    }


# ---------------------------------------------------------------------------
# Process 8 — REGISTRY_INTEGRITY_CHECK
# Verifies the BRAINK registry block count is at expected capacity.
# All 39 call names must be present — a shortfall indicates a missing
# bootloader entry.
# ---------------------------------------------------------------------------
def _proc_registry_check(tick_id: int = 0) -> Dict[str, Any]:
    count = len(REGISTRY_BLOCKS)
    expected = 39
    missing = expected - count
    return {
        "process_id": "REGISTRY_INTEGRITY_CHECK",
        "tick_id": tick_id,
        "block_count": count,
        "expected": expected,
        "missing": max(0, missing),
        "ok": count >= expected,
    }


# ---------------------------------------------------------------------------
# Process catalogue — ordered execution sequence
# ---------------------------------------------------------------------------
PROCESS_CATALOGUE: List[OpsProcess] = [
    OpsProcess(
        process_id="VM_BRAIN",
        title="Virtual Machine + Brain Controller",
        lane="CORE_VM",
        version="v1.0",
        description="Boot VirtualComputer, step instruction cycle, evaluate BrainInspiredController directive.",
        run=_proc_vm_brain,
    ),
    OpsProcess(
        process_id="BRAINK_RUNTIME_LANE",
        title="BRAINK Full Runtime Lane (§69)",
        lane="BRAINK_RUNTIME",
        version="v1.4",
        description="Execute 14-step §69 BRAINK runtime lane from HEARTBEAT to SIGNAL_OUTPUT.",
        run=_proc_braink_runtime,
    ),
    OpsProcess(
        process_id="ORGANISM_CORE_PROCESS",
        title="Organism Core Process Loop (§34)",
        lane="ORGANISM_CORE",
        version="v1.5",
        description="Run power-core, thinking, mirror-update, learning, and theorem-ledger organism loop.",
        run=_proc_organism_core,
    ),
    OpsProcess(
        process_id="SPIKE_BOUNDARY_CALIBRATION",
        title="Spike Boundary Calibration Lane",
        lane="SPIKE_CALIBRATION",
        version="v1.4",
        description="Classify a spike event and commit boundary proof to the BRAINK ledger.",
        run=_proc_spike_calibration,
    ),
    OpsProcess(
        process_id="MATERIAL_FAILURE_CALIBRATION",
        title="Material Failure Calibration Lane",
        lane="MATERIAL_CALIBRATION",
        version="v1.3",
        description="Bind material whole-identity, cross stress boundary, and commit failure calibration ledger.",
        run=_proc_material_calibration,
    ),
    OpsProcess(
        process_id="ZERO_CLASSIFIER_GATE",
        title="Zero Classifier and Symbolic Gate (§7)",
        lane="ZERO_CLASSIFIER",
        version="v1.5",
        description="Classify zero, resolve relation, and pass through CALL_SYMBOLIC_ZERO_GATE.",
        run=_proc_zero_classifier,
    ),
    OpsProcess(
        process_id="BUILD_MATRIX_PIPELINE",
        title="Uniform Build Matrix Pipeline",
        lane="BUILD_MATRIX",
        version="v1.0",
        description="Run BuildAgent, ValidationAgent, PackagingAgent across linux/windows/macos.",
        run=_proc_build_matrix,
    ),
    OpsProcess(
        process_id="REGISTRY_INTEGRITY_CHECK",
        title="Registry Integrity Check",
        lane="REGISTRY",
        version="v1.6",
        description="Verify all 39 BRAINK registry call blocks are present — no missing bootloaders.",
        run=_proc_registry_check,
    ),
]

PROCESS_INDEX: Dict[str, OpsProcess] = {p.process_id: p for p in PROCESS_CATALOGUE}


# ---------------------------------------------------------------------------
# Process 9 — GOVERNANCE_AUTOMATION_ENGINE
# Executes the full 1-Keddeh Matrix Standard governance automation lifecycle:
# FILESYSTEM_TOPOLOGY_SCAN → KEDDEH_MATRIX_EVALUATION →
# DISCREPANCY_DECOMPOSITION → RESOLUTION_TELEMETRY_ARCHIVE →
# POST_MUTATION_REVERIFICATION → SUCCESSFUL_ALIGNMENT_TERMINATION
# ---------------------------------------------------------------------------
def _proc_governance_automation(tick_id: int = 0) -> Dict[str, Any]:
    repository_root_string: str = str(
        pathlib.Path(__file__).resolve().parents[2]
    )
    result = run_governance_automation(
        repository_root_absolute_path_string=repository_root_string
    )
    return {
        "process_id": "GOVERNANCE_AUTOMATION_ENGINE",
        "tick_id": tick_id,
        "execution_status": result.get("execution_status_name_string", "UNKNOWN"),
        "keddeh_matrix_alignment_verified": result.get(
            "keddeh_matrix_alignment_verified_boolean", False
        ),
        "all_governance_artifacts_present": result.get(
            "all_governance_artifacts_present_boolean", False
        ),
        "total_discrepancy_count": result.get("total_discrepancy_count_integer", -1),
        "recursive_depth_reached": result.get(
            "recursive_decomposition_depth_reached_integer", 0
        ),
        "engine_hash": result.get("engine_execution_deterministic_hash_string", ""),
        "ok": result.get("ok", False),
    }


PROCESS_CATALOGUE.append(
    OpsProcess(
        process_id="GOVERNANCE_AUTOMATION_ENGINE",
        title="1-Keddeh Matrix Governance Automation Engine",
        lane="GOVERNANCE_AUTOMATION",
        version="v1.0",
        description=(
            "Execute full 1-Keddeh Matrix Standard governance automation lifecycle: "
            "topology scan, matrix evaluation, discrepancy decomposition, resolution, "
            "and post-mutation re-verification."
        ),
        run=_proc_governance_automation,
    )
)

PROCESS_INDEX = {p.process_id: p for p in PROCESS_CATALOGUE}


def run_single_process(process_id: str, tick_id: int = 0) -> Dict[str, Any]:
    """Execute one named process by ID and return its result dict."""
    if process_id not in PROCESS_INDEX:
        raise KeyError(f"Unknown process_id: {process_id!r}. Valid: {sorted(PROCESS_INDEX)}")
    proc = PROCESS_INDEX[process_id]
    import inspect
    sig = inspect.signature(proc.run)
    if "tick_id" in sig.parameters:
        result = proc.run(tick_id=tick_id)  # type: ignore[call-arg]
    else:
        result = proc.run()
    raw = json.dumps(result, sort_keys=True).encode()
    result["process_hash"] = hashlib.sha256(raw).hexdigest()
    result["process_title"] = proc.title
    result["lane"] = proc.lane
    result["version"] = proc.version
    return result


def run_all_processes(tick_id: int = 0) -> List[Dict[str, Any]]:
    """Run every process in catalogue order and return list of results."""
    return [run_single_process(p.process_id, tick_id=tick_id) for p in PROCESS_CATALOGUE]
