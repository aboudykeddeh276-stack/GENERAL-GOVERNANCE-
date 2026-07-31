from virtual_brain_pc.cli import (
    _braink_run,
    _build,
    _build_all,
    _material_calibrate,
    _ops_run,
    _organism_run,
    _run_virtual_machine,
    _spike_calibrate,
    _automation_protocol_run,
)
from virtual_brain_pc.naming_protocol import (
    FUNCTION_NAMING_PROTOCOL_VALIDATE_SINGLE_IDENTIFIER_AGAINST_GOVERNANCE_PREFIX_REGISTRY,
    FUNCTION_NAMING_PROTOCOL_VALIDATE_ALL_IDENTIFIERS_IN_ORDERED_SEQUENCE_AND_RETURN_FULL_MAPPING,
    FUNCTION_NAMING_PROTOCOL_GENERATE_CANONICAL_ENVIRONMENT_IDENTIFIER_FROM_PLAIN_DESCRIPTION,
    FUNCTION_NAMING_PROTOCOL_GENERATE_CANONICAL_STATE_IDENTIFIER_FROM_PLAIN_DESCRIPTION,
    FUNCTION_NAMING_PROTOCOL_GENERATE_CANONICAL_FUNCTION_IDENTIFIER_FROM_PLAIN_DESCRIPTION,
    FUNCTION_NAMING_PROTOCOL_EMIT_PROOF_RECORD_FOR_COMPLETED_VALIDATION_SEQUENCE,
    FUNCTION_NAMING_PROTOCOL_EXECUTE_SYSTEM_WIDE_IDENTIFIER_SWEEP_AND_EMIT_PROOF_RECORD,
    NamingProtocolViolationException,
    GOVERNANCE_PREFIX_REGISTRY,
)
from virtual_brain_pc.iterative_resolution_engine import (
    FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_BUILT_IN_SELF_TEST_WITH_CONTROLLED_SCENARIO,
    FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_COMPLETE_SELF_RESOLVING_PROTOCOL,
    ResolutionStep,
    STATE_RESOLUTION_COMPLETED_ALL_STEPS_PASSED,
)
from virtual_brain_pc.agent_directive_dispatcher import (
    FUNCTION_AGENT_DIRECTIVE_DISPATCHER_BUILD_STANDARD_DIRECTIVE_ASSIGNMENTS_FOR_ALL_SEVEN_AGENTS,
    FUNCTION_AGENT_DIRECTIVE_DISPATCHER_EXECUTE_ALL_AGENT_DIRECTIVES_IN_SEQUENCE,
    AGENT_DIRECTIVE_UNIT_REGISTRY,
    ALL_AGENT_CANONICAL_NAMES_IN_DISPATCH_ORDER,
)
from virtual_brain_pc.automation_protocol import (
    FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_COMPLETE_GOVERNANCE_CYCLE,
    FUNCTION_AUTOMATION_PROTOCOL_SERIALIZE_GOVERNANCE_CYCLE_RESULT_TO_DICT,
    STATE_AUTOMATION_PROTOCOL_COMPLETED,
)
import pytest


def test_vm_smoke() -> None:
    result = _run_virtual_machine(cycles=10)
    assert result["vm_snapshot"]["halted"] is True
    assert result["vm_snapshot"]["A"] == 1


def test_single_target_pipeline() -> None:
    result = _build("linux")
    assert result["target"] == "linux"
    assert len(result["reports"]) == 3


def test_matrix_pipeline() -> None:
    result = _build_all()
    assert len(result["matrix"]) == 3


def test_material_calibration_near_failure_band() -> None:
    result = _material_calibrate(
        material="steel_beam",
        environment="test_lab",
        whole_identity="beam_integrity",
        force=97.0,
        lower=-100.0,
        upper=100.0,
        force_kind="stress",
    )
    assert result["failure_event"]["near_boundary_band"] == 2.97
    assert result["failure_event"]["achieved_boundary"] is None


