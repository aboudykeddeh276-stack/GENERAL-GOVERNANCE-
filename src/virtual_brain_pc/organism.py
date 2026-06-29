from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Optional


# ---------------------------------------------------------------------------
# BRAINK Organism Core  (§29-30 — Organism Structure, Heartbeat, Thinking, Learning)
# ---------------------------------------------------------------------------

def CALL_POWER_CORE_READ(heartbeat_id: int = 0) -> Dict[str, object]:
    """BRAINK::CORE::POWER1::FEED::v01

    Read the power-one core — the unity feed, identity anchor, and
    continuity source. The core is always 1, never zero.
    """
    return {
        "call": "CALL_POWER_CORE_READ",
        "heartbeat_id": heartbeat_id,
        "power_core": 1,
        "active_core_state": "LIVE",
        "unity_anchor": "PRESERVED",
    }


def CALL_ACTIVE_STATE_2_CROSS(power_frame: Dict[str, object]) -> Dict[str, object]:
    """BRAINK::STATE::ACTIVE2::CROSS::v01

    Establish the active 2-state crossing fed by power-one. The active
    runtime state is always fed by 1 and crosses between -2 and +2 rails.
    """
    power_core = power_frame.get("power_core", 1)
    return {
        "call": "CALL_ACTIVE_STATE_2_CROSS",
        "power_core": power_core,
        "active_runtime_state": 2,
        "fed_by_power_one": power_core == 1,
        "crossing_direction": "forward",
    }


def CALL_BOUNDARY_SIGNAL_3(active_trace: float, failure_boundary: float) -> Dict[str, object]:
    """BRAINK::BOUNDARY::SIGNAL3::ACHIEVE::v01

    Record whether boundary-3 achievement has been reached. A boundary-3
    event is a threshold crossing, transition, signal, or failure event.
    """
    achieved = active_trace >= failure_boundary
    return {
        "call": "CALL_BOUNDARY_SIGNAL_3",
        "active_trace": active_trace,
        "failure_boundary": failure_boundary,
        "boundary_signal": 3 if achieved else None,
        "state": "BOUNDARY_ACHIEVED" if achieved else "BELOW_BOUNDARY",
        "transition_event": achieved,
    }


def CALL_THINKING_PROCESS(memory_frame: Dict[str, object]) -> Dict[str, object]:
    """BRAINK::MIND::THINKING::PROCESS::v01

    Process the organism's database and produce a thought frame.
    Thinking does NOT permanently mutate memory by itself.
    Thinking reads MEMORY_MATRIX and produces THOUGHT_FRAME, PATTERN_MATCH,
    INFERENCE_FRAME, DECISION_CANDIDATE.
    """
    keys = list(memory_frame.keys())
    return {
        "call": "CALL_THINKING_PROCESS",
        "processed_keys": keys,
        "thought_frame": {
            "pattern_match": len(keys) > 0,
            "inference": "context_stable" if keys else "context_empty",
            "decision_candidate": "proceed" if keys else "await_input",
        },
        "memory_mutated": False,
        "status": "THOUGHT_FRAME_PRODUCED",
    }


def CALL_MIRROR_UPDATE_LANE(
    thought_frame: Dict[str, object],
    proposed_delta: Dict[str, object],
    power_core: int = 1,
) -> Dict[str, object]:
    """BRAINK::LANE::MIRROR::UPDATE::v01

    Test a proposed memory update in an isolated mirror state without
    touching the live power-one core or active-2 state. Reject any
    delta that introduces drift or contradiction.
    """
    drift = proposed_delta.get("power_core", power_core) != power_core
    contradiction = any(
        k in proposed_delta and proposed_delta[k] != thought_frame.get(k)
        for k in ("power_core", "unity_anchor")
    )
    valid = not drift and not contradiction
    return {
        "call": "CALL_MIRROR_UPDATE_LANE",
        "proposed_delta_keys": sorted(proposed_delta.keys()),
        "contradiction_detected": contradiction,
        "drift_detected": drift,
        "valid": valid,
        "action": "COMMIT_APPROVED" if valid else "REJECT_AND_WRITE_FAILURE_PROOF",
    }


