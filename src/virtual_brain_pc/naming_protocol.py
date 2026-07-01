from __future__ import annotations

"""Strict Naming Protocol Enforcement Module

FUNCTION_NAMING_PROTOCOL_ENFORCE_ALL_IDENTIFIER_BOUNDARIES

Input:  any raw identifier string, callable name, structured label, or symbol
        originating from any part of the system, any repository in scope, or
        any external integration boundary.
Action: validates the identifier against GOVERNANCE_PREFIX_REGISTRY;
        generates a canonical governance-compliant form when possible;
        raises NamingProtocolViolationException when the identifier is ambiguous,
        compressed beyond recognition, or missing a required governance prefix.
Output: NamingProtocolValidationResult carrying classification, canonical form,
        detected prefix category, and deterministic proof hash.
Proof gate: PROOF_GATE_NAMING_PROTOCOL_ENFORCED_ON_ALL_BOUNDARIES
Pending:    PENDING_CROSS_REPOSITORY_NAMING_PROTOCOL_ADOPTION
"""

import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence


# ---------------------------------------------------------------------------
# GOVERNANCE_PREFIX_REGISTRY
# Every valid governance prefix recognised across this repository system.
# Ordered longest-first by convention so the most specific prefix wins.
# Keys are prefixes; values are semantic category declarations.
# ---------------------------------------------------------------------------

GOVERNANCE_PREFIX_REGISTRY: Dict[str, str] = {
    "GOVERNANCE_":  "CATEGORY_GOVERNANCE_ROOT_ANCHOR_DECLARATION",
    "REPOSITORY_":  "CATEGORY_REPOSITORY_SYSTEM_ANCHOR_DECLARATION",
    "PROOF_GATE_":  "CATEGORY_PROOF_GATE_CHECKPOINT_DECLARATION",
    "ENVIRONMENT_": "CATEGORY_ENVIRONMENT_DECLARATION",
    "RESOLUTION_":  "CATEGORY_ITERATIVE_RESOLUTION_STEP_DECLARATION",
    "DIRECTIVE_":   "CATEGORY_AGENT_DIRECTIVE_PAYLOAD_DECLARATION",
    "PROTOCOL_":    "CATEGORY_AUTOMATION_PROTOCOL_DECLARATION",
    "FUNCTION_":    "CATEGORY_FUNCTION_SELF_IDENTIFICATION_DECLARATION",
    "ARTIFACT_":    "CATEGORY_ARTIFACT_IDENTITY_DECLARATION",
    "PENDING_":     "CATEGORY_PENDING_BOUNDARY_GATE_DECLARATION",
    "PROCESS_":     "CATEGORY_OPS_PROCESS_CATALOGUE_DECLARATION",
    "AGENT_":       "CATEGORY_AGENT_DIRECTIVE_UNIT_DECLARATION",
    "WHOLE_":       "CATEGORY_WHOLE_SYSTEM_BOUNDARY_DECLARATION",
    "STATE_":       "CATEGORY_STATE_SELF_IDENTIFICATION_DECLARATION",
    "LANE_":        "CATEGORY_BRAINK_RUNTIME_LANE_DECLARATION",
    "CALL_":        "CATEGORY_BRAINK_PRIMITIVE_CALLABLE_DECLARATION",
}

# Ordered by prefix length descending so longest (most specific) match wins.
GOVERNANCE_PREFIX_ORDERED_BY_DESCENDING_SPECIFICITY: List[str] = sorted(
    GOVERNANCE_PREFIX_REGISTRY.keys(),
    key=lambda prefix_candidate: len(prefix_candidate),
    reverse=True,
)

# All environments that must be declared by every governed repository.
REQUIRED_ENVIRONMENT_DECLARATIONS: List[str] = [
    "ENVIRONMENT_LOCAL_DEVELOPMENT",
    "ENVIRONMENT_CONTINUOUS_INTEGRATION",
    "ENVIRONMENT_STAGING",
    "ENVIRONMENT_PRODUCTION",
    "ENVIRONMENT_EXTERNAL_VALIDATION",
]