def test_material_calibration_boundary_achievement() -> None:
    result = _material_calibrate(
        material="glass_pane",
        environment="thermal_ramp",
        whole_identity="pane_continuity",
        force=120.0,
        lower=-100.0,
        upper=100.0,
        force_kind="thermal_stress",
    )
    assert result["failure_event"]["achieved_boundary"] == 3
    assert result["proof_ledger"]["proof_status"] == "committed"


def test_spike_calibration_runtime_existence() -> None:
    result = _spike_calibrate(
        spike_kind="temperature",
        observed_value=97.0,
        safe_boundary=90.0,
        failure_boundary=100.0,
        environment="lab",
        target_system="cpu_runtime",
    )
    assert result["classification"]["spike_type"] == "RUNTIME_EXISTENCE_SPIKE"
    assert result["classification"]["near_boundary_297"] is True
    assert result["classification"]["boundary_3_achieved"] is False


def test_spike_calibration_detrimental_failure() -> None:
    result = _spike_calibrate(
        spike_kind="voltage",
        observed_value=105.0,
        safe_boundary=90.0,
        failure_boundary=100.0,
        environment="power_rail",
        target_system="drive_controller",
    )
    assert result["classification"]["spike_type"] == "DETRIMENTAL_FAILURE_SPIKE"
    assert result["classification"]["boundary_3_achieved"] is True
    assert result["proof_ledger"]["proof_status"] == "committed"


def test_braink_run_full_lane() -> None:
    result = _braink_run(
        tick_id=1,
        system="cpu_runtime",
        environment="production",
        spike_kind="temperature",
        observed_value=97.0,
        safe_boundary=90.0,
        failure_boundary=100.0,
    )
    assert len(result["runtime_lane"]) == 14
    assert result["whole_state_preserved"] is True
    assert result["proof_ledger"]["proof_status"] == "committed"
    assert result["output_state"] == 2


def test_organism_run_core_process() -> None:
    result = _organism_run(
        tick_id=1,
        payload={"signal_strength": 0.88, "env": "production", "load": 0.72},
    )
    assert result["organism_alive"] is True
    assert result["learning_committed"] is True
    assert result["theorem_compliant"] is True
    assert result["output_state"] == 2


def test_ops_run_all_lanes_pass() -> None:
    result = _ops_run(tick_id=0)
    summary = result["summary"]
    assert summary["all_ok"] is True, f"Failed lanes: {summary['failed']}"
    assert summary["lanes_passed"] == summary["lanes_total"]
    assert summary["lanes_failed"] == 0
    assert "ops_hash" in summary


def test_ops_run_lane_structure() -> None:
    result = _ops_run(tick_id=5)
    lanes = result["lanes"]
    expected_lanes = {
        "vm_brain", "braink_runtime", "organism_core",
        "spike_calibration", "material_calibration",
        "zero_classifier", "build_matrix", "registry_check",
        "naming_protocol", "iterative_resolution", "agent_dispatcher",
        "automation_protocol",
    }
    assert set(lanes.keys()) == expected_lanes
    for name, lane in lanes.items():
        assert lane["ok"] is True, f"Lane {name!r} reported ok=False"


# ---------------------------------------------------------------------------
# Naming Protocol tests
# ---------------------------------------------------------------------------

def test_naming_protocol_valid_identifier_returns_compliant_result() -> None:
    result = FUNCTION_NAMING_PROTOCOL_VALIDATE_SINGLE_IDENTIFIER_AGAINST_GOVERNANCE_PREFIX_REGISTRY(
        "FUNCTION_TEST_VALIDATION_IDENTIFIER"
    )
    assert result.is_compliant is True
    assert result.detected_prefix == "FUNCTION_"
    assert result.canonical_identifier == "FUNCTION_TEST_VALIDATION_IDENTIFIER"
    assert result.proof_hash is not None


