# KEX Conformance Checklist

**Spec version:** `kex-canonical v1`  
**Author / Origin Authority:** A. Keddeh  
**Governance Root:** `GENERAL-GOVERNANCE-`

---

## Purpose

Any repository claiming KEX-conformance must pass all 10 acceptance tests listed below. Each test is marked:

- **VERIFIABLE NOW** — the test can be run against the current repository implementation.
- **AUTHOR TO RATIFY** — the test references a formal KEX definition not yet present in this repository. The test is included as a reserved slot; it must not be claimed as passing until A. Keddeh supplies the verbatim formal definition and a reference implementation is produced.

The Python reference validator `SPEC/kex_reference_validator.py` implements all VERIFIABLE NOW tests and marks AUTHOR TO RATIFY tests as explicit skips with rationale.

---

## Acceptance Tests

### Test 1 — No host/zero value accepted as an active state

**Status:** VERIFIABLE NOW  
**Citation:** `src/virtual_brain_pc/zero_classifier.py — CALL_ZERO_CLASSIFY`, `CALL_SYMBOLIC_ZERO_GATE`

A raw zero value (`0`, `None`, `False`) presented to the active-state layer without prior classification must be rejected. The gate `CALL_SYMBOLIC_ZERO_GATE` must return `gate_passed = False` for any value classified as `ZERO_AS_INVALID_WEIGHT`.

**Acceptance criterion:** `CALL_SYMBOLIC_ZERO_GATE({"zero_class": "ZERO_AS_INVALID_WEIGHT", "valid_for_use": False})["gate_passed"] == False`

---

### Test 2 — topologicalDistance(−2, 1) == 1

**Status:** AUTHOR TO RATIFY  
**Citation:** `SPEC/kex-canonical.md §1.2`

> A. Keddeh must define the topological distance metric over the active-state set `{−3, −2, 1, +2, +3}` and ratify that `topologicalDistance(−2, 1) == 1`.
>
> Until ratified, this test must be skipped; it must not be claimed as passing.

**Acceptance criterion (pending ratification):** `topologicalDistance(-2, 1) == 1`

---

### Test 3 — scalarDelta(−2, 1) == 3

**Status:** AUTHOR TO RATIFY  
**Citation:** `SPEC/kex-canonical.md §1.2`

> A. Keddeh must define the scalar delta metric over the active-state set and ratify that `scalarDelta(−2, 1) == 3`.
>
> Until ratified, this test must be skipped; it must not be claimed as passing.

**Acceptance criterion (pending ratification):** `scalarDelta(-2, 1) == 3`

---

### Test 4 — add(1, −1) returns Balanced

**Status:** AUTHOR TO RATIFY (formal Balanced type) / VERIFIABLE NOW (operational precursor)  
**Citation:** `SPEC/kex-canonical.md §3`, `src/virtual_brain_pc/zero_classifier.py — CALL_ZERO_RELATION_RESOLVE`

The operational precursor is verifiable: `CALL_ZERO_RELATION_RESOLVE(1.0, -1.0)` must return `produced_zero = True`, `zero_interpretation = "ZERO_AS_CANCELLATION"`, and `power_one_preserved = 1`.

The formal `Balanced` type requires A. Keddeh to ratify the state-kind enumeration (§2 of kex-canonical.md) before the full test can be claimed as passing.

**Acceptance criterion (operational):** `CALL_ZERO_RELATION_RESOLVE(1.0, -1.0)["produced_zero"] == True and CALL_ZERO_RELATION_RESOLVE(1.0, -1.0)["zero_interpretation"] == "ZERO_AS_CANCELLATION"`  
**Acceptance criterion (formal — pending ratification):** `add(1, -1)` returns an instance of `Balanced` state kind.

---

### Test 5 — Balanced state projects to typed zero

**Status:** AUTHOR TO RATIFY  
**Citation:** `SPEC/kex-canonical.md §3.2`, `SPEC/kex-canonical.md §4`

> A. Keddeh must define the typed projection law (§3.2) and the typed projection kinds (§4) before this test can be verified. Until ratified, this test must be skipped.

**Acceptance criterion (pending ratification):** A `Balanced` state carries a projection field of a typed zero kind (e.g. `BalancedZero`), never a bare scalar `0`.

---

### Test 6 — Both operands recoverable from Balanced result

**Status:** AUTHOR TO RATIFY  
**Citation:** `SPEC/kex-canonical.md §3.2`

> A. Keddeh must define the formal `Balanced` type and its operand-recovery interface before this test can be verified.
>
> The operational implementation (`CALL_ZERO_RELATION_RESOLVE`) does preserve both `left_value` and `right_value` in its output dict, which satisfies the spirit of recoverability.