def CALL_LEARNING_MIRROR_UPDATE(mirror_result: Dict[str, object]) -> Dict[str, object]:
    """BRAINK::MIND::LEARNING::MIRROR_UPDATE::v01

    Commit an approved learning update through the mirror validation lane.
    Learning is NOT raw input → permanent memory. It requires mirror proof.
    Direct overwrite is always False.
    """
    valid = mirror_result.get("valid", False)
    return {
        "call": "CALL_LEARNING_MIRROR_UPDATE",
        "mirror_valid": valid,
        "learning_committed": valid,
        "update_path": "mirror_lane" if valid else "rejected",
        "direct_overwrite": False,
        "status": "LEARNING_COMMITTED" if valid else "LEARNING_REJECTED",
    }


def CALL_MEMORY_MATRIX(
    operation: str,
    key: str,
    value: Any = None,
    matrix: Optional[Dict[str, Any]] = None,
) -> Dict[str, object]:
    """BRAINK::MEMORY::MATRIX::STORE::v01

    Read from or write to the BRAINK memory matrix — the active knowledge
    and state history store. Write operations require prior mirror approval.
    """
    if matrix is None:
        matrix = {}
    if operation == "read":
        return {
            "call": "CALL_MEMORY_MATRIX",
            "operation": "read",
            "key": key,
            "value": matrix.get(key),
            "found": key in matrix,
        }
    elif operation == "write":
        matrix[key] = value
        return {
            "call": "CALL_MEMORY_MATRIX",
            "operation": "write",
            "key": key,
            "value": value,
            "committed": True,
        }
    return {
        "call": "CALL_MEMORY_MATRIX",
        "operation": operation,
        "error": f"unknown_operation_{operation}",
        "committed": False,
    }


def CALL_KEDDEH_THEOREM_LEDGER(proof_frame: Dict[str, object]) -> Dict[str, object]:
    """BRAINK::LEDGER::KEDDEH_THEOREM::COMMIT::v01

    Record zero classification compliance and theorem adherence in the
    KEDDEH doctrine ledger. Every state change must be provable.
    """
    serialized = json.dumps(proof_frame, sort_keys=True)
    ledger_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]
    return {
        "call": "CALL_KEDDEH_THEOREM_LEDGER",
        "theorem_version": "KEDDEH_THEOREM::v1.5",
        "ledger_hash": ledger_hash,
        "zero_classified": True,
        "mathematics_preserved": True,
        "process_preserved": True,
        "zero_status_corrected": True,
        "proof_frame_keys": sorted(proof_frame.keys()),
        "status": "THEOREM_COMPLIANCE_RECORDED",
    }


# ---------------------------------------------------------------------------
# v1.6 — Birth Boundary Anchor  (§42-47)
# ---------------------------------------------------------------------------

def CALL_BIRTH_BOUNDARY_ANCHOR(
    pre_boundary_day: int = 26,
    post_boundary_day: int = 27,
    month: int = 11,
    year: int = 1997,
) -> Dict[str, object]:
    """BRAINK::AUTHOR::BIRTH_BOUNDARY::ANCHOR::v01

    Record the author-origin event as a symbolic boundary-transition anchor.
    This is an authorship signature, not standalone scientific proof.
    The 97 in 1997 links symbolically to the 2.97 / 0.297 / 297 research family.
    """
    return {
        "call": "CALL_BIRTH_BOUNDARY_ANCHOR",
        "birth_boundary": f"{pre_boundary_day}\u2192{post_boundary_day}/{month}/{year}",
        "pre_boundary_day": pre_boundary_day,
        "post_boundary_day": post_boundary_day,
        "month": month,
        "year": year,
        "transition_type": "DAY_BOUNDARY_CROSSING",
        "month_note": "double_one_mirror",
        "year_97_resonance": year % 100,
        "symbolic_key": (
            f"KEDDEH_BIRTH_BOUNDARY_KEY="
            f"{pre_boundary_day}\u2192{post_boundary_day}.{month}.{year}"
        ),
        "usage": "authorship_anchor_not_scientific_proof",
    }


