# KEX Canonical Specification — kex-canonical v1

**Spec version:** `kex-canonical v1`  
**Author / Origin Authority:** A. Keddeh  
**System Lineage:** KEX / KEDDEH THEOREM / BRAINK / BRAINK⁶  
**Governance Root:** `GENERAL-GOVERNANCE-`  
**Status:** `STATE_MODEL_LOCAL` — formal sections marked `AUTHOR TO RATIFY` must be ratified verbatim by A. Keddeh before any downstream repository treats them as frozen.

---

## How to read this document

Every section is marked with one of two statuses:

- **DEFINED HERE** — the rule is faithfully transcribed from artifacts already present in this repository (files cited inline). Downstream repositories may rely on it immediately.
- **AUTHOR TO RATIFY** — the slot is explicitly reserved. The existing repository does not yet contain a verbatim formal definition. A. Keddeh must supply the canonical text; nothing in this section may be treated as authoritative until that ratification is committed.

This document is a *transcription target*, not an invented authority.

---

## §1 — Active-State Numerical Model (DEFINED HERE)

*Sources: `docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.3.md §49`, `docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.4.md §61`, `src/virtual_brain_pc/braink_runtime.py`*

The BRAINK/KEX active-state numerical model assigns concrete roles to a fixed set of numbers. Zero is **never** a live active weight.

| Number | Role | Meaning |
|---|---|---|
| `1` | Power / feed / source whole | The foundational live source that feeds the active process |
| `2` | Active runtime state | The system under active crossing, load, electricity, heat, or transformation |
| `-2` | Lower boundary rail | The lower limit the active state crosses against |
| `+2` | Upper boundary rail | The upper limit the active state crosses against |
| `2.97` | Near-boundary band | The system is extremely close to boundary achievement or failure (99 % of the full 3 boundary) |
| `3` | Boundary achievement | The threshold is reached; a new state, failure, transition, or signal is produced |
| `0` | Symbolic result only | Cancellation, absence, or boundary label — **never** a live active weight |

Corrected statement (verbatim from §61):

```
1 feeds.
2 runs.
-2 and +2 bound.
2.97 warns.
3 transitions.
0 symbolises.
```

### 1.1 — No-zero invariant

Zero **must not** be re-introduced as a live active weight at any layer of the system. The invariant is:

> A value of `0` entering weighted calculation is a **protocol violation**. Every zero-like value must first pass through zero classification (`CALL_ZERO_CLASSIFY`) before it may proceed. Any zero that cannot be classified is rejected as `ZERO_AS_INVALID_WEIGHT`.

This invariant is enforced at runtime by `CALL_SYMBOLIC_ZERO_GATE` (`src/virtual_brain_pc/zero_classifier.py`).

---

### 1.2 — KEX Active-State Set {−3, −2, 1, +2, +3} with ranks 1..5

> **AUTHOR TO RATIFY**
>
> The problem statement and prior conversation reference a formal five-element KEX active-state set `{−3, −2, 1, +2, +3}` with an associated rank map (rank 1 through rank 5). The current repository encodes the operational analogue (`-2/+2` boundary rails, `1` power source, `3` boundary achievement) but does **not** contain a verbatim formal definition of this five-element set or its rank assignment.
>
> A. Keddeh must supply:
> - The explicit enumeration `{−3, −2, 1, +2, +3}` with each element's formal rank (1..5).
> - The topological distance metric: `topologicalDistance(a, b)` = ?
> - The scalar delta metric: `scalarDelta(a, b)` = ?
> - A proof that the set is closed under the defined topology.
> - An explicit statement forbidding the re-introduction of a zero axis.
>
> Until ratified, downstream repositories **must not** hard-code these values as if they were defined here.

---

## §2 — State Kinds