**Acceptance criterion (pending ratification):** Given `b = add(a, neg_a)`, `b.left == a` and `b.right == neg_a`.  
**Acceptance criterion (operational):** `CALL_ZERO_RELATION_RESOLVE(a, -a)["left_value"] == a and CALL_ZERO_RELATION_RESOLVE(a, -a)["right_value"] == -a`

---

### Test 7 — Balanced(1, −1) ≠ Balanced(2, −2) canonically

**Status:** AUTHOR TO RATIFY  
**Citation:** `SPEC/kex-canonical.md §3.2`

> A. Keddeh must define the canonical identity rule for `Balanced` states before this test can be verified. The rule must specify that two `Balanced` states with different operand pairs are not equal, even though both produce a scalar result of zero.

**Acceptance criterion (pending ratification):** The canonical encoding (or hash) of `Balanced(1, -1)` differs from that of `Balanced(2, -2)`.

---

### Test 8 — Canonical encoding is byte-identical across runs

**Status:** VERIFIABLE NOW  
**Citation:** `src/virtual_brain_pc/braink_runtime.py — CALL_PROOF_LEDGER_COMMIT`

The proof ledger uses `json.dumps(entry, sort_keys=True)` followed by SHA-256. For a fixed input dict, two calls must produce the same `proof_hash`.

**Acceptance criterion:** Two calls to `CALL_PROOF_LEDGER_COMMIT` with the same dict produce `proof_hash` values that are equal.

---

### Test 9 — Invalid coordinates / denominators unconstructable

**Status:** AUTHOR TO RATIFY (formal constraint type) / VERIFIABLE NOW (gate enforcement)  
**Citation:** `src/virtual_brain_pc/zero_classifier.py — CALL_SYMBOLIC_ZERO_GATE`

The operational gate enforces that values with class `ZERO_AS_INVALID_WEIGHT` cannot proceed to weighted calculation. The formal constraint that invalid state-set coordinates are unconstructable (i.e. the type system prevents them at construction time) requires the state-kind enumeration (§2) to be ratified first.

**Acceptance criterion (operational):** `CALL_SYMBOLIC_ZERO_GATE({"zero_class": "ZERO_AS_INVALID_WEIGHT", "valid_for_use": False})["action"] == "REJECT_UNCLASSIFIED_WEIGHT"`  
**Acceptance criterion (formal — pending ratification):** Construction of a state with an invalid coordinate raises a type error at the boundary, not a runtime exception after the fact.

---

### Test 10 — Every state carries identity, observer, provenance

**Status:** AUTHOR TO RATIFY  
**Citation:** `SPEC/kex-canonical.md §6`

> A. Keddeh must define the formal observer, identity, and provenance fields (§6) before this test can be fully verified.
>
> Operationally, every proof ledger entry carries `system` (identity) and `environment` (provenance context) and a `proof_hash` (content-based provenance link). The `observer` field is not yet formally defined.

**Acceptance criterion (pending ratification):** Every active-state event record carries non-null `identity`, `observer`, and `provenance` fields as defined in §6 of kex-canonical.md.

---

## Summary Table

| # | Test | Status |
|---|---|---|
| 1 | No host/zero value accepted as active state | VERIFIABLE NOW |
| 2 | topologicalDistance(−2, 1) == 1 | AUTHOR TO RATIFY |
| 3 | scalarDelta(−2, 1) == 3 | AUTHOR TO RATIFY |
| 4 | add(1, −1) returns Balanced | PARTIAL (operational precursor verifiable) |
| 5 | Balanced state projects to typed zero | AUTHOR TO RATIFY |
| 6 | Both operands recoverable | PARTIAL (operational precursor verifiable) |
| 7 | Balanced(1,−1) ≠ Balanced(2,−2) canonically | AUTHOR TO RATIFY |
| 8 | Canonical encoding byte-identical across runs | VERIFIABLE NOW |
| 9 | Invalid coordinates unconstructable | PARTIAL (gate verifiable; type-level pending ratification) |
| 10 | Every state carries identity, observer, provenance | AUTHOR TO RATIFY |

**VERIFIABLE NOW:** 2 tests (1, 8)  
**PARTIAL (operational precursor verifiable):** 3 tests (4, 6, 9)  
**AUTHOR TO RATIFY:** 5 tests (2, 3, 5, 7, 10)

---

## AUTHOR TO RATIFY — Open Gate

Before a repository may claim full KEX-conformance, A. Keddeh must:

1. Ratify the KEX active-state set `{−3, −2, 1, +2, +3}` with rank map and distance metrics (gates tests 2, 3).
2. Ratify the state-kind enumeration with 1-based encodings (gates tests 4, 5, 9).
3. Ratify the formal non-erasing arithmetic law with typed projections (gates tests 5, 6, 7).
4. Ratify the observer/identity/provenance fields (gates test 10).

These slots are recorded in `SPEC/kex-canonical.md §11`.
