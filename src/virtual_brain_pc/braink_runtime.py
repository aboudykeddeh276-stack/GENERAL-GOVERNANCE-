from __future__ import annotations

import hashlib
import json
from typing import Any, Dict


# ---------------------------------------------------------------------------
# BRAINK Core Lane Primitives  (§69 full runtime lane – preamble + postamble)
# ---------------------------------------------------------------------------

def CALL_HEARTBEAT_TICK(tick_id: int = 0) -> Dict[str, object]:
    """Step 1 — Emit a heartbeat confirming ACTIVE_CORE_1 is alive."""
    return {
        "call": "CALL_HEARTBEAT_TICK",
        "tick_id": tick_id,
        "active_core": 1,
        "status": "alive",
    }


def CALL_INGESTION_INPUT(payload: Dict[str, Any]) -> Dict[str, object]:
    """Step 2 — Ingest raw input into the BRAINK runtime for processing."""
    return {
        "call": "CALL_INGESTION_INPUT",
        "ingested_keys": sorted(payload.keys()),
        "payload_size": len(payload),
        "status": "ingested",
    }


def CALL_WHOLE_ONE_BIND(system: str, environment: str) -> Dict[str, object]:
    """Step 6 — Bind the 1-whole identity of the target system in its environment."""
    return {
        "call": "CALL_WHOLE_ONE_BIND",
        "system": system,
        "environment": environment,
        "active_whole_before": 1,
        "whole_state": "bound",
    }


def CALL_ACTIVE_VALUE_PRESERVE(
    active_value: float,
    lower_boundary: float,
    upper_boundary: float,
) -> Dict[str, object]:
    """Step 7 — Verify that the active 2-state value is preserved within -2/+2 rails."""
    preserved = lower_boundary <= active_value <= upper_boundary
    return {
        "call": "CALL_ACTIVE_VALUE_PRESERVE",
        "active_value": active_value,
        "lower_boundary": lower_boundary,
        "upper_boundary": upper_boundary,
        "active_runtime_state": 2,
        "preserved": preserved,
    }


def CALL_PROOF_LEDGER_COMMIT(ledger_entry: Dict[str, object]) -> Dict[str, object]:
    """Step 13 — Commit a proof entry to the BRAINK ledger with a deterministic hash."""
    serialized = json.dumps(ledger_entry, sort_keys=True)
    proof_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]
    return {
        "call": "CALL_PROOF_LEDGER_COMMIT",
        "proof_hash": proof_hash,
        "proof_status": "committed",
        "entry": ledger_entry,
    }


def CALL_SIGNAL_OUTPUT(
    signal_value: float,
    spike_type: str,
    boundary_achieved: bool,
) -> Dict[str, object]:
    """Step 14 — Emit the final BRAINK signal after all boundary processing.

    Output state is 3 if boundary was achieved (transition), otherwise 2 (active runtime).
    Zero is symbolic only and never carries live active weight.
    """
    return {
        "call": "CALL_SIGNAL_OUTPUT",
        "signal_value": round(signal_value, 4),
        "spike_type": spike_type,
        "boundary_achieved": boundary_achieved,
        "output_state": 3 if boundary_achieved else 2,
        "symbolic_zero": None,
    }


# ---------------------------------------------------------------------------
# Full 14-step BRAINK Runtime Lane  (§69)
# ---------------------------------------------------------------------------

def run_full_braink_lane(
    tick_id: int,
    system: str,
    environment: str,
    spike_kind: str,
    observed_value: float,
    safe_boundary: float,
    failure_boundary: float,
) -> Dict[str, object]:
    """Execute the complete 14-step BRAINK runtime lane defined in §69.

    Steps 1-2   : heartbeat + ingestion (this module)
    Steps 3-12  : spike classification + boundary evaluation (spike_calibration)
    Steps 6-7   : whole-one-bind + active-value-preserve (this module, interleaved)
    Steps 13-14 : proof-ledger-commit + signal-output (this module)
    """
    from .spike_calibration import run_spike_boundary_calibration

    # Steps 1-2: BRAINK core preamble
    heartbeat = CALL_HEARTBEAT_TICK(tick_id)
    ingestion = CALL_INGESTION_INPUT({
        "system": system,
        "environment": environment,
        "spike_kind": spike_kind,
        "observed_value": observed_value,
        "safe_boundary": safe_boundary,
        "failure_boundary": failure_boundary,
    })

    # Steps 3-12: spike calibration lane (classify, temp/volt boundary,
    #             near-297, boundary-3, existence-trace, detrimental,
    #             realignment engine)
    spike_result = run_spike_boundary_calibration(
        spike_kind=spike_kind,
        observed_value=observed_value,
        safe_boundary=safe_boundary,
        failure_boundary=failure_boundary,
        environment=environment,
        target_system=system,
    )

    # Steps 6-7: whole-one-bind and active-value-preserve
    # Active 2-state is preserved as long as observed_value stays below the
    # failure_boundary; the near-boundary band (safe→failure) is still active.
    whole_bind = CALL_WHOLE_ONE_BIND(system, environment)
    active_preserve = CALL_ACTIVE_VALUE_PRESERVE(
        active_value=observed_value,
        lower_boundary=0.0,
        upper_boundary=failure_boundary,
    )

    # Step 13: proof ledger commit (independent hash over the failure_spike frame)
    proof_commit = CALL_PROOF_LEDGER_COMMIT(spike_result["failure_spike"])

    # Step 14: signal output
    signal_out = CALL_SIGNAL_OUTPUT(
        signal_value=observed_value,
        spike_type=spike_result["classification"]["spike_type"],
        boundary_achieved=spike_result["classification"]["boundary_3_achieved"],
    )

    return {
        "runtime_lane": [
            "CALL_HEARTBEAT_TICK",
            "CALL_INGESTION_INPUT",
            "CALL_SPIKE_EVENT_CLASSIFY",
            "CALL_TEMPERATURE_SPIKE_BOUNDARY",
            "CALL_VOLTAGE_SPIKE_BOUNDARY",
            "CALL_WHOLE_ONE_BIND",
            "CALL_ACTIVE_VALUE_PRESERVE",
            "CALL_NEAR_FAILURE_297_BAND",
            "CALL_BOUNDARY_3_ACHIEVEMENT",
            "CALL_RUNTIME_EXISTENCE_TRACE",
            "CALL_DETRIMENTAL_FAILURE_SPIKE",
            "CALL_BOUNDARY_REALIGNMENT_ENGINE",
            "CALL_PROOF_LEDGER_COMMIT",
            "CALL_SIGNAL_OUTPUT",
        ],
        "steps": {
            "heartbeat": heartbeat,
            "ingestion": ingestion,
            "spike_lane": spike_result["lane"],
            "whole_bind": whole_bind,
            "active_preserve": active_preserve,
            "proof_commit": proof_commit,
            "signal_output": signal_out,
        },
        "classification": spike_result["classification"],
        "ratios": spike_result["ratios"],
        "failure_spike": spike_result["failure_spike"],
        "proof_ledger": proof_commit,
        "whole_state_preserved": active_preserve["preserved"],
        "output_state": signal_out["output_state"],
    }
