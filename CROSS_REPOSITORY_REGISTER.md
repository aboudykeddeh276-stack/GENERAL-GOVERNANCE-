# Cross-Repository Register

This register is the explicit, authoritative record of all repositories governed by GENERAL-GOVERNANCE-.

Rule: no cross-repository integration may be assumed implicitly. A repository is in scope only when it is listed here with an explicit entry.

## Governed Repositories

| Repository | Owner | Role | Governance State | Notes |
|---|---|---|---|---|
| GENERAL-GOVERNANCE- | aboudykeddeh276-stack | GOVERNANCE_ROOT — source-of-truth standards | STATE_MODEL_LOCAL | This repository. Canonical governance standard. |
| BRAINK | aboudykeddeh276-stack | Application repository — BRAINK/KEX system anchor | STATE_MODEL_LOCAL | Swift. NativeChatBot, KEX scripts, governance artifacts. |
| KEDDEH_SOFTWARE_NODES | aboudykeddeh276-stack | Engineering repository — in-house dependencies, calls, and nodes | STATE_MODEL_LOCAL | TypeScript. KEX HyperDrive Dashboard UI. KEX-* inventory. |

## Adoption Status

| Repository | Standard Copied | Checker Run | Result | Proof Gate |
|---|---|---|---|---|
| GENERAL-GOVERNANCE- | N/A (root) | Yes | PROOF_GATE_CHECKER_PASSED | `python scripts/validate-governance.py` |
| BRAINK | Yes | Yes | PROOF_GATE_CHECKER_PASSED | `python scripts/validate-governance.py` |
| KEDDEH_SOFTWARE_NODES | PENDING_GOVERNANCE_ARTIFACT_CREATION | PENDING_CHECKER_RUN | PENDING | — |

## Integration Rules

1. Every integration point between repositories must be explicitly named in this register.
2. No implicit cross-repository access is permitted. Access to a repository requires it to be listed here.
3. When a new repository is added to the ecosystem, add an entry here before referencing it in any other governance artifact.
4. The adoption status table must be updated each time a downstream repository passes its governance checker.

## Pending Gates

- `PENDING_KEDDEH_SOFTWARE_NODES_GOVERNANCE_ARTIFACTS` — KEDDEH_SOFTWARE_NODES must adopt governance baseline files.
- `PENDING_DOWNSTREAM_CHECKER_RUNS` — downstream repositories must run `python scripts/validate-governance.py` and record proof.
- `PENDING_CI_PIPELINE_CONFIGURATION` — continuous integration checks are not yet configured for any repository.