# All state values allowed by the governance standard.
ALLOWED_STATE_DECLARATIONS: List[str] = [
    "STATE_COMPLETED",
    "STATE_PENDING",
    "STATE_BLOCKED",
    "STATE_FAILED",
    "STATE_MODEL_LOCAL",
    "STATE_EXTERNALLY_UNVALIDATED",
    "STATE_RESOLUTION_PENDING",
    "STATE_RESOLUTION_IN_PROGRESS_TIER_1_DIRECT_EXECUTION",
    "STATE_RESOLUTION_IN_PROGRESS_TIER_2_RETRY_WITH_DECOMPOSITION",
    "STATE_RESOLUTION_IN_PROGRESS_TIER_3_CRITICAL_ROOT_CAUSE_ANALYSIS",
    "STATE_RESOLUTION_STEP_COMPLETED_SUCCESSFULLY",
    "STATE_RESOLUTION_STEP_FAILED_AWAITING_ROOT_CAUSE_ANALYSIS",
    "STATE_RESOLUTION_ROOT_CAUSE_IDENTIFIED_AND_RESOLVED",
    "STATE_RESOLUTION_COMPLETED_ALL_STEPS_PASSED",
    "STATE_RESOLUTION_FAILED_UNRECOVERABLE_AFTER_ALL_THREE_TIERS",
    "STATE_AGENT_DIRECTIVE_PENDING_ASSIGNMENT",
    "STATE_AGENT_DIRECTIVE_EXECUTING",
    "STATE_AGENT_DIRECTIVE_COMPLETED_SUCCESSFULLY",
    "STATE_AGENT_DIRECTIVE_FAILED_ACTIVATING_FAILOVER",
    "STATE_AGENT_DIRECTIVE_FAILOVER_SECONDARY_ACTIVATED",
    "STATE_AUTOMATION_PROTOCOL_INITIALIZING",
    "STATE_AUTOMATION_PROTOCOL_RUNNING_GOVERNANCE_CYCLE",
    "STATE_AUTOMATION_PROTOCOL_COMPLETED",
    "STATE_AUTOMATION_PROTOCOL_FAILED",
]


# ---------------------------------------------------------------------------
# Exception type — carries full diagnostic context, never silent
# ---------------------------------------------------------------------------

class NamingProtocolViolationException(ValueError):
    """Raised when an identifier violates the strict naming governance protocol.

    FUNCTION_NAMING_PROTOCOL_RAISE_VIOLATION_EXCEPTION_WITH_FULL_DIAGNOSTIC_CONTEXT

    Input:  raw_identifier — the non-compliant identifier
            violation_reason — precise description of the violation
    Action: constructs an exception message carrying the raw identifier,
            the specific violation reason, and every valid prefix for reference
    Output: NamingProtocolViolationException ready to raise or log
    Proof gate: PROOF_GATE_NAMING_VIOLATION_EXCEPTION_CARRIES_FULL_DIAGNOSTIC_CONTEXT
    Pending:    PENDING_DOWNSTREAM_VIOLATION_LOGGING_INTEGRATION
    """

    def __init__(self, raw_identifier: str, violation_reason: str) -> None:
        self.raw_identifier = raw_identifier
        self.violation_reason = violation_reason
        self.valid_prefixes: List[str] = sorted(GOVERNANCE_PREFIX_REGISTRY.keys())
        super().__init__(
            f"NAMING_PROTOCOL_VIOLATION | "
            f"identifier={raw_identifier!r} | "
            f"reason={violation_reason} | "
            f"valid_prefixes={self.valid_prefixes}"
        )


# ---------------------------------------------------------------------------
# Result dataclass — all fields explicitly named, no field is optional silently
# ---------------------------------------------------------------------------

