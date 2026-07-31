# KEX Conformance Checklist

**Spec version:** `kex-canonical v1`  
**Authority:** A. Keddeh — BRAINK / KEX / GENERAL-GOVERNANCE-  
**Governance root:** `GENERAL-GOVERNANCE-`  
**Status:** `STATE_MODEL_LOCAL`  
**Proof gate:** `PROOF_GATE_CHECKER_PASSED`  
**Reference validator:** `src/virtual_brain_pc/kex_canonical.py`  
**Test file:** `tests/test_kex_canonical.py`

---

## Purpose

This checklist defines the 10 acceptance tests that every conforming implementation
of the KEX zeroless active-state architecture must pass.  Tests backed by the
**Python reference validator** (`kex_canonical.py`) are executable now.  Tests
whose specification is **AUTHOR TO RATIFY** are listed with a placeholder
assertion; the assertion is skipped (`None`-guarded) until the author provides the
formal definition.

---

## Acceptance Tests

### AT-01 — No zero active state (EXECUTABLE)

**Requirement:** A raw zero value (`0`, `0.0`, `None`, or any value within
`1e-10` of zero) must never be admitted as a live active weight or active state.

**Invariant (§1.3):** `is_active_state(0) == False`

**Validator call:**

```python
from virtual_brain_pc.kex_canonical import assert_no_zero_active_state
assert_no_zero_active_state(0)      # must raise ValueError
assert_no_zero_active_state(0.0)    # must raise ValueError
assert_no_zero_active_state(None)   # must raise ValueError
assert_no_zero_active_state(1)      # must NOT raise
assert_no_zero_active_state(-2)     # must NOT raise
assert_no_zero_active_state(3)      # must NOT raise
```

**Pass condition:** `ValueError` raised for zero/non-numeric; no exception for
valid active values.

---

### AT-02 — topologicalDistance(−2, 1) == 1 (AUTHOR TO RATIFY)

**Requirement:** The topological distance between the lower boundary rail (−2)
and the power core (1) on the KEX active-state topology is exactly 1.

**Validator call:**

```python
from virtual_brain_pc.kex_canonical import topological_distance
result = topological_distance(-2, 1)
assert result == 1   # currently returns None — AUTHOR TO RATIFY
```

**Pass condition:** `topological_distance(-2, 1) == 1`

> **AUTHOR TO RATIFY — AT-02**
>
> The formal metric definition for the signed 5-element set is pending (§1.2 / §A1).
> Once the author ratifies the topology, `topological_distance` must be
> implemented and this assertion enabled.

---

### AT-03 — scalarDelta(−2, 1) == 3 (AUTHOR TO RATIFY)

**Requirement:** The scalar delta between the lower boundary rail (−2) and the
power core (1) is exactly 3 (i.e. `|1 − (−2)| = 3`).

**Validator call:**

```python
from virtual_brain_pc.kex_canonical import scalar_delta
result = scalar_delta(-2, 1)
assert result == 3   # currently returns None — AUTHOR TO RATIFY
```

**Pass condition:** `scalar_delta(-2, 1) == 3`

> **AUTHOR TO RATIFY — AT-03**
>
> This assertion may be satisfied by the simple absolute-difference formula
> `|b − a| = |1 − (−2)| = 3`.  The author must confirm whether `scalarDelta`
> is this simple formula or a more complex algebraic operation, and ratify the
> definition.

---

### AT-04 — add(1, −1) yields Balanced (EXECUTABLE)

**Requirement:** Adding equal-and-opposing active values must produce a Balanced
result, never bare zero.

**Validator call:**

```python
from virtual_brain_pc.kex_canonical import add, is_balanced
record = add(1, -1)
assert is_balanced(record) is True
assert record["result"] == 0.0          # arithmetic result is zero …
assert record["projection"] == "ZERO_AS_CANCELLATION"  # … but typed, not bare
assert record["power_one_preserved"] == 1
```

**Pass condition:** `is_balanced(add(1, -1)) is True` and result carries
`ZERO_AS_CANCELLATION` projection.

---

### AT-05 — Balanced projects to typed zero (EXECUTABLE)

**Requirement:** A Balanced result must yield a non-None typed-zero projection
(not bare `0`).

**Validator call:**

```python
from virtual_brain_pc.kex_canonical import add, project_to_typed_zero
record = add(1, -1)
projection = project_to_typed_zero(record)
assert projection is not None
assert isinstance(projection, str)
assert projection != "0"
assert projection != 0
```

**Pass condition:** `project_to_typed_zero(add(1,-1))` returns a non-None,
non-zero string tag.

---

### AT-06 — Both operands recoverable from Balanced (EXECUTABLE)

**Requirement:** A Balanced record must allow recovery of both original operands
so the non-erasing property is verifiable.

**Validator call:**

```python
from virtual_brain_pc.kex_canonical import add, recover_operands
record = add(1, -1)
operands = recover_operands(record)
assert operands["left_value"] == 1
assert operands["right_value"] == -1
```

**Pass condition:** `recover_operands(add(1,-1))` returns `{"left_value":1, "right_value":-1}`.

---