def test_naming_protocol_invalid_identifier_returns_non_compliant_result() -> None:
    result = FUNCTION_NAMING_PROTOCOL_VALIDATE_SINGLE_IDENTIFIER_AGAINST_GOVERNANCE_PREFIX_REGISTRY(
        "compressed_name"
    )
    assert result.is_compliant is False
    assert result.violation_reason is not None
    assert result.canonical_identifier is None


def test_naming_protocol_raise_on_violation_raises_exception() -> None:
    with pytest.raises(NamingProtocolViolationException):
        FUNCTION_NAMING_PROTOCOL_VALIDATE_SINGLE_IDENTIFIER_AGAINST_GOVERNANCE_PREFIX_REGISTRY(
            "bad_name_no_prefix",
            raise_on_violation=True,
        )


def test_naming_protocol_validate_sequence_returns_full_mapping() -> None:
    identifiers = [
        "ENVIRONMENT_LOCAL_DEVELOPMENT",
        "STATE_COMPLETED",
        "FUNCTION_VALIDATE_GOVERNANCE",
        "AGENT_BUILD_UNIT",
        "PROOF_GATE_CHECKER_PASSED",
        "PENDING_ADOPTION",
        "WHOLE_SYSTEM",
    ]
    mapping = (
        FUNCTION_NAMING_PROTOCOL_VALIDATE_ALL_IDENTIFIERS_IN_ORDERED_SEQUENCE_AND_RETURN_FULL_MAPPING(
            identifiers
        )
    )
    assert len(mapping) == len(identifiers)
    for raw_id, result in mapping.items():
        assert result.is_compliant is True, f"Expected {raw_id!r} to be compliant"


def test_naming_protocol_generate_canonical_environment_identifier() -> None:
    canonical = (
        FUNCTION_NAMING_PROTOCOL_GENERATE_CANONICAL_ENVIRONMENT_IDENTIFIER_FROM_PLAIN_DESCRIPTION(
            "local development"
        )
    )
    assert canonical == "ENVIRONMENT_LOCAL_DEVELOPMENT"


def test_naming_protocol_generate_canonical_state_identifier() -> None:
    canonical = (
        FUNCTION_NAMING_PROTOCOL_GENERATE_CANONICAL_STATE_IDENTIFIER_FROM_PLAIN_DESCRIPTION(
            "completed"
        )
    )
    assert canonical == "STATE_COMPLETED"


def test_naming_protocol_generate_canonical_function_identifier() -> None:
    canonical = (
        FUNCTION_NAMING_PROTOCOL_GENERATE_CANONICAL_FUNCTION_IDENTIFIER_FROM_PLAIN_DESCRIPTION(
            "validate governance"
        )
    )
    assert canonical == "FUNCTION_VALIDATE_GOVERNANCE"


def test_naming_protocol_proof_record_all_compliant() -> None:
    identifiers = ["FUNCTION_TEST", "STATE_OK", "AGENT_UNIT"]
    mapping = (
        FUNCTION_NAMING_PROTOCOL_VALIDATE_ALL_IDENTIFIERS_IN_ORDERED_SEQUENCE_AND_RETURN_FULL_MAPPING(
            identifiers
        )
    )
    proof_record = FUNCTION_NAMING_PROTOCOL_EMIT_PROOF_RECORD_FOR_COMPLETED_VALIDATION_SEQUENCE(
        mapping
    )
    assert proof_record["state"] == "STATE_COMPLETED"
    assert proof_record["non_compliant_identifier_count"] == 0
    assert proof_record["proof_gate"] == "PROOF_GATE_NAMING_PROTOCOL_ENFORCED_ON_ALL_BOUNDARIES"