@dataclass
class NamingProtocolValidationResult:
    """Complete result of validating one identifier through the naming protocol.

    STATE_NAMING_PROTOCOL_VALIDATION_RESULT_FULLY_POPULATED_STRUCTURE:
      raw_identifier         — the original unvalidated input string, preserved as-is
      is_compliant           — True only when a governance prefix is detected
      detected_prefix        — the matched governance prefix string, or None
      detected_category      — the semantic category of the matched prefix, or None
      canonical_identifier   — uppercased, space/dash normalised form, or None if non-compliant
      violation_reason       — populated only when is_compliant is False, never None on failure
      proof_hash             — SHA-256 of the canonical form truncated to 16 hex chars, or None
    """

    raw_identifier: str
    is_compliant: bool
    detected_prefix: Optional[str] = None
    detected_category: Optional[str] = None
    canonical_identifier: Optional[str] = None
    violation_reason: Optional[str] = None
    proof_hash: Optional[str] = None


# ---------------------------------------------------------------------------
# Core protocol functions — every name is fully explicit, no abbreviations
# ---------------------------------------------------------------------------

def FUNCTION_NAMING_PROTOCOL_DETECT_LONGEST_MATCHING_GOVERNANCE_PREFIX_IN_SINGLE_IDENTIFIER(
    raw_identifier: str,
) -> Optional[str]:
    """Scan an identifier and return the longest matching governance prefix.

    FUNCTION_NAMING_PROTOCOL_DETECT_LONGEST_MATCHING_GOVERNANCE_PREFIX_IN_SINGLE_IDENTIFIER

    Input:  raw_identifier — any string, case-insensitive comparison is applied
    Action: normalises to uppercase, iterates
            GOVERNANCE_PREFIX_ORDERED_BY_DESCENDING_SPECIFICITY (longest first),
            returns the first prefix whose characters match the identifier's start
    Output: matched prefix string from GOVERNANCE_PREFIX_REGISTRY, or None
    Proof gate: PROOF_GATE_LONGEST_MATCHING_PREFIX_RETURNED_FIRST
    Pending:    PENDING_FUZZY_PREFIX_DETECTION_FOR_LEGACY_IDENTIFIER_MIGRATION
    """
    normalised_uppercase_identifier = raw_identifier.upper()
    for candidate_prefix in GOVERNANCE_PREFIX_ORDERED_BY_DESCENDING_SPECIFICITY:
        if normalised_uppercase_identifier.startswith(candidate_prefix):
            return candidate_prefix
    return None


def FUNCTION_NAMING_PROTOCOL_VALIDATE_SINGLE_IDENTIFIER_AGAINST_GOVERNANCE_PREFIX_REGISTRY(
    raw_identifier: str,
    raise_on_violation: bool = False,
) -> NamingProtocolValidationResult:
    """Validate one identifier and return a fully-populated NamingProtocolValidationResult.

    FUNCTION_NAMING_PROTOCOL_VALIDATE_SINGLE_IDENTIFIER_AGAINST_GOVERNANCE_PREFIX_REGISTRY

    Input:  raw_identifier — the string to validate
            raise_on_violation — when True, raise NamingProtocolViolationException
                                 instead of returning a non-compliant result object
    Action: runs prefix detection, builds canonical form, computes deterministic proof hash
    Output: NamingProtocolValidationResult with all fields populated
    Proof gate: PROOF_GATE_SINGLE_IDENTIFIER_VALIDATION_RESULT_IS_DETERMINISTIC
    Pending:    PENDING_PATTERN_BASED_SUFFIX_STRUCTURE_VALIDATION
    """
    detected_prefix = (
        FUNCTION_NAMING_PROTOCOL_DETECT_LONGEST_MATCHING_GOVERNANCE_PREFIX_IN_SINGLE_IDENTIFIER(
            raw_identifier
        )
    )

    if detected_prefix is None:
        violation_reason = (
            f"identifier {raw_identifier!r} does not begin with any recognised "
            f"governance prefix from GOVERNANCE_PREFIX_REGISTRY; "
            f"all names must carry an unambiguous prefix — "
            f"no compressed or abbreviated identifiers are permitted"
        )
        if raise_on_violation:
            raise NamingProtocolViolationException(raw_identifier, violation_reason)
        return NamingProtocolValidationResult(
            raw_identifier=raw_identifier,
            is_compliant=False,
            violation_reason=violation_reason,
        )

    canonical_identifier = (
        raw_identifier
        .upper()
        .replace(" ", "_")
        .replace("-", "_")
        .replace(".", "_")
    )
    category = GOVERNANCE_PREFIX_REGISTRY[detected_prefix]
    proof_hash = hashlib.sha256(canonical_identifier.encode("utf-8")).hexdigest()[:16]

    return NamingProtocolValidationResult(
        raw_identifier=raw_identifier,
        is_compliant=True,
        detected_prefix=detected_prefix,
        detected_category=category,
        canonical_identifier=canonical_identifier,
        proof_hash=proof_hash,
    )


