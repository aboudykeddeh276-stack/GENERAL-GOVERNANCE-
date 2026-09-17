from virtual_brain_pc.cli import (
    _braink_run,
    _build,
    _build_all,
    _governance_run,
    _material_calibrate,
    _ops_run,
    _organism_run,
    _run_virtual_machine,
    _spike_calibrate,
)
from virtual_brain_pc.governance_automation import (
    AbsoluteMathematicalStateSeedAndDiscrepancyVectorRecord,
    GlobalMasterRepositoryAutomatedSystemIntegrityAndStateSeedTransferEngineMasterController,
    GlobalRepositoryAutomationAndMeshKernelExecutionStatusEnumeration,
    GlobalStateDiscrepancyDecompositionAndReverseEngineeringAgentWorker,
    GlobalStateResolutionExecutionAndAtomicMutationDeploymentAgentWorker,
    KEDDEH_MATRIX_STANDARD_REFERENCE_CONFIGURATION_BLUEPRINT,
    run_governance_automation,
)


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
    }
    assert set(lanes.keys()) == expected_lanes
    for name, lane in lanes.items():
        assert lane["ok"] is True, f"Lane {name!r} reported ok=False"


# ---------------------------------------------------------------------------
# 1-Keddeh Matrix Standard Governance Automation Engine Tests
# ---------------------------------------------------------------------------

def test_governance_automation_execution_status_enumeration_cardinality() -> None:
    all_status_values = list(GlobalRepositoryAutomationAndMeshKernelExecutionStatusEnumeration)
    assert len(all_status_values) == 8


def test_governance_automation_discrepancy_vector_record_is_immutable() -> None:
    record = AbsoluteMathematicalStateSeedAndDiscrepancyVectorRecord(
        targeted_absolute_file_system_or_network_node_path_string="/repo/README.md",
        expected_state_mathematical_hash_value_literal_string="EXPECTED_HASH",
        observed_state_mathematical_hash_value_literal_string="OBSERVED_HASH",
        discrepancy_and_seed_classification_type_literal_string="MISSING_REQUIRED_GOVERNANCE_ARTIFACT",
        estimated_algorithmic_complexity_score_integer=1,
    )
    import pytest
    with pytest.raises((AttributeError, TypeError)):
        record.estimated_algorithmic_complexity_score_integer = 99  # type: ignore[misc]


def test_governance_automation_master_controller_rejects_hex_path() -> None:
    import pytest
    with pytest.raises(ValueError, match="CRITICAL_NAMING_ERROR"):
        GlobalMasterRepositoryAutomatedSystemIntegrityAndStateSeedTransferEngineMasterController(
            target_repository_root_directory_absolute_path_string="/repo/path0xcorrupt",
            keddeh_matrix_reference_configuration_blueprint_dictionary={},
        )


def test_governance_automation_topology_manifest_generation() -> None:
    import pathlib
    import tempfile
    import os

    with tempfile.TemporaryDirectory() as temp_dir_string:
        (pathlib.Path(temp_dir_string) / "README.md").write_text("test", encoding="utf-8")
        (pathlib.Path(temp_dir_string) / "pyproject.toml").write_text("[project]", encoding="utf-8")

        engine = GlobalMasterRepositoryAutomatedSystemIntegrityAndStateSeedTransferEngineMasterController(
            target_repository_root_directory_absolute_path_string=temp_dir_string,
            keddeh_matrix_reference_configuration_blueprint_dictionary={
                "required_artifact_paths": [],
            },
        )
        manifest = engine.generate_exhaustive_uncompressed_filesystem_and_mesh_topology_manifest()
        assert isinstance(manifest, dict)
        assert len(manifest) == 2


def test_governance_automation_discrepancy_decomposition_detects_missing_artifacts() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir_string:
        engine = GlobalMasterRepositoryAutomatedSystemIntegrityAndStateSeedTransferEngineMasterController(
            target_repository_root_directory_absolute_path_string=temp_dir_string,
            keddeh_matrix_reference_configuration_blueprint_dictionary={
                "required_artifact_paths": ["README.md", "missing_file.md"],
            },
        )
        manifest = engine.generate_exhaustive_uncompressed_filesystem_and_mesh_topology_manifest()
        discrepancies = engine.isolate_and_analyze_all_active_state_discrepancy_and_seed_vectors(
            current_topology_manifest=manifest,
        )
        assert len(discrepancies) == 2
        for record in discrepancies:
            assert record.discrepancy_and_seed_classification_type_literal_string == (
                "MISSING_REQUIRED_GOVERNANCE_ARTIFACT"
            )
            assert record.estimated_algorithmic_complexity_score_integer == 1


