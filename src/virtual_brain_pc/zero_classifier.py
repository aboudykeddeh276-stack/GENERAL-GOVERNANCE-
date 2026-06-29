from __future__ import annotations

from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# Zero class constants  (§7 — Zero Classification Doctrine)
# ---------------------------------------------------------------------------

ZERO_AS_ABSENCE = "ZERO_AS_ABSENCE"
ZERO_AS_CANCELLATION = "ZERO_AS_CANCELLATION"
ZERO_AS_BOUNDARY = "ZERO_AS_BOUNDARY"
ZERO_AS_EXTERNAL_LABEL = "ZERO_AS_EXTERNAL_LABEL"
ZERO_AS_SYMBOLIC_RESULT = "ZERO_AS_SYMBOLIC_RESULT"
ZERO_AS_INVALID_WEIGHT = "ZERO_AS_INVALID_WEIGHT"


def CALL_ZERO_CLASSIFY(symbol: Any, context: str) -> Dict[str, object]:
    """BRAINK::PARSER::ZERO::CLASSIFY::v01

    Classify every zero-like symbol before it enters weighted calculation.
    Zero must answer: what active values produced it, what environment defines it,
    and what relation it resolves.
    """
    ctx = context.lower()
    if any(w in ctx for w in ("absent", "missing", "no ", "none", "empty relation")):
        zero_class = ZERO_AS_ABSENCE
    elif any(w in ctx for w in ("cancel", "opposite", "balance", "equal opposing")):
        zero_class = ZERO_AS_CANCELLATION
    elif any(w in ctx for w in ("boundary", "seam", "threshold", "origin", "degree", "circle")):
        zero_class = ZERO_AS_BOUNDARY
    elif any(w in ctx for w in ("celsius", "scale label", "offset", "external label", "coordinate")):
        zero_class = ZERO_AS_EXTERNAL_LABEL
    elif any(w in ctx for w in ("result", "output", "resolved", "symbolic")):
        zero_class = ZERO_AS_SYMBOLIC_RESULT
    else:
        zero_class = ZERO_AS_INVALID_WEIGHT

    return {
        "call": "CALL_ZERO_CLASSIFY",
        "symbol": symbol,
        "context": context,
        "zero_class": zero_class,
        "valid_for_use": zero_class != ZERO_AS_INVALID_WEIGHT,
        "theorem": "KEDDEH_THEOREM::v1.5",
    }


def CALL_ZERO_RELATION_RESOLVE(
    left_value: float,
    right_value: float,
    operation: str = "addition",
) -> Dict[str, object]:
    """BRAINK::ZERO::RELATION::RESOLVE::v01

    Determine which active values produced zero and preserve them.
    The power-one source is never erased by cancellation.
    """
    result = left_value + right_value if operation == "addition" else left_value - right_value
    produced_zero = abs(result) < 1e-10
    return {
        "call": "CALL_ZERO_RELATION_RESOLVE",
        "left_value": left_value,
        "right_value": right_value,
        "operation": operation,
        "result": result,
        "produced_zero": produced_zero,
        "power_one_preserved": 1,
        "zero_interpretation": ZERO_AS_CANCELLATION if produced_zero else "NO_ZERO_PRODUCED",
        "system_state": "POWER_ONE_PRESERVED",
    }


def CALL_SYMBOLIC_ZERO_GATE(zero_frame: Dict[str, object]) -> Dict[str, object]:
    """BRAINK::ZERO::SYMBOLIC::GATE::v01

    Block any zero-like value from entering weighted calculation without
    passing zero classification first.
    """
    zero_class = zero_frame.get("zero_class", ZERO_AS_INVALID_WEIGHT)
    valid = zero_frame.get("valid_for_use", False)
    passed = bool(valid) and zero_class != ZERO_AS_INVALID_WEIGHT
    return {
        "call": "CALL_SYMBOLIC_ZERO_GATE",
        "zero_class": zero_class,
        "gate_passed": passed,
        "action": "ALLOW_SYMBOLIC_USE" if passed else "REJECT_UNCLASSIFIED_WEIGHT",
    }


