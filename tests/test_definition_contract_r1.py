from __future__ import annotations

import json
from pathlib import Path

from semantic_control.definition_contract.conformance import assert_promotable, validate_instance

ROOT = Path(__file__).resolve().parents[1]
DEFINITION = json.loads((ROOT / "semantic_control/definitions/DEFINITION_R1.json").read_text())


def conforming_instance():
    return {
        "classification": ["SEMANTIC_CLASS_CONTRACT"],
        "properties": {
            "stable_semantic_identity": True,
            "versioned_mutation_only": True,
            "inward_reducibility": True,
            "outward_reconstructability": True,
            "conformance_testability": True,
        },
        "satisfied_invariants": list(DEFINITION["invariants"]),
        "primitive_evidence": list(DEFINITION["primitive_basis"]),
        "proof_evidence": list(DEFINITION["proof_conditions"]),
        "semantic_claims": [],
        "substrate_boundary": {"claimed_inside": list(DEFINITION["substrate_boundary"]["inside"])},
    }


def test_definition_validates_conforming_instance():
    report = assert_promotable(DEFINITION, conforming_instance())
    assert report.status == "CONFORMANT"
    assert len(report.report_root) == 64
    assert report.inward_trace[-1] == "primitive_basis"
    assert report.outward_trace[-1] == "definition_conformance"


def test_silent_reinterpretation_is_rejected():
    instance = conforming_instance()
    instance["semantic_claims"] = ["agent_may_reinterpret_identifier_silently"]
    report = validate_instance(DEFINITION, instance)
    assert report.status == "NON_CONFORMANT"
    assert any(issue.code == "INVALID_INTERPRETATION" for issue in report.issues)


def test_missing_primitive_is_rejected():
    instance = conforming_instance()
    instance["primitive_evidence"].remove("primitive://proof")
    report = validate_instance(DEFINITION, instance)
    assert report.status == "NON_CONFORMANT"
    assert any(issue.code == "PRIMITIVE_UNRESOLVED" and issue.detail == "primitive://proof" for issue in report.issues)


def test_substrate_boundary_corruption_is_rejected():
    instance = conforming_instance()
    instance["substrate_boundary"]["claimed_inside"].append("agent-local reinterpretation")
    report = validate_instance(DEFINITION, instance)
    assert report.status == "NON_CONFORMANT"
    assert any(issue.code == "SUBSTRATE_BOUNDARY_VIOLATION" for issue in report.issues)


def test_required_property_mismatch_is_rejected():
    instance = conforming_instance()
    instance["properties"]["versioned_mutation_only"] = False
    report = validate_instance(DEFINITION, instance)
    assert report.status == "NON_CONFORMANT"
    assert any(issue.code == "PROPERTY_VALUE_MISMATCH" for issue in report.issues)


if __name__ == "__main__":
    test_definition_validates_conforming_instance()
    test_silent_reinterpretation_is_rejected()
    test_missing_primitive_is_rejected()
    test_substrate_boundary_corruption_is_rejected()
    test_required_property_mismatch_is_rejected()
    print("DEFINITION_CONTRACT_R1_PASS")