def test_governance_automation_resolution_agent_archives_telemetry() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir_string:
        engine = GlobalMasterRepositoryAutomatedSystemIntegrityAndStateSeedTransferEngineMasterController(
            target_repository_root_directory_absolute_path_string=temp_dir_string,
            keddeh_matrix_reference_configuration_blueprint_dictionary={},
        )
        resolution_agent = GlobalStateResolutionExecutionAndAtomicMutationDeploymentAgentWorker(
            associated_parent_orchestration_engine=engine
        )
        discrepancy_record = AbsoluteMathematicalStateSeedAndDiscrepancyVectorRecord(
            targeted_absolute_file_system_or_network_node_path_string="/tmp/missing.md",
            expected_state_mathematical_hash_value_literal_string="EXPECTED",
            observed_state_mathematical_hash_value_literal_string="ABSENT",
            discrepancy_and_seed_classification_type_literal_string="MISSING_REQUIRED_GOVERNANCE_ARTIFACT",
            estimated_algorithmic_complexity_score_integer=1,
        )
        resolution_result = resolution_agent.execute_repository_and_mesh_state_discrepancy_resolution_process(
            individual_state_discrepancy_or_seed_vector=discrepancy_record
        )
        assert resolution_result["resolution_execution_status_string"] == (
            "RESOLUTION_TELEMETRY_LOGGED_AND_ARCHIVED_IN_KEDDEH_MATRIX_ENGINE"
        )
        assert len(engine.internal_agent_execution_telemetry_historical_archive_list) == 1


def test_governance_automation_successful_lifecycle_empty_requirements() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as temp_dir_string:
        engine = GlobalMasterRepositoryAutomatedSystemIntegrityAndStateSeedTransferEngineMasterController(
            target_repository_root_directory_absolute_path_string=temp_dir_string,
            keddeh_matrix_reference_configuration_blueprint_dictionary={
                "required_artifact_paths": [],
            },
        )
        result = (
            engine
            .execute_complete_repository_state_integrity_verification_and_self_healing_lifecycle()
        )
        assert result["ok"] is True
        assert result["keddeh_matrix_alignment_verified_boolean"] is True
        assert result["total_discrepancy_count_integer"] == 0
        assert "engine_execution_deterministic_hash_string" in result


def test_governance_automation_full_repository_lifecycle() -> None:
    import pathlib as _pathlib

    repository_root_string = str(
        _pathlib.Path(__file__).resolve().parents[1]
    )
    result = _governance_run(repository_root=repository_root_string)
    assert result["ok"] is True, (
        f"Governance automation failed. Status: {result.get('execution_status_name_string')}. "
        f"Discrepancies: {result.get('unresolved_discrepancy_path_string_list', [])}"
    )
    assert result["keddeh_matrix_alignment_verified_boolean"] is True
    assert result["all_governance_artifacts_present_boolean"] is True
    assert "engine_execution_deterministic_hash_string" in result


def test_governance_automation_keddeh_matrix_reference_configuration_integrity() -> None:
    assert "required_artifact_paths" in KEDDEH_MATRIX_STANDARD_REFERENCE_CONFIGURATION_BLUEPRINT
    assert isinstance(
        KEDDEH_MATRIX_STANDARD_REFERENCE_CONFIGURATION_BLUEPRINT["required_artifact_paths"],
        list,
    )
    assert len(
        KEDDEH_MATRIX_STANDARD_REFERENCE_CONFIGURATION_BLUEPRINT["required_artifact_paths"]
    ) > 0
    assert (
        KEDDEH_MATRIX_STANDARD_REFERENCE_CONFIGURATION_BLUEPRINT[
            "governance_protocol_enforcement_level_string"
        ]
        == "ABSOLUTE_MATHEMATICAL_ENFORCEMENT"
    )

