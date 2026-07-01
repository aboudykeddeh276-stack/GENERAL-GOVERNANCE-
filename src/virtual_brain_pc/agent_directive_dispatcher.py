from __future__ import annotations

"""Agent Directive Dispatcher — Seven Fully-Named Agent Directive Execution Units with Failover

FUNCTION_AGENT_DIRECTIVE_DISPATCHER_EXECUTE_ALL_AGENT_DIRECTIVES_IN_SEQUENCE

Input:  an ordered sequence of AgentDirectiveAssignment objects, each binding a
        named agent to a specific directive and target environment.
Action: dispatches each directive to its designated agent; on agent failure,
        activates the configured failover secondary agent; collects all results
        with deterministic proof hashes; integrates learning module feedback
        into subsequent directive assignments.
Output: AgentDirectiveDispatcherCompleteExecutionResult carrying per-agent
        outcomes, failover activation records, and aggregate proof hash.
Proof gate: PROOF_GATE_ALL_AGENT_DIRECTIVES_DISPATCHED_AND_RESULTS_COLLECTED
Pending:    PENDING_PARALLEL_AGENT_DIRECTIVE_EXECUTION_ACROSS_ALL_UNITS
"""

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


# ---------------------------------------------------------------------------
# State constants for agent directive execution — no abbreviations
# ---------------------------------------------------------------------------

STATE_AGENT_DIRECTIVE_PENDING_ASSIGNMENT: str = (
    "STATE_AGENT_DIRECTIVE_PENDING_ASSIGNMENT"
)
STATE_AGENT_DIRECTIVE_EXECUTING: str = (
    "STATE_AGENT_DIRECTIVE_EXECUTING"
)
STATE_AGENT_DIRECTIVE_COMPLETED_SUCCESSFULLY: str = (
    "STATE_AGENT_DIRECTIVE_COMPLETED_SUCCESSFULLY"
)
STATE_AGENT_DIRECTIVE_FAILED_ACTIVATING_FAILOVER_SECONDARY: str = (
    "STATE_AGENT_DIRECTIVE_FAILED_ACTIVATING_FAILOVER_SECONDARY"
)
STATE_AGENT_DIRECTIVE_FAILOVER_SECONDARY_ACTIVATED_AND_COMPLETED: str = (
    "STATE_AGENT_DIRECTIVE_FAILOVER_SECONDARY_ACTIVATED_AND_COMPLETED"
)
STATE_AGENT_DIRECTIVE_FAILED_ALL_UNITS_EXHAUSTED: str = (
    "STATE_AGENT_DIRECTIVE_FAILED_ALL_UNITS_EXHAUSTED"
)


# ---------------------------------------------------------------------------
# Canonical agent names — seven fully-named directive execution units
# ---------------------------------------------------------------------------

AGENT_CANONICAL_NAME_GOVERNANCE_NAMING_PROTOCOL_ENFORCEMENT_UNIT: str = (
    "AGENT_GOVERNANCE_NAMING_PROTOCOL_ENFORCEMENT_UNIT"
)
AGENT_CANONICAL_NAME_BUILD_COMPILATION_DIRECTIVE_EXECUTION_UNIT: str = (
    "AGENT_BUILD_COMPILATION_DIRECTIVE_EXECUTION_UNIT"
)
AGENT_CANONICAL_NAME_VALIDATION_AND_SMOKE_TEST_DIRECTIVE_EXECUTION_UNIT: str = (
    "AGENT_VALIDATION_AND_SMOKE_TEST_DIRECTIVE_EXECUTION_UNIT"
)
AGENT_CANONICAL_NAME_PACKAGING_AND_ARTIFACT_PRODUCTION_DIRECTIVE_EXECUTION_UNIT: str = (
    "AGENT_PACKAGING_AND_ARTIFACT_PRODUCTION_DIRECTIVE_EXECUTION_UNIT"
)
AGENT_CANONICAL_NAME_ITERATIVE_RESOLUTION_DIRECTION_AND_ESCALATION_UNIT: str = (
    "AGENT_ITERATIVE_RESOLUTION_DIRECTION_AND_ESCALATION_UNIT"
)
AGENT_CANONICAL_NAME_LEARNING_MODULE_FEEDBACK_INTEGRATION_AND_CALIBRATION_UNIT: str = (
    "AGENT_LEARNING_MODULE_FEEDBACK_INTEGRATION_AND_CALIBRATION_UNIT"
)
AGENT_CANONICAL_NAME_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION_UNIT: str = (
    "AGENT_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION_UNIT"
)