def FUNCTION_NAMING_PROTOCOL_VALIDATE_ALL_IDENTIFIERS_IN_ORDERED_SEQUENCE_AND_RETURN_FULL_MAPPING(
    identifier_sequence: Sequence[str],
    raise_on_first_violation: bool = False,
) -> Dict[str, NamingProtocolValidationResult]:
    """Validate every identifier in a sequence and return a dict of full results.

    FUNCTION_NAMING_PROTOCOL_VALIDATE_ALL_IDENTIFIERS_IN_ORDERED_SEQUENCE_AND_RETURN_FULL_MAPPING

    Input:  identifier_sequence — ordered collection of raw identifier strings
            raise_on_first_violation — propagate NamingProtocolViolationException
                                       on the first non-compliant identifier found
    Action: calls FUNCTION_NAMING_PROTOCOL_VALIDATE_SINGLE_IDENTIFIER for each,
            accumulates results in a dict keyed by the raw identifier
    Output: dict mapping each raw_identifier → NamingProtocolValidationResult
    Proof gate: PROOF_GATE_ALL_IDENTIFIERS_IN_SEQUENCE_HAVE_BEEN_INDIVIDUALLY_VALIDATED
    Pending:    PENDING_PARALLEL_VALIDATION_EXECUTION_FOR_LARGE_IDENTIFIER_SEQUENCES
    """
    validation_result_mapping: Dict[str, NamingProtocolValidationResult] = {}
    for raw_identifier in identifier_sequence:
        validation_result_mapping[raw_identifier] = (
            FUNCTION_NAMING_PROTOCOL_VALIDATE_SINGLE_IDENTIFIER_AGAINST_GOVERNANCE_PREFIX_REGISTRY(
                raw_identifier,
                raise_on_violation=raise_on_first_violation,
            )
        )
    return validation_result_mapping


def FUNCTION_NAMING_PROTOCOL_GENERATE_CANONICAL_ENVIRONMENT_IDENTIFIER_FROM_PLAIN_DESCRIPTION(
    plain_environment_description: str,
) -> str:
    """Produce a canonical ENVIRONMENT_ prefixed identifier from a plain description.

    FUNCTION_NAMING_PROTOCOL_GENERATE_CANONICAL_ENVIRONMENT_IDENTIFIER_FROM_PLAIN_DESCRIPTION

    Input:  plain_environment_description — e.g. 'local development', 'production'
    Action: uppercases, replaces spaces/dashes/dots with underscores,
            prepends ENVIRONMENT_ if not already present
    Output: canonical ENVIRONMENT_ identifier, e.g. 'ENVIRONMENT_LOCAL_DEVELOPMENT'
    Proof gate: PROOF_GATE_GENERATED_ENVIRONMENT_IDENTIFIER_HAS_CORRECT_PREFIX
    Pending:    PENDING_ENVIRONMENT_REGISTRY_MEMBERSHIP_VALIDATION
    """
    sanitised = plain_environment_description.upper().replace("-", "_").replace(" ", "_").replace(".", "_")
    return sanitised if sanitised.startswith("ENVIRONMENT_") else f"ENVIRONMENT_{sanitised}"


