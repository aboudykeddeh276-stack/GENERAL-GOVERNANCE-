#!/usr/bin/env python3
"""KEX Conformance Reference Validator — kex-canonical v1

FUNCTION_VALIDATE_KEX_CONFORMANCE

Input: the BRAINK/KEX runtime package installed in the current Python environment.
Action: runs the 10 KEX conformance acceptance tests defined in SPEC/conformance-checklist.md.
        Tests that are VERIFIABLE NOW are executed and asserted.
        Tests that are AUTHOR TO RATIFY are recorded as explicit skips with rationale.
Output: CONFORMANCE_CHECK_STATUS: COMPLETED (exit 0) or CONFORMANCE_CHECK_STATUS: FAILED (exit 1).
Proof gate: PROOF_GATE_CONFORMANCE_PASSED — this script exits 0.
Pending: PENDING_AUTHOR_RATIFICATION — 5 tests skipped until A. Keddeh supplies formal definitions.

Spec version: kex-canonical v1
Governance Root: GENERAL-GOVERNANCE-
"""

from __future__ import annotations

import sys
from typing import Any, Dict, List


# ---------------------------------------------------------------------------
# Result helpers
# ---------------------------------------------------------------------------

_results: List[Dict[str, Any]] = []


def _pass(test_id: int, name: str, detail: str = "") -> None:
    _results.append({"id": test_id, "name": name, "status": "PASS", "detail": detail})


def _fail(test_id: int, name: str, detail: str) -> None:
    _results.append({"id": test_id, "name": name, "status": "FAIL", "detail": detail})


def _skip(test_id: int, name: str, reason: str) -> None:
    _results.append({"id": test_id, "name": name, "status": "SKIP_AUTHOR_TO_RATIFY", "reason": reason})


# ---------------------------------------------------------------------------
# Test 1 — No host/zero value accepted as an active state  (VERIFIABLE NOW)
# ---------------------------------------------------------------------------

def _test_1() -> None:
    """VERIFIABLE NOW — SPEC/conformance-checklist.md test 1"""
    from virtual_brain_pc.zero_classifier import (
        CALL_SYMBOLIC_ZERO_GATE,
        ZERO_AS_INVALID_WEIGHT,
    )

    gate_result = CALL_SYMBOLIC_ZERO_GATE(
        {"zero_class": ZERO_AS_INVALID_WEIGHT, "valid_for_use": False}
    )
    if gate_result["gate_passed"] is not False:
        _fail(1, "no_host_zero_as_active_state",
              f"gate_passed expected False, got {gate_result['gate_passed']!r}")
        return
    if gate_result["action"] != "REJECT_UNCLASSIFIED_WEIGHT":
        _fail(1, "no_host_zero_as_active_state",
              f"action expected REJECT_UNCLASSIFIED_WEIGHT, got {gate_result['action']!r}")
        return
    _pass(1, "no_host_zero_as_active_state",
          "CALL_SYMBOLIC_ZERO_GATE correctly rejects ZERO_AS_INVALID_WEIGHT")


# ---------------------------------------------------------------------------
# Test 2 — topologicalDistance(−2, 1) == 1  (AUTHOR TO RATIFY)
# ---------------------------------------------------------------------------

def _test_2() -> None:
    """AUTHOR TO RATIFY — SPEC/conformance-checklist.md test 2"""
    _skip(
        2,
        "topological_distance_minus2_1_equals_1",
        "The KEX active-state set {-3,-2,1,+2,+3} and its topological distance metric "
        "are not yet formally defined in GENERAL-GOVERNANCE-. "
        "See SPEC/kex-canonical.md §1.2. A. Keddeh must ratify this before the test can run.",
    )


# ---------------------------------------------------------------------------
# Test 3 — scalarDelta(−2, 1) == 3  (AUTHOR TO RATIFY)
# ---------------------------------------------------------------------------

def _test_3() -> None:
    """AUTHOR TO RATIFY — SPEC/conformance-checklist.md test 3"""
    _skip(
        3,
        "scalar_delta_minus2_1_equals_3",
        "The scalar delta metric over the active-state set is not yet formally defined. "
        "See SPEC/kex-canonical.md §1.2. A. Keddeh must ratify this before the test can run.",
    )


# ---------------------------------------------------------------------------
# Test 4 — add(1, −1) returns Balanced  (PARTIAL — operational precursor)
# ---------------------------------------------------------------------------

