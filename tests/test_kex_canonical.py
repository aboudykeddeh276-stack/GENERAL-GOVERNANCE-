"""Tests for the KEX Canonical Reference Validator (kex-canonical v1).

Covers all 10 acceptance tests defined in SPEC/conformance-checklist.md.
Tests whose specification is AUTHOR TO RATIFY are present but guarded so
that they do not fail the suite; they assert the current contract (returns
None) and will be strengthened when the author ratifies the definition.
"""

from __future__ import annotations

import pytest

from virtual_brain_pc.kex_canonical import (
    BALANCED_ZERO_TAG,
    SPEC_VERSION,
    add,
    assert_no_zero_active_state,
    balanced_canonical_key,
    canonical_encode,
    construct_active_state,
    is_active_state,
    is_balanced,
    project_to_typed_zero,
    proof_hash,
    recover_operands,
    scalar_delta,
    topological_distance,
    validate_event_provenance,
)

# ---------------------------------------------------------------------------
# AT-01 — No zero active state
# ---------------------------------------------------------------------------

def test_at01_zero_is_not_active() -> None:
    assert is_active_state(0) is False
    assert is_active_state(0.0) is False
    assert is_active_state(None) is False
    assert is_active_state("x") is False


def test_at01_nonzero_is_active() -> None:
    assert is_active_state(1) is True
    assert is_active_state(-2) is True
    assert is_active_state(3) is True
    assert is_active_state(0.5) is True


def test_at01_assert_raises_for_zero() -> None:
    with pytest.raises(ValueError, match="NO-Zero-Axis"):
        assert_no_zero_active_state(0)
    with pytest.raises(ValueError):
        assert_no_zero_active_state(0.0)
    with pytest.raises(ValueError):
        assert_no_zero_active_state(None)


def test_at01_assert_passes_for_active() -> None:
    assert_no_zero_active_state(1)
    assert_no_zero_active_state(-2)
    assert_no_zero_active_state(3)


# ---------------------------------------------------------------------------
# AT-02 — topologicalDistance(−2, 1) == 1  [AUTHOR TO RATIFY]
# ---------------------------------------------------------------------------

def test_at02_topology_distance_pending() -> None:
    # Returns None until §1.2 is ratified by the author.
    result = topological_distance(-2, 1)
    assert result is None, (
        "topological_distance is AUTHOR TO RATIFY; expected None until ratified. "
        "If ratified, update this test to assert result == 1."
    )


# ---------------------------------------------------------------------------
# AT-03 — scalarDelta(−2, 1) == 3  [AUTHOR TO RATIFY]
# ---------------------------------------------------------------------------

def test_at03_scalar_delta_pending() -> None:
    # Returns None until the author ratifies the scalarDelta definition.
    result = scalar_delta(-2, 1)
    assert result is None, (
        "scalar_delta is AUTHOR TO RATIFY; expected None until ratified. "
        "If ratified, update this test to assert result == 3."
    )


# ---------------------------------------------------------------------------
# AT-04 — add(1, −1) → Balanced
# ---------------------------------------------------------------------------

def test_at04_add_cancellation_yields_balanced() -> None:
    record = add(1, -1)
    assert is_balanced(record) is True


def test_at04_result_is_zero_but_typed() -> None:
    record = add(1, -1)
    assert abs(record["result"]) < 1e-10
    assert record["projection"] == BALANCED_ZERO_TAG
    assert record["projection"] != 0
    assert isinstance(record["projection"], str)


def test_at04_power_one_preserved() -> None:
    record = add(1, -1)
    assert record["power_one_preserved"] == 1


def test_at04_non_cancellation_not_balanced() -> None:
    record = add(1, 2)
    assert is_balanced(record) is False
    assert record["projection"] == "NO_ZERO_PRODUCED"


# ---------------------------------------------------------------------------
# AT-05 — Balanced projects to typed zero
# ---------------------------------------------------------------------------

def test_at05_projection_is_non_none_string() -> None:
    record = add(1, -1)
    proj = project_to_typed_zero(record)
    assert proj is not None
    assert isinstance(proj, str)
    assert proj != "0"
    assert proj != 0


def test_at05_non_balanced_projects_to_none() -> None:
    record = add(1, 2)
    assert project_to_typed_zero(record) is None


