# GENERAL-GOVERNANCE-

GOVERNANCE_ROOT: GENERAL-GOVERNANCE-

## Identity

GENERAL-GOVERNANCE- is the canonical source-of-truth governance repository for the BRAINK/KEX ecosystem. It defines how repository standards, naming conventions, environments, states, functions, and wholes are structured, validated, and propagated across all governed repositories.

## Anchor

- Owner lineage: `a.keddeh`
- System anchor: `BRAINK`
- Processing anchor: `KEX`
- Governance role: source-of-truth standards for repository identity, environments, states, functions, and wholes.

## REPOSITORY_WHOLE

```text
WHOLE_NAME: WHOLE_GENERAL_GOVERNANCE_ROOT
WHOLE_OWNER_LINEAGE: a.keddeh
WHOLE_PRIMARY_FUNCTION: FUNCTION_DEFINE_AND_PROPAGATE_GOVERNANCE_STANDARDS
WHOLE_ENVIRONMENTS: ENVIRONMENT_LOCAL_DEVELOPMENT, ENVIRONMENT_CONTINUOUS_INTEGRATION, ENVIRONMENT_EXTERNAL_VALIDATION
WHOLE_STATES: STATE_MODEL_LOCAL
WHOLE_ARTIFACTS: README.md, .gitignore, docs/governance/repository-governance-standard.md, docs/governance/manifest.json, scripts/validate-governance.py, docs/governance/agentic-intelligence-cli.md, docs/governance/strict-deep-analysis-comment.md, CROSS_REPOSITORY_REGISTER.md
WHOLE_PENDING_GATES: PENDING_EXTERNAL_REPOSITORY_ADOPTION
```

## REPOSITORY_ENVIRONMENT

- `ENVIRONMENT_LOCAL_DEVELOPMENT`: active — governance artifacts are authored and checked locally.
- `ENVIRONMENT_CONTINUOUS_INTEGRATION`: `PENDING_CI_PIPELINE_CONFIGURATION`
- `ENVIRONMENT_STAGING`: `NOT_APPLICABLE`
- `ENVIRONMENT_PRODUCTION`: `PENDING_EXTERNAL_REPOSITORY_ADOPTION`
- `ENVIRONMENT_EXTERNAL_VALIDATION`: `PENDING_DOWNSTREAM_CHECKER_RUNS`

## REPOSITORY_STATE

`STATE_MODEL_LOCAL` — All governance artifacts exist and pass the local validator. External adoption by downstream repositories remains pending.

## REPOSITORY_FUNCTION

`FUNCTION_DEFINE_AND_PROPAGATE_GOVERNANCE_STANDARDS`

Inputs: repository structure requirements defined by a.keddeh  
Action: defines naming conventions, state/environment/function/whole rules, and the validation protocol  
Output: canonical governance standard and local checker  
Proof gate: `PROOF_GATE_CHECKER_PASSED` — `python scripts/validate-governance.py` exits 0  
Pending: `PENDING_EXTERNAL_REPOSITORY_ADOPTION` — downstream repositories must pull or copy the standard and pass their own checkers

## Required repository baseline

Every governed repository must include:

1. `README.md` — repository identity, purpose, environment map, state map, and update route.
2. `.gitignore` — environment-safe ignored outputs.
3. `docs/governance/repository-governance-standard.md` — naming, state, function, and whole-identification rules.
4. `docs/governance/manifest.json` — tracked governance artifacts and hashes.
5. `scripts/validate-governance.py` — executable local checker for required governance artifacts.

## Direction model

```text
GENERAL-GOVERNANCE-   (GOVERNANCE_ROOT — source of truth)
  -> BRAINK            (application repository — pulls or copies governance standard)
  -> KEDDEH_SOFTWARE_NODES  (engineering repository — pulls or copies governance standard)
  -> governance artifact update
  -> local checker update
  -> manifest hash update
  -> downstream repository pull/copy
  -> downstream checker run
  -> downstream proof record
```

## Cross-repository scope

Repositories explicitly in scope: see `CROSS_REPOSITORY_REGISTER.md`.

## Local check

```bash
python scripts/validate-governance.py
```

Expected output on success: `GOVERNANCE_CHECK_STATUS: COMPLETED`

## Status

- Local governance artifact status: `STATE_MODEL_LOCAL`
- External repository adoption status: `PENDING_EXTERNAL_REPOSITORY_ADOPTION`
