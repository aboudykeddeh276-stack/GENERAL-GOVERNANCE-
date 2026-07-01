# Automation Protocol Standard — GENERAL-GOVERNANCE-

## 1. Purpose

FUNCTION_AUTOMATION_PROTOCOL_ENFORCE_ALL_REPOSITORY_AUTOMATION_BOUNDARIES

This document defines the Automation Protocol Standard for the BRAINK/KEX repository
ecosystem. It governs how all in-repository automation is named, structured, executed,
and proved. Every automated process, agent directive, and protocol function must comply
with this standard before it may be considered a governed artifact.

This standard is an extension of `repository-governance-standard.md`. All prefixes,
state declarations, and proof gate requirements defined there also apply here.

## 2. Automation System Boundary

```
WHOLE_AUTOMATION_PROTOCOL_MASTER_COORDINATOR
  WHOLE_OWNER_LINEAGE:     GENERAL-GOVERNANCE- / BRAINK / KEX
  WHOLE_PRIMARY_FUNCTION:  coordinate naming enforcement, agent dispatch,
                           iterative resolution, and learning feedback into
                           one deterministic governance cycle
  WHOLE_ENVIRONMENTS:      ENVIRONMENT_LOCAL_DEVELOPMENT,
                           ENVIRONMENT_CONTINUOUS_INTEGRATION,
                           ENVIRONMENT_STAGING,
                           ENVIRONMENT_PRODUCTION,
                           ENVIRONMENT_EXTERNAL_VALIDATION
  WHOLE_STATES:            STATE_AUTOMATION_PROTOCOL_INITIALIZING,
                           STATE_AUTOMATION_PROTOCOL_RUNNING_GOVERNANCE_CYCLE,
                           STATE_AUTOMATION_PROTOCOL_COMPLETED,
                           STATE_AUTOMATION_PROTOCOL_FAILED
  WHOLE_ARTIFACTS:         ARTIFACT_AUTOMATION_PROTOCOL_MODULE,
                           ARTIFACT_NAMING_PROTOCOL_MODULE,
                           ARTIFACT_ITERATIVE_RESOLUTION_ENGINE_MODULE,
                           ARTIFACT_AGENT_DIRECTIVE_DISPATCHER_MODULE
  WHOLE_PENDING_GATES:     PENDING_DOWNSTREAM_REPOSITORY_AUTOMATION_PROTOCOL_ADOPTION
```

## 3. Strict Naming Protocol

### 3.1 Non-negotiable naming rule

No identifier in the automation system may be abbreviated, compressed, or ambiguous.
Every name must carry its governance prefix and be fully descriptive of its purpose
without relying on surrounding context for interpretation.

| Identifier type        | Required prefix  | Example |
|------------------------|------------------|---------|
| Agent directive unit   | `AGENT_`         | `AGENT_BUILD_COMPILATION_DIRECTIVE_EXECUTION_UNIT` |
| Agent directive payload| `DIRECTIVE_`     | `DIRECTIVE_BUILD_COMPILATION_TARGET_ALL_PLATFORMS` |
| Protocol function      | `FUNCTION_`      | `FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_COMPLETE_GOVERNANCE_CYCLE` |
| Resolution step        | `RESOLUTION_`    | `RESOLUTION_TIER_1_DIRECT_EXECUTION` |
| Protocol version       | `PROTOCOL_`      | `PROTOCOL_AUTOMATION_GOVERNANCE_CYCLE_V1` |

### 3.2 Prohibited naming patterns

The following patterns are violations of this standard:

- Single-word identifiers without a governance prefix (e.g., `run`, `execute`, `check`)
- CamelCase identifiers (e.g., `runBuild`, `validateName`)
- Abbreviated identifiers (e.g., `cfg`, `proc`, `fn`, `cb`)
- Generic names that do not identify the function's domain (e.g., `helper`, `utils`)

### 3.3 Enforcement

The `naming_protocol.py` module enforces this standard programmatically. Every identifier
registered in `SYSTEM_WIDE_GOVERNANCE_IDENTIFIER_REGISTRY` is validated during the
`NAMING_PROTOCOL_VALIDATION_SWEEP` ops lane. Non-compliant identifiers cause a
`STATE_FAILED` sweep result and block the governance cycle.

