from __future__ import annotations

import hashlib
import json
from typing import Dict, Literal


SpikeKind = Literal["temperature", "voltage", "stress", "runtime", "signal"]


def CALL_SPIKE_EVENT_CLASSIFY(spike_kind: SpikeKind, observed_value: float) -> Dict[str, object]:
    return {
        "call": "CALL_SPIKE_EVENT_CLASSIFY",
        "spike_kind": spike_kind,
        "observed_value": observed_value,
        "classification": "boundary_signal",
    }


def CALL_TEMPERATURE_SPIKE_BOUNDARY(
    temperature: float,
    safe_boundary: float,
    failure_boundary: float,
) -> Dict[str, object]:
    if temperature < safe_boundary:
        status = "runtime_safe"
    elif safe_boundary <= temperature < failure_boundary:
        status = "near_boundary"
    else:
        status = "failure_calibrating"

    return {
        "call": "CALL_TEMPERATURE_SPIKE_BOUNDARY",
        "status": status,
        "temperature": temperature,
        "safe_boundary": safe_boundary,
        "failure_boundary": failure_boundary,
    }


def CALL_VOLTAGE_SPIKE_BOUNDARY(
    voltage: float,
    safe_boundary: float,
    failure_boundary: float,
) -> Dict[str, object]:
    if voltage <= safe_boundary:
        status = "runtime_safe"
    elif safe_boundary < voltage < failure_boundary:
        status = "near_boundary"
    else:
        status = "failure_calibrating"

    return {
        "call": "CALL_VOLTAGE_SPIKE_BOUNDARY",
        "status": status,
        "voltage": voltage,
        "safe_boundary": safe_boundary,
        "failure_boundary": failure_boundary,
    }


def CALL_RUNTIME_EXISTENCE_TRACE(
    target_system: str,
    preserved_whole_state: bool,
    observed_value: float,
) -> Dict[str, object]:
    return {
        "call": "CALL_RUNTIME_EXISTENCE_TRACE",
        "target_system": target_system,
        "runtime_spike_type": "RUNTIME_EXISTENCE_SPIKE",
        "whole_state_preserved": preserved_whole_state,
        "observed_value": observed_value,
    }


def CALL_DETRIMENTAL_FAILURE_SPIKE(
    target_system: str,
    observed_value: float,
    failure_boundary: float,
) -> Dict[str, object]:
    return {
        "call": "CALL_DETRIMENTAL_FAILURE_SPIKE",
        "target_system": target_system,
        "runtime_spike_type": "DETRIMENTAL_FAILURE_SPIKE",
        "observed_value": observed_value,
        "failure_boundary": failure_boundary,
    }


def CALL_BOUNDARY_REALIGNMENT_ENGINE(
    safe_boundary: float,
    failure_boundary: float,
    observed_value: float,
    detrimental: bool,
) -> Dict[str, object]:
    # Conservative update: detrimental spikes tighten safe margin; recoverable spikes keep baseline.
    if detrimental:
        next_safe_boundary = round(min(safe_boundary, observed_value * 0.95), 4)
        next_failure_boundary = round(max(next_safe_boundary + 0.01, failure_boundary), 4)
    else:
        next_safe_boundary = round(safe_boundary, 4)
        next_failure_boundary = round(failure_boundary, 4)

    return {
        "call": "CALL_BOUNDARY_REALIGNMENT_ENGINE",
        "next_safe_boundary": next_safe_boundary,
        "next_failure_boundary": next_failure_boundary,
        "model_update": "applied",
    }


def _proof_hash(payload: Dict[str, object]) -> str:
    serialized = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]