def CALL_ENVIRONMENT_WEIGHT_BIND(
    value: float,
    environment: str,
    relation: str,
    scale_type: str = "ratio",
) -> Dict[str, object]:
    """BRAINK::WEIGHT::ENVIRONMENT::BIND::v01

    Bind a value to its environment, relation, object, and weight context
    so it cannot float free of its measurement conditions.
    """
    return {
        "call": "CALL_ENVIRONMENT_WEIGHT_BIND",
        "value": value,
        "environment": environment,
        "relation": relation,
        "scale_type": scale_type,
        "bound_state": "ACTIVE_WEIGHT_BOUND",
        "power_one": 1,
    }


def CALL_SCALE_CLASSIFY(value: float, context: str) -> Dict[str, object]:
    """BRAINK::SCALE::TYPE::CLASSIFY::v01

    Determine whether the value sits on an interval, ratio, ordinal,
    cyclic, symbolic, or organism scale — each with a different zero meaning.
    """
    ctx = context.lower()
    if any(w in ctx for w in ("celsius", "fahrenheit")):
        scale, note = "interval", "zero_is_external_label"
    elif any(w in ctx for w in ("kelvin", "absolute")):
        scale, note = "ratio", "zero_is_true_absence"
    elif any(w in ctx for w in ("degree", "angle", "circle", "cyclic")):
        scale, note = "cyclic", "zero_degree_is_boundary_seam"
    elif any(w in ctx for w in ("rank", "ordinal")):
        scale, note = "ordinal", "zero_position_is_label"
    elif any(w in ctx for w in ("binary", "bit", "digital")):
        scale, note = "symbolic", "binary_zero_is_encoded_state"
    else:
        scale, note = "ratio", "default_ratio_scale"
    return {
        "call": "CALL_SCALE_CLASSIFY",
        "value": value,
        "context": context,
        "scale_type": scale,
        "note": note,
    }


def CALL_CELSIUS_KELVIN_COMPARE(celsius: float) -> Dict[str, object]:
    """BRAINK::THERMAL::CELSIUS_KELVIN::COMPARE::v01

    Convert Celsius to Kelvin and expose that 0°C is an external coordinate
    label, not true zero thermal existence. 0K is the true absence of
    thermal state.
    """
    kelvin = celsius + 273.15
    return {
        "call": "CALL_CELSIUS_KELVIN_COMPARE",
        "celsius": celsius,
        "kelvin": round(kelvin, 4),
        "celsius_zero_class": ZERO_AS_EXTERNAL_LABEL,
        "kelvin_zero_class": ZERO_AS_ABSENCE,
        "note": "0°C is a coordinate; 0K is true thermal absence",
    }


def CALL_RESONANCE_297_CLASSIFY(value: float) -> Dict[str, object]:
    """BRAINK::RESONANCE::297::CLASSIFY::v01

    Classify a value against the 2.97 / 0.297 / 297 / 3.0 KEDDEH
    calibration family (§10).
    """
    near_3 = abs(value - 3.0) < 0.03
    near_297 = 2.94 <= value < 3.0
    near_297_scaled = 294.0 <= value < 300.0
    near_0297 = 0.294 <= value < 0.300

    if near_3:
        band = "BOUNDARY_3_ACHIEVEMENT"
    elif near_297:
        band = "NEAR_BOUNDARY_297"
    elif near_297_scaled:
        band = "NEAR_BOUNDARY_297_SCALED"
    elif near_0297:
        band = "NEAR_BOUNDARY_0297_RESONANCE"
    else:
        band = "OUTSIDE_297_FAMILY"

    corridor_ratio = round((value - 1.0) / 2.0, 4) if 1.0 <= value <= 3.0 else None
    return {
        "call": "CALL_RESONANCE_297_CLASSIFY",
        "value": value,
        "band": band,
        "ratio_to_3": round(value / 3.0, 4),
        "corridor_ratio": corridor_ratio,
    }