### AT-07 — Balanced(1,−1) ≠ Balanced(2,−2) canonically (EXECUTABLE)

**Requirement:** Two Balanced records with different operands must produce distinct
canonical keys, even though both arithmetic results are zero.

**Validator call:**

```python
from virtual_brain_pc.kex_canonical import add, balanced_canonical_key
r1 = add(1, -1)
r2 = add(2, -2)
assert balanced_canonical_key(r1) != balanced_canonical_key(r2)
```

**Pass condition:** `balanced_canonical_key(add(1,-1)) != balanced_canonical_key(add(2,-2))`

---

### AT-08 — Canonical encoding is byte-identical across runs (EXECUTABLE)

**Requirement:** The canonical encoding of any given event dict must produce
the same bytes on every run, on any platform (sorted-key compact JSON → SHA-256).

**Validator call:**

```python
from virtual_brain_pc.kex_canonical import canonical_encode, proof_hash
event = {
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
encoded_a = canonical_encode(event)
encoded_b = canonical_encode(event)
assert encoded_a == encoded_b

hash_a = proof_hash(event)
hash_b = proof_hash(event)
assert hash_a == hash_b
assert len(hash_a) == 16
```

**Pass condition:** `canonical_encode(event) == canonical_encode(event)` and
`proof_hash(event) == proof_hash(event)` for all deterministic inputs.

---

### AT-09 — Invalid denominators are unconstructable (AUTHOR TO RATIFY)

**Requirement:** An active-state value that violates the invariants (e.g. bare
zero) must be unconstructable — the constructor must reject it.

**Validator call:**

```python
from virtual_brain_pc.kex_canonical import construct_active_state
import pytest
with pytest.raises(ValueError):
    construct_active_state(0)      # zero rejected
with pytest.raises(ValueError):
    construct_active_state(None)   # non-numeric rejected

s = construct_active_state(1)
assert s["value"] == 1.0
assert s["active"] is True
```

**Pass condition:** `construct_active_state(0)` raises `ValueError`; valid
non-zero values construct successfully.

> **AUTHOR TO RATIFY — AT-09 (additional constraints)**
>
> The current implementation enforces only the NO-Zero-Axis invariant.  If the
> active-state type has additional domain constraints (e.g. must be a member of
> the formal signed set `{−3,−2,1,+2,+3}`, or denominators must be non-zero in
> some ratio representation), those constraints must be ratified and added to
> `construct_active_state`.

---

### AT-10 — Every state carries identity, observer, provenance (AUTHOR TO RATIFY)

**Requirement:** Every canonical event record must carry three provenance fields:
`identity` (what system produced the state), `observer` (what entity observed
it), and `provenance` (chain of prior proof hashes or other lineage data).

**Validator call:**

```python
from virtual_brain_pc.kex_canonical import validate_event_provenance
result = validate_event_provenance(event)
assert result is None or isinstance(result, str)   # None until ratified
```

**Pass condition (once ratified):** `validate_event_provenance(event)` returns
`None` (no errors) when all three required fields are present and non-empty.

> **AUTHOR TO RATIFY — AT-10**
>
> The exact field names and schemas for `identity`, `observer`, and `provenance`
> must be defined (§5.2 / §A6).  Once ratified, `validate_event_provenance`
> must be updated to enforce them and this test must be strengthened to supply
> the fields and assert no errors.

---

## Summary Table

| Test | Description | Status |
|------|-------------|--------|
| AT-01 | No zero active state | ✅ EXECUTABLE |
| AT-02 | topologicalDistance(−2, 1) == 1 | ⏳ AUTHOR TO RATIFY |
| AT-03 | scalarDelta(−2, 1) == 3 | ⏳ AUTHOR TO RATIFY |
| AT-04 | add(1,−1) → Balanced | ✅ EXECUTABLE |
| AT-05 | Balanced projects to typed zero | ✅ EXECUTABLE |
| AT-06 | Both operands recoverable | ✅ EXECUTABLE |
| AT-07 | Balanced(1,−1) ≠ Balanced(2,−2) | ✅ EXECUTABLE |
| AT-08 | Canonical encoding byte-identical | ✅ EXECUTABLE |
| AT-09 | Invalid denominators unconstructable | ✅ EXECUTABLE (zero check); ⏳ full constraints AUTHOR TO RATIFY |
| AT-10 | Every state carries identity/observer/provenance | ⏳ AUTHOR TO RATIFY |

---

## Running the reference validator

```bash
python -m pytest tests/test_kex_canonical.py -v
```

All EXECUTABLE tests must pass.  AUTHOR TO RATIFY tests are present but
guarded so that they do not fail the suite until the author supplies the
formal definitions.

---

## Pending Gates

| Gate | Condition |
|------|-----------|
| `PENDING_AT02_TOPOLOGY_DEFINITION` | Author ratifies §1.2 signed set and distance metric |
| `PENDING_AT03_SCALAR_DELTA_DEFINITION` | Author ratifies `scalarDelta` formula |
| `PENDING_AT09_FULL_CONSTRAINTS` | Author ratifies all invalid-denominator constraints |
| `PENDING_AT10_PROVENANCE_SCHEMA` | Author ratifies identity/observer/provenance field schema |