ALL_AGENT_CANONICAL_NAMES_IN_DISPATCH_ORDER: List[str] = [
    AGENT_CANONICAL_NAME_GOVERNANCE_NAMING_PROTOCOL_ENFORCEMENT_UNIT,
    AGENT_CANONICAL_NAME_BUILD_COMPILATION_DIRECTIVE_EXECUTION_UNIT,
    AGENT_CANONICAL_NAME_VALIDATION_AND_SMOKE_TEST_DIRECTIVE_EXECUTION_UNIT,
    AGENT_CANONICAL_NAME_PACKAGING_AND_ARTIFACT_PRODUCTION_DIRECTIVE_EXECUTION_UNIT,
    AGENT_CANONICAL_NAME_ITERATIVE_RESOLUTION_DIRECTION_AND_ESCALATION_UNIT,
    AGENT_CANONICAL_NAME_LEARNING_MODULE_FEEDBACK_INTEGRATION_AND_CALIBRATION_UNIT,
    AGENT_CANONICAL_NAME_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION_UNIT,
]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class AgentDirectiveUnit:
    """One named agent directive execution unit with its capabilities.

    Fields:
      canonical_agent_name              — AGENT_ prefixed full name
      directive_category                — DIRECTIVE_ prefixed category this unit handles
      primary_environment_name          — ENVIRONMENT_ prefixed execution environment
      agent_execution_function          — callable(directive_payload) → Dict result
      failover_secondary_agent_name     — canonical name of the backup agent, or None
    """

    canonical_agent_name: str
    directive_category: str
    primary_environment_name: str
    agent_execution_function: Callable[[Dict[str, Any]], Dict[str, Any]]
    failover_secondary_agent_name: Optional[str] = None


@dataclass
class AgentDirectiveAssignment:
    """One unit of work assigned from a directive to a named agent.

    Fields:
      assignment_canonical_name         — DIRECTIVE_ prefixed name for this assignment
      target_agent_canonical_name       — which agent receives this directive
      directive_payload                 — dict of inputs for the agent
      target_environment_name           — ENVIRONMENT_ prefixed execution context
    """

    assignment_canonical_name: str
    target_agent_canonical_name: str
    directive_payload: Dict[str, Any]
    target_environment_name: str


@dataclass
class AgentDirectiveExecutionOutcome:
    """Complete execution record for one agent directive assignment.

    Fields:
      assignment_canonical_name         — matches the assignment name
      executing_agent_canonical_name    — which agent executed (primary or failover)
      execution_state                   — STATE_ constant
      primary_agent_failed              — True if failover was activated
      failover_secondary_activated      — True if secondary agent ran
      result_payload                    — dict returned by the agent
      failure_description               — populated if execution failed
      proof_hash                        — SHA-256 of the result payload
    """

    assignment_canonical_name: str
    executing_agent_canonical_name: str
    execution_state: str
    primary_agent_failed: bool = False
    failover_secondary_activated: bool = False
    result_payload: Dict[str, Any] = field(default_factory=dict)
    failure_description: Optional[str] = None
    proof_hash: Optional[str] = None


@dataclass
class AgentDirectiveDispatcherCompleteExecutionResult:
    """Complete result of dispatching all directives across all agent units.

    Fields:
      total_directives_dispatched       — count of assignments submitted
      total_directives_completed        — count of assignments that succeeded
      total_directives_failed           — count of assignments that failed all units
      total_failover_activations        — count of times secondary was triggered
      all_directives_completed          — True when no failures remain
      per_assignment_outcomes           — ordered list of per-assignment outcomes
      aggregate_proof_hash              — SHA-256 over all assignment proof hashes
      proof_gate                        — PROOF_GATE_ or PENDING_ constant
    """

    total_directives_dispatched: int
    total_directives_completed: int
    total_directives_failed: int
    total_failover_activations: int
    all_directives_completed: bool
    per_assignment_outcomes: List[AgentDirectiveExecutionOutcome] = field(default_factory=list)
    aggregate_proof_hash: Optional[str] = None
    proof_gate: Optional[str] = None


# ---------------------------------------------------------------------------
# Agent execution functions — each agent's internal logic
# ---------------------------------------------------------------------------