def _test_4() -> None:
    """PARTIAL — operational precursor VERIFIABLE NOW; formal Balanced type AUTHOR TO RATIFY.
    SPEC/conformance-checklist.md test 4.
    """
    from virtual_brain_pc.zero_classifier import (
        CALL_ZERO_RELATION_RESOLVE,
        ZERO_AS_CANCELLATION,
    )

    result = CALL_ZERO_RELATION_RESOLVE(left_value=1.0, right_value=-1.0)

    failures = []
    if result.get("produced_zero") is not True:
        failures.append(f"produced_zero expected True, got {result.get('produced_zero')!r}")
    if result.get("zero_interpretation") != ZERO_AS_CANCELLATION:
        failures.append(
            f"zero_interpretation expected {ZERO_AS_CANCELLATION!r}, "
            f"got {result.get('zero_interpretation')!r}"
        )
    if result.get("power_one_preserved") != 1:
        failures.append(
            f"power_one_preserved expected 1, got {result.get('power_one_preserved')!r}"
        )
    if result.get("left_value") != 1.0 or result.get("right_value") != -1.0:
        failures.append("operands not preserved in result")

    if failures:
        _fail(4, "add_1_neg1_returns_balanced_operational", "; ".join(failures))
    else:
        _pass(4, "add_1_neg1_returns_balanced_operational",
              "CALL_ZERO_RELATION_RESOLVE(1, -1) cancels correctly and preserves both operands "
              "(operational precursor). Formal Balanced type: AUTHOR TO RATIFY — see "
              "SPEC/kex-canonical.md §3.2.")


# ---------------------------------------------------------------------------
# Test 5 — Balanced state projects to typed zero  (AUTHOR TO RATIFY)
# ---------------------------------------------------------------------------

def _test_5() -> None:
    """AUTHOR TO RATIFY — SPEC/conformance-checklist.md test 5"""
    _skip(
        5,
        "balanced_projects_to_typed_zero",
        "Formal typed projection kinds (BalancedZero, BaselineZero, Absent) are not yet "
        "defined. See SPEC/kex-canonical.md §3.2 and §4. "
        "A. Keddeh must ratify this before the test can run.",
    )


# ---------------------------------------------------------------------------
# Test 6 — Both operands recoverable  (PARTIAL — operational precursor)
# ---------------------------------------------------------------------------

def _test_6() -> None:
    """PARTIAL — operational precursor VERIFIABLE NOW; formal Balanced type AUTHOR TO RATIFY.
    SPEC/conformance-checklist.md test 6.
    """
    from virtual_brain_pc.zero_classifier import CALL_ZERO_RELATION_RESOLVE

    for a, b in [(1.0, -1.0), (2.0, -2.0), (3.0, -3.0)]:
        result = CALL_ZERO_RELATION_RESOLVE(left_value=a, right_value=b)
        if result.get("left_value") != a or result.get("right_value") != b:
            _fail(
                6,
                "both_operands_recoverable_operational",
                f"add({a},{b}): operands not preserved; "
                f"left={result.get('left_value')!r}, right={result.get('right_value')!r}",
            )
            return

    _pass(6, "both_operands_recoverable_operational",
          "CALL_ZERO_RELATION_RESOLVE preserves both operands in all tested pairs "
          "(operational precursor). Formal recovery API: AUTHOR TO RATIFY — see "
          "SPEC/kex-canonical.md §3.2.")


# ---------------------------------------------------------------------------
# Test 7 — Balanced(1, −1) ≠ Balanced(2, −2) canonically  (AUTHOR TO RATIFY)
# ---------------------------------------------------------------------------

def _test_7() -> None:
    """AUTHOR TO RATIFY — SPEC/conformance-checklist.md test 7"""
    _skip(
        7,
        "balanced_1_neg1_neq_balanced_2_neg2",
        "The canonical identity rule for Balanced states is not yet formally defined. "
        "See SPEC/kex-canonical.md §3.2. "
        "A. Keddeh must ratify this before the test can run.",
    )


# ---------------------------------------------------------------------------
# Test 8 — Canonical encoding byte-identical across runs  (VERIFIABLE NOW)
# ---------------------------------------------------------------------------

