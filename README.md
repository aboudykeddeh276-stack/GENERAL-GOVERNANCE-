# GENERAL-GOVERNANCE-

Brain-inspired virtualized computer with agent-driven uniform builds across Linux, Windows, and macOS.

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
WHOLE_ARTIFACTS: README.md, .gitignore, docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.3.md, docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.4.md, src/virtual_brain_pc/, scripts/, tests/
WHOLE_PENDING_GATES: PENDING_EXTERNAL_REPOSITORY_ADOPTION
```

## REPOSITORY_ENVIRONMENT

- `ENVIRONMENT_LOCAL_DEVELOPMENT`: active — governance artifacts are authored and checked locally.
- `ENVIRONMENT_CONTINUOUS_INTEGRATION`: active — GitHub Actions CI matrix on ubuntu/windows/macos.
- `ENVIRONMENT_STAGING`: `NOT_APPLICABLE`
- `ENVIRONMENT_PRODUCTION`: active — BRAINK runtime lanes operational.
- `ENVIRONMENT_EXTERNAL_VALIDATION`: `PENDING_DOWNSTREAM_CHECKER_RUNS`

## REPOSITORY_STATE

`STATE_MODEL_LOCAL` — All governance and runtime artifacts exist, pass tests, and produce verified proof ledger commits.

## What This Build Includes

- Virtualized computer core:
	- Instruction stepping
	- Register and memory model
	- Deterministic trace output
- Brain-inspired runtime controller:
	- Multi-layer "cortex" signal transforms
	- Adaptive directive output (`expand`, `hold`, `throttle`)
- Agent system for uniform builds:
	- `BuildAgent`
	- `ValidationAgent`
	- `PackagingAgent`
- Material failure calibration lane:
	- `CALL_MATERIAL_WHOLE_BIND`
	- `CALL_ACTIVE_STRESS_CROSSING`
	- `CALL_BOUNDARY_PAIR_DETECT`
	- `CALL_NEAR_FAILURE_297_BAND`
	- `CALL_BOUNDARY_3_ACHIEVEMENT`
	- `CALL_FAILURE_CALIBRATION_LEDGER`
- Spike calibration lane:
	- `CALL_SPIKE_EVENT_CLASSIFY`
	- `CALL_TEMPERATURE_SPIKE_BOUNDARY`
	- `CALL_VOLTAGE_SPIKE_BOUNDARY`
	- `CALL_RUNTIME_EXISTENCE_TRACE`
	- `CALL_DETRIMENTAL_FAILURE_SPIKE`
	- `CALL_BOUNDARY_REALIGNMENT_ENGINE`
- BRAINK full runtime lane (§69):
	- 14-step proof-committed lane via `braink-run`
- Organism core process loop (§34):
	- Power-core, thinking, mirror-update, learning, theorem ledger via `organism-run`
- Zero classifier (§7):
	- Full zero doctrine classification and symbolic gate
- Cross-platform build execution:
	- Linux script
	- macOS script
	- Windows PowerShell script
- CI matrix on GitHub Actions for all three operating systems
- Registry: 39 BRAINK call blocks, all resolved

## Project Layout

```
.
|-- .github/workflows/uniform-build.yml
|-- pyproject.toml
|-- docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.3.md
|-- docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.4.md
|-- docs/LIVE_STATE_v1.6.json
|-- src/virtual_brain_pc/
|   |-- __init__.py
|   |-- agents.py
|   |-- braink_runtime.py
|   |-- cli.py
|   |-- cognition.py
|   |-- core.py
|   |-- material_calibration.py
|   |-- orchestrator.py
|   |-- organism.py
|   |-- registry.py
|   |-- spike_calibration.py
|   `-- zero_classifier.py
|-- scripts/
|   |-- bilateral_rollout.sh
|   |-- build_linux.sh
|   |-- build_macos.sh
|   `-- build_windows.ps1
`-- tests/test_smoke.py
```

## Quick Start

Install local package:

```bash
python -m pip install -e .
```

Run the virtual computer simulation:

```bash
python -m virtual_brain_pc.cli run --cycles 8
```

Run one platform agent build pipeline:

```bash
python -m virtual_brain_pc.cli build --target linux
python -m virtual_brain_pc.cli build --target windows
python -m virtual_brain_pc.cli build --target macos
```

Run full uniform build matrix locally:

```bash
python -m virtual_brain_pc.cli build-all
```

Run material-failure calibration lane:

```bash
python -m virtual_brain_pc.cli material-calibrate --material steel_beam --environment ambient_lab --whole-identity beam_integrity --force 97 --lower -100 --upper 100
```

Print registry blocks:

```bash
python -m virtual_brain_pc.cli registry
```

Run spike-boundary calibration lane:

```bash
python -m virtual_brain_pc.cli spike-calibrate --spike-kind temperature --observed-value 97 --safe-boundary 90 --failure-boundary 100 --environment ambient_lab --target-system cpu_runtime
```

Run BRAINK full runtime lane (§69):

```bash
python -m virtual_brain_pc.cli braink-run --tick-id 1 --system cpu_runtime --environment production --spike-kind temperature --observed-value 97 --safe-boundary 90 --failure-boundary 100
```

Run organism core process loop (§34):

```bash
python -m virtual_brain_pc.cli organism-run --tick-id 1 --payload '{"signal_strength":0.88,"env":"production","load":0.72}'
```

Run tests:

```bash
pytest -q
```

## Build Agent Flow

For each target OS, the orchestrator runs the same ordered agent pipeline:

1. BuildAgent
2. ValidationAgent
3. PackagingAgent

This gives a uniform build contract independent of host platform.

## KEDDEH Master Documents

- `docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.3.md` — material calibration doctrine
- `docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.4.md` — spike-boundary doctrine

## Multi-Repo Bilateral Rollout

To propagate the BRAINK stack across multiple repositories, use:

- `scripts/bilateral_rollout.sh`

Rollout guide:

- `docs/BILATERAL_ROLLOUT.md`

## Live State

The last verified LIVE state snapshot is at:

- `docs/LIVE_STATE_v1.6.json`

## Direction model

```text
GENERAL-GOVERNANCE-   (GOVERNANCE_ROOT — source of truth)
  -> BRAINK            (application repository — pulls or copies governance standard)
  -> KEDDEH_SOFTWARE_NODES  (engineering repository — pulls or copies governance standard)
  -> governance artifact update
  -> local checker update
  -> downstream repository pull/copy
  -> downstream checker run
  -> downstream proof record
```

## Status

- Local governance artifact status: `STATE_MODEL_LOCAL`
- Runtime lane status: `OPERATIONAL`
- Registry blocks: `39 / 39 resolved`
- External repository adoption status: `PENDING_EXTERNAL_REPOSITORY_ADOPTION`

## Current Work Critique

- Scope completion is incomplete: no concrete cross-repository script integrations are recorded yet.
- Infrastructure completion is incomplete: no implemented virtualization/server provisioning artifacts are present in this repository.
- Validation evidence is incomplete: no build/lint/test framework exists in this repository to confirm behavior changes.
- Governance clarity needs tightening: cross-repository actions must name the exact repositories in scope and cannot rely on implied access.

## Immediate Improvement Actions

- List exact repositories in scope before planning any integration.
- Produce an explicit script inventory per repository (name, purpose, dependencies).
- Define an ordered integration plan with verification steps and naming-governance checks.
