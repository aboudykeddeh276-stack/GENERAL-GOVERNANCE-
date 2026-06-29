from virtual_brain_pc.cli import (
    _braink_run,
    _build,
    _build_all,
    _material_calibrate,
    _ops_run,
    _organism_run,
    _run_virtual_machine,
    _spike_calibrate,
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

