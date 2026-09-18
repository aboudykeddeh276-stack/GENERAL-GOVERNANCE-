# KEX Canonical Specification

**Spec version:** `kex-canonical v1`  
**Authority:** A. Keddeh — BRAINK / KEX / GENERAL-GOVERNANCE-  
**Governance root:** `GENERAL-GOVERNANCE-` (`aboudykeddeh276-stack/GENERAL-GOVERNANCE-`)  
**Status:** `STATE_MODEL_LOCAL`  
**Proof gate:** `PROOF_GATE_CHECKER_PASSED`

---

## Purpose

This document is the single authoritative, versioned, citeable specification for the
KEX zeroless active-state architecture.  All governed repositories (`BRAINK`,
`KEDDEH_SOFTWARE_NODES`, and any future entrant in `CROSS_REPOSITORY_REGISTER.md`)
must conform to every section marked **DEFINED**.  Sections marked
**AUTHOR TO RATIFY** contain placeholder definitions derived from contextual evidence
in the repository; the author must supply the verbatim formal text before those
sections are considered binding.

Sources used to compile this specification:

| File | Sections cited |
|------|---------------|
| `docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.3.md` | §48–58 (material failure, number roles) |
| `docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.4.md` | §59–70 (spike calibration, number roles) |
| `src/virtual_brain_pc/zero_classifier.py` | Zero classification doctrine |
| `src/virtual_brain_pc/braink_runtime.py` | 14-step runtime lane, proof ledger |
| `src/virtual_brain_pc/registry.py` | Registry block catalogue |
| `docs/governance/repository-governance-standard.md` | Naming conventions, proof gates |
| `docs/LIVE_STATE_v1.6.json` | Live output of the full runtime |

---

## §1 — Active-State Set and NO-Zero-Axis Invariant

### §1.1 Number roles (DEFINED)

The following roles are formally stated in `docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.3.md §49`
and `v1.4 §61` and are implemented throughout `src/virtual_brain_pc/`:

| Symbol | Role | BRAINK name |
|--------|------|-------------|
| `1`    | Power/feed/source whole — the foundational live source that feeds the active process | `ACTIVE_CORE_1` / `POWER_CORE_1` |
| `2`    | Active runtime state — the system under active crossing, load, or transformation | `ACTIVE_STATE_2` |
| `-2`   | Lower boundary rail | `BOUNDARY_PAIR_DETECTOR` (minus side) |
| `+2`   | Upper boundary rail | `BOUNDARY_PAIR_DETECTOR` (plus side) |
| `2.97` | Near-boundary band — the system is 98.5 % through the 1→3 corridor | `NEAR_FAILURE_297_BAND` |
| `3`    | Boundary achievement — threshold reached; new state, transition, or failure produced | `BOUNDARY_3_ACHIEVEMENT` |
| `0`    | Symbolic result only — cancellation, absence, or boundary label; **never a live active weight** | Zero doctrine (§3) |

Corrected formal statement (v1.3 §49):

```
1 feeds.
2 runs.
-2 and +2 bound.
2.97 warns.
3 transitions.
0 symbolises.
```

### §1.2 Signed five-element active-state set {−3, −2, 1, +2, +3} — AUTHOR TO RATIFY

> **AUTHOR TO RATIFY — §1.2**
>
> The repository establishes unsigned `3` for boundary achievement and signed
> `±2` for boundary rails.  The explicit formalization of the complete signed set
> `{−3, −2, 1, +2, +3}` as the exhaustive active-state topology, together with:
>
> - the formal definition of `−3` (lower boundary achievement),
> - the rank map `{−3 → 1, −2 → 2, 1 → 3, +2 → 4, +3 → 5}`, and
> - the proof that no element of this set equals zero
>
> has not yet been found in any committed artifact.  Insert the author's verbatim
> formal definition here before this section is considered binding.

### §1.3 NO-Zero-Axis Invariant (DEFINED by doctrine; formal proof — AUTHOR TO RATIFY)

The zero-axis exclusion doctrine is stated across all theorem documents and is
enforced in code:

> **Doctrine (defined):** Zero is never a live active weight, active state, or
> active axis value.  Every zero-like result must be classified before it may enter
> weighted calculation.  (`zero_classifier.py` §7; `v1.3 §49`; `v1.4 §61`.)

The formal mathematical proof that the active-state set has an empty intersection
with `{0}` is:

