from __future__ import annotations

"""Automation Protocol Master Coordinator — Complete Governance Cycle Execution

FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_COMPLETE_GOVERNANCE_CYCLE

Input:  tick_id (integer) identifying this governance cycle execution,
        and an optional target_platform string for build/validation directives.
Action: initialises all subsystem modules; validates all naming boundaries
        across the system; dispatches all seven agent directives; runs iterative
        resolution on any failures; integrates learning module feedback;
        emits a complete proof record for the full cycle.
Output: AutomationProtocolCompleteGovernanceCycleResult carrying subsystem
        states, agent outcomes, resolution outcomes, learning feedback, and
        aggregate cycle proof hash.
Proof gate: PROOF_GATE_AUTOMATION_PROTOCOL_GOVERNANCE_CYCLE_COMPLETED
Pending:    PENDING_DOWNSTREAM_REPOSITORY_AUTOMATION_PROTOCOL_ADOPTION

WHOLE_AUTOMATION_PROTOCOL_SYSTEM_BOUNDARY:
  WHOLE_NAME:             WHOLE_AUTOMATION_PROTOCOL_MASTER_COORDINATOR
  WHOLE_OWNER_LINEAGE:    GENERAL-GOVERNANCE- / BRAINK / KEX
  WHOLE_PRIMARY_FUNCTION: coordinate naming enforcement, agent dispatch,
                          iterative resolution, and learning feedback into
                          one deterministic governance cycle
  WHOLE_ENVIRONMENTS:     ENVIRONMENT_LOCAL_DEVELOPMENT,
                          ENVIRONMENT_CONTINUOUS_INTEGRATION,
                          ENVIRONMENT_STAGING,
                          ENVIRONMENT_PRODUCTION,
                          ENVIRONMENT_EXTERNAL_VALIDATION
  WHOLE_STATES:           STATE_AUTOMATION_PROTOCOL_INITIALIZING,
                          STATE_AUTOMATION_PROTOCOL_RUNNING_GOVERNANCE_CYCLE,
                          STATE_AUTOMATION_PROTOCOL_COMPLETED,
                          STATE_AUTOMATION_PROTOCOL_FAILED
  WHOLE_ARTIFACTS:        ARTIFACT_AUTOMATION_PROTOCOL_MODULE,
                          ARTIFACT_NAMING_PROTOCOL_MODULE,
                          ARTIFACT_ITERATIVE_RESOLUTION_ENGINE_MODULE,
                          ARTIFACT_AGENT_DIRECTIVE_DISPATCHER_MODULE
  WHOLE_PENDING_GATES:    PENDING_DOWNSTREAM_REPOSITORY_AUTOMATION_PROTOCOL_ADOPTION
"""

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Protocol state constants
# ---------------------------------------------------------------------------

STATE_AUTOMATION_PROTOCOL_INITIALIZING: str = (
    "STATE_AUTOMATION_PROTOCOL_INITIALIZING"
)
STATE_AUTOMATION_PROTOCOL_RUNNING_GOVERNANCE_CYCLE: str = (
    "STATE_AUTOMATION_PROTOCOL_RUNNING_GOVERNANCE_CYCLE"
)
STATE_AUTOMATION_PROTOCOL_COMPLETED: str = (
    "STATE_AUTOMATION_PROTOCOL_COMPLETED"
)
STATE_AUTOMATION_PROTOCOL_FAILED: str = (
    "STATE_AUTOMATION_PROTOCOL_FAILED"
)