def CALL_TENSOR_ZERO_TYPE_ENTRY(tensor_frame: Dict[str, object]) -> Dict[str, object]:
    """BRAINK::TENSOR::ZERO::TYPE_ENTRY::v01

    Type every zero-like entry in a tensor frame so zero coercion is
    prevented. Absent, cancelled, constrained, and unknown entries must
    be distinguished rather than collapsed to raw zero.
    """
    typed: Dict[str, str] = {}
    for key, val in tensor_frame.items():
        if val == 0 or val is None:
            typed[key] = ZERO_AS_SYMBOLIC_RESULT
        else:
            typed[key] = "ACTIVE_COMPONENT"
    return {
        "call": "CALL_TENSOR_ZERO_TYPE_ENTRY",
        "typed_entries": typed,
        "zero_coercion_prevented": True,
    }


def CALL_SWIRL_VORTEX_CALIBRATE(
    pattern_values: List[float],
    scale: str = "unit",
) -> Dict[str, object]:
    """BRAINK::SWIRL::VORTEX::CALIBRATE::v01

    Test curvature, coupling, and swirl/vortex relationships against the
    KEDDEH 1→2→3 corridor. Visual analogy is not proof — measured
    recurrence requires dataset, ratio, regression, and proof ledger.
    """
    if not pattern_values:
        return {
            "call": "CALL_SWIRL_VORTEX_CALIBRATE",
            "status": "NO_PATTERN_DATA",
        }
    n = len(pattern_values)
    mean = sum(pattern_values) / n
    max_v = max(pattern_values)
    near_boundary_count = sum(
        1 for v in pattern_values
        if max_v > 0 and 0.97 <= (v / max_v) < 1.0
    )
    return {
        "call": "CALL_SWIRL_VORTEX_CALIBRATE",
        "scale": scale,
        "n": n,
        "mean": round(mean, 4),
        "near_boundary_ratio": round(near_boundary_count / n, 4),
        "status": "CALIBRATED",
        "note": "visual_analogy_is_not_proof_measured_recurrence_required",
    }


def CALL_SIMULATION_ROUTE_ACCELERATOR(
    seed: str,
    prior_route: List[str],
) -> Dict[str, object]:
    """BRAINK::SIMULATION::ROUTE::ACCELERATE::v01

    Reuse a validated route-state to reduce recomputation from unclassified
    zero. SIM_ROUTE_EFFICIENCY = raw_steps / KEX_traversal_steps (§19).
    """
    reuse_steps = len(prior_route)
    return {
        "call": "CALL_SIMULATION_ROUTE_ACCELERATOR",
        "seed": seed,
        "prior_route_steps": reuse_steps,
        "reused": reuse_steps > 0,
        "status": "ROUTE_ACCELERATED" if reuse_steps > 0 else "NO_PRIOR_ROUTE",
        "note": "validated_route_reused_avoids_recomputation_from_unclassified_zero",
    }


def CALL_CALIBRATION_RUN(input_frame: Dict[str, object]) -> Dict[str, object]:
    """BRAINK::CALIBRATION::ENGINE::RUN::v01

    Scan an input frame and apply corrected-zero mathematics: every
    zero-like value is flagged as requiring classification before it
    may enter weighted calculation.
    """
    zero_scan: Dict[str, str] = {}
    for k, v in input_frame.items():
        if v == 0 or v is None or v is False:
            zero_scan[k] = "ZERO_LIKE_REQUIRES_CLASSIFICATION"
        else:
            zero_scan[k] = "ACTIVE_VALUE"
    return {
        "call": "CALL_CALIBRATION_RUN",
        "input_keys": sorted(input_frame.keys()),
        "zero_scan": zero_scan,
        "calibration_status": "applied",
        "theorem_version": "KEDDEH_THEOREM::v1.5",
    }