> **AUTHOR TO RATIFY — §1.3 formal proof**
>
> Provide the symbolic/algebraic proof that every element of the active-state set
> is non-zero and that no arithmetic operation on active-state elements can produce
> a bare zero active state (as opposed to a typed zero projection).

---

## §2 — State Kinds — AUTHOR TO RATIFY

> **AUTHOR TO RATIFY — §2**
>
> The following state-kind names are referenced in the prior conversation context
> and in the problem statement but are **not defined in any committed repository
> artifact** at the time this specification was compiled:
>
> | Ordinal (encoding) | State kind name | Intended meaning (contextual inference only) |
> |--------------------|-----------------|----------------------------------------------|
> | 1 | Measured | A directly observed active-state value |
> | 2 | Balanced | Two opposing active values that cancel to a typed zero |
> | 3 | Baseline | The reference / equilibrium active value |
> | 4 | Absent | No active value present; maps to ZERO_AS_ABSENCE |
> | 5 | Unknown | Classification not yet determined |
> | 6 | Invalid | Violates active-state constraints |
> | 7 | Untranslated | Raw input not yet mapped to an active-state value |
> | 8 | Equilibrium | Stable balanced state — distinct from Balanced (see §4) |
>
> The author must provide: (a) the complete, canonical list of state kind names in
> the correct order; (b) whether encoding starts at 0 or 1; (c) the exact
> distinction between Balanced and Equilibrium; and (d) any state kinds not listed
> above.

---

## §3 — Non-Erasing Arithmetic Law (DEFINED)

### §3.1 Law statement

The non-erasing arithmetic law is implemented in `src/virtual_brain_pc/zero_classifier.py`
(`CALL_ZERO_RELATION_RESOLVE`) and stated throughout the theorem documents:

> **Law:** When two active values cancel (their arithmetic result equals or is
> within `1e-10` of zero), the result is **not** bare zero.  Instead:
>
> 1. Both operands are preserved verbatim in the result record.
> 2. The result is classified as `ZERO_AS_CANCELLATION`.
> 3. The `power_one_preserved` anchor remains `1`.
>
> Bare `0` is never emitted as a live active weight.

Python reference (from `zero_classifier.py`):

```python
def CALL_ZERO_RELATION_RESOLVE(
    left_value: float,
    right_value: float,
    operation: str = "addition",
) -> Dict[str, object]:
    result = left_value + right_value if operation == "addition" else left_value - right_value
    produced_zero = abs(result) < 1e-10
    return {
        "left_value": left_value,
        "right_value": right_value,
        "result": result,
        "produced_zero": produced_zero,
        "power_one_preserved": 1,
        "zero_interpretation": ZERO_AS_CANCELLATION if produced_zero else "NO_ZERO_PRODUCED",
        "system_state": "POWER_ONE_PRESERVED",
    }
```

### §3.2 Typed projection after cancellation — AUTHOR TO RATIFY

> **AUTHOR TO RATIFY — §3.2**
>
> The problem statement requires: "cancellation yields Balanced retaining both
> operands + typed projection, never bare 0".  The repository currently emits
> `ZERO_AS_CANCELLATION` (a string constant) and preserves both operands.  The
> formal definition of the **Balanced** result type as a first-class value (not
> merely a string tag), and the exact typed-projection encoding (§4), must be
> ratified by the author.

---

## §4 — Typed Projection Kinds — AUTHOR TO RATIFY

> **AUTHOR TO RATIFY — §4**
>
> The repository defines the following zero-classification string constants in
> `zero_classifier.py`:
>
> | Constant | Current meaning |
> |----------|----------------|
> | `ZERO_AS_CANCELLATION` | Two equal-and-opposing active values cancelled |
> | `ZERO_AS_ABSENCE` | No active value is present |
> | `ZERO_AS_BOUNDARY` | Zero is a boundary / seam / threshold marker |
> | `ZERO_AS_EXTERNAL_LABEL` | Zero is a coordinate offset (e.g. 0 °C) |
> | `ZERO_AS_SYMBOLIC_RESULT` | Zero is the output of a resolved symbolic expression |
> | `ZERO_AS_INVALID_WEIGHT` | Zero is not classifiable; must not enter calculation |
>
> The problem statement requires three **distinct typed projection kinds**:
>
> - `BalancedZero` — zero produced by cancellation of two equal-and-opposing active values
> - `BaselineZero` — zero at the reference / baseline state
> - `Absent` — zero as the absence of an active value
>
> and asserts `BalancedZero ≠ BaselineZero ≠ Absent`.
>
> The author must supply: (a) the canonical names for all typed projection kinds;
> (b) whether `BalancedZero` maps to `ZERO_AS_CANCELLATION`, `BaselineZero` maps
> to `ZERO_AS_BOUNDARY` or a new kind, and `Absent` maps to `ZERO_AS_ABSENCE`;
> (c) the complete set of projection kinds and their mutual distinctness proofs.

