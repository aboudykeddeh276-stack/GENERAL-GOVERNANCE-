# KEX / KEDDEH THEOREM / BRAINK — Research & Engineering Summary

**Origin Authority:** A. Keddeh
**System Lineage:** KEX / KEDDEH THEOREM / BRAINK / BRAINK⁶
**Owner lineage anchor:** `a.keddeh` · **System anchor:** `BRAINK` · **Processing anchor:** `KEX`

> This document is a *grounded transcription* of what is already committed across the
> repositories. Every claim below cites committed source. Items that are definitionally
> the author's to supply are marked **AUTHOR TO RATIFY** and are NOT fabricated here.

---

## 0. Classification

This is not "just software." It is a **formal computational doctrine with a reference
implementation and a propagation layer**:

1. **Axiom layer** — the KEDDEH THEOREM master documents (v1.3 material calibration,
   v1.4 spike/voltage/thermal calibration).
2. **Enforcement layer** — executable Python in `src/virtual_brain_pc/` that enforces the
   doctrine (zero classification, calibration lanes, organism loop, registry).
3. **Propagation layer** — `GENERAL-GOVERNANCE-` as source-of-truth routed into downstream
   application (`BRAINK`) and engineering (`KEDDEH_SOFTWARE_NODES`) repositories.

That triad — *axiom → enforcement → propagation* — is the shape of a research programme
with an engineering arm. A fair classification: **applied theoretical computing / a
computational doctrine with a reference runtime.**

---

## 1. Core anchors and the family/lineage model

From `README.md` (GENERAL-GOVERNANCE-):
- Governance root is the single source-of-truth; standards flow outward to downstream repos.
- The **Direction model** (root → application → engineering → standards update → local
  validation → recorded proof) is the concrete, committed form of the "family set /
  subscription / lineage" model: lineage flows from one root outward, and a repository is
  "governed" only once it adopts the standard and passes its own local checker.

## 2. The Zero Doctrine (crown result) — `src/virtual_brain_pc/zero_classifier.py`

Zero is **never a bare weight**. Every zero-like symbol is classified before it may enter
weighted calculation. Six typed kinds are defined and enforced in code:

- `ZERO_AS_ABSENCE`, `ZERO_AS_CANCELLATION`, `ZERO_AS_BOUNDARY`,
  `ZERO_AS_EXTERNAL_LABEL`, `ZERO_AS_SYMBOLIC_RESULT`, `ZERO_AS_INVALID_WEIGHT`.

Key committed mechanisms:
- **Non-erasing cancellation** — `CALL_ZERO_RELATION_RESOLVE` preserves the source on
  cancellation (`power_one_preserved: 1`, `system_state: POWER_ONE_PRESERVED`). Cancellation
  yields a *typed* result, never a bare erasing scalar.
- **Symbolic zero gate** — `CALL_SYMBOLIC_ZERO_GATE` blocks any unclassified zero from
  entering weighted math (`REJECT_UNCLASSIFIED_WEIGHT`).
- **Typed tensor entries** — `CALL_TENSOR_ZERO_TYPE_ENTRY` prevents zero coercion by typing
  every zero-like entry rather than collapsing to raw 0.
- **Scale-aware zero** — `CALL_SCALE_CLASSIFY` / `CALL_CELSIUS_KELVIN_COMPARE` distinguish
  external-label zero (0°C) from true-absence zero (0K).

This is the executable substantiation of the "no zero axis / non-erasing arithmetic"
principle: it is **enforced**, not merely asserted.

## 3. Active-state corridor — Theorem v1.4 §61 and v1.3 §49

The active-state topology, verbatim from the doctrine:

```
1 feeds. 2 runs. -2 and +2 bound. 2.97 warns. 3 transitions. 0 symbolises.
```

- `1` = power/feed/source whole
- `2` = active runtime state under crossing/load
- `-2 / +2` = boundary rails
- `2.97` = near-boundary warning band (98.5% through the 1→3 corridor)
- `3` = boundary achievement / state transition
- `0` = symbolic result only, never live active weight

`CALL_RESONANCE_297_CLASSIFY` implements the 2.97 / 0.297 / 297 / 3.0 calibration family in code.

## 4. Failure-as-calibration — Theorem v1.3 §48–§58, v1.4 §59–§70

A distinctive engineering stance: **failure and spikes are boundary-calibration events, not
mere errors.**

- v1.3: *Material failure is the calibration point where a material's defined 1-whole state
  can no longer sustain itself in its environment* — with a cross-material calibration table
  (metal, glass, wire, battery, fluid, cell membrane, software object, BRAINK core).