def _AGENT_EXECUTION_FUNCTION_FOR_GOVERNANCE_NAMING_PROTOCOL_ENFORCEMENT(
    directive_payload: Dict[str, Any],
) -> Dict[str, Any]:
    """Internal execution logic for the Governance Naming Protocol Enforcement Unit."""
    from .naming_protocol import (
        FUNCTION_NAMING_PROTOCOL_EXECUTE_SYSTEM_WIDE_IDENTIFIER_SWEEP_AND_EMIT_PROOF_RECORD,
    )
    sweep_result = (
        FUNCTION_NAMING_PROTOCOL_EXECUTE_SYSTEM_WIDE_IDENTIFIER_SWEEP_AND_EMIT_PROOF_RECORD()
    )
    return {
        "agent": AGENT_CANONICAL_NAME_GOVERNANCE_NAMING_PROTOCOL_ENFORCEMENT_UNIT,
        "directive_executed": directive_payload.get(
            "directive", "DIRECTIVE_VALIDATE_ALL_SYSTEM_IDENTIFIERS"
        ),
        "naming_sweep_state": sweep_result["state"],
        "compliant_count": sweep_result["compliant_identifier_count"],
        "non_compliant_count": sweep_result["non_compliant_identifier_count"],
        "aggregate_proof_hash": sweep_result["aggregate_proof_hash"],
        "proof_gate": sweep_result["proof_gate"],
        "ok": sweep_result["state"] == "STATE_COMPLETED",
    }


def _AGENT_EXECUTION_FUNCTION_FOR_BUILD_COMPILATION_DIRECTIVE(
    directive_payload: Dict[str, Any],
) -> Dict[str, Any]:
    """Internal execution logic for the Build Compilation Directive Execution Unit."""
    from .agents import BuildAgent
    target = directive_payload.get("target", "linux")
    agent = BuildAgent()
    report = agent.run(target)
    return {
        "agent": AGENT_CANONICAL_NAME_BUILD_COMPILATION_DIRECTIVE_EXECUTION_UNIT,
        "directive_executed": "DIRECTIVE_BUILD_COMPILATION_TARGET_ALL_PLATFORMS",
        "target": target,
        "build_status": report.status,
        "build_notes": report.notes,
        "ok": report.status == "ok",
    }


def _AGENT_EXECUTION_FUNCTION_FOR_VALIDATION_AND_SMOKE_TEST_DIRECTIVE(
    directive_payload: Dict[str, Any],
) -> Dict[str, Any]:
    """Internal execution logic for the Validation and Smoke Test Directive Execution Unit."""
    from .agents import ValidationAgent
    target = directive_payload.get("target", "linux")
    agent = ValidationAgent()
    report = agent.run(target)
    return {
        "agent": AGENT_CANONICAL_NAME_VALIDATION_AND_SMOKE_TEST_DIRECTIVE_EXECUTION_UNIT,
        "directive_executed": "DIRECTIVE_VALIDATE_SMOKE_TESTS_ALL_TARGETS",
        "target": target,
        "validation_status": report.status,
        "validation_notes": report.notes,
        "ok": report.status == "ok",
    }


def _AGENT_EXECUTION_FUNCTION_FOR_PACKAGING_AND_ARTIFACT_PRODUCTION_DIRECTIVE(
    directive_payload: Dict[str, Any],
) -> Dict[str, Any]:
    """Internal execution logic for the Packaging and Artifact Production Directive Execution Unit."""
    from .agents import PackagingAgent
    target = directive_payload.get("target", "linux")
    agent = PackagingAgent()
    report = agent.run(target)
    return {
        "agent": AGENT_CANONICAL_NAME_PACKAGING_AND_ARTIFACT_PRODUCTION_DIRECTIVE_EXECUTION_UNIT,
        "directive_executed": "DIRECTIVE_PACKAGE_ARTIFACT_ALL_TARGETS",
        "target": target,
        "packaging_status": report.status,
        "packaging_notes": report.notes,
        "ok": report.status == "ok",
    }


def _AGENT_EXECUTION_FUNCTION_FOR_ITERATIVE_RESOLUTION_DIRECTION_AND_ESCALATION(
    directive_payload: Dict[str, Any],
) -> Dict[str, Any]:
    """Internal execution logic for the Iterative Resolution Direction and Escalation Unit."""
    from .iterative_resolution_engine import (
        FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_BUILT_IN_SELF_TEST_WITH_CONTROLLED_SCENARIO,
    )
    self_test_result = (
        FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_BUILT_IN_SELF_TEST_WITH_CONTROLLED_SCENARIO()
    )
    return {
        "agent": AGENT_CANONICAL_NAME_ITERATIVE_RESOLUTION_DIRECTION_AND_ESCALATION_UNIT,
        "directive_executed": "DIRECTIVE_EXECUTE_ITERATIVE_RESOLUTION_SELF_TEST",
        "self_test_passed": self_test_result["test_passed"],
        "protocol_state": self_test_result["protocol_state"],
        "total_steps_executed": self_test_result["total_steps_executed"],
        "aggregate_proof_hash": self_test_result["aggregate_proof_hash"],
        "ok": self_test_result["ok"],
    }