def run_spike_boundary_calibration(
    spike_kind: SpikeKind,
    observed_value: float,
    safe_boundary: float,
    failure_boundary: float,
    environment: str,
    target_system: str,
) -> Dict[str, object]:
    if failure_boundary <= 0:
        raise ValueError("failure_boundary must be positive")
    if safe_boundary >= failure_boundary:
        raise ValueError("safe_boundary must be lower than failure_boundary")

    classify = CALL_SPIKE_EVENT_CLASSIFY(spike_kind, observed_value)

    if spike_kind == "temperature":
        temp_eval = CALL_TEMPERATURE_SPIKE_BOUNDARY(observed_value, safe_boundary, failure_boundary)
        volt_eval = {
            "call": "CALL_VOLTAGE_SPIKE_BOUNDARY",
            "status": "not_applicable",
        }
        status = temp_eval["status"]
    elif spike_kind == "voltage":
        temp_eval = {
            "call": "CALL_TEMPERATURE_SPIKE_BOUNDARY",
            "status": "not_applicable",
        }
        volt_eval = CALL_VOLTAGE_SPIKE_BOUNDARY(observed_value, safe_boundary, failure_boundary)
        status = volt_eval["status"]
    else:
        # Generic spike fallback uses boundary ratio only.
        temp_eval = {
            "call": "CALL_TEMPERATURE_SPIKE_BOUNDARY",
            "status": "not_applicable",
        }
        volt_eval = {
            "call": "CALL_VOLTAGE_SPIKE_BOUNDARY",
            "status": "not_applicable",
        }
        if observed_value < safe_boundary:
            status = "runtime_safe"
        elif observed_value < failure_boundary:
            status = "near_boundary"
        else:
            status = "failure_calibrating"

    boundary_ratio = observed_value / failure_boundary
    near_297 = 0.97 <= boundary_ratio < 1.0
    achieved_3 = boundary_ratio >= 1.0
    corridor_ratio = (2.97 - 1.0) / (3.0 - 1.0)

    detrimental = status == "failure_calibrating"
    if detrimental:
        runtime_trace = {
            "call": "CALL_RUNTIME_EXISTENCE_TRACE",
            "status": "not_preserved",
        }
        fail_trace = CALL_DETRIMENTAL_FAILURE_SPIKE(target_system, observed_value, failure_boundary)
        spike_type = "DETRIMENTAL_FAILURE_SPIKE"
    else:
        runtime_trace = CALL_RUNTIME_EXISTENCE_TRACE(
            target_system=target_system,
            preserved_whole_state=True,
            observed_value=observed_value,
        )
        fail_trace = {
            "call": "CALL_DETRIMENTAL_FAILURE_SPIKE",
            "status": "not_triggered",
        }
        spike_type = "RUNTIME_EXISTENCE_SPIKE"

    realignment = CALL_BOUNDARY_REALIGNMENT_ENGINE(
        safe_boundary=safe_boundary,
        failure_boundary=failure_boundary,
        observed_value=observed_value,
        detrimental=detrimental,
    )

    failure_spike = {
        "system": target_system,
        "active_whole_before": 1,
        "active_runtime_state": 2,
        "lower_boundary": -2,
        "upper_boundary": 2,
        "near_boundary_band": 2.97 if near_297 else None,
        "achieved_boundary": 3 if achieved_3 else None,
        "spike_value": observed_value,
        "environment": environment,
        "result": "symbolic_zero_only_if_cancelled_or_absent",
    }

    proof_ledger = {
        "proof_status": "committed",
        "spike_type": spike_type,
        "proof_hash": _proof_hash(failure_spike),
        "event": failure_spike,
    }

    return {
        "runtime_lane": [
            "CALL_SPIKE_EVENT_CLASSIFY",
            "CALL_TEMPERATURE_SPIKE_BOUNDARY",
            "CALL_VOLTAGE_SPIKE_BOUNDARY",
            "CALL_RUNTIME_EXISTENCE_TRACE",
            "CALL_DETRIMENTAL_FAILURE_SPIKE",
            "CALL_BOUNDARY_REALIGNMENT_ENGINE",
            "CALL_PROOF_LEDGER_COMMIT",
        ],
        "lane": [
            classify,
            temp_eval,
            volt_eval,
            runtime_trace,
            fail_trace,
            realignment,
        ],
        "ratios": {
            "boundary_ratio": round(boundary_ratio, 4),
            "whole_cycle_ratio_297_to_3": 0.99,
            "corridor_ratio_1_to_3_at_297": round(corridor_ratio, 3),
        },
        "classification": {
            "status": status,
            "spike_type": spike_type,
            "near_boundary_297": near_297,
            "boundary_3_achieved": achieved_3,
        },
        "failure_spike": failure_spike,
        "proof_ledger": proof_ledger,
    }