## 4. Seven Named Agent Directive Execution Units

Every agent in the automation system is a named directive execution unit. There are
exactly seven registered agents at v1.0:

| Canonical Agent Name | Directive Category | Failover |
|---|---|---|
| `AGENT_GOVERNANCE_NAMING_PROTOCOL_ENFORCEMENT_UNIT` | `DIRECTIVE_VALIDATE_ALL_SYSTEM_IDENTIFIERS` | Yes |
| `AGENT_BUILD_COMPILATION_DIRECTIVE_EXECUTION_UNIT` | `DIRECTIVE_BUILD_COMPILATION_TARGET_ALL_PLATFORMS` | Yes |
| `AGENT_VALIDATION_AND_SMOKE_TEST_DIRECTIVE_EXECUTION_UNIT` | `DIRECTIVE_VALIDATE_SMOKE_TESTS_ALL_TARGETS` | Yes |
| `AGENT_PACKAGING_AND_ARTIFACT_PRODUCTION_DIRECTIVE_EXECUTION_UNIT` | `DIRECTIVE_PACKAGE_ARTIFACT_ALL_TARGETS` | Yes |
| `AGENT_ITERATIVE_RESOLUTION_DIRECTION_AND_ESCALATION_UNIT` | `DIRECTIVE_EXECUTE_ITERATIVE_RESOLUTION_SELF_TEST` | Yes |
| `AGENT_LEARNING_MODULE_FEEDBACK_INTEGRATION_AND_CALIBRATION_UNIT` | `DIRECTIVE_INTEGRATE_LEARNING_MODULE_FEEDBACK` | Yes |
| `AGENT_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION_UNIT` | `DIRECTIVE_VERIFY_FAILOVER_CHAIN_BOUNDARY_INTEGRITY` | No (is the failover) |

Every agent that is not the failover agent has the failover agent registered as its secondary.
This ensures no single agent failure propagates to a complete governance cycle failure.

## 5. Iterative Resolution Engine

### 5.1 Three-tier resolution protocol

The iterative resolution engine resolves complex failures through three ordered tiers:

| Tier | Name | Action |
|------|------|--------|
| 1 | `RESOLUTION_TIER_1_DIRECT_EXECUTION` | Execute each step directly with configured retry count |
| 2 | `RESOLUTION_TIER_2_RETRY_WITH_DECOMPOSITION` | Run root cause analysis; retry with augmented retry count |
| 3 | `RESOLUTION_TIER_3_CRITICAL_ROOT_CAUSE_ANALYSIS_AND_FIX` | Final attempt with maximum retries; all outcomes recorded |

### 5.2 Root cause categories

The engine classifies all failures into one of these root cause categories:

- `ROOT_CAUSE_CATEGORY_MISSING_DEPENDENCY_OR_MODULE`
- `ROOT_CAUSE_CATEGORY_STATE_CONTRACT_VIOLATION`
- `ROOT_CAUSE_CATEGORY_PROOF_ASSERTION_FAILURE`
- `ROOT_CAUSE_CATEGORY_ENVIRONMENT_CONNECTIVITY_FAILURE`
- `ROOT_CAUSE_CATEGORY_UNCLASSIFIED_RUNTIME_EXCEPTION`
- `ROOT_CAUSE_CATEGORY_STEP_CALLABLE_RETURNED_WITHOUT_EXCEPTION`

No failure is silently discarded. Every failure produces a `root_cause_description`
and `resolution_action_recommendation` at minimum.

### 5.3 Proof record requirement

Every execution of the resolution engine — including the built-in self-test — must
produce a `tier_proof_hash` per tier and an `aggregate_proof_hash` for the complete
execution. These hashes are deterministic and reproducible.

## 6. Automation Protocol Governance Cycle

### 6.1 Cycle execution sequence