def test_naming_protocol_proof_record_with_violation() -> None:
    identifiers = ["FUNCTION_VALID", "bad_name"]
    mapping = (
        FUNCTION_NAMING_PROTOCOL_VALIDATE_ALL_IDENTIFIERS_IN_ORDERED_SEQUENCE_AND_RETURN_FULL_MAPPING(
            identifiers
        )
    )
    proof_record = FUNCTION_NAMING_PROTOCOL_EMIT_PROOF_RECORD_FOR_COMPLETED_VALIDATION_SEQUENCE(
        mapping
    )
    assert proof_record["state"] == "STATE_FAILED"
    assert proof_record["non_compliant_identifier_count"] == 1


def test_naming_protocol_system_wide_sweep_passes_all_registry_identifiers() -> None:
    result = FUNCTION_NAMING_PROTOCOL_EXECUTE_SYSTEM_WIDE_IDENTIFIER_SWEEP_AND_EMIT_PROOF_RECORD()
    assert result["state"] == "STATE_COMPLETED", (
        f"System-wide sweep failed. Violations: {result.get('violation_list')}"
    )
    assert result["non_compliant_identifier_count"] == 0
    assert result["proof_gate"] == "PROOF_GATE_NAMING_PROTOCOL_ENFORCED_ON_ALL_BOUNDARIES"


def test_naming_protocol_governance_prefix_registry_has_expected_prefixes() -> None:
    required_prefixes = [
        "ENVIRONMENT_", "STATE_", "FUNCTION_", "WHOLE_",
        "ARTIFACT_", "PROOF_GATE_", "PENDING_", "AGENT_",
    ]
    for prefix in required_prefixes:
        assert prefix in GOVERNANCE_PREFIX_REGISTRY, (
            f"Required prefix {prefix!r} missing from GOVERNANCE_PREFIX_REGISTRY"
        )


# ---------------------------------------------------------------------------
# Iterative Resolution Engine tests
# ---------------------------------------------------------------------------

def test_iterative_resolution_engine_built_in_self_test_passes() -> None:
    result = (
        FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_BUILT_IN_SELF_TEST_WITH_CONTROLLED_SCENARIO()
    )
    assert result["test_passed"] is True
    assert result["ok"] is True
    assert result["total_steps_executed"] == 3
    assert result["total_steps_passed"] == 3
    assert result["total_steps_failed"] == 0
    assert result["tiers_used"] == 1
    assert result["aggregate_proof_hash"] is not None


def test_iterative_resolution_engine_executes_complete_protocol_all_steps_pass() -> None:
    def _step_a() -> dict:
        return {"result": "A", "ok": True}

    def _step_b() -> dict:
        return {"result": "B", "ok": True}

    steps = [
        ResolutionStep(
            step_canonical_name="FUNCTION_RESOLUTION_STEP_TEST_A",
            step_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
            step_callable=_step_a,
        ),
        ResolutionStep(
            step_canonical_name="FUNCTION_RESOLUTION_STEP_TEST_B",
            step_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
            step_callable=_step_b,
        ),
    ]
    protocol_result = FUNCTION_ITERATIVE_RESOLUTION_ENGINE_EXECUTE_COMPLETE_SELF_RESOLVING_PROTOCOL(
        problem_whole_name="WHOLE_TEST_PROBLEM",
        problem_environment_name="ENVIRONMENT_CONTINUOUS_INTEGRATION",
        problem_description="Unit test of resolution protocol.",
        resolution_steps=steps,
    )
    assert protocol_result.all_steps_resolved is True
    assert protocol_result.protocol_state == STATE_RESOLUTION_COMPLETED_ALL_STEPS_PASSED
    assert protocol_result.total_steps_passed == 2
    assert protocol_result.total_steps_failed == 0


# ---------------------------------------------------------------------------
# Agent Directive Dispatcher tests
# ---------------------------------------------------------------------------