> **AUTHOR TO RATIFY**
>
> The prior conversation references the following named state kinds whose encoding starts at 1 (never 0):
>
> | State kind | Informal meaning |
> |---|---|
> | `Measured` | An observed, quantified reading |
> | `Balanced` | Two active contributions that cancel into a typed result |
> | `Baseline` | A reference-point state |
> | `Absent` | No value present |
> | `Unknown` | Value not yet determined |
> | `Invalid` | A value that violates the active-state constraints |
> | `Untranslated` | A value that has not yet been mapped into the active-state domain |
> | `Equilibrium` | A state where opposing forces are in balance |
>
> The current repository does **not** contain a verbatim formal definition of these kinds, their encoding integers (starting at 1), or their enumeration rules. The zero-classifier doctrine (`src/virtual_brain_pc/zero_classifier.py`) classifies zero-like results into `ZERO_AS_ABSENCE`, `ZERO_AS_CANCELLATION`, `ZERO_AS_BOUNDARY`, `ZERO_AS_EXTERNAL_LABEL`, `ZERO_AS_SYMBOLIC_RESULT`, and `ZERO_AS_INVALID_WEIGHT`, which are the related operational classifications — but these are not the same as the formal state-kind enumeration.
>
> A. Keddeh must supply:
> - The exhaustive list of state kinds, each with its integer encoding (1-based, never 0).
> - The rule governing which state kinds may appear as the source or target of a state transition.
> - Whether the list is open (extensible) or closed.

---

## §3 — Non-Erasing Arithmetic Law

*Sources: `src/virtual_brain_pc/zero_classifier.py` — `CALL_ZERO_RELATION_RESOLVE`; `docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.3.md §48–50`*

### 3.1 — Operational definition (DEFINED HERE)

The repository enforces a *non-erasing* relation-resolution rule: when two active values cancel each other (their sum is within `1e-10` of zero), the power-one source is **always** preserved and the result is classified as `ZERO_AS_CANCELLATION`, not discarded.

```python
# src/virtual_brain_pc/zero_classifier.py — CALL_ZERO_RELATION_RESOLVE
{
    "left_value": left_value,
    "right_value": right_value,
    "result": 0.0,                          # scalar result
    "produced_zero": True,
    "power_one_preserved": 1,               # source is never erased
    "zero_interpretation": "ZERO_AS_CANCELLATION",
    "system_state": "POWER_ONE_PRESERVED",
}
```

The material calibration doctrine (§48–50, v1.3) states:

> "Failure does not imply matter disappears. It means the prior functional whole-state identity is no longer preserved."

### 3.2 — Formal law for typed projections

> **AUTHOR TO RATIFY**
>
> The prior conversation describes a formal non-erasing arithmetic law: cancelling contributions must yield a `Balanced` state that retains both operands plus a *typed projection*, never a bare scalar `0`. The formal law reads approximately:
>
> ```
> add(a, b) where a + b = 0  →  Balanced(a, b, projection: TypedZero)
> ```
>
> and must satisfy:
> - Both operands `a` and `b` are recoverable from the `Balanced` result.
> - `Balanced(1, -1)` is canonically distinct from `Balanced(2, -2)`.
> - The result is never a bare scalar `0`.
>
> The current repository does **not** contain a verbatim formal algebraic statement of this law (only the operational implementation above).
>
> A. Keddeh must supply:
> - The formal algebraic statement of `add(a, b)` for the active-state set.
> - The definition of `TypedZero` as a type (not a scalar).
> - Proof that both operands are recoverable.
> - The canonical identity rule for `Balanced(a, b)`.

---

## §4 — Typed Projection Kinds

> **AUTHOR TO RATIFY**
>
> The prior conversation distinguishes typed projection kinds:
>
> - `BalancedZero` — the projection produced when two equal and opposite active contributions cancel.
> - `BaselineZero` — the projection produced by a baseline reference state.
> - `Absent` — the projection produced by absence of a value.
>
> These are distinct types; `BalancedZero ≠ BaselineZero ≠ Absent`. The zero-classifier doctrine (`src/virtual_brain_pc/zero_classifier.py`) provides the operational precursors (`ZERO_AS_CANCELLATION`, `ZERO_AS_ABSENCE`, etc.) but does **not** yet define these as formal typed projection kinds with algebraic identities.
>
> A. Keddeh must supply:
> - The exhaustive list of typed projection kinds with formal definitions.
> - The algebraic rule specifying when each projection kind is emitted.
> - A proof or invariant establishing that no two distinct projection kinds are equal.