```
FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_COMPLETE_GOVERNANCE_CYCLE
  Step 1: FUNCTION_AUTOMATION_PROTOCOL_INITIALIZE_ALL_SUBSYSTEM_MODULES_AND_VERIFY_READINESS
  Step 2: FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_NAMING_PROTOCOL_SYSTEM_WIDE_VALIDATION_SWEEP
  Step 3: FUNCTION_AUTOMATION_PROTOCOL_DISPATCH_ALL_SEVEN_AGENT_DIRECTIVES_AND_COLLECT_RESULTS
  Step 4: FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_ITERATIVE_RESOLUTION_ENGINE_SELF_VERIFICATION
  Step 5: FUNCTION_AUTOMATION_PROTOCOL_INTEGRATE_LEARNING_MODULE_ORGANISM_FEEDBACK_INTO_CYCLE
  Step 6: Compute aggregate_cycle_proof_hash and emit proof_gate
```

### 6.2 Cycle state transitions

```
STATE_AUTOMATION_PROTOCOL_INITIALIZING
  → (all modules ready) → STATE_AUTOMATION_PROTOCOL_RUNNING_GOVERNANCE_CYCLE
  → (all subsystems ok) → STATE_AUTOMATION_PROTOCOL_COMPLETED
  → (any subsystem fails) → STATE_AUTOMATION_PROTOCOL_FAILED
```

### 6.3 Cycle proof gates

| Gate | Condition |
|------|-----------|
| `PROOF_GATE_AUTOMATION_PROTOCOL_GOVERNANCE_CYCLE_COMPLETED` | All subsystems pass |
| `PENDING_GOVERNANCE_CYCLE_SUBSYSTEM_FAILURES_REQUIRE_RESOLUTION` | Any subsystem failed |

## 7. Ops Process Catalogue Integration

The automation framework adds four new processes to the PROCESS_CATALOGUE:

| Process ID | Lane | Description |
|------------|------|-------------|
| `NAMING_PROTOCOL_VALIDATION_SWEEP` | `NAMING_PROTOCOL` | Sweep all identifiers through naming protocol |
| `ITERATIVE_RESOLUTION_ENGINE_SELF_TEST` | `ITERATIVE_RESOLUTION` | Run resolution engine self-test |
| `AGENT_DIRECTIVE_DISPATCHER_FULL_SWEEP` | `AGENT_DISPATCHER` | Dispatch directives to all seven agents |
| `AUTOMATION_PROTOCOL_COMPLETE_GOVERNANCE_CYCLE` | `AUTOMATION_PROTOCOL` | Full governance cycle |

The internal ops runner (`ops.py`) has four corresponding lanes:

- `naming_protocol`
- `iterative_resolution`
- `agent_dispatcher`
- `automation_protocol`

The ops runner now executes 12 lanes total (was 8).

## 8. CI Integration

The `uniform-build.yml` workflow includes:

1. `python -m pip install -e ".[dev]"` — installs the package and `pytest`
2. `python -m pytest -q` — runs the full test suite including automation tests
3. `python -m virtual_brain_pc.cli automation-protocol-run --tick-id 0` — validates the governance cycle
4. `python -m virtual_brain_pc.cli ops-run --tick-id 0` — verifies all 12 ops lanes pass

## 9. Learning Module Integration

The automation protocol integrates with the BRAINK learning system through:

- `CALL_THINKING_PROCESS` — reads the memory matrix and produces a thought frame
- `CALL_MIRROR_UPDATE_LANE` — validates proposed deltas without touching live state
- `CALL_LEARNING_MIRROR_UPDATE` — commits approved learning through the mirror lane
- `CALL_KEDDEH_THEOREM_LEDGER` — records theorem compliance for each cycle

Learning is never committed without prior mirror validation. Direct overwrite is always False.

## 10. Proof record requirements

Every completed automation protocol cycle must record:

- `protocol_version` — the PROTOCOL_ constant
- `tick_id` — the monotonic cycle identifier
- `cycle_state` — the final STATE_ constant
- `aggregate_cycle_proof_hash` — deterministic SHA-256 over all subsystem hashes
- `proof_gate` — the PROOF_GATE_ or PENDING_ constant
- `pending_items` — the list of open PENDING_ gates

## 11. Status

- `STATE_MODEL_LOCAL` — this is the local governance standard for the automation protocol.
- `PENDING_DOWNSTREAM_REPOSITORY_AUTOMATION_PROTOCOL_ADOPTION` — downstream repositories
  must adopt or reference this standard before it becomes a cross-repository constraint.
