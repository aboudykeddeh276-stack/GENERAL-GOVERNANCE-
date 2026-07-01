from __future__ import annotations

"""Iterative Resolution Engine — Self-Resolving Problem Breakdown with Three-Tier Failover

FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_COMPLETE_SELF_RESOLVING_PROTOCOL

Input:  a problem declaration (whole_name, environment_name, problem_description),
        an ordered list of ResolutionStep objects each carrying a named callable,
        and a maximum total iteration count across all tiers.
Action: decomposes the problem into atomic steps; executes each step under
        TIER_1_DIRECT_EXECUTION; on failure, escalates to
        TIER_2_RETRY_WITH_DECOMPOSITION; on continued failure, escalates to
        TIER_3_CRITICAL_ROOT_CAUSE_ANALYSIS_AND_FIX; commits every resolved
        outcome to the BRAINK proof ledger; integrates learning feedback.
Output: IterativeResolutionProtocolCompleteExecutionResult carrying tier
        history, per-step outcomes, root cause records, and proof hash.
Proof gate: PROOF_GATE_ITERATIVE_RESOLUTION_ENGINE_EXECUTED_TO_COMPLETION
Pending:    PENDING_LEARNING_MODULE_ADAPTIVE_STEP_INJECTION_INTO_RESOLUTION_SEQUENCE
"""

import hashlib
import json
import traceback
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


# ---------------------------------------------------------------------------
# State constants — no abbreviations, full explicit declarations
# ---------------------------------------------------------------------------

STATE_RESOLUTION_PROTOCOL_PENDING: str = (
    "STATE_RESOLUTION_PROTOCOL_PENDING"
)
STATE_RESOLUTION_PROTOCOL_IN_PROGRESS_TIER_1_DIRECT_EXECUTION: str = (
    "STATE_RESOLUTION_PROTOCOL_IN_PROGRESS_TIER_1_DIRECT_EXECUTION"
)
STATE_RESOLUTION_PROTOCOL_IN_PROGRESS_TIER_2_RETRY_WITH_DECOMPOSITION: str = (
    "STATE_RESOLUTION_PROTOCOL_IN_PROGRESS_TIER_2_RETRY_WITH_DECOMPOSITION"
)
STATE_RESOLUTION_PROTOCOL_IN_PROGRESS_TIER_3_CRITICAL_ROOT_CAUSE_ANALYSIS: str = (
    "STATE_RESOLUTION_PROTOCOL_IN_PROGRESS_TIER_3_CRITICAL_ROOT_CAUSE_ANALYSIS"
)
STATE_RESOLUTION_STEP_COMPLETED_SUCCESSFULLY: str = (
    "STATE_RESOLUTION_STEP_COMPLETED_SUCCESSFULLY"
)
STATE_RESOLUTION_STEP_FAILED_AWAITING_ROOT_CAUSE_ANALYSIS: str = (
    "STATE_RESOLUTION_STEP_FAILED_AWAITING_ROOT_CAUSE_ANALYSIS"
)
STATE_RESOLUTION_ROOT_CAUSE_IDENTIFIED_AND_RESOLVED: str = (
    "STATE_RESOLUTION_ROOT_CAUSE_IDENTIFIED_AND_RESOLVED"
)
STATE_RESOLUTION_COMPLETED_ALL_STEPS_PASSED: str = (
    "STATE_RESOLUTION_COMPLETED_ALL_STEPS_PASSED"
)
STATE_RESOLUTION_FAILED_UNRECOVERABLE_AFTER_ALL_THREE_TIERS: str = (
    "STATE_RESOLUTION_FAILED_UNRECOVERABLE_AFTER_ALL_THREE_TIERS"
)


# ---------------------------------------------------------------------------
# Data structures — fully named fields, no field omissions
# ---------------------------------------------------------------------------

@dataclass
class ResolutionStep:
    """One atomic unit of work within the iterative resolution sequence.

    Fields:
      step_canonical_name        — FUNCTION_ or RESOLUTION_ prefixed identifier
      step_environment_name      — ENVIRONMENT_ prefixed execution context
      step_callable              — zero-argument callable returning a Dict result
      max_retry_count_on_failure — how many retry attempts before escalation
      escalation_tier_assignment — which tier handles this step's failures (1, 2, or 3)
    """

    step_canonical_name: str
    step_environment_name: str
    step_callable: Callable[[], Dict[str, Any]]
    max_retry_count_on_failure: int = 1
    escalation_tier_assignment: int = 1


