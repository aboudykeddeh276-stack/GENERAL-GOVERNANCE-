from keddeh_mesh_os.zero_less_runtime import KeddehMeshOSRuntime, ZeroLessIndex, ZeroLessIndexEngine


def test_zero_less_index_validation() -> None:
    assert ZeroLessIndex.validate(-3) is True
    assert ZeroLessIndex.validate(0) is False


def test_zero_less_runtime_system_init_and_scale_doubling() -> None:
    runtime = KeddehMeshOSRuntime()
    init = runtime.execute_system_init()

    assert init["status"] == "OPERATIONAL"
    assert init["zero_less_verified"] is True
    assert init["proof"]["cartesian_free"] is True

    scaling = runtime.execute_scale_doubling()
    assert scaling["dns_registry_capacity"] == 2000
    assert scaling["ram_core_capacity"] == 2000
    assert scaling["vram_core_capacity"] == 2000
    assert scaling["ram_volume_capacity"] == 2000


def test_zero_less_runtime_deployment_autocorrect_and_proof() -> None:
    runtime = KeddehMeshOSRuntime()
    result = runtime.execute_deployment([-3, 0, 3, 99])

    assert result["zero_less_verified"] is True
    assert len(result["corrections"]) == 2
    assert result["corrections"] == [{"original": 0, "corrected": 1}, {"original": 99, "corrected": 1}]
    assert result["proof_artifact"]["success"] is True
    assert runtime.proof_engine.verify_artifact(result["proof_artifact"]) is True


def test_zero_less_engine_rejects_invalid_literal_mapping() -> None:
    engine = ZeroLessIndexEngine()
    try:
        engine.map_to_uncompressed_literal_state(0)
    except ValueError as exc:
        assert "Cartesian hallucination" in str(exc)
    else:
        raise AssertionError("Expected ValueError for non-zero-less index")