---

## §5 — Canonical Event Schema + Exclusion List

### 5.1 — Canonical event schema (DEFINED HERE)

*Sources: `docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.3.md §54`, `docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.4.md §64`, `src/virtual_brain_pc/braink_runtime.py — CALL_PROOF_LEDGER_COMMIT`*

A transition/calibration event has the following canonical fields, drawn from the failure spike schema used throughout the runtime:

```json
{
  "system":              "<string — target system identity>",
  "active_whole_before": 1,
  "active_runtime_state": 2,
  "lower_boundary":      "<number — the -2 rail>",
  "upper_boundary":      "<number — the +2 rail>",
  "near_boundary_band":  "<number | null — 2.97 or null>",
  "achieved_boundary":   "<3 | null>",
  "spike_value":         "<number — the observed value>",
  "environment":         "<string — the runtime environment>",
  "result":              "symbolic_zero_only_if_cancelled_or_absent"
}
```

The proof record additionally carries:

```json
{
  "proof_hash":   "<16-character hex — SHA-256 prefix over sorted-key canonical JSON>",
  "proof_status": "committed"
}
```

Hashing is performed deterministically: `json.dumps(entry, sort_keys=True)` → UTF-8 encode → SHA-256 (`src/virtual_brain_pc/braink_runtime.py — CALL_PROOF_LEDGER_COMMIT`).

### 5.2 — Canonicalization exclusion list

> **AUTHOR TO RATIFY (partial)**
>
> The prior conversation lists host values that **must be excluded** from canonical event payloads to guarantee byte-identical encoding across runs:
>
> | Excluded value | Reason |
> |---|---|
> | Memory addresses | Platform-dependent; change across runs and processes |
> | Thread / goroutine IDs | Non-deterministic; vary across concurrency schedules |
> | Unsorted map / dict iteration order | Language-runtime-dependent; must always be sorted |
> | Wall-clock timestamp as identity | Changes per run; use content-addressing, not time, for identity |
> | Platform-dependent float formatting | Trailing digits differ across platforms |
>
> The current repository enforces `sort_keys=True` in all canonical JSON serialisation (operationally present). The full exclusion list has not been ratified as an explicit governance rule.
>
> A. Keddeh must supply a verbatim, exhaustive exclusion list that every governed repository must enforce.

---

## §6 — Observer, Identity, and Provenance Requirements

> **AUTHOR TO RATIFY**
>
> The prior conversation states: "Every state carries identity, observer, provenance." The current repository embeds `system`, `environment`, and `proof_hash` in every event record, which correspond operationally to identity, context, and proof provenance. However, a formal definition of the *observer* field — what it means, what values are valid, and how it is bound to an event — is **not** present as a verbatim rule.
>
> A. Keddeh must supply:
> - A formal definition of `observer` (who or what observed the transition).
> - A formal definition of `identity` (the unique identifier of the state/event).
> - A formal definition of `provenance` (the chain of prior states/events that produced this one).
> - The rule that every active-state event must carry all three.

---

## §7 — Zero Classification Doctrine (DEFINED HERE)

*Source: `src/virtual_brain_pc/zero_classifier.py §7`*

Zero must be classified before it may enter weighted calculation. The classification kinds are:

| Class constant | Meaning |
|---|---|
| `ZERO_AS_ABSENCE` | The value is absent or missing |
| `ZERO_AS_CANCELLATION` | Two equal and opposite active values cancelled |
| `ZERO_AS_BOUNDARY` | The value is a boundary seam, threshold, or origin |
| `ZERO_AS_EXTERNAL_LABEL` | The value is a coordinate label (e.g. 0°C) not a true zero |
| `ZERO_AS_SYMBOLIC_RESULT` | The value is a symbolic output of a resolved relation |
| `ZERO_AS_INVALID_WEIGHT` | The value cannot be classified; **must be rejected** |