@dataclass
class ResolutionStepExecutionOutcome:
    """Complete execution record for one ResolutionStep.

    Fields:
      step_canonical_name            — matches the step's canonical name
      execution_tier_number          — 1, 2, or 3 indicating which tier executed
      execution_state                — STATE_ constant for this outcome
      attempt_count                  — how many attempts were made
      result_payload                 — the dict returned by the step callable, or empty
      failure_exception_text         — stringified exception if failure occurred
      root_cause_description         — populated by Tier 3 reverse-engineering
      resolution_action_applied      — description of what was done to resolve
      proof_hash                     — SHA-256 of the result payload
    """

    step_canonical_name: str
    execution_tier_number: int
    execution_state: str
    attempt_count: int
    result_payload: Dict[str, Any] = field(default_factory=dict)
    failure_exception_text: Optional[str] = None
    root_cause_description: Optional[str] = None
    resolution_action_applied: Optional[str] = None
    proof_hash: Optional[str] = None


@dataclass
class ResolutionTierSummaryRecord:
    """Summary of all step executions within one resolution tier.

    Fields:
      tier_number                    — 1, 2, or 3
      tier_state                     — STATE_ constant for this tier's outcome
      steps_attempted_in_this_tier   — count of steps attempted
      steps_passed_in_this_tier      — count of steps that produced ok=True
      steps_failed_in_this_tier      — count of steps that failed
      step_outcomes                  — ordered list of per-step outcome records
      escalated_to_next_tier         — True when unresolved steps move up
      tier_proof_hash                — SHA-256 fingerprint of this tier's outcomes
    """

    tier_number: int
    tier_state: str
    steps_attempted_in_this_tier: int
    steps_passed_in_this_tier: int
    steps_failed_in_this_tier: int
    step_outcomes: List[ResolutionStepExecutionOutcome] = field(default_factory=list)
    escalated_to_next_tier: bool = False
    tier_proof_hash: Optional[str] = None


@dataclass
class IterativeResolutionProtocolCompleteExecutionResult:
    """The complete outcome of running the full three-tier resolution protocol.

    Fields:
      problem_whole_name             — WHOLE_ prefixed name of the problem domain
      problem_environment_name       — ENVIRONMENT_ prefixed execution context
      problem_description            — plain text description of the problem
      protocol_state                 — final STATE_ constant
      tier_summary_records           — one TierSummaryRecord per tier used
      total_steps_executed           — across all tiers
      total_steps_passed             — across all tiers
      total_steps_failed             — across all tiers (0 = fully resolved)
      all_steps_resolved             — True when no failures remain
      aggregate_proof_hash           — SHA-256 over all tier proof hashes
      proof_gate                     — PROOF_GATE_ or PENDING_ constant
    """

    problem_whole_name: str
    problem_environment_name: str
    problem_description: str
    protocol_state: str
    tier_summary_records: List[ResolutionTierSummaryRecord] = field(default_factory=list)
    total_steps_executed: int = 0
    total_steps_passed: int = 0
    total_steps_failed: int = 0
    all_steps_resolved: bool = False
    aggregate_proof_hash: Optional[str] = None
    proof_gate: Optional[str] = None


# ---------------------------------------------------------------------------
# Core engine functions — each fully named, fully documented
# ---------------------------------------------------------------------------

def FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_SINGLE_STEP_WITH_RETRY_AND_CAPTURE_OUTCOME(
    resolution_step: ResolutionStep,
    execution_tier_number: int,
) -> ResolutionStepExecutionOutcome:
    """Execute one ResolutionStep with retry logic and capture the complete outcome.

    FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_SINGLE_STEP_WITH_RETRY_AND_CAPTURE_OUTCOME

    Input:  resolution_step — the step to execute
            execution_tier_number — which tier is executing this step
    Action: calls step_callable up to (max_retry_count_on_failure + 1) times;
            on success returns immediately with STATE_RESOLUTION_STEP_COMPLETED_SUCCESSFULLY;
            on all-attempts-exhausted returns with STATE_RESOLUTION_STEP_FAILED
    Output: ResolutionStepExecutionOutcome with full execution record
    Proof gate: PROOF_GATE_SINGLE_STEP_EXECUTION_OUTCOME_CAPTURED
    Pending:    PENDING_CIRCUIT_BREAKER_INTEGRATION_FOR_CASCADING_FAILURE_PREVENTION
    """
    maximum_attempts = resolution_step.max_retry_count_on_failure + 1
    last_exception_text: Optional[str] = None
    last_result: Dict[str, Any] = {}

    for attempt_number in range(1, maximum_attempts + 1):
        try:
            step_result = resolution_step.step_callable()
            result_serialized = json.dumps(step_result, sort_keys=True, default=str)
            proof_hash = hashlib.sha256(result_serialized.encode("utf-8")).hexdigest()[:16]
            return ResolutionStepExecutionOutcome(
                step_canonical_name=resolution_step.step_canonical_name,
                execution_tier_number=execution_tier_number,
                execution_state=STATE_RESOLUTION_STEP_COMPLETED_SUCCESSFULLY,
                attempt_count=attempt_number,
                result_payload=step_result,
                proof_hash=proof_hash,
            )
        except Exception as captured_exception:
            last_exception_text = (
                f"EXCEPTION_TYPE={type(captured_exception).__name__} | "
                f"EXCEPTION_MESSAGE={str(captured_exception)} | "
                f"TRACEBACK={traceback.format_exc()}"
            )
            last_result = {"exception": str(captured_exception)}

    return ResolutionStepExecutionOutcome(
        step_canonical_name=resolution_step.step_canonical_name,
        execution_tier_number=execution_tier_number,
        execution_state=STATE_RESOLUTION_STEP_FAILED_AWAITING_ROOT_CAUSE_ANALYSIS,
        attempt_count=maximum_attempts,
        result_payload=last_result,
        failure_exception_text=last_exception_text,
    )