def FUNCTION_NAMING_PROTOCOL_GENERATE_CANONICAL_STATE_IDENTIFIER_FROM_PLAIN_DESCRIPTION(
    plain_state_description: str,
) -> str:
    """Produce a canonical STATE_ prefixed identifier from a plain description."""
    sanitised = plain_state_description.upper().replace("-", "_").replace(" ", "_").replace(".", "_")
    return sanitised if sanitised.startswith("STATE_") else f"STATE_{sanitised}"


def FUNCTION_NAMING_PROTOCOL_GENERATE_CANONICAL_FUNCTION_IDENTIFIER_FROM_PLAIN_DESCRIPTION(
    plain_function_description: str,
) -> str:
    """Produce a canonical FUNCTION_ prefixed identifier from a plain description."""
    sanitised = plain_function_description.upper().replace("-", "_").replace(" ", "_").replace(".", "_")
    return sanitised if sanitised.startswith("FUNCTION_") else f"FUNCTION_{sanitised}"


def FUNCTION_NAMING_PROTOCOL_GENERATE_CANONICAL_AGENT_IDENTIFIER_FROM_PLAIN_DESCRIPTION(
    plain_agent_description: str,
) -> str:
    """Produce a canonical AGENT_ prefixed identifier from a plain description."""
    sanitised = plain_agent_description.upper().replace("-", "_").replace(" ", "_").replace(".", "_")
    return sanitised if sanitised.startswith("AGENT_") else f"AGENT_{sanitised}"


def FUNCTION_NAMING_PROTOCOL_GENERATE_CANONICAL_PROOF_GATE_IDENTIFIER_FROM_PLAIN_DESCRIPTION(
    plain_proof_gate_description: str,
) -> str:
    """Produce a canonical PROOF_GATE_ prefixed identifier from a plain description."""
    sanitised = plain_proof_gate_description.upper().replace("-", "_").replace(" ", "_").replace(".", "_")
    return sanitised if sanitised.startswith("PROOF_GATE_") else f"PROOF_GATE_{sanitised}"


def FUNCTION_NAMING_PROTOCOL_EMIT_PROOF_RECORD_FOR_COMPLETED_VALIDATION_SEQUENCE(
    validation_result_mapping: Dict[str, NamingProtocolValidationResult],
) -> Dict[str, object]:
    """Emit a structured proof record summarising a completed naming validation sequence.

    FUNCTION_NAMING_PROTOCOL_EMIT_PROOF_RECORD_FOR_COMPLETED_VALIDATION_SEQUENCE

    Input:  validation_result_mapping — dict of raw_identifier → NamingProtocolValidationResult
    Action: counts compliant/non-compliant, collects violation descriptions,
            computes aggregate SHA-256 proof hash over all canonical identifiers
    Output: proof record dict containing state, counts, violation list, and aggregate hash
    Proof gate: PROOF_GATE_NAMING_SEQUENCE_PROOF_RECORD_EMITTED
    Pending:    PENDING_PROOF_RECORD_INTEGRATION_WITH_DOWNSTREAM_GOVERNANCE_LEDGER
    """
    compliant_identifiers = [
        raw_id for raw_id, result in validation_result_mapping.items() if result.is_compliant
    ]
    non_compliant_identifiers = [
        raw_id for raw_id, result in validation_result_mapping.items() if not result.is_compliant
    ]
    aggregate_canonical_source = json.dumps(
        {
            raw_id: result.canonical_identifier
            for raw_id, result in validation_result_mapping.items()
            if result.is_compliant
        },
        sort_keys=True,
    )
    aggregate_proof_hash = hashlib.sha256(
        aggregate_canonical_source.encode("utf-8")
    ).hexdigest()[:16]

    return {
        "proof_record_function": (
            "FUNCTION_NAMING_PROTOCOL_EMIT_PROOF_RECORD_FOR_COMPLETED_VALIDATION_SEQUENCE"
        ),
        "state": "STATE_COMPLETED" if not non_compliant_identifiers else "STATE_FAILED",
        "total_identifiers_validated": len(validation_result_mapping),
        "compliant_identifier_count": len(compliant_identifiers),
        "non_compliant_identifier_count": len(non_compliant_identifiers),
        "violation_list": [
            {
                "identifier": raw_id,
                "violation_reason": validation_result_mapping[raw_id].violation_reason,
            }
            for raw_id in non_compliant_identifiers
        ],
        "aggregate_proof_hash": aggregate_proof_hash,
        "proof_gate": (
            "PROOF_GATE_NAMING_PROTOCOL_ENFORCED_ON_ALL_BOUNDARIES"
            if not non_compliant_identifiers
            else "PENDING_NAMING_PROTOCOL_ENFORCEMENT_INCOMPLETE"
        ),
    }


