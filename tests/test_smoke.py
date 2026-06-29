from virtual_brain_pc.cli import (
    _build,
    _build_all,
    _material_calibrate,
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