PROTOCOL_AUTOMATION_GOVERNANCE_CYCLE_VERSION: str = "PROTOCOL_AUTOMATION_GOVERNANCE_CYCLE_V1"


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class AutomationProtocolCompleteGovernanceCycleResult:
    """Complete result of one full automation protocol governance cycle execution.

    Fields:
      protocol_version                  — PROTOCOL_ constant identifying this cycle version
      tick_id                           — monotonic cycle identifier
      cycle_state                       — STATE_AUTOMATION_PROTOCOL_ constant
      naming_protocol_sweep_state       — state from the naming sweep
      naming_protocol_sweep_proof_hash  — proof hash from the naming sweep
      agent_dispatcher_all_completed    — True when all seven agents completed
      agent_dispatcher_proof_hash       — aggregate proof hash from dispatcher
      agent_dispatcher_failover_count   — count of failover activations
      resolution_engine_all_resolved    — True when all resolution steps passed
      resolution_engine_proof_hash      — aggregate proof hash from resolution engine
      resolution_engine_tiers_used      — count of tiers activated
      learning_feedback_committed       — True when learning update was committed
      learning_feedback_theorem_hash    — KEDDEH theorem ledger hash
      cycle_all_subsystems_passed       — True only when all subsystems report ok
      aggregate_cycle_proof_hash        — SHA-256 over all subsystem proof hashes
      proof_gate                        — PROOF_GATE_ or PENDING_ constant
      pending_items                     — list of PENDING_ items for this cycle
    """

    protocol_version: str
    tick_id: int
    cycle_state: str
    naming_protocol_sweep_state: str = "STATE_PENDING"
    naming_protocol_sweep_proof_hash: Optional[str] = None
    agent_dispatcher_all_completed: bool = False
    agent_dispatcher_proof_hash: Optional[str] = None
    agent_dispatcher_failover_count: int = 0
    resolution_engine_all_resolved: bool = False
    resolution_engine_proof_hash: Optional[str] = None
    resolution_engine_tiers_used: int = 0
    learning_feedback_committed: bool = False
    learning_feedback_theorem_hash: Optional[str] = None
    cycle_all_subsystems_passed: bool = False
    aggregate_cycle_proof_hash: Optional[str] = None
    proof_gate: Optional[str] = None
    pending_items: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Subsystem initialisation
# ---------------------------------------------------------------------------

def FUNCTION_AUTOMATION_PROTOCOL_INITIALIZE_ALL_SUBSYSTEM_MODULES_AND_VERIFY_READINESS(
    tick_id: int,
) -> Dict[str, Any]:
    """Initialise all automation protocol subsystem modules and verify they are ready.

    FUNCTION_AUTOMATION_PROTOCOL_INITIALIZE_ALL_SUBSYSTEM_MODULES_AND_VERIFY_READINESS

    Input:  tick_id — the monotonic identifier for this governance cycle
    Action: imports and verifies the naming_protocol, iterative_resolution_engine,
            and agent_directive_dispatcher modules; checks each is importable and
            that its public API surface is intact
    Output: dict with module readiness flags and initialisation proof hash
    Proof gate: PROOF_GATE_ALL_SUBSYSTEM_MODULES_INITIALISED_AND_READY
    Pending:    PENDING_HEALTH_CHECK_ENDPOINT_FOR_LONG_RUNNING_SUBSYSTEMS
    """
    module_readiness: Dict[str, bool] = {}
    module_errors: Dict[str, str] = {}

    # Verify naming_protocol
    try:
        from .naming_protocol import (
            GOVERNANCE_PREFIX_REGISTRY,
            FUNCTION_NAMING_PROTOCOL_EXECUTE_SYSTEM_WIDE_IDENTIFIER_SWEEP_AND_EMIT_PROOF_RECORD,
        )
        module_readiness["naming_protocol"] = (
            bool(GOVERNANCE_PREFIX_REGISTRY)
            and callable(
                FUNCTION_NAMING_PROTOCOL_EXECUTE_SYSTEM_WIDE_IDENTIFIER_SWEEP_AND_EMIT_PROOF_RECORD
            )
        )
    except Exception as exc:
        module_readiness["naming_protocol"] = False
        module_errors["naming_protocol"] = str(exc)

    # Verify iterative_resolution_engine
    try:
        from .iterative_resolution_engine import (
            FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_COMPLETE_SELF_RESOLVING_PROTOCOL,
            FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_BUILT_IN_SELF_TEST_WITH_CONTROLLED_SCENARIO,
        )
        module_readiness["iterative_resolution_engine"] = (
            callable(
                FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_COMPLETE_SELF_RESOLVING_PROTOCOL
            )
            and callable(
                FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_BUILT_IN_SELF_TEST_WITH_CONTROLLED_SCENARIO
            )
        )
    except Exception as exc:
        module_readiness["iterative_resolution_engine"] = False
        module_errors["iterative_resolution_engine"] = str(exc)

    # Verify agent_directive_dispatcher
    try:
        from .agent_directive_dispatcher import (
            AGENT_DIRECTIVE_UNIT_REGISTRY,
            FUNCTION_AGENT_DIRECTIVE_DISPATCHER_EXECUTE_ALL_AGENT_DIRECTIVES_IN_SEQUENCE,
        )
        module_readiness["agent_directive_dispatcher"] = (
            len(AGENT_DIRECTIVE_UNIT_REGISTRY) == 7
            and callable(
                FUNCTION_AGENT_DIRECTIVE_DISPATCHER_EXECUTE_ALL_AGENT_DIRECTIVES_IN_SEQUENCE
            )
        )
    except Exception as exc:
        module_readiness["agent_directive_dispatcher"] = False
        module_errors["agent_directive_dispatcher"] = str(exc)

    all_ready = all(module_readiness.values())
    readiness_source = json.dumps(module_readiness, sort_keys=True)
    readiness_hash = hashlib.sha256(readiness_source.encode("utf-8")).hexdigest()[:16]

    return {
        "tick_id": tick_id,
        "module_readiness": module_readiness,
        "module_errors": module_errors,
        "all_modules_ready": all_ready,
        "readiness_proof_hash": readiness_hash,
        "proof_gate": (
            "PROOF_GATE_ALL_SUBSYSTEM_MODULES_INITIALISED_AND_READY"
            if all_ready
            else "PENDING_SUBSYSTEM_MODULE_INITIALISATION_FAILURE_RESOLUTION"
        ),
    }