The gate `CALL_SYMBOLIC_ZERO_GATE` blocks any value with class `ZERO_AS_INVALID_WEIGHT` from entering weighted calculation. `valid_for_use = True` only when the class is not `ZERO_AS_INVALID_WEIGHT`.

---

## §8 — Proof Ledger (DEFINED HERE)

*Source: `src/virtual_brain_pc/braink_runtime.py — CALL_PROOF_LEDGER_COMMIT`*

Every state transition must be committed to the proof ledger. The ledger entry is:

```python
serialized = json.dumps(ledger_entry, sort_keys=True)
proof_hash  = hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]
```

Properties:
- **Deterministic**: same entry always produces the same hash.
- **Content-addressed**: the hash is derived from the entry content, not from time or host state.
- **Non-repudiable**: the full entry is stored alongside the hash; the hash cannot be verified without the entry.

The proof ledger is the mechanism by which failure and boundary-achievement events become calibration data (§48–54 of v1.3, §64–67 of v1.4).

---

## §9 — Naming Convention (DEFINED HERE)

*Source: `docs/governance/repository-governance-standard.md §3`*

All names across all governed repositories must carry the following required prefixes:

| Category | Required prefix | Example |
|---|---|---|
| Environment | `ENVIRONMENT_` | `ENVIRONMENT_LOCAL_DEVELOPMENT` |
| State | `STATE_` | `STATE_MODEL_LOCAL` |
| Function | `FUNCTION_` | `FUNCTION_VALIDATE_GOVERNANCE` |
| Whole system | `WHOLE_` | `WHOLE_GENERAL_GOVERNANCE_ROOT` |
| Artifact | `ARTIFACT_` | `ARTIFACT_GOVERNANCE_MANIFEST_JSON` |
| Proof gate | `PROOF_GATE_` | `PROOF_GATE_CHECKER_PASSED` |
| Pending boundary | `PENDING_` | `PENDING_EXTERNAL_REPOSITORY_ADOPTION` |

BRAINK call blocks use the naming convention `BRAINK::<MODULE>::<ACTION>::v<N>` and are invoked as `CALL_<NAME>`. All 39 registered call blocks are resolved as of `LIVE_STATE_v1.6`.

---

## §10 — Spec Version Identifier

**Spec version string:** `kex-canonical v1`

Other repositories pin this spec by recording:

```
KEX_CANONICAL_SPEC_VERSION: kex-canonical v1
GOVERNANCE_ROOT: GENERAL-GOVERNANCE-
```

A change to any **DEFINED HERE** section increments the minor version. A change to any **AUTHOR TO RATIFY** section (when ratified) increments the major version. The version is updated in this file and re-recorded in `docs/governance/manifest.json`.

---

## §11 — Open Slots Summary

The following items are explicitly unratified and require A. Keddeh's verbatim formal definitions before any downstream repository may treat them as frozen:

| Slot | Section | What is needed |
|---|---|---|
| KEX active-state set `{−3, −2, 1, +2, +3}` with ranks 1..5 | §1.2 | Enumeration, rank map, topological distance, scalar delta |
| State kinds (Measured, Balanced, Baseline, Absent, Unknown, Invalid, Untranslated, Equilibrium) | §2 | Exhaustive list with 1-based integer encodings |
| Formal non-erasing arithmetic law | §3.2 | Algebraic statement of `add(a,b)` with typed projection |
| Typed projection kinds (BalancedZero, BaselineZero, Absent, …) | §4 | Formal list with algebraic identities |
| Canonicalization exclusion list | §5.2 | Verbatim exhaustive list |
| Observer, identity, provenance fields | §6 | Formal definitions and binding rules |