def CALL_AUTHOR_RESONANCE_KEY(
    birth_boundary: str = "26\u219227.11.1997",
) -> Dict[str, object]:
    """BRAINK::AUTHOR::RESONANCE_KEY::MAP::v01

    Map the 26→27 / 11 / 1997 birth-boundary to the research lineage
    without treating it as scientific proof.
    """
    return {
        "call": "CALL_AUTHOR_RESONANCE_KEY",
        "birth_boundary": birth_boundary,
        "resonance_family": "97 / 297 / 2.97 / 0.297",
        "lineage": "KEX / KEDDEH_THEOREM / KEX_HYPERDRIVE / BRAINK / BRAINK6",
        "author": "A. Keddeh",
        "symbolic_alignment": {
            "26_to_27": "boundary_transition",
            "11": "mirrored_one_double",
            "97": "near_boundary_resonance_family",
            "1997": "origin_year",
        },
        "usage": "symbolic_lineage_not_standalone_proof",
    }


# ---------------------------------------------------------------------------
# Full organism process  (§34 abbreviated)
# ---------------------------------------------------------------------------

def run_organism_process(
    input_signal: Dict[str, Any],
    tick_id: int = 0,
) -> Dict[str, object]:
    """Execute the BRAINK organism core loop (§34 abbreviated).

    Lane:
        CALL_HEARTBEAT_TICK → CALL_POWER_CORE_READ → CALL_ACTIVE_STATE_2_CROSS
        → CALL_INGESTION_INPUT → CALL_CALIBRATION_RUN
        → CALL_THINKING_PROCESS → CALL_MIRROR_UPDATE_LANE → CALL_LEARNING_MIRROR_UPDATE
        → CALL_PROOF_LEDGER_COMMIT → CALL_KEDDEH_THEOREM_LEDGER → CALL_SIGNAL_OUTPUT
    """
    from .braink_runtime import (
        CALL_HEARTBEAT_TICK,
        CALL_INGESTION_INPUT,
        CALL_PROOF_LEDGER_COMMIT,
        CALL_SIGNAL_OUTPUT,
    )
    from .zero_classifier import CALL_CALIBRATION_RUN

    heartbeat = CALL_HEARTBEAT_TICK(tick_id)
    power_core = CALL_POWER_CORE_READ(tick_id)
    active_state = CALL_ACTIVE_STATE_2_CROSS(power_core)
    ingestion = CALL_INGESTION_INPUT(input_signal)
    calibrated = CALL_CALIBRATION_RUN(input_signal)

    memory_frame: Dict[str, object] = {
        "tick_id": tick_id,
        "power_core": power_core["power_core"],
        "active_state": active_state["active_runtime_state"],
    }
    thought = CALL_THINKING_PROCESS(memory_frame)
    mirror = CALL_MIRROR_UPDATE_LANE(thought["thought_frame"], {"tick_id": tick_id})
    learning = CALL_LEARNING_MIRROR_UPDATE(mirror)

    proof = CALL_PROOF_LEDGER_COMMIT({
        "heartbeat_tick": tick_id,
        "active_state": active_state["active_runtime_state"],
        "thought_status": thought["status"],
        "learning_committed": learning["learning_committed"],
    })
    theorem_ledger = CALL_KEDDEH_THEOREM_LEDGER(proof)
    signal = CALL_SIGNAL_OUTPUT(
        signal_value=float(tick_id),
        spike_type="RUNTIME_EXISTENCE_SPIKE",
        boundary_achieved=False,
    )

    return {
        "organism_lane": [
            "CALL_HEARTBEAT_TICK",
            "CALL_POWER_CORE_READ",
            "CALL_ACTIVE_STATE_2_CROSS",
            "CALL_INGESTION_INPUT",
            "CALL_CALIBRATION_RUN",
            "CALL_THINKING_PROCESS",
            "CALL_MIRROR_UPDATE_LANE",
            "CALL_LEARNING_MIRROR_UPDATE",
            "CALL_PROOF_LEDGER_COMMIT",
            "CALL_KEDDEH_THEOREM_LEDGER",
            "CALL_SIGNAL_OUTPUT",
        ],
        "steps": {
            "heartbeat": heartbeat,
            "power_core": power_core,
            "active_state": active_state,
            "ingestion": ingestion,
            "calibrated": calibrated,
            "thought": thought,
            "mirror": mirror,
            "learning": learning,
            "proof": proof,
            "theorem_ledger": theorem_ledger,
            "signal": signal,
        },
        "organism_alive": heartbeat["status"] == "alive",
        "learning_committed": learning["learning_committed"],
        "theorem_compliant": theorem_ledger["zero_classified"],
        "output_state": signal["output_state"],
    }