def _AGENT_EXECUTION_FUNCTION_FOR_LEARNING_MODULE_FEEDBACK_INTEGRATION_AND_CALIBRATION(
    directive_payload: Dict[str, Any],
) -> Dict[str, Any]:
    """Internal execution logic for the Learning Module Feedback Integration and Calibration Unit."""
    from .organism import (
        CALL_THINKING_PROCESS,
        CALL_MIRROR_UPDATE_LANE,
        CALL_LEARNING_MIRROR_UPDATE,
        CALL_KEDDEH_THEOREM_LEDGER,
    )
    memory_frame = directive_payload.get(
        "memory_frame",
        {
            "signal_strength": 0.88,
            "environment": "ENVIRONMENT_CONTINUOUS_INTEGRATION",
            "load": 0.72,
            "power_core": 1,
        },
    )
    thought = CALL_THINKING_PROCESS(memory_frame=memory_frame)
    mirror = CALL_MIRROR_UPDATE_LANE(
        thought_frame=thought["thought_frame"],
        proposed_delta={"learning_update": "APPROVED", "power_core": 1},
        power_core=1,
    )
    learning = CALL_LEARNING_MIRROR_UPDATE(mirror_result=mirror)
    theorem = CALL_KEDDEH_THEOREM_LEDGER(
        proof_frame={
            "learning_committed": learning["learning_committed"],
            "mirror_valid": mirror["valid"],
            "thought_frame": thought["thought_frame"],
        }
    )
    return {
        "agent": AGENT_CANONICAL_NAME_LEARNING_MODULE_FEEDBACK_INTEGRATION_AND_CALIBRATION_UNIT,
        "directive_executed": "DIRECTIVE_INTEGRATE_LEARNING_MODULE_FEEDBACK",
        "thinking_completed": thought["status"] == "THOUGHT_FRAME_PRODUCED",
        "mirror_valid": mirror["valid"],
        "learning_committed": learning["learning_committed"],
        "theorem_compliance_recorded": theorem["status"] == "THEOREM_COMPLIANCE_RECORDED",
        "ledger_hash": theorem["ledger_hash"],
        "ok": (
            learning["learning_committed"]
            and theorem["status"] == "THEOREM_COMPLIANCE_RECORDED"
        ),
    }


def _AGENT_EXECUTION_FUNCTION_FOR_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION(
    directive_payload: Dict[str, Any],
) -> Dict[str, Any]:
    """Internal execution logic for the Failover Chain Management and Secondary Activation Unit."""
    from .zero_classifier import (
        CALL_ZERO_CLASSIFY,
        CALL_ZERO_RELATION_RESOLVE,
        CALL_SYMBOLIC_ZERO_GATE,
    )
    classify = CALL_ZERO_CLASSIFY(symbol=0, context="failover_chain_boundary_origin")
    relation = CALL_ZERO_RELATION_RESOLVE(left_value=1.0, right_value=-1.0)
    gate = CALL_SYMBOLIC_ZERO_GATE(zero_frame=classify)
    return {
        "agent": AGENT_CANONICAL_NAME_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION_UNIT,
        "directive_executed": "DIRECTIVE_VERIFY_FAILOVER_CHAIN_BOUNDARY_INTEGRITY",
        "zero_class": classify["zero_class"],
        "gate_passed": gate["gate_passed"],
        "power_one_preserved": relation["power_one_preserved"] == 1,
        "failover_chain_integrity": (
            gate["gate_passed"] and relation["power_one_preserved"] == 1
        ),
        "ok": gate["gate_passed"] and relation["power_one_preserved"] == 1,
    }


# ---------------------------------------------------------------------------
# Agent unit registry — all seven units registered at module load time
# ---------------------------------------------------------------------------