def _test_8() -> None:
    """VERIFIABLE NOW — SPEC/conformance-checklist.md test 8"""
    from virtual_brain_pc.braink_runtime import CALL_PROOF_LEDGER_COMMIT

    entry: Dict[str, Any] = {
        "system": "reference_validator",
        "active_whole_before": 1,
        "active_runtime_state": 2,
        "lower_boundary": -2,
        "upper_boundary": 2,
        "near_boundary_band": 2.97,
        "achieved_boundary": None,
        "spike_value": 97.0,
        "environment": "test",
        "result": "symbolic_zero_only_if_cancelled_or_absent",
    }

    result_a = CALL_PROOF_LEDGER_COMMIT(entry)
    result_b = CALL_PROOF_LEDGER_COMMIT(entry)

    if result_a["proof_hash"] != result_b["proof_hash"]:
        _fail(8, "canonical_encoding_byte_identical",
              f"proof_hash differs between calls: "
              f"{result_a['proof_hash']!r} vs {result_b['proof_hash']!r}")
        return
    if result_a["proof_status"] != "committed":
        _fail(8, "canonical_encoding_byte_identical",
              f"proof_status expected 'committed', got {result_a['proof_status']!r}")
        return

    _pass(8, "canonical_encoding_byte_identical",
          f"CALL_PROOF_LEDGER_COMMIT produces stable hash {result_a['proof_hash']!r} "
          "across two calls with identical input")


# ---------------------------------------------------------------------------
# Test 9 — Invalid coordinates unconstructable  (PARTIAL — gate verifiable)
# ---------------------------------------------------------------------------

def _test_9() -> None:
    """PARTIAL — gate enforcement VERIFIABLE NOW; type-level construction prevention
    AUTHOR TO RATIFY. SPEC/conformance-checklist.md test 9.
    """
    from virtual_brain_pc.zero_classifier import (
        CALL_SYMBOLIC_ZERO_GATE,
        ZERO_AS_INVALID_WEIGHT,
    )

    gate_result = CALL_SYMBOLIC_ZERO_GATE(
        {"zero_class": ZERO_AS_INVALID_WEIGHT, "valid_for_use": False}
    )

    if gate_result["action"] != "REJECT_UNCLASSIFIED_WEIGHT":
        _fail(9, "invalid_coordinates_gate_enforcement",
              f"action expected REJECT_UNCLASSIFIED_WEIGHT, got {gate_result['action']!r}")
        return

    _pass(9, "invalid_coordinates_gate_enforcement",
          "CALL_SYMBOLIC_ZERO_GATE enforces rejection of ZERO_AS_INVALID_WEIGHT at the "
          "calculation boundary (gate enforcement). Type-level construction prevention: "
          "AUTHOR TO RATIFY — see SPEC/kex-canonical.md §2.")


# ---------------------------------------------------------------------------
# Test 10 — Every state carries identity, observer, provenance  (AUTHOR TO RATIFY)
# ---------------------------------------------------------------------------

def _test_10() -> None:
    """AUTHOR TO RATIFY — SPEC/conformance-checklist.md test 10"""
    _skip(
        10,
        "every_state_carries_identity_observer_provenance",
        "The formal observer, identity, and provenance fields are not yet defined. "
        "See SPEC/kex-canonical.md §6. "
        "A. Keddeh must ratify this before the test can run.",
    )


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

_TESTS = [
    _test_1, _test_2, _test_3, _test_4, _test_5,
    _test_6, _test_7, _test_8, _test_9, _test_10,
]


def run_all() -> int:
    for t in _TESTS:
        try:
            t()
        except Exception as exc:  # noqa: BLE001
            test_id = int(t.__name__.split("_")[1])
            _fail(test_id, t.__name__, f"unexpected exception: {exc}")

    passed = [r for r in _results if r["status"] == "PASS"]
    failed = [r for r in _results if r["status"] == "FAIL"]
    skipped = [r for r in _results if r["status"] == "SKIP_AUTHOR_TO_RATIFY"]

    for r in _results:
        status = r["status"]
        name = r.get("name", "?")
        if status == "PASS":
            print(f"  PASS  [{r['id']:2d}] {name}: {r.get('detail', '')}")
        elif status == "FAIL":
            print(f"  FAIL  [{r['id']:2d}] {name}: {r.get('detail', '')}")
        else:
            print(f"  SKIP  [{r['id']:2d}] {name}: {r.get('reason', '')}")

    print()
    print(f"KEX_CONFORMANCE_PASS:    {len(passed)}")
    print(f"KEX_CONFORMANCE_FAIL:    {len(failed)}")
    print(f"KEX_CONFORMANCE_PENDING: {len(skipped)}  (AUTHOR TO RATIFY)")
    print(f"SPEC_VERSION: kex-canonical v1")

    if failed:
        print("CONFORMANCE_CHECK_STATUS: FAILED")
        return 1

    print("CONFORMANCE_CHECK_STATUS: COMPLETED")
    print("PROOF_GATE_CONFORMANCE_PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(run_all())