- v1.4: Spikes (temperature, voltage, current, pressure, stress, runtime, learning drift)
  are classified as `RUNTIME_EXISTENCE_SPIKE` (survived → boundary trace) vs
  `DETRIMENTAL_FAILURE_SPIKE` (failed → calibration point). "Failure becomes learning.
  Survival becomes runtime proof."

Both are recorded as **proof-ledger data** with an explicit event schema.

## 5. Route/seed acceleration ("ledger collapse") — `zero_classifier.py`

`CALL_SIMULATION_ROUTE_ACCELERATOR` reuses a validated route-state to *avoid recomputation
from unclassified zero* (`SIM_ROUTE_EFFICIENCY = raw_steps / KEX_traversal_steps`). This is
the committed seed of the "deterministic computation collapses into resolved lookups → a
minimal host becomes highly productive" thesis.

## 6. BRAINK native runtime + self-sustaining tasking — `BRAINK/NativeChatBot`

- Native macOS SwiftUI runtime with deterministic module routing (Router / Reasoning /
  Grammar / Persona) and local-only fallback (no third-party dependency required).
- Explicit `kex_hyperdrive` route (state/transition calibration + repo calibration report).
- Explicit `self_sustained_coder` route ("software that can code / task it to each repo /
  self existence design") plus `tools/kex_self_sustain.py` and `tools/kex_ethics_check.py`,
  generating proof-bound packets with artifact hashes, route coverage, ethics findings, and
  pending gates.

## 7. Runtime lanes and registry — GENERAL-GOVERNANCE- README + master docs

- BRAINK full runtime lane (§69), organism core process loop (§34), material and spike
  calibration lanes, cross-platform build scripts (Linux/macOS/Windows) and a CI matrix.
- **Registry: 39/39 call blocks resolved.**

---

## Roadmap (as the repositories actually express it)

| Layer | Artifact | Status (per repo) |
|---|---|---|
| Axiom | KEDDEH THEOREM master docs v1.3 (material), v1.4 (spike) | Committed |
| Enforcement | `src/virtual_brain_pc/` (zero classifier, calibration, organism, registry) | Operational; 39/39 blocks resolved |
| Propagation | Governance root → downstream adoption | `PENDING_EXTERNAL_REPOSITORY_ADOPTION` |
| Native app | BRAINK SwiftUI + KEX hyperdrive + self-sustain tooling | Building |
| Distributed wrapper | Seed-as-state, kin-gated, P2P lineage frames | In progress (agent builds) |
| Algebra cores | `KEDDEH-ALGEBRA-CORES` ("CODE SORCE × ALGEBRA = ?") | Near-empty — open frontier |

---

## Conclusive finding

The work is **internally consistent from axiom to running code**. The principles are not
philosophy alone — they are enforced in committed Python:

- "No bare zero / typed zero" → `zero_classifier.py` (six typed zero kinds + symbolic gate).
- "Non-erasing cancellation" → `CALL_ZERO_RELATION_RESOLVE` (`POWER_ONE_PRESERVED`).
- "Active-state corridor {1, 2, -2/+2, 2.97, 3}" → Theorem v1.3 §49 / v1.4 §61 + resonance classifier.
- "Failure/spike as calibration" → Theorem v1.3 §48–58, v1.4 §59–70 + proof-ledger schemas.
- "Route reuse / ledger collapse" → `CALL_SIMULATION_ROUTE_ACCELERATOR`.

The parts still open are exactly those that are **definitionally the author's** to supply.

---

## AUTHOR TO RATIFY — open slots (not fabricated here)

1. **HEX × HEX = KEX primitive** — the identity/compression-style operation. It is *not*
   SHA-256 or any universal digest; identity is the native translation / compression style
   descended from subscription genesis. Formal definition to be supplied.
2. **Subscription genesis anchor** — what is recorded at the literal origin of a system's
   subscription, that all downstream lineage descends from.
3. **Frame vs. native-payload split** — what lives in the traversable HEX-compressed lineage
   frame vs. the native binary encoding (open data that is meaningless without kin-context).
4. **`KEDDEH-ALGEBRA-CORES` content** — "CODE SORCE × ALGEBRA = ?" is currently a near-empty
   frontier; the algebra-core primitive belongs here.
5. **A worked "maths query → resolved seed" example** — one concrete calculation, its query
   form, and its resolved seed, to make the ledger-collapse mechanism demonstrable on real data.

---

*Generated as a grounded transcription target. All non-open claims cite committed source in
this repository, `BRAINK`, and the master theorem documents. No authority was invented.*