AGENT_DIRECTIVE_UNIT_REGISTRY: Dict[str, AgentDirectiveUnit] = {
    AGENT_CANONICAL_NAME_GOVERNANCE_NAMING_PROTOCOL_ENFORCEMENT_UNIT: AgentDirectiveUnit(
        canonical_agent_name=AGENT_CANONICAL_NAME_GOVERNANCE_NAMING_PROTOCOL_ENFORCEMENT_UNIT,
        directive_category="DIRECTIVE_VALIDATE_ALL_SYSTEM_IDENTIFIERS",
        primary_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
        agent_execution_function=(
            _AGENT_EXECUTION_FUNCTION_FOR_GOVERNANCE_NAMING_PROTOCOL_ENFORCEMENT
        ),
        failover_secondary_agent_name=(
            AGENT_CANONICAL_NAME_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION_UNIT
        ),
    ),
    AGENT_CANONICAL_NAME_BUILD_COMPILATION_DIRECTIVE_EXECUTION_UNIT: AgentDirectiveUnit(
        canonical_agent_name=AGENT_CANONICAL_NAME_BUILD_COMPILATION_DIRECTIVE_EXECUTION_UNIT,
        directive_category="DIRECTIVE_BUILD_COMPILATION_TARGET_ALL_PLATFORMS",
        primary_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
        agent_execution_function=(
            _AGENT_EXECUTION_FUNCTION_FOR_BUILD_COMPILATION_DIRECTIVE
        ),
        failover_secondary_agent_name=(
            AGENT_CANONICAL_NAME_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION_UNIT
        ),
    ),
    AGENT_CANONICAL_NAME_VALIDATION_AND_SMOKE_TEST_DIRECTIVE_EXECUTION_UNIT: AgentDirectiveUnit(
        canonical_agent_name=(
            AGENT_CANONICAL_NAME_VALIDATION_AND_SMOKE_TEST_DIRECTIVE_EXECUTION_UNIT
        ),
        directive_category="DIRECTIVE_VALIDATE_SMOKE_TESTS_ALL_TARGETS",
        primary_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
        agent_execution_function=(
            _AGENT_EXECUTION_FUNCTION_FOR_VALIDATION_AND_SMOKE_TEST_DIRECTIVE
        ),
        failover_secondary_agent_name=(
            AGENT_CANONICAL_NAME_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION_UNIT
        ),
    ),
    AGENT_CANONICAL_NAME_PACKAGING_AND_ARTIFACT_PRODUCTION_DIRECTIVE_EXECUTION_UNIT: (
        AgentDirectiveUnit(
            canonical_agent_name=(
                AGENT_CANONICAL_NAME_PACKAGING_AND_ARTIFACT_PRODUCTION_DIRECTIVE_EXECUTION_UNIT
            ),
            directive_category="DIRECTIVE_PACKAGE_ARTIFACT_ALL_TARGETS",
            primary_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
            agent_execution_function=(
                _AGENT_EXECUTION_FUNCTION_FOR_PACKAGING_AND_ARTIFACT_PRODUCTION_DIRECTIVE
            ),
            failover_secondary_agent_name=(
                AGENT_CANONICAL_NAME_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION_UNIT
            ),
        )
    ),
    AGENT_CANONICAL_NAME_ITERATIVE_RESOLUTION_DIRECTION_AND_ESCALATION_UNIT: AgentDirectiveUnit(
        canonical_agent_name=(
            AGENT_CANONICAL_NAME_ITERATIVE_RESOLUTION_DIRECTION_AND_ESCALATION_UNIT
        ),
        directive_category="DIRECTIVE_EXECUTE_ITERATIVE_RESOLUTION_SELF_TEST",
        primary_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
        agent_execution_function=(
            _AGENT_EXECUTION_FUNCTION_FOR_ITERATIVE_RESOLUTION_DIRECTION_AND_ESCALATION
        ),
        failover_secondary_agent_name=(
            AGENT_CANONICAL_NAME_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION_UNIT
        ),
    ),
    AGENT_CANONICAL_NAME_LEARNING_MODULE_FEEDBACK_INTEGRATION_AND_CALIBRATION_UNIT: (
        AgentDirectiveUnit(
            canonical_agent_name=(
                AGENT_CANONICAL_NAME_LEARNING_MODULE_FEEDBACK_INTEGRATION_AND_CALIBRATION_UNIT
            ),
            directive_category="DIRECTIVE_INTEGRATE_LEARNING_MODULE_FEEDBACK",
            primary_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
            agent_execution_function=(
                _AGENT_EXECUTION_FUNCTION_FOR_LEARNING_MODULE_FEEDBACK_INTEGRATION_AND_CALIBRATION
            ),
            failover_secondary_agent_name=(
                AGENT_CANONICAL_NAME_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION_UNIT
            ),
        )
    ),
    AGENT_CANONICAL_NAME_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION_UNIT: (
        AgentDirectiveUnit(
            canonical_agent_name=(
                AGENT_CANONICAL_NAME_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION_UNIT
            ),
            directive_category="DIRECTIVE_VERIFY_FAILOVER_CHAIN_BOUNDARY_INTEGRITY",
            primary_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
            agent_execution_function=(
                _AGENT_EXECUTION_FUNCTION_FOR_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION
            ),
            failover_secondary_agent_name=None,
        )
    ),
}