# ---------------------------------------------------------------------------
# AT-06 — Both operands recoverable
# ---------------------------------------------------------------------------

def test_at06_operands_recovered() -> None:
    record = add(1, -1)
    operands = recover_operands(record)
    assert operands["left_value"] == 1
    assert operands["right_value"] == -1


def test_at06_operands_recovered_larger() -> None:
    record = add(2, -2)
    operands = recover_operands(record)
    assert operands["left_value"] == 2
    assert operands["right_value"] == -2


# ---------------------------------------------------------------------------
# AT-07 — Balanced(1,−1) ≠ Balanced(2,−2) canonically
# ---------------------------------------------------------------------------

def test_at07_distinct_balanced_records_have_distinct_keys() -> None:
    r1 = add(1, -1)
    r2 = add(2, -2)
    assert is_balanced(r1)
    assert is_balanced(r2)
    assert balanced_canonical_key(r1) != balanced_canonical_key(r2)


def test_at07_same_record_yields_same_key() -> None:
    r = add(1, -1)
    assert balanced_canonical_key(r) == balanced_canonical_key(r)


# ---------------------------------------------------------------------------
# AT-08 — Canonical encoding is byte-identical across runs
# ---------------------------------------------------------------------------

_SAMPLE_EVENT = {
    "system": "cpu_runtime",
    "active_whole_before": 1,
    "active_runtime_state": 2,
    "lower_boundary": -2,
    "upper_boundary": 2,
    "near_boundary_band": None,
    "achieved_boundary": None,
    "spike_value": 97.0,
    "environment": "production",
    "result": "symbolic_zero_only_if_cancelled_or_absent",
}

_EXPECTED_CANONICAL = (
    b'{"achieved_boundary":null,"active_runtime_state":2,'
    b'"active_whole_before":1,"environment":"production",'
    b'"lower_boundary":-2,"near_boundary_band":null,'
    b'"result":"symbolic_zero_only_if_cancelled_or_absent",'
    b'"spike_value":97.0,"system":"cpu_runtime","upper_boundary":2}'
)


def test_at08_canonical_encode_deterministic() -> None:
    a = canonical_encode(_SAMPLE_EVENT)
    b = canonical_encode(_SAMPLE_EVENT)
    assert a == b


def test_at08_canonical_encode_known_value() -> None:
    encoded = canonical_encode(_SAMPLE_EVENT)
    assert encoded == _EXPECTED_CANONICAL


def test_at08_proof_hash_deterministic() -> None:
    h1 = proof_hash(_SAMPLE_EVENT)
    h2 = proof_hash(_SAMPLE_EVENT)
    assert h1 == h2
    assert len(h1) == 16
    assert all(c in "0123456789abcdef" for c in h1)


def test_at08_different_events_different_hashes() -> None:
    event_a = dict(_SAMPLE_EVENT, spike_value=50.0)
    event_b = dict(_SAMPLE_EVENT, spike_value=97.0)
    assert proof_hash(event_a) != proof_hash(event_b)


# ---------------------------------------------------------------------------
# AT-09 — Invalid denominators unconstructable
# ---------------------------------------------------------------------------

def test_at09_zero_rejected() -> None:
    with pytest.raises(ValueError):
        construct_active_state(0)


def test_at09_none_rejected() -> None:
    with pytest.raises(ValueError):
        construct_active_state(None)


def test_at09_valid_values_constructable() -> None:
    s = construct_active_state(1)
    assert s["value"] == 1.0
    assert s["active"] is True
    assert s["spec_version"] == SPEC_VERSION

    s2 = construct_active_state(-2)
    assert s2["value"] == -2.0


# ---------------------------------------------------------------------------
# AT-10 — Every state carries identity, observer, provenance [AUTHOR TO RATIFY]
# ---------------------------------------------------------------------------

def test_at10_provenance_validation_pending() -> None:
    # Returns None until §5.2 is ratified by the author.
    result = validate_event_provenance(_SAMPLE_EVENT)
    assert result is None, (
        "validate_event_provenance is AUTHOR TO RATIFY; expected None until ratified. "
        "Update this test when identity/observer/provenance schema is defined."
    )


# ---------------------------------------------------------------------------
# Spec version sanity check
# ---------------------------------------------------------------------------

def test_spec_version_tag() -> None:
    assert SPEC_VERSION == "kex-canonical v1"