# ---------------------------------------------------------------------------
# Step functions for the governance cycle
# ---------------------------------------------------------------------------

def FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_NAMING_PROTOCOL_SYSTEM_WIDE_VALIDATION_SWEEP(
) -> Dict[str, Any]:
    """Run the naming protocol system-wide identifier sweep and return structured result.

    FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_NAMING_PROTOCOL_SYSTEM_WIDE_VALIDATION_SWEEP

    Input:  none — operates on SYSTEM_WIDE_GOVERNANCE_IDENTIFIER_REGISTRY
    Action: imports naming_protocol module and runs the full sweep function
    Output: dict with state, counts, violations, and proof hash
    Proof gate: PROOF_GATE_NAMING_PROTOCOL_SYSTEM_WIDE_SWEEP_COMPLETED
    Pending:    PENDING_DYNAMIC_IDENTIFIER_DISCOVERY_FROM_ALL_REPOSITORY_SOURCE_FILES
    """
    from .naming_protocol import (
        FUNCTION_NAMING_PROTOCOL_EXECUTE_SYSTEM_WIDE_IDENTIFIER_SWEEP_AND_EMIT_PROOF_RECORD,
    )
    return FUNCTION_NAMING_PROTOCOL_EXECUTE_SYSTEM_WIDE_IDENTIFIER_SWEEP_AND_EMIT_PROOF_RECORD()


def FUNCTION_AUTOMATION_PROTOCOL_DISPATCH_ALL_SEVEN_AGENT_DIRECTIVES_AND_COLLECT_RESULTS(
    target_platform: str = "linux",
) -> Dict[str, Any]:
    """Dispatch all seven agent directives and collect complete results.

    FUNCTION_AUTOMATION_PROTOCOL_DISPATCH_ALL_SEVEN_AGENT_DIRECTIVES_AND_COLLECT_RESULTS

    Input:  target_platform — build/validation target (default: 'linux')
    Action: builds standard directive assignment list and runs the full dispatcher
    Output: dict summarising dispatcher result with proof hash
    Proof gate: PROOF_GATE_ALL_SEVEN_AGENT_DIRECTIVES_DISPATCHED_AND_RESULTS_COLLECTED
    Pending:    PENDING_PARALLEL_AGENT_DIRECTIVE_EXECUTION_ACROSS_ALL_UNITS
    """
    from .agent_directive_dispatcher import (
        FUNCTION_AGENT_DIRECTIVE_DISPATCHER_BUILD_STANDARD_DIRECTIVE_ASSIGNMENTS_FOR_ALL_SEVEN_AGENTS,
        FUNCTION_AGENT_DIRECTIVE_DISPATCHER_EXECUTE_ALL_AGENT_DIRECTIVES_IN_SEQUENCE,
    )
    assignments = (
        FUNCTION_AGENT_DIRECTIVE_DISPATCHER_BUILD_STANDARD_DIRECTIVE_ASSIGNMENTS_FOR_ALL_SEVEN_AGENTS(
            target_platform=target_platform
        )
    )
    dispatch_result = (
        FUNCTION_AGENT_DIRECTIVE_DISPATCHER_EXECUTE_ALL_AGENT_DIRECTIVES_IN_SEQUENCE(
            assignments
        )
    )
    return {
        "total_dispatched": dispatch_result.total_directives_dispatched,
        "total_completed": dispatch_result.total_directives_completed,
        "total_failed": dispatch_result.total_directives_failed,
        "failover_activation_count": dispatch_result.total_failover_activations,
        "all_completed": dispatch_result.all_directives_completed,
        "aggregate_proof_hash": dispatch_result.aggregate_proof_hash,
        "proof_gate": dispatch_result.proof_gate,
        "ok": dispatch_result.all_directives_completed,
    }


def FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_ITERATIVE_RESOLUTION_ENGINE_SELF_VERIFICATION(
) -> Dict[str, Any]:
    """Run the iterative resolution engine built-in self-test and return result.

    FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_ITERATIVE_RESOLUTION_ENGINE_SELF_VERIFICATION

    Input:  none — uses the engine's built-in controlled test scenario
    Action: imports iterative_resolution_engine and calls the self-test function
    Output: dict with test_passed, protocol_state, and proof hash
    Proof gate: PROOF_GATE_ITERATIVE_RESOLUTION_ENGINE_SELF_VERIFICATION_PASSED
    Pending:    PENDING_FAILURE_INJECTION_SCENARIO_FOR_TIER_2_TIER_3_SELF_TEST
    """
    from .iterative_resolution_engine import (
        FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_BUILT_IN_SELF_TEST_WITH_CONTROLLED_SCENARIO,
    )
    return (
        FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_BUILT_IN_SELF_TEST_WITH_CONTROLLED_SCENARIO()
    )


def FUNCTION_AUTOMATION_PROTOCOL_INTEGRATE_LEARNING_MODULE_ORGANISM_FEEDBACK_INTO_CYCLE(
    tick_id: int,
) -> Dict[str, Any]:
    """Run the organism core process to integrate learning feedback into the governance cycle.

    FUNCTION_AUTOMATION_PROTOCOL_INTEGRATE_LEARNING_MODULE_ORGANISM_FEEDBACK_INTO_CYCLE

    Input:  tick_id — the cycle identifier passed through to the organism process
    Action: runs the full organism core process (power-core → thinking → mirror →
            learning → theorem ledger) with a governance-cycle-specific payload
    Output: dict with learning_committed, theorem_hash, and proof hash
    Proof gate: PROOF_GATE_LEARNING_MODULE_FEEDBACK_INTEGRATED_INTO_GOVERNANCE_CYCLE
    Pending:    PENDING_ADAPTIVE_PAYLOAD_CONSTRUCTION_FROM_PREVIOUS_CYCLE_OUTCOMES
    """
    from .organism import run_organism_process
    organism_result = run_organism_process(
        input_signal={
            "signal_strength": 0.88,
            "environment": "ENVIRONMENT_CONTINUOUS_INTEGRATION",
            "load": 0.72,
            "governance_cycle_tick_id": tick_id,
        },
        tick_id=tick_id,
    )
    # `steps` is a dict keyed by step name; `organism_lane` is a list of step name strings
    steps = organism_result.get("steps", {})
    theorem_step = steps.get("theorem_ledger", {})
    theorem_hash = theorem_step.get("ledger_hash") if isinstance(theorem_step, dict) else None

    return {
        "learning_committed": organism_result.get("learning_committed", False),
        "theorem_compliant": organism_result.get("theorem_compliant", False),
        "organism_alive": organism_result.get("organism_alive", False),
        "output_state": organism_result.get("output_state", 0),
        "theorem_hash": theorem_hash,
        "ok": (
            organism_result.get("learning_committed", False)
            and organism_result.get("theorem_compliant", False)
        ),
    }


# ---------------------------------------------------------------------------
# Master coordinator — complete governance cycle
# ---------------------------------------------------------------------------

def FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_COMPLETE_GOVERNANCE_CYCLE(
    tick_id: int = 0,
    target_platform: str = "linux",
) -> AutomationProtocolCompleteGovernanceCycleResult:
    """Execute one complete automation protocol governance cycle.

    FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_COMPLETE_GOVERNANCE_CYCLE

    Input:  tick_id — monotonic cycle identifier (default 0)
            target_platform — build/validation platform (default 'linux')
    Action:
      1. FUNCTION_AUTOMATION_PROTOCOL_INITIALIZE_ALL_SUBSYSTEM_MODULES_AND_VERIFY_READINESS
      2. FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_NAMING_PROTOCOL_SYSTEM_WIDE_VALIDATION_SWEEP
      3. FUNCTION_AUTOMATION_PROTOCOL_DISPATCH_ALL_SEVEN_AGENT_DIRECTIVES_AND_COLLECT_RESULTS
      4. FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_ITERATIVE_RESOLUTION_ENGINE_SELF_VERIFICATION
      5. FUNCTION_AUTOMATION_PROTOCOL_INTEGRATE_LEARNING_MODULE_ORGANISM_FEEDBACK_INTO_CYCLE
      6. FUNCTION_AUTOMATION_PROTOCOL_EMIT_COMPLETE_PROOF_RECORD_FOR_GOVERNANCE_CYCLE
    Output: AutomationProtocolCompleteGovernanceCycleResult
    Proof gate: PROOF_GATE_AUTOMATION_PROTOCOL_GOVERNANCE_CYCLE_COMPLETED
    Pending:    PENDING_DOWNSTREAM_REPOSITORY_AUTOMATION_PROTOCOL_ADOPTION
    """
    cycle_result = AutomationProtocolCompleteGovernanceCycleResult(
        protocol_version=PROTOCOL_AUTOMATION_GOVERNANCE_CYCLE_VERSION,
        tick_id=tick_id,
        cycle_state=STATE_AUTOMATION_PROTOCOL_INITIALIZING,
        pending_items=[
            "PENDING_DOWNSTREAM_REPOSITORY_AUTOMATION_PROTOCOL_ADOPTION",
            "PENDING_CROSS_REPOSITORY_NAMING_PROTOCOL_ADOPTION",
            "PENDING_LEARNING_MODULE_ADAPTIVE_STEP_INJECTION_INTO_RESOLUTION_SEQUENCE",
            "PENDING_PARALLEL_AGENT_DIRECTIVE_EXECUTION_ACROSS_ALL_UNITS",
        ],
    )

    # Step 1: Initialise subsystems
    init_result = (
        FUNCTION_AUTOMATION_PROTOCOL_INITIALIZE_ALL_SUBSYSTEM_MODULES_AND_VERIFY_READINESS(
            tick_id
        )
    )
    if not init_result["all_modules_ready"]:
        cycle_result.cycle_state = STATE_AUTOMATION_PROTOCOL_FAILED
        cycle_result.proof_gate = (
            "PENDING_SUBSYSTEM_MODULE_INITIALISATION_FAILURE_BLOCKS_GOVERNANCE_CYCLE"
        )
        return cycle_result

    cycle_result.cycle_state = STATE_AUTOMATION_PROTOCOL_RUNNING_GOVERNANCE_CYCLE

    # Step 2: Naming protocol sweep
    naming_sweep = (
        FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_NAMING_PROTOCOL_SYSTEM_WIDE_VALIDATION_SWEEP()
    )
    cycle_result.naming_protocol_sweep_state = naming_sweep.get("state", "STATE_FAILED")
    cycle_result.naming_protocol_sweep_proof_hash = naming_sweep.get("aggregate_proof_hash")

    # Step 3: Agent directive dispatch
    dispatch_result = (
        FUNCTION_AUTOMATION_PROTOCOL_DISPATCH_ALL_SEVEN_AGENT_DIRECTIVES_AND_COLLECT_RESULTS(
            target_platform=target_platform
        )
    )
    cycle_result.agent_dispatcher_all_completed = dispatch_result.get("all_completed", False)
    cycle_result.agent_dispatcher_proof_hash = dispatch_result.get("aggregate_proof_hash")
    cycle_result.agent_dispatcher_failover_count = dispatch_result.get(
        "failover_activation_count", 0
    )

    # Step 4: Iterative resolution self-verification
    resolution_result = (
        FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_ITERATIVE_RESOLUTION_ENGINE_SELF_VERIFICATION()
    )
    cycle_result.resolution_engine_all_resolved = resolution_result.get("test_passed", False)
    cycle_result.resolution_engine_proof_hash = resolution_result.get("aggregate_proof_hash")
    cycle_result.resolution_engine_tiers_used = resolution_result.get("tiers_used", 0)

    # Step 5: Learning module feedback integration
    learning_result = (
        FUNCTION_AUTOMATION_PROTOCOL_INTEGRATE_LEARNING_MODULE_ORGANISM_FEEDBACK_INTO_CYCLE(
            tick_id
        )
    )
    cycle_result.learning_feedback_committed = learning_result.get("learning_committed", False)
    cycle_result.learning_feedback_theorem_hash = learning_result.get("theorem_hash")

    # Step 6: Determine overall cycle outcome and emit proof hash
    all_subsystems_passed = (
        cycle_result.naming_protocol_sweep_state == "STATE_COMPLETED"
        and cycle_result.agent_dispatcher_all_completed
        and cycle_result.resolution_engine_all_resolved
        and cycle_result.learning_feedback_committed
    )
    cycle_result.cycle_all_subsystems_passed = all_subsystems_passed
    cycle_result.cycle_state = (
        STATE_AUTOMATION_PROTOCOL_COMPLETED
        if all_subsystems_passed
        else STATE_AUTOMATION_PROTOCOL_FAILED
    )

    aggregate_source = json.dumps(
        {
            "naming_proof": cycle_result.naming_protocol_sweep_proof_hash,
            "dispatch_proof": cycle_result.agent_dispatcher_proof_hash,
            "resolution_proof": cycle_result.resolution_engine_proof_hash,
            "learning_theorem_hash": cycle_result.learning_feedback_theorem_hash,
        },
        sort_keys=True,
    )
    cycle_result.aggregate_cycle_proof_hash = hashlib.sha256(
        aggregate_source.encode("utf-8")
    ).hexdigest()[:16]

    cycle_result.proof_gate = (
        "PROOF_GATE_AUTOMATION_PROTOCOL_GOVERNANCE_CYCLE_COMPLETED"
        if all_subsystems_passed
        else "PENDING_GOVERNANCE_CYCLE_SUBSYSTEM_FAILURES_REQUIRE_RESOLUTION"
    )

    return cycle_result


