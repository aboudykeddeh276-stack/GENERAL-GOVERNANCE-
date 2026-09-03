from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
from typing import Any, Mapping, Sequence
import json

REQUIRED_FIELDS = (
    "identifier",
    "version",
    "classification",
    "primitive_basis",
    "properties",
    "invariants",
    "relationships",
    "substrate_boundary",
    "executable_role",
    "traversal_rules",
    "proof_conditions",
    "invalid_interpretations",
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def root(value: Any) -> str:
    return sha256(canonical(value)).hexdigest()


@dataclass(frozen=True)
class ConformanceIssue:
    code: str
    field: str
    detail: str


@dataclass(frozen=True)
class ConformanceReport:
    identifier: str
    definition_version: str
    definition_root: str
    implementation_root: str
    status: str
    inward_trace: tuple[str, ...]
    outward_trace: tuple[str, ...]
    issues: tuple[ConformanceIssue, ...]

    @property
    def report_root(self) -> str:
        return root({
            **asdict(self),
            "issues": [asdict(issue) for issue in self.issues],
        })


def validate_definition(definition: Mapping[str, Any]) -> list[ConformanceIssue]:
    issues: list[ConformanceIssue] = []
    for field in REQUIRED_FIELDS:
        if field not in definition:
            issues.append(ConformanceIssue("DEFINITION_FIELD_MISSING", field, "required by Definition Contract R1"))
    if issues:
        return issues

    if not definition["identifier"]:
        issues.append(ConformanceIssue("IDENTIFIER_EMPTY", "identifier", "identifier must be stable and non-empty"))
    if not definition["classification"]:
        issues.append(ConformanceIssue("CLASSIFICATION_EMPTY", "classification", "at least one class is required"))
    if not definition["primitive_basis"]:
        issues.append(ConformanceIssue("PRIMITIVE_BASIS_EMPTY", "primitive_basis", "inward traversal must terminate in declared primitives"))
    if not definition["invariants"]:
        issues.append(ConformanceIssue("INVARIANTS_EMPTY", "invariants", "a class without invariants cannot be conformance-tested"))
    if not definition["proof_conditions"]:
        issues.append(ConformanceIssue("PROOF_CONDITIONS_EMPTY", "proof_conditions", "promotion requires explicit proof conditions"))
    if not definition["invalid_interpretations"]:
        issues.append(ConformanceIssue("INVALID_INTERPRETATIONS_EMPTY", "invalid_interpretations", "semantic drift guards are required"))

    traversal = definition.get("traversal_rules", {})
    if not traversal.get("inward"):
        issues.append(ConformanceIssue("INWARD_TRAVERSAL_EMPTY", "traversal_rules.inward", "resolve-to-primitive path required"))
    if not traversal.get("outward"):
        issues.append(ConformanceIssue("OUTWARD_TRAVERSAL_EMPTY", "traversal_rules.outward", "primitive-to-capability validation path required"))

    boundary = definition.get("substrate_boundary", {})
    if "inside" not in boundary or "outside" not in boundary:
        issues.append(ConformanceIssue("SUBSTRATE_BOUNDARY_INVALID", "substrate_boundary", "inside/outside boundary must be explicit"))
    return issues


def _as_set(value: Any) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, str):
        return {value}
    return {str(v) for v in value}


def validate_instance(definition: Mapping[str, Any], implementation: Mapping[str, Any]) -> ConformanceReport:
    issues = validate_definition(definition)
    identifier = str(definition.get("identifier", "UNRESOLVED"))
    version = str(definition.get("version", "UNVERSIONED"))

    if not issues:
        impl_classes = _as_set(implementation.get("classification"))
        allowed_classes = _as_set(definition["classification"])
        if not impl_classes or not impl_classes.issubset(allowed_classes):
            issues.append(ConformanceIssue(
                "CLASSIFICATION_MISMATCH",
                "classification",
                f"implementation={sorted(impl_classes)} definition={sorted(allowed_classes)}",
            ))

        observed_properties = implementation.get("properties", {})
        for key, required in definition["properties"].items():
            if key not in observed_properties:
                issues.append(ConformanceIssue("PROPERTY_MISSING", f"properties.{key}", "required property not observed"))
                continue
            observed = observed_properties[key]
            if isinstance(required, Mapping) and "required_value" in required and observed != required["required_value"]:
                issues.append(ConformanceIssue(
                    "PROPERTY_VALUE_MISMATCH",
                    f"properties.{key}",
                    f"expected={required['required_value']!r} observed={observed!r}",
                ))

        observed_invariants = _as_set(implementation.get("satisfied_invariants"))
        for invariant in definition["invariants"]:
            if invariant not in observed_invariants:
                issues.append(ConformanceIssue("INVARIANT_UNPROVEN", "invariants", invariant))

        observed_primitives = _as_set(implementation.get("primitive_evidence"))
        for primitive in definition["primitive_basis"]:
            if primitive not in observed_primitives:
                issues.append(ConformanceIssue("PRIMITIVE_UNRESOLVED", "primitive_basis", primitive))

        observed_proof = _as_set(implementation.get("proof_evidence"))
        for condition in definition["proof_conditions"]:
            if condition not in observed_proof:
                issues.append(ConformanceIssue("PROOF_CONDITION_UNMET", "proof_conditions", condition))

        claimed_semantics = _as_set(implementation.get("semantic_claims"))
        for invalid in definition["invalid_interpretations"]:
            if invalid in claimed_semantics:
                issues.append(ConformanceIssue("INVALID_INTERPRETATION", "semantic_claims", invalid))

        observed_boundary = implementation.get("substrate_boundary", {})
        for item in definition["substrate_boundary"]["outside"]:
            if item in _as_set(observed_boundary.get("claimed_inside")):
                issues.append(ConformanceIssue("SUBSTRATE_BOUNDARY_VIOLATION", "substrate_boundary", item))

    inward = tuple(definition.get("traversal_rules", {}).get("inward", ()))
    outward = tuple(definition.get("traversal_rules", {}).get("outward", ()))
    status = "CONFORMANT" if not issues else "NON_CONFORMANT"
    return ConformanceReport(
        identifier=identifier,
        definition_version=version,
        definition_root=root(definition),
        implementation_root=root(implementation),
        status=status,
        inward_trace=inward,
        outward_trace=outward,
        issues=tuple(issues),
    )


def assert_promotable(definition: Mapping[str, Any], implementation: Mapping[str, Any]) -> ConformanceReport:
    report = validate_instance(definition, implementation)
    if report.status != "CONFORMANT":
        summary = "; ".join(f"{i.code}:{i.field}:{i.detail}" for i in report.issues)
        raise RuntimeError(f"DEFINITION_CONFORMANCE_FAILED:{summary}")
    return report