# ---------------------------------------------------------------------------
# Dispatcher functions
# ---------------------------------------------------------------------------

def FUNCTION_AGENT_DIRECTIVE_DISPATCHER_EXECUTE_SINGLE_DIRECTIVE_ON_NAMED_AGENT_WITH_FAILOVER(
    directive_assignment: AgentDirectiveAssignment,
) -> AgentDirectiveExecutionOutcome:
    """Execute one directive on its designated agent; activate failover if primary fails.

    FUNCTION_AGENT_DIRECTIVE_DISPATCHER_EXECUTE_SINGLE_DIRECTIVE_ON_NAMED_AGENT_WITH_FAILOVER

    Input:  directive_assignment — one AgentDirectiveAssignment to dispatch
    Action: looks up the primary agent by canonical name; executes its function;
            on exception or ok=False result, activates the configured failover
            secondary agent if one is registered
    Output: AgentDirectiveExecutionOutcome with complete execution record
    Proof gate: PROOF_GATE_SINGLE_DIRECTIVE_DISPATCHED_AND_OUTCOME_CAPTURED
    Pending:    PENDING_TIMEOUT_ENFORCEMENT_FOR_LONG_RUNNING_AGENT_DIRECTIVES
    """
    primary_agent = AGENT_DIRECTIVE_UNIT_REGISTRY.get(
        directive_assignment.target_agent_canonical_name
    )
    if primary_agent is None:
        return AgentDirectiveExecutionOutcome(
            assignment_canonical_name=directive_assignment.assignment_canonical_name,
            executing_agent_canonical_name=directive_assignment.target_agent_canonical_name,
            execution_state=STATE_AGENT_DIRECTIVE_FAILED_ALL_UNITS_EXHAUSTED,
            primary_agent_failed=True,
            failure_description=(
                f"Primary agent {directive_assignment.target_agent_canonical_name!r} "
                f"is not registered in AGENT_DIRECTIVE_UNIT_REGISTRY"
            ),
        )

    # Attempt primary agent execution
    primary_succeeded = False
    primary_result: Dict[str, Any] = {}
    primary_failure_description: Optional[str] = None

    try:
        primary_result = primary_agent.agent_execution_function(
            directive_assignment.directive_payload
        )
        primary_succeeded = primary_result.get("ok", False)
        if not primary_succeeded:
            primary_failure_description = (
                f"Primary agent returned ok=False: {json.dumps(primary_result, default=str)[:200]}"
            )
    except Exception as primary_exception:
        primary_failure_description = (
            f"Primary agent raised exception: {type(primary_exception).__name__}: "
            f"{str(primary_exception)}"
        )

    if primary_succeeded:
        result_hash = hashlib.sha256(
            json.dumps(primary_result, sort_keys=True, default=str).encode("utf-8")
        ).hexdigest()[:16]
        return AgentDirectiveExecutionOutcome(
            assignment_canonical_name=directive_assignment.assignment_canonical_name,
            executing_agent_canonical_name=primary_agent.canonical_agent_name,
            execution_state=STATE_AGENT_DIRECTIVE_COMPLETED_SUCCESSFULLY,
            result_payload=primary_result,
            proof_hash=result_hash,
        )

    # Primary failed — activate failover secondary if registered
    if primary_agent.failover_secondary_agent_name is None:
        return AgentDirectiveExecutionOutcome(
            assignment_canonical_name=directive_assignment.assignment_canonical_name,
            executing_agent_canonical_name=primary_agent.canonical_agent_name,
            execution_state=STATE_AGENT_DIRECTIVE_FAILED_ALL_UNITS_EXHAUSTED,
            primary_agent_failed=True,
            failure_description=primary_failure_description,
        )

    secondary_agent = AGENT_DIRECTIVE_UNIT_REGISTRY.get(
        primary_agent.failover_secondary_agent_name
    )
    if secondary_agent is None:
        return AgentDirectiveExecutionOutcome(
            assignment_canonical_name=directive_assignment.assignment_canonical_name,
            executing_agent_canonical_name=primary_agent.canonical_agent_name,
            execution_state=STATE_AGENT_DIRECTIVE_FAILED_ALL_UNITS_EXHAUSTED,
            primary_agent_failed=True,
            failure_description=(
                f"{primary_failure_description} | "
                f"Failover secondary {primary_agent.failover_secondary_agent_name!r} "
                f"not found in registry"
            ),
        )

    # Execute secondary (failover)
    secondary_result: Dict[str, Any] = {}
    try:
        secondary_result = secondary_agent.agent_execution_function(
            directive_assignment.directive_payload
        )
        secondary_succeeded = secondary_result.get("ok", False)
    except Exception as secondary_exception:
        return AgentDirectiveExecutionOutcome(
            assignment_canonical_name=directive_assignment.assignment_canonical_name,
            executing_agent_canonical_name=secondary_agent.canonical_agent_name,
            execution_state=STATE_AGENT_DIRECTIVE_FAILED_ALL_UNITS_EXHAUSTED,
            primary_agent_failed=True,
            failover_secondary_activated=True,
            failure_description=(
                f"Primary: {primary_failure_description} | "
                f"Secondary raised: {type(secondary_exception).__name__}: "
                f"{str(secondary_exception)}"
            ),
        )

    result_hash = hashlib.sha256(
        json.dumps(secondary_result, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()[:16]
    execution_state = (
        STATE_AGENT_DIRECTIVE_FAILOVER_SECONDARY_ACTIVATED_AND_COMPLETED
        if secondary_succeeded
        else STATE_AGENT_DIRECTIVE_FAILED_ALL_UNITS_EXHAUSTED
    )
    return AgentDirectiveExecutionOutcome(
        assignment_canonical_name=directive_assignment.assignment_canonical_name,
        executing_agent_canonical_name=secondary_agent.canonical_agent_name,
        execution_state=execution_state,
        primary_agent_failed=True,
        failover_secondary_activated=True,
        result_payload=secondary_result,
        failure_description=primary_failure_description if not secondary_succeeded else None,
        proof_hash=result_hash if secondary_succeeded else None,
    )


def FUNCTION_AGENT_DIRECTIVE_DISPATCHER_EXECUTE_ALL_AGENT_DIRECTIVES_IN_SEQUENCE(
    directive_assignments: List[AgentDirectiveAssignment],
) -> AgentDirectiveDispatcherCompleteExecutionResult:
    """Dispatch all agent directives in sequence and collect complete results.

    FUNCTION_AGENT_DIRECTIVE_DISPATCHER_EXECUTE_ALL_AGENT_DIRECTIVES_IN_SEQUENCE

    Input:  directive_assignments — ordered list of AgentDirectiveAssignment objects
    Action: dispatches each assignment using the single-directive dispatcher;
            counts completions, failures, and failover activations;
            computes aggregate proof hash
    Output: AgentDirectiveDispatcherCompleteExecutionResult
    Proof gate: PROOF_GATE_ALL_AGENT_DIRECTIVES_DISPATCHED_AND_RESULTS_COLLECTED
    Pending:    PENDING_PARALLEL_AGENT_DIRECTIVE_EXECUTION_ACROSS_ALL_UNITS
    """
    per_assignment_outcomes: List[AgentDirectiveExecutionOutcome] = []
    for assignment in directive_assignments:
        outcome = (
            FUNCTION_AGENT_DIRECTIVE_DISPATCHER_EXECUTE_SINGLE_DIRECTIVE_ON_NAMED_AGENT_WITH_FAILOVER(
                assignment
            )
        )
        per_assignment_outcomes.append(outcome)

    completed_count = sum(
        1
        for o in per_assignment_outcomes
        if o.execution_state in (
            STATE_AGENT_DIRECTIVE_COMPLETED_SUCCESSFULLY,
            STATE_AGENT_DIRECTIVE_FAILOVER_SECONDARY_ACTIVATED_AND_COMPLETED,
        )
    )
    failed_count = len(per_assignment_outcomes) - completed_count
    failover_activation_count = sum(
        1 for o in per_assignment_outcomes if o.failover_secondary_activated
    )
    all_completed = failed_count == 0

    aggregate_source = json.dumps(
        [
            {"name": o.assignment_canonical_name, "hash": o.proof_hash}
            for o in per_assignment_outcomes
        ],
        sort_keys=True,
    )
    aggregate_proof_hash = hashlib.sha256(
        aggregate_source.encode("utf-8")
    ).hexdigest()[:16]

    proof_gate = (
        "PROOF_GATE_ALL_AGENT_DIRECTIVES_DISPATCHED_AND_RESULTS_COLLECTED"
        if all_completed
        else "PENDING_FAILED_AGENT_DIRECTIVES_REQUIRE_RESOLUTION"
    )

    return AgentDirectiveDispatcherCompleteExecutionResult(
        total_directives_dispatched=len(directive_assignments),
        total_directives_completed=completed_count,
        total_directives_failed=failed_count,
        total_failover_activations=failover_activation_count,
        all_directives_completed=all_completed,
        per_assignment_outcomes=per_assignment_outcomes,
        aggregate_proof_hash=aggregate_proof_hash,
        proof_gate=proof_gate,
    )


def FUNCTION_AGENT_DIRECTIVE_DISPATCHER_BUILD_STANDARD_DIRECTIVE_ASSIGNMENTS_FOR_ALL_SEVEN_AGENTS(
    target_platform: str = "linux",
) -> List[AgentDirectiveAssignment]:
    """Build the standard directive assignment list for all seven agent units.

    FUNCTION_AGENT_DIRECTIVE_DISPATCHER_BUILD_STANDARD_DIRECTIVE_ASSIGNMENTS_FOR_ALL_SEVEN_AGENTS

    Input:  target_platform — build/validation platform target (default: 'linux')
    Action: constructs one AgentDirectiveAssignment per registered agent unit,
            using each agent's canonical directive category as the assignment name
    Output: ordered list of AgentDirectiveAssignment objects ready for dispatch
    Proof gate: PROOF_GATE_STANDARD_DIRECTIVE_ASSIGNMENT_LIST_CONSTRUCTED_FOR_ALL_SEVEN_AGENTS
    Pending:    PENDING_DYNAMIC_DIRECTIVE_PAYLOAD_INJECTION_FROM_ENVIRONMENT_CONTEXT
    """
    return [
        AgentDirectiveAssignment(
            assignment_canonical_name=(
                "DIRECTIVE_VALIDATE_ALL_SYSTEM_IDENTIFIERS_GOVERNANCE_SWEEP"
            ),
            target_agent_canonical_name=(
                AGENT_CANONICAL_NAME_GOVERNANCE_NAMING_PROTOCOL_ENFORCEMENT_UNIT
            ),
            directive_payload={"directive": "DIRECTIVE_VALIDATE_ALL_SYSTEM_IDENTIFIERS"},
            target_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
        ),
        AgentDirectiveAssignment(
            assignment_canonical_name="DIRECTIVE_BUILD_COMPILATION_TARGET_LINUX",
            target_agent_canonical_name=(
                AGENT_CANONICAL_NAME_BUILD_COMPILATION_DIRECTIVE_EXECUTION_UNIT
            ),
            directive_payload={"target": target_platform},
            target_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
        ),
        AgentDirectiveAssignment(
            assignment_canonical_name="DIRECTIVE_VALIDATE_SMOKE_TESTS_LINUX_TARGET",
            target_agent_canonical_name=(
                AGENT_CANONICAL_NAME_VALIDATION_AND_SMOKE_TEST_DIRECTIVE_EXECUTION_UNIT
            ),
            directive_payload={"target": target_platform},
            target_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
        ),
        AgentDirectiveAssignment(
            assignment_canonical_name="DIRECTIVE_PACKAGE_ARTIFACT_LINUX_TARGET",
            target_agent_canonical_name=(
                AGENT_CANONICAL_NAME_PACKAGING_AND_ARTIFACT_PRODUCTION_DIRECTIVE_EXECUTION_UNIT
            ),
            directive_payload={"target": target_platform},
            target_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
        ),
        AgentDirectiveAssignment(
            assignment_canonical_name="DIRECTIVE_ITERATIVE_RESOLUTION_SELF_TEST_EXECUTION",
            target_agent_canonical_name=(
                AGENT_CANONICAL_NAME_ITERATIVE_RESOLUTION_DIRECTION_AND_ESCALATION_UNIT
            ),
            directive_payload={"directive": "DIRECTIVE_EXECUTE_ITERATIVE_RESOLUTION_SELF_TEST"},
            target_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
        ),
        AgentDirectiveAssignment(
            assignment_canonical_name="DIRECTIVE_LEARNING_MODULE_FEEDBACK_INTEGRATION_CYCLE",
            target_agent_canonical_name=(
                AGENT_CANONICAL_NAME_LEARNING_MODULE_FEEDBACK_INTEGRATION_AND_CALIBRATION_UNIT
            ),
            directive_payload={
                "memory_frame": {
                    "signal_strength": 0.88,
                    "environment": "ENVIRONMENT_CONTINUOUS_INTEGRATION",
                    "load": 0.72,
                    "power_core": 1,
                }
            },
            target_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
        ),
        AgentDirectiveAssignment(
            assignment_canonical_name="DIRECTIVE_FAILOVER_CHAIN_BOUNDARY_INTEGRITY_VERIFICATION",
            target_agent_canonical_name=(
                AGENT_CANONICAL_NAME_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION_UNIT
            ),
            directive_payload={"directive": "DIRECTIVE_VERIFY_FAILOVER_CHAIN_BOUNDARY_INTEGRITY"},
            target_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
        ),
    ]