def FUNCTION_AUTOMATION_PROTOCOL_SERIALIZE_GOVERNANCE_CYCLE_RESULT_TO_DICT(
    cycle_result: AutomationProtocolCompleteGovernanceCycleResult,
) -> Dict[str, Any]:
    """Serialise an AutomationProtocolCompleteGovernanceCycleResult to a plain dict.

    FUNCTION_AUTOMATION_PROTOCOL_SERIALIZE_GOVERNANCE_CYCLE_RESULT_TO_DICT

    Input:  cycle_result — completed governance cycle result dataclass
    Action: extracts all fields into a plain serialisable dict
    Output: flat dict suitable for JSON serialisation and CLI output
    Proof gate: PROOF_GATE_GOVERNANCE_CYCLE_RESULT_SERIALISED_WITHOUT_LOSS
    Pending:    PENDING_SCHEMA_VERSIONED_SERIALISATION_FOR_DOWNSTREAM_CONSUMERS
    """
    return {
        "protocol_version": cycle_result.protocol_version,
        "tick_id": cycle_result.tick_id,
        "cycle_state": cycle_result.cycle_state,
        "naming_protocol_sweep_state": cycle_result.naming_protocol_sweep_state,
        "naming_protocol_sweep_proof_hash": cycle_result.naming_protocol_sweep_proof_hash,
        "agent_dispatcher_all_completed": cycle_result.agent_dispatcher_all_completed,
        "agent_dispatcher_proof_hash": cycle_result.agent_dispatcher_proof_hash,
        "agent_dispatcher_failover_count": cycle_result.agent_dispatcher_failover_count,
        "resolution_engine_all_resolved": cycle_result.resolution_engine_all_resolved,
        "resolution_engine_proof_hash": cycle_result.resolution_engine_proof_hash,
        "resolution_engine_tiers_used": cycle_result.resolution_engine_tiers_used,
        "learning_feedback_committed": cycle_result.learning_feedback_committed,
        "learning_feedback_theorem_hash": cycle_result.learning_feedback_theorem_hash,
        "cycle_all_subsystems_passed": cycle_result.cycle_all_subsystems_passed,
        "aggregate_cycle_proof_hash": cycle_result.aggregate_cycle_proof_hash,
        "proof_gate": cycle_result.proof_gate,
        "pending_items": cycle_result.pending_items,
        "ok": cycle_result.cycle_all_subsystems_passed,
    }