def test_agent_directive_dispatcher_registry_has_seven_agents() -> None:
    assert len(AGENT_DIRECTIVE_UNIT_REGISTRY) == 7
    for canonical_name in ALL_AGENT_CANONICAL_NAMES_IN_DISPATCH_ORDER:
        assert canonical_name in AGENT_DIRECTIVE_UNIT_REGISTRY, (
            f"Agent {canonical_name!r} missing from AGENT_DIRECTIVE_UNIT_REGISTRY"
        )


def test_agent_directive_dispatcher_all_agents_have_agent_prefix() -> None:
    for canonical_name in AGENT_DIRECTIVE_UNIT_REGISTRY:
        assert canonical_name.startswith("AGENT_"), (
            f"Agent canonical name {canonical_name!r} does not start with AGENT_"
        )


def test_agent_directive_dispatcher_standard_assignments_count() -> None:
    assignments = (
        FUNCTION_AGENT_DIRECTIVE_DISPATCHER_BUILD_STANDARD_DIRECTIVE_ASSIGNMENTS_FOR_ALL_SEVEN_AGENTS()
    )
    assert len(assignments) == 7


def test_agent_directive_dispatcher_full_sweep_all_complete() -> None:
    assignments = (
        FUNCTION_AGENT_DIRECTIVE_DISPATCHER_BUILD_STANDARD_DIRECTIVE_ASSIGNMENTS_FOR_ALL_SEVEN_AGENTS(
            target_platform="linux"
        )
    )
    dispatch_result = FUNCTION_AGENT_DIRECTIVE_DISPATCHER_EXECUTE_ALL_AGENT_DIRECTIVES_IN_SEQUENCE(
        assignments
    )
    assert dispatch_result.all_directives_completed is True, (
        f"Not all directives completed. Failed: "
        f"{[o.assignment_canonical_name for o in dispatch_result.per_assignment_outcomes if not o.result_payload.get('ok')]}"
    )
    assert dispatch_result.total_directives_completed == 7
    assert dispatch_result.total_directives_failed == 0
    assert dispatch_result.aggregate_proof_hash is not None


# ---------------------------------------------------------------------------
# Automation Protocol tests
# ---------------------------------------------------------------------------

def test_automation_protocol_governance_cycle_completes_successfully() -> None:
    cycle_result = FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_COMPLETE_GOVERNANCE_CYCLE(
        tick_id=0,
        target_platform="linux",
    )
    assert cycle_result.cycle_state == STATE_AUTOMATION_PROTOCOL_COMPLETED
    assert cycle_result.cycle_all_subsystems_passed is True
    assert cycle_result.naming_protocol_sweep_state == "STATE_COMPLETED"
    assert cycle_result.agent_dispatcher_all_completed is True
    assert cycle_result.resolution_engine_all_resolved is True
    assert cycle_result.learning_feedback_committed is True
    assert cycle_result.aggregate_cycle_proof_hash is not None
    assert cycle_result.proof_gate == "PROOF_GATE_AUTOMATION_PROTOCOL_GOVERNANCE_CYCLE_COMPLETED"


def test_automation_protocol_serialised_result_has_ok_true() -> None:
    cycle_result = FUNCTION_AUTOMATION_PROTOCOL_EXECUTE_COMPLETE_GOVERNANCE_CYCLE(tick_id=1)
    serialised = FUNCTION_AUTOMATION_PROTOCOL_SERIALIZE_GOVERNANCE_CYCLE_RESULT_TO_DICT(
        cycle_result
    )
    assert serialised["ok"] is True
    assert serialised["cycle_state"] == STATE_AUTOMATION_PROTOCOL_COMPLETED
    assert "aggregate_cycle_proof_hash" in serialised
    assert "pending_items" in serialised
    assert len(serialised["pending_items"]) > 0


def test_automation_protocol_run_cli_function_returns_ok_true() -> None:
    result = _automation_protocol_run(tick_id=0, target_platform="linux")
    assert result["ok"] is True
    assert result["cycle_state"] == STATE_AUTOMATION_PROTOCOL_COMPLETED