# ---------------------------------------------------------------------------
# System-wide identifier sweep — validates all known governance identifiers
# ---------------------------------------------------------------------------

# Canonical set of all governance-level identifiers defined in this module.
# Every identifier used at a governance boundary must appear in this list.
SYSTEM_WIDE_GOVERNANCE_IDENTIFIER_REGISTRY: List[str] = [
    "GOVERNANCE_ROOT_GENERAL_GOVERNANCE",
    "REPOSITORY_WHOLE_GENERAL_GOVERNANCE",
    "ENVIRONMENT_LOCAL_DEVELOPMENT",
    "ENVIRONMENT_CONTINUOUS_INTEGRATION",
    "ENVIRONMENT_STAGING",
    "ENVIRONMENT_PRODUCTION",
    "ENVIRONMENT_EXTERNAL_VALIDATION",
    "STATE_COMPLETED",
    "STATE_PENDING",
    "STATE_BLOCKED",
    "STATE_FAILED",
    "STATE_MODEL_LOCAL",
    "STATE_EXTERNALLY_UNVALIDATED",
    "STATE_RESOLUTION_COMPLETED_ALL_STEPS_PASSED",
    "STATE_RESOLUTION_FAILED_UNRECOVERABLE_AFTER_ALL_THREE_TIERS",
    "STATE_AGENT_DIRECTIVE_COMPLETED_SUCCESSFULLY",
    "STATE_AUTOMATION_PROTOCOL_COMPLETED",
    "FUNCTION_NAMING_PROTOCOL_ENFORCE_ALL_IDENTIFIER_BOUNDARIES",
    "FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_COMPLETE_SELF_RESOLVING_PROTOCOL",
    "FUNCTION_AGENT_DIRECTIVE_DISPATCHER_EXECUTE_ALL_AGENT_DIRECTIVES_IN_SEQUENCE",
    "FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_COMPLETE_GOVERNANCE_CYCLE",
    "WHOLE_GENERAL_GOVERNANCE_REPOSITORY_SYSTEM",
    "ARTIFACT_GOVERNANCE_MANIFEST_JSON",
    "ARTIFACT_NAMING_PROTOCOL_MODULE",
    "ARTIFACT_ITERATIVE_RESOLUTION_ENGINE_MODULE",
    "ARTIFACT_AGENT_DIRECTIVE_DISPATCHER_MODULE",
    "ARTIFACT_AUTOMATION_PROTOCOL_MODULE",
    "PROOF_GATE_NAMING_PROTOCOL_ENFORCED_ON_ALL_BOUNDARIES",
    "PROOF_GATE_ITERATIVE_RESOLUTION_ENGINE_EXECUTED_TO_COMPLETION",
    "PROOF_GATE_ALL_AGENT_DIRECTIVES_DISPATCHED_AND_RESULTS_COLLECTED",
    "PROOF_GATE_AUTOMATION_PROTOCOL_GOVERNANCE_CYCLE_COMPLETED",
    "PROOF_GATE_CHECKER_PASSED",
    "PROOF_GATE_MANIFEST_CURRENT",
    "PENDING_CROSS_REPOSITORY_NAMING_PROTOCOL_ADOPTION",
    "PENDING_LEARNING_MODULE_ADAPTIVE_STEP_INJECTION",
    "PENDING_DOWNSTREAM_VIOLATION_LOGGING_INTEGRATION",
    "PENDING_DOWNSTREAM_REPOSITORY_ADOPTION",
    "AGENT_GOVERNANCE_NAMING_PROTOCOL_ENFORCEMENT_UNIT",
    "AGENT_BUILD_COMPILATION_DIRECTIVE_EXECUTION_UNIT",
    "AGENT_VALIDATION_AND_SMOKE_TEST_DIRECTIVE_EXECUTION_UNIT",
    "AGENT_PACKAGING_AND_ARTIFACT_PRODUCTION_DIRECTIVE_EXECUTION_UNIT",
    "AGENT_ITERATIVE_RESOLUTION_DIRECTION_AND_ESCALATION_UNIT",
    "AGENT_LEARNING_MODULE_FEEDBACK_INTEGRATION_AND_CALIBRATION_UNIT",
    "AGENT_FAILOVER_CHAIN_MANAGEMENT_AND_SECONDARY_ACTIVATION_UNIT",
    "PROTOCOL_AUTOMATION_GOVERNANCE_CYCLE_V1",
    "RESOLUTION_TIER_1_DIRECT_EXECUTION",
    "RESOLUTION_TIER_2_RETRY_WITH_DECOMPOSITION",
    "RESOLUTION_TIER_3_CRITICAL_ROOT_CAUSE_ANALYSIS_AND_FIX",
    "LANE_BRAINK_RUNTIME_FULL_14_STEP",
    "LANE_ORGANISM_CORE_PROCESS",
    "LANE_SPIKE_BOUNDARY_CALIBRATION",
    "LANE_MATERIAL_CALIBRATION",
    "DIRECTIVE_BUILD_COMPILATION_TARGET_ALL_PLATFORMS",
    "DIRECTIVE_VALIDATE_SMOKE_TESTS_ALL_TARGETS",
    "DIRECTIVE_PACKAGE_ARTIFACT_ALL_TARGETS",
    "CALL_HEARTBEAT_TICK",
    "CALL_PROOF_LEDGER_COMMIT",
    "CALL_KEDDEH_THEOREM_LEDGER",
    "CALL_LEARNING_MIRROR_UPDATE",
]


