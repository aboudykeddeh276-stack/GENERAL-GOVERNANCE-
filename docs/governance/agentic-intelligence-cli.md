# BRAINK/KEX Agentic Intelligence CLI Start

## Purpose

This document starts the automated agentic tool, intelligence software tool, and programmer route for BRAINK/KEX repositories.

## Function

`FUNCTION_INVENTORY_REPOSITORIES_AND_PLAN_AGENTIC_PROGRAMMER_INPUTS`

The governance root defines the boundary within which agentic tools are permitted to operate. The first executable artifact for agentic intelligence is `scripts/braink-agent-cli.py` in the BRAINK repository.

## Scope

Agentic tools may only operate on repositories explicitly listed in `CROSS_REPOSITORY_REGISTER.md`. No implicit cross-repository access is permitted.

Repositories currently in scope:
- `GENERAL-GOVERNANCE-` (governance root)
- `BRAINK` (system anchor — contains `scripts/braink-agent-cli.py`)
- `KEDDEH_SOFTWARE_NODES` (engineering repository — in-house dependencies and nodes)

## Commands (executed from BRAINK repository)

```bash
python scripts/braink-agent-cli.py status
python scripts/braink-agent-cli.py scan --repo-root ..
```

## Boundary

- Agentic tools do not execute arbitrary code from discovered repositories.
- Agentic tools only prove local repository discovery and local artifact classification.
- Repositories not present in the filesystem remain `PENDING_EXTERNAL_REPOSITORY_ACCESS_FOR_REPOS_NOT_PRESENT_LOCALLY`.
- Remote fetch, push, and cross-repository adoption remain pending until authenticated access is provided and each repository passes its own checker.

## Next build gates

1. `PENDING_KEDDEH_SOFTWARE_NODES_GOVERNANCE_ARTIFACTS` — add governance baseline to KEDDEH_SOFTWARE_NODES.
2. `PENDING_CI_PIPELINE_CONFIGURATION` — configure CI to run `python scripts/validate-governance.py` on each governed repository.
3. `PENDING_DOWNSTREAM_CHECKER_RUNS` — downstream repositories must run the checker and record proof.
4. `PENDING_AUTHENTICATED_REMOTE_FETCH_OR_PUSH` — remote operations require authenticated credentials.

## Status

- `STATE_MODEL_LOCAL` — this document is a local governance artifact.
- `PENDING_EXTERNAL_ADOPTION` — external tools and collaborators must adopt or reference this before it becomes an external process constraint.
