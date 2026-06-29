from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MaterialFrame:
    material: str
    environment: str
    whole_identity: str
    lower_boundary: float
    upper_boundary: float


def CALL_MATERIAL_WHOLE_BIND(frame: MaterialFrame) -> Dict[str, object]:
    return {
        "call": "CALL_MATERIAL_WHOLE_BIND",
        "material": frame.material,
        "environment": frame.environment,
        "whole_state_before": 1,
        "whole_identity": frame.whole_identity,
    }


def CALL_ACTIVE_STRESS_CROSSING(force_value: float, force_kind: str = "stress") -> Dict[str, object]:
    return {
        "call": "CALL_ACTIVE_STRESS_CROSSING",
        "active_crossing_force": 2,
        "force_kind": force_kind,
        "force_value": force_value,
    }


def CALL_BOUNDARY_PAIR_DETECT(frame: MaterialFrame) -> Dict[str, object]:
    return {
        "call": "CALL_BOUNDARY_PAIR_DETECT",
        "boundary_pair": {"minus_2": frame.lower_boundary, "plus_2": frame.upper_boundary},
    }


def CALL_NEAR_FAILURE_297_BAND(force_value: float, upper_boundary: float) -> Dict[str, object]:
    if upper_boundary <= 0:
        raise ValueError("upper_boundary must be positive")

    ratio_to_boundary = force_value / upper_boundary
    near_failure = 0.97 <= ratio_to_boundary < 1.0
    return {
        "call": "CALL_NEAR_FAILURE_297_BAND",
        "ratio_to_boundary": round(ratio_to_boundary, 4),
        "near_boundary_band": 2.97 if near_failure else None,
        "detected": near_failure,
    }


def CALL_BOUNDARY_3_ACHIEVEMENT(force_value: float, upper_boundary: float) -> Dict[str, object]:
    achieved = force_value >= upper_boundary
    return {
        "call": "CALL_BOUNDARY_3_ACHIEVEMENT",
        "achieved_boundary": 3 if achieved else None,
        "boundary_reached": achieved,
    }


def CALL_FAILURE_CALIBRATION_LEDGER(event: Dict[str, object]) -> Dict[str, object]:
    event_serialized = json.dumps(event, sort_keys=True)
    event_hash = hashlib.sha256(event_serialized.encode("utf-8")).hexdigest()[:16]
    return {
        "call": "CALL_FAILURE_CALIBRATION_LEDGER",
        "proof_status": "committed",
        "event_hash": event_hash,
        "event": event,
    }


def run_material_failure_calibration(
    material: str,
    environment: str,
    whole_identity: str,
    force_value: float,
    lower_boundary: float,
    upper_boundary: float,
    force_kind: str = "stress",
) -> Dict[str, object]:
    frame = MaterialFrame(
        material=material,
        environment=environment,
        whole_identity=whole_identity,
        lower_boundary=lower_boundary,
        upper_boundary=upper_boundary,
    )

    lane: List[Dict[str, object]] = [
        CALL_MATERIAL_WHOLE_BIND(frame),
        CALL_ACTIVE_STRESS_CROSSING(force_value, force_kind=force_kind),
        CALL_BOUNDARY_PAIR_DETECT(frame),
    ]

    near_band = CALL_NEAR_FAILURE_297_BAND(force_value, upper_boundary)
    boundary = CALL_BOUNDARY_3_ACHIEVEMENT(force_value, upper_boundary)
    lane.append(near_band)
    lane.append(boundary)

    event = {
        "material": material,
        "environment": environment,
        "whole_state_before": 1,
        "active_crossing_force": 2,
        "boundary_crossed": "B+" if boundary["boundary_reached"] else None,
        "near_boundary_band": 2.97 if near_band["detected"] else None,
        "achieved_boundary": 3 if boundary["boundary_reached"] else None,
        "zero_result": "symbolic_only",
    }
    ledger_record = CALL_FAILURE_CALIBRATION_LEDGER(event)
    lane.append(ledger_record)

    return {
        "runtime_sequence": [
            "CALL_MATERIAL_WHOLE_BIND",
            "CALL_ACTIVE_STRESS_CROSSING",
            "CALL_BOUNDARY_PAIR_DETECT",
            "CALL_NEAR_FAILURE_297_BAND",
            "CALL_BOUNDARY_3_ACHIEVEMENT",
            "CALL_FAILURE_CALIBRATION_LEDGER",
        ],
        "lane": lane,
        "failure_event": event,
        "proof_ledger": ledger_record,
    }