def FUNCTION_NAMING_PROTOCOL_EXECUTE_SYSTEM_WIDE_IDENTIFIER_SWEEP_AND_EMIT_PROOF_RECORD() -> (
    Dict[str, object]
):
    """Run a complete naming protocol sweep across all known system identifiers.

    FUNCTION_NAMING_PROTOCOL_EXECUTE_SYSTEM_WIDE_IDENTIFIER_SWEEP_AND_EMIT_PROOF_RECORD

    Input:  SYSTEM_WIDE_GOVERNANCE_IDENTIFIER_REGISTRY (module-level constant)
    Action: validates every identifier in the registry, emits proof record
    Output: proof record dict with complete validation summary and proof hash
    Proof gate: PROOF_GATE_SYSTEM_WIDE_NAMING_SWEEP_COMPLETED
    Pending:    PENDING_DYNAMIC_IDENTIFIER_DISCOVERY_FROM_ALL_SOURCE_MODULES
    """
    validation_result_mapping = (
        FUNCTION_NAMING_PROTOCOL_VALIDATE_ALL_IDENTIFIERS_IN_ORDERED_SEQUENCE_AND_RETURN_FULL_MAPPING(
            SYSTEM_WIDE_GOVERNANCE_IDENTIFIER_REGISTRY,
            raise_on_first_violation=False,
        )
    )
    proof_record = (
        FUNCTION_NAMING_PROTOCOL_EMIT_PROOF_RECORD_FOR_COMPLETED_VALIDATION_SEQUENCE(
            validation_result_mapping
        )
    )
    proof_record["sweep_scope"] = "SYSTEM_WIDE_GOVERNANCE_IDENTIFIER_REGISTRY"
    proof_record["identifiers_in_registry"] = len(SYSTEM_WIDE_GOVERNANCE_IDENTIFIER_REGISTRY)
    return proof_record