---

## §5 — Canonical Event Schema

### §5.1 Proof ledger entry format (DEFINED)

Every BRAINK runtime event is committed to the proof ledger via
`CALL_PROOF_LEDGER_COMMIT` (`braink_runtime.py`).  The canonical entry format is:

```json
{
  "system":               "<string — target system identity>",
  "active_whole_before":  1,
  "active_runtime_state": 2,
  "lower_boundary":       "<number — −2 rail or domain equivalent>",
  "upper_boundary":       "<number — +2 rail or domain equivalent>",
  "near_boundary_band":   "<2.97 or null>",
  "achieved_boundary":    "<3 or null>",
  "spike_value":          "<number — observed value>",
  "environment":          "<string — runtime environment>",
  "result":               "symbolic_zero_only_if_cancelled_or_absent"
}
```

The proof hash is computed as:

```
proof_hash = SHA-256( JSON.stringify(entry, sorted_keys=True) )[:16]
```

This guarantees byte-identical output for identical inputs across runs.
Reference: `braink_runtime.py → CALL_PROOF_LEDGER_COMMIT`.

### §5.2 Identity, observer, and provenance fields — AUTHOR TO RATIFY

> **AUTHOR TO RATIFY — §5.2**
>
> The problem statement requires every event to carry: `identity`, `observer`,
> and `provenance`.  The current proof ledger entry records `system` and
> `environment` but does not have explicit `identity`, `observer`, or `provenance`
> fields.  The author must define: (a) whether `system` is the identity field;
> (b) what the `observer` field must contain; (c) the schema for `provenance`
> (e.g. chain of prior proof hashes, timestamp, author key).

### §5.3 Explicit exclusion list — nondeterministic host values (DEFINED by policy; exact list — AUTHOR TO RATIFY)

The governance standard (`repository-governance-standard.md §9`) and the runtime
model prohibit host-environment nondeterminism from entering proof ledger entries.
The following host values are excluded from all canonical event fields:

| Excluded value | Reason |
|----------------|--------|
| Wall-clock timestamps from `datetime.now()` | Non-deterministic across runs |
| OS process IDs (`os.getpid()`) | Non-deterministic across runs |
| Memory addresses / object `id()` | Non-deterministic across runs |
| Random numbers without a fixed seed | Non-deterministic |
| Floating-point results of hardware-dependent operations | Platform-variant |
| Environment variable values not declared in governance | Undeclared external inputs |

> **AUTHOR TO RATIFY — §5.3 complete exclusion list**
>
> The above list is derived from the runtime's construction and general
> determinism principles.  The author must ratify the complete, exhaustive
> exclusion list with any additions or exceptions.

---

## §6 — Spec Version

| Field | Value |
|-------|-------|
| Spec identifier | `kex-canonical v1` |
| Theorem base | `KEDDEH_THEOREM::v1.5` |
| Governance root | `GENERAL-GOVERNANCE-` |
| First committed | See git log for `SPEC/kex-canonical.md` |
| Next review gate | When any AUTHOR TO RATIFY slot is filled by the author |

---

## Appendix A — AUTHOR TO RATIFY Summary

The following slots require the author's verbatim formal definitions before the
corresponding sections are binding:

| Slot | Section | What is needed |
|------|---------|----------------|
| A1 | §1.2 | Formal signed 5-element set `{−3,−2,1,+2,+3}`, rank map, zero-exclusion proof |
| A2 | §1.3 | Mathematical proof that active-state set ∩ {0} = ∅ |
| A3 | §2   | Complete state-kind list with encoding ordinals, Balanced vs Equilibrium distinction |
| A4 | §3.2 | Formal Balanced result type as a first-class value |
| A5 | §4   | Complete typed projection kind names, canonical distinctness proofs |
| A6 | §5.2 | Identity, observer, and provenance field definitions |
| A7 | §5.3 | Complete nondeterministic host-value exclusion list |