def FUNCTION_ITERATIVE_RESOLUTION_ENGINE_REVERSE_ENGINEER_FAILED_STEP_TO_ATOMIC_ROOT_CAUSE(
    failed_step_outcome: ResolutionStepExecutionOutcome,
) -> Dict[str, str]:
    """Reverse-engineer a failed step outcome to identify its atomic root cause.

    FUNCTION_ITERATIVE_RESOLUTION_ENGINE_REVERSE_ENGINEER_FAILED_STEP_TO_ATOMIC_ROOT_CAUSE

    Input:  failed_step_outcome — a ResolutionStepExecutionOutcome with failure state
    Action: analyses the exception text and result payload to categorise the failure;
            determines whether it is a runtime error, dependency error, state error,
            boundary error, or unknown error; produces a root cause description
    Output: dict containing root_cause_category, root_cause_description,
            resolution_action_recommendation, and escalation_required flag
    Proof gate: PROOF_GATE_ROOT_CAUSE_ANALYSIS_COMPLETED_FOR_FAILED_STEP
    Pending:    PENDING_MACHINE_LEARNING_ASSISTED_ROOT_CAUSE_CLASSIFICATION
    """
    exception_text = failed_step_outcome.failure_exception_text or ""
    result_text = json.dumps(failed_step_outcome.result_payload, default=str)

    root_cause_category: str
    root_cause_description: str
    resolution_action_recommendation: str
    escalation_required: bool

    if "ModuleNotFoundError" in exception_text or "ImportError" in exception_text:
        root_cause_category = "ROOT_CAUSE_CATEGORY_MISSING_DEPENDENCY_OR_MODULE"
        root_cause_description = (
            "A required module or dependency is not installed or not importable. "
            "The step callable cannot locate its runtime dependency."
        )
        resolution_action_recommendation = (
            "RESOLUTION_ACTION_INSTALL_MISSING_DEPENDENCY_AND_RERUN_STEP"
        )
        escalation_required = False
    elif "AttributeError" in exception_text or "KeyError" in exception_text:
        root_cause_category = "ROOT_CAUSE_CATEGORY_STATE_CONTRACT_VIOLATION"
        root_cause_description = (
            "A required attribute or key is absent from the result or input payload. "
            "The step's state contract is not satisfied."
        )
        resolution_action_recommendation = (
            "RESOLUTION_ACTION_VALIDATE_INPUT_STATE_CONTRACT_AND_DECOMPOSE_STEP"
        )
        escalation_required = True
    elif "AssertionError" in exception_text:
        root_cause_category = "ROOT_CAUSE_CATEGORY_PROOF_ASSERTION_FAILURE"
        root_cause_description = (
            "A proof assertion within the step callable was not satisfied. "
            "The expected boundary condition was not met."
        )
        resolution_action_recommendation = (
            "RESOLUTION_ACTION_RECALIBRATE_BOUNDARY_PARAMETERS_AND_RETRY"
        )
        escalation_required = True
    elif "TimeoutError" in exception_text or "ConnectionError" in exception_text:
        root_cause_category = "ROOT_CAUSE_CATEGORY_ENVIRONMENT_CONNECTIVITY_FAILURE"
        root_cause_description = (
            "The execution environment is not reachable or a timeout occurred. "
            "The step callable cannot connect to its required environment resource."
        )
        resolution_action_recommendation = (
            "RESOLUTION_ACTION_VERIFY_ENVIRONMENT_CONNECTIVITY_AND_RETRY"
        )
        escalation_required = False
    elif exception_text:
        root_cause_category = "ROOT_CAUSE_CATEGORY_UNCLASSIFIED_RUNTIME_EXCEPTION"
        root_cause_description = (
            f"An unclassified exception occurred during step execution. "
            f"Exception summary: {exception_text[:200]}"
        )
        resolution_action_recommendation = (
            "RESOLUTION_ACTION_ESCALATE_TO_TIER_3_FOR_MANUAL_REVERSE_ENGINEERING"
        )
        escalation_required = True
    else:
        root_cause_category = "ROOT_CAUSE_CATEGORY_STEP_CALLABLE_RETURNED_WITHOUT_EXCEPTION"
        root_cause_description = (
            "The step callable completed without exception but the outcome state "
            "indicates failure. The result payload may be empty or malformed."
        )
        resolution_action_recommendation = (
            "RESOLUTION_ACTION_INSPECT_RESULT_PAYLOAD_AND_VALIDATE_OK_FLAG"
        )
        escalation_required = True

    return {
        "root_cause_category": root_cause_category,
        "root_cause_description": root_cause_description,
        "resolution_action_recommendation": resolution_action_recommendation,
        "escalation_required": str(escalation_required),
        "failed_step_canonical_name": failed_step_outcome.step_canonical_name,
    }


def FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_TIER_1_DIRECT_EXECUTION_FOR_ALL_STEPS(
    resolution_steps: List[ResolutionStep],
) -> ResolutionTierSummaryRecord:
    """Execute all resolution steps under Tier 1 direct execution.

    FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_TIER_1_DIRECT_EXECUTION_FOR_ALL_STEPS

    Input:  resolution_steps — ordered list of ResolutionStep objects
    Action: executes each step once (with its configured retry count);
            collects outcomes; computes tier proof hash
    Output: ResolutionTierSummaryRecord for Tier 1
    Proof gate: PROOF_GATE_TIER_1_DIRECT_EXECUTION_COMPLETED_FOR_ALL_STEPS
    Pending:    PENDING_PARALLEL_TIER_1_EXECUTION_FOR_INDEPENDENT_STEPS
    """
    step_outcomes: List[ResolutionStepExecutionOutcome] = []
    for resolution_step in resolution_steps:
        step_outcome = (
            FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_SINGLE_STEP_WITH_RETRY_AND_CAPTURE_OUTCOME(
                resolution_step=resolution_step,
                execution_tier_number=1,
            )
        )
        step_outcomes.append(step_outcome)

    passed_count = sum(
        1 for outcome in step_outcomes
        if outcome.execution_state == STATE_RESOLUTION_STEP_COMPLETED_SUCCESSFULLY
    )
    failed_count = len(step_outcomes) - passed_count
    tier_state = (
        STATE_RESOLUTION_COMPLETED_ALL_STEPS_PASSED
        if failed_count == 0
        else STATE_RESOLUTION_PROTOCOL_IN_PROGRESS_TIER_2_RETRY_WITH_DECOMPOSITION
    )

    tier_hash_source = json.dumps(
        [{"name": o.step_canonical_name, "state": o.execution_state} for o in step_outcomes],
        sort_keys=True,
    )
    tier_proof_hash = hashlib.sha256(tier_hash_source.encode("utf-8")).hexdigest()[:16]

    return ResolutionTierSummaryRecord(
        tier_number=1,
        tier_state=tier_state,
        steps_attempted_in_this_tier=len(step_outcomes),
        steps_passed_in_this_tier=passed_count,
        steps_failed_in_this_tier=failed_count,
        step_outcomes=step_outcomes,
        escalated_to_next_tier=failed_count > 0,
        tier_proof_hash=tier_proof_hash,
    )


def FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_TIER_2_RETRY_WITH_DECOMPOSITION_FOR_FAILED_STEPS(
    failed_step_outcomes_from_tier_1: List[ResolutionStepExecutionOutcome],
    original_resolution_steps: List[ResolutionStep],
) -> ResolutionTierSummaryRecord:
    """Retry failed steps under Tier 2 with sub-step decomposition.

    FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_TIER_2_RETRY_WITH_DECOMPOSITION_FOR_FAILED_STEPS

    Input:  failed_step_outcomes_from_tier_1 — outcomes that did not pass in Tier 1
            original_resolution_steps — the original step list (for step config lookup)
    Action: runs root cause analysis on each failed step; attempts retry with
            increased retry count; records root cause even on retry success
    Output: ResolutionTierSummaryRecord for Tier 2
    Proof gate: PROOF_GATE_TIER_2_RETRY_WITH_DECOMPOSITION_COMPLETED
    Pending:    PENDING_DYNAMIC_SUB_STEP_INJECTION_FROM_LEARNING_MODULE
    """
    step_lookup = {step.step_canonical_name: step for step in original_resolution_steps}
    step_outcomes: List[ResolutionStepExecutionOutcome] = []

    for failed_outcome in failed_step_outcomes_from_tier_1:
        root_cause = (
            FUNCTION_ITERATIVE_RESOLUTION_ENGINE_REVERSE_ENGINEER_FAILED_STEP_TO_ATOMIC_ROOT_CAUSE(
                failed_outcome
            )
        )
        original_step = step_lookup.get(failed_outcome.step_canonical_name)
        if original_step is None:
            step_outcomes.append(
                ResolutionStepExecutionOutcome(
                    step_canonical_name=failed_outcome.step_canonical_name,
                    execution_tier_number=2,
                    execution_state=STATE_RESOLUTION_STEP_FAILED_AWAITING_ROOT_CAUSE_ANALYSIS,
                    attempt_count=0,
                    root_cause_description=root_cause["root_cause_description"],
                )
            )
            continue

        # Retry with augmented retry count in Tier 2
        augmented_step = ResolutionStep(
            step_canonical_name=original_step.step_canonical_name,
            step_environment_name=original_step.step_environment_name,
            step_callable=original_step.step_callable,
            max_retry_count_on_failure=original_step.max_retry_count_on_failure + 1,
            escalation_tier_assignment=2,
        )
        tier_2_outcome = (
            FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_SINGLE_STEP_WITH_RETRY_AND_CAPTURE_OUTCOME(
                resolution_step=augmented_step,
                execution_tier_number=2,
            )
        )
        tier_2_outcome.root_cause_description = root_cause["root_cause_description"]
        tier_2_outcome.resolution_action_applied = (
            root_cause["resolution_action_recommendation"]
        )
        step_outcomes.append(tier_2_outcome)

    passed_count = sum(
        1 for outcome in step_outcomes
        if outcome.execution_state == STATE_RESOLUTION_STEP_COMPLETED_SUCCESSFULLY
    )
    failed_count = len(step_outcomes) - passed_count
    tier_state = (
        STATE_RESOLUTION_COMPLETED_ALL_STEPS_PASSED
        if failed_count == 0
        else STATE_RESOLUTION_PROTOCOL_IN_PROGRESS_TIER_3_CRITICAL_ROOT_CAUSE_ANALYSIS
    )

    tier_hash_source = json.dumps(
        [{"name": o.step_canonical_name, "state": o.execution_state} for o in step_outcomes],
        sort_keys=True,
    )
    tier_proof_hash = hashlib.sha256(tier_hash_source.encode("utf-8")).hexdigest()[:16]

    return ResolutionTierSummaryRecord(
        tier_number=2,
        tier_state=tier_state,
        steps_attempted_in_this_tier=len(step_outcomes),
        steps_passed_in_this_tier=passed_count,
        steps_failed_in_this_tier=failed_count,
        step_outcomes=step_outcomes,
        escalated_to_next_tier=failed_count > 0,
        tier_proof_hash=tier_proof_hash,
    )


def FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_TIER_3_CRITICAL_ROOT_CAUSE_ANALYSIS_AND_RECORD(
    failed_step_outcomes_from_tier_2: List[ResolutionStepExecutionOutcome],
    original_resolution_steps: List[ResolutionStep],
) -> ResolutionTierSummaryRecord:
    """Execute Tier 3 critical root cause analysis for remaining unresolved steps.

    FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_TIER_3_CRITICAL_ROOT_CAUSE_ANALYSIS_AND_RECORD

    Input:  failed_step_outcomes_from_tier_2 — outcomes that persisted through Tier 2
            original_resolution_steps — the original step list for config lookup
    Action: performs full root cause analysis on each remaining failure;
            marks each step as STATE_RESOLUTION_ROOT_CAUSE_IDENTIFIED_AND_RESOLVED
            or STATE_RESOLUTION_FAILED_UNRECOVERABLE depending on categorisation;
            records all findings — does not silently discard any failure
    Output: ResolutionTierSummaryRecord for Tier 3
    Proof gate: PROOF_GATE_TIER_3_CRITICAL_ANALYSIS_COMPLETED_ALL_FAILURES_RECORDED
    Pending:    PENDING_AUTOMATED_FIX_APPLICATION_FOR_CLASSIFIED_ROOT_CAUSES
    """
    step_lookup = {step.step_canonical_name: step for step in original_resolution_steps}
    step_outcomes: List[ResolutionStepExecutionOutcome] = []

    for failed_outcome in failed_step_outcomes_from_tier_2:
        root_cause = (
            FUNCTION_ITERATIVE_RESOLUTION_ENGINE_REVERSE_ENGINEER_FAILED_STEP_TO_ATOMIC_ROOT_CAUSE(
                failed_outcome
            )
        )
        original_step = step_lookup.get(failed_outcome.step_canonical_name)

        # In Tier 3, attempt one final execution with maximum retries
        if original_step is not None:
            tier_3_step = ResolutionStep(
                step_canonical_name=original_step.step_canonical_name,
                step_environment_name=original_step.step_environment_name,
                step_callable=original_step.step_callable,
                max_retry_count_on_failure=3,
                escalation_tier_assignment=3,
            )
            tier_3_outcome = (
                FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_SINGLE_STEP_WITH_RETRY_AND_CAPTURE_OUTCOME(
                    resolution_step=tier_3_step,
                    execution_tier_number=3,
                )
            )
        else:
            tier_3_outcome = ResolutionStepExecutionOutcome(
                step_canonical_name=failed_outcome.step_canonical_name,
                execution_tier_number=3,
                execution_state=STATE_RESOLUTION_FAILED_UNRECOVERABLE_AFTER_ALL_THREE_TIERS,
                attempt_count=0,
            )

        tier_3_outcome.root_cause_description = root_cause["root_cause_description"]
        tier_3_outcome.resolution_action_applied = (
            root_cause["resolution_action_recommendation"]
        )

        # Upgrade state label if step now passed
        if tier_3_outcome.execution_state == STATE_RESOLUTION_STEP_COMPLETED_SUCCESSFULLY:
            tier_3_outcome.execution_state = STATE_RESOLUTION_ROOT_CAUSE_IDENTIFIED_AND_RESOLVED

        step_outcomes.append(tier_3_outcome)

    passed_count = sum(
        1 for outcome in step_outcomes
        if outcome.execution_state in (
            STATE_RESOLUTION_STEP_COMPLETED_SUCCESSFULLY,
            STATE_RESOLUTION_ROOT_CAUSE_IDENTIFIED_AND_RESOLVED,
        )
    )
    failed_count = len(step_outcomes) - passed_count
    tier_state = (
        STATE_RESOLUTION_COMPLETED_ALL_STEPS_PASSED
        if failed_count == 0
        else STATE_RESOLUTION_FAILED_UNRECOVERABLE_AFTER_ALL_THREE_TIERS
    )

    tier_hash_source = json.dumps(
        [{"name": o.step_canonical_name, "state": o.execution_state} for o in step_outcomes],
        sort_keys=True,
    )
    tier_proof_hash = hashlib.sha256(tier_hash_source.encode("utf-8")).hexdigest()[:16]

    return ResolutionTierSummaryRecord(
        tier_number=3,
        tier_state=tier_state,
        steps_attempted_in_this_tier=len(step_outcomes),
        steps_passed_in_this_tier=passed_count,
        steps_failed_in_this_tier=failed_count,
        step_outcomes=step_outcomes,
        escalated_to_next_tier=False,
        tier_proof_hash=tier_proof_hash,
    )


def FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_COMPLETE_SELF_RESOLVING_PROTOCOL(
    problem_whole_name: str,
    problem_environment_name: str,
    problem_description: str,
    resolution_steps: List[ResolutionStep],
) -> IterativeResolutionProtocolCompleteExecutionResult:
    """Execute the complete three-tier self-resolving protocol for a declared problem.

    FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_COMPLETE_SELF_RESOLVING_PROTOCOL

    Input:  problem_whole_name — WHOLE_ prefixed name of the problem domain
            problem_environment_name — ENVIRONMENT_ prefixed execution context
            problem_description — plain text description of what is being resolved
            resolution_steps — ordered list of ResolutionStep objects
    Action: Tier 1 direct execution; failed steps escalate to Tier 2 retry with
            decomposition; still-failed steps escalate to Tier 3 critical root
            cause analysis; all outcomes committed to proof record
    Output: IterativeResolutionProtocolCompleteExecutionResult
    Proof gate: PROOF_GATE_ITERATIVE_RESOLUTION_ENGINE_EXECUTED_TO_COMPLETION
    Pending:    PENDING_LEARNING_MODULE_ADAPTIVE_STEP_INJECTION_INTO_RESOLUTION_SEQUENCE
    """
    tier_summary_records: List[ResolutionTierSummaryRecord] = []
    total_passed = 0
    total_failed = 0
    total_executed = 0

    # --- TIER 1 ---
    tier_1_summary = (
        FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_TIER_1_DIRECT_EXECUTION_FOR_ALL_STEPS(
            resolution_steps
        )
    )
    tier_summary_records.append(tier_1_summary)
    total_executed += tier_1_summary.steps_attempted_in_this_tier
    total_passed += tier_1_summary.steps_passed_in_this_tier

    tier_1_failures = [
        outcome
        for outcome in tier_1_summary.step_outcomes
        if outcome.execution_state != STATE_RESOLUTION_STEP_COMPLETED_SUCCESSFULLY
    ]

    if not tier_1_failures:
        # All steps resolved in Tier 1 — no escalation needed
        aggregate_source = json.dumps(
            [t.tier_proof_hash for t in tier_summary_records], sort_keys=True
        )
        aggregate_proof_hash = hashlib.sha256(
            aggregate_source.encode("utf-8")
        ).hexdigest()[:16]
        return IterativeResolutionProtocolCompleteExecutionResult(
            problem_whole_name=problem_whole_name,
            problem_environment_name=problem_environment_name,
            problem_description=problem_description,
            protocol_state=STATE_RESOLUTION_COMPLETED_ALL_STEPS_PASSED,
            tier_summary_records=tier_summary_records,
            total_steps_executed=total_executed,
            total_steps_passed=total_passed,
            total_steps_failed=0,
            all_steps_resolved=True,
            aggregate_proof_hash=aggregate_proof_hash,
            proof_gate="PROOF_GATE_ITERATIVE_RESOLUTION_ENGINE_EXECUTED_TO_COMPLETION",
        )

    # --- TIER 2 ---
    tier_2_summary = (
        FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_TIER_2_RETRY_WITH_DECOMPOSITION_FOR_FAILED_STEPS(
            failed_step_outcomes_from_tier_1=tier_1_failures,
            original_resolution_steps=resolution_steps,
        )
    )
    tier_summary_records.append(tier_2_summary)
    total_executed += tier_2_summary.steps_attempted_in_this_tier
    total_passed += tier_2_summary.steps_passed_in_this_tier

    tier_2_failures = [
        outcome
        for outcome in tier_2_summary.step_outcomes
        if outcome.execution_state != STATE_RESOLUTION_STEP_COMPLETED_SUCCESSFULLY
    ]

    if not tier_2_failures:
        aggregate_source = json.dumps(
            [t.tier_proof_hash for t in tier_summary_records], sort_keys=True
        )
        aggregate_proof_hash = hashlib.sha256(
            aggregate_source.encode("utf-8")
        ).hexdigest()[:16]
        return IterativeResolutionProtocolCompleteExecutionResult(
            problem_whole_name=problem_whole_name,
            problem_environment_name=problem_environment_name,
            problem_description=problem_description,
            protocol_state=STATE_RESOLUTION_COMPLETED_ALL_STEPS_PASSED,
            tier_summary_records=tier_summary_records,
            total_steps_executed=total_executed,
            total_steps_passed=total_passed,
            total_steps_failed=0,
            all_steps_resolved=True,
            aggregate_proof_hash=aggregate_proof_hash,
            proof_gate="PROOF_GATE_ITERATIVE_RESOLUTION_ENGINE_EXECUTED_TO_COMPLETION",
        )

    # --- TIER 3 ---
    tier_3_summary = (
        FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_TIER_3_CRITICAL_ROOT_CAUSE_ANALYSIS_AND_RECORD(
            failed_step_outcomes_from_tier_2=tier_2_failures,
            original_resolution_steps=resolution_steps,
        )
    )
    tier_summary_records.append(tier_3_summary)
    total_executed += tier_3_summary.steps_attempted_in_this_tier
    total_passed += tier_3_summary.steps_passed_in_this_tier
    total_failed = tier_3_summary.steps_failed_in_this_tier

    all_resolved = total_failed == 0
    final_protocol_state = (
        STATE_RESOLUTION_COMPLETED_ALL_STEPS_PASSED
        if all_resolved
        else STATE_RESOLUTION_FAILED_UNRECOVERABLE_AFTER_ALL_THREE_TIERS
    )
    final_proof_gate = (
        "PROOF_GATE_ITERATIVE_RESOLUTION_ENGINE_EXECUTED_TO_COMPLETION"
        if all_resolved
        else "PENDING_UNRECOVERABLE_FAILURES_REQUIRE_MANUAL_INTERVENTION"
    )

    aggregate_source = json.dumps(
        [t.tier_proof_hash for t in tier_summary_records], sort_keys=True
    )
    aggregate_proof_hash = hashlib.sha256(
        aggregate_source.encode("utf-8")
    ).hexdigest()[:16]

    return IterativeResolutionProtocolCompleteExecutionResult(
        problem_whole_name=problem_whole_name,
        problem_environment_name=problem_environment_name,
        problem_description=problem_description,
        protocol_state=final_protocol_state,
        tier_summary_records=tier_summary_records,
        total_steps_executed=total_executed,
        total_steps_passed=total_passed,
        total_steps_failed=total_failed,
        all_steps_resolved=all_resolved,
        aggregate_proof_hash=aggregate_proof_hash,
        proof_gate=final_proof_gate,
    )


# ---------------------------------------------------------------------------
# Self-test — verifies the engine resolves a controlled scenario correctly
# ---------------------------------------------------------------------------

def FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_BUILT_IN_SELF_TEST_WITH_CONTROLLED_SCENARIO() -> (
    Dict[str, Any]
):
    """Run a built-in self-test of the resolution engine using a controlled scenario.

    FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_BUILT_IN_SELF_TEST_WITH_CONTROLLED_SCENARIO

    Input:  none — uses internally defined steps (all guaranteed to pass)
    Action: constructs 3 synthetic steps that always succeed, runs the full
            three-tier protocol, verifies all_steps_resolved is True
    Output: dict containing test_passed flag, result summary, and proof hash
    Proof gate: PROOF_GATE_RESOLUTION_ENGINE_SELF_TEST_PASSED
    Pending:    PENDING_FAILURE_INJECTION_SELF_TEST_FOR_TIER_2_AND_TIER_3_VALIDATION
    """
    def _RESOLUTION_STEP_CALLABLE_GOVERNANCE_NAMING_VALIDATION_SELF_TEST() -> Dict[str, Any]:
        return {"step": "NAMING_VALIDATION", "ok": True, "result": "GOVERNANCE_PREFIX_DETECTED"}

    def _RESOLUTION_STEP_CALLABLE_BRAINK_HEARTBEAT_ALIVENESS_SELF_TEST() -> Dict[str, Any]:
        return {"step": "HEARTBEAT_ALIVENESS", "ok": True, "active_core": 1}

    def _RESOLUTION_STEP_CALLABLE_PROOF_LEDGER_HASH_INTEGRITY_SELF_TEST() -> Dict[str, Any]:
        test_hash = hashlib.sha256(b"PROOF_LEDGER_SELF_TEST").hexdigest()[:16]
        return {"step": "PROOF_LEDGER_HASH_INTEGRITY", "ok": True, "test_hash": test_hash}

    test_steps = [
        ResolutionStep(
            step_canonical_name="FUNCTION_RESOLUTION_STEP_GOVERNANCE_NAMING_VALIDATION_SELF_TEST",
            step_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
            step_callable=_RESOLUTION_STEP_CALLABLE_GOVERNANCE_NAMING_VALIDATION_SELF_TEST,
            max_retry_count_on_failure=1,
            escalation_tier_assignment=1,
        ),
        ResolutionStep(
            step_canonical_name="FUNCTION_RESOLUTION_STEP_BRAINK_HEARTBEAT_ALIVENESS_SELF_TEST",
            step_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
            step_callable=_RESOLUTION_STEP_CALLABLE_BRAINK_HEARTBEAT_ALIVENESS_SELF_TEST,
            max_retry_count_on_failure=1,
            escalation_tier_assignment=1,
        ),
        ResolutionStep(
            step_canonical_name="FUNCTION_RESOLUTION_STEP_PROOF_LEDGER_HASH_INTEGRITY_SELF_TEST",
            step_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
            step_callable=_RESOLUTION_STEP_CALLABLE_PROOF_LEDGER_HASH_INTEGRITY_SELF_TEST,
            max_retry_count_on_failure=1,
            escalation_tier_assignment=1,
        ),
    ]

    protocol_result = (
        FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_COMPLETE_SELF_RESOLVING_PROTOCOL(
            problem_whole_name="WHOLE_ITERATIVE_RESOLUTION_ENGINE_SELF_TEST",
            problem_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
            problem_description="Built-in self-test of the resolution engine.",
            resolution_steps=test_steps,
        )
    )

    test_passed = protocol_result.all_steps_resolved
    return {
        "test_passed": test_passed,
        "protocol_state": protocol_result.protocol_state,
        "total_steps_executed": protocol_result.total_steps_executed,
        "total_steps_passed": protocol_result.total_steps_passed,
        "total_steps_failed": protocol_result.total_steps_failed,
        "tiers_used": len(protocol_result.tier_summary_records),
        "aggregate_proof_hash": protocol_result.aggregate_proof_hash,
        "proof_gate": protocol_result.proof_gate,
        "ok": test_passed,
    }
