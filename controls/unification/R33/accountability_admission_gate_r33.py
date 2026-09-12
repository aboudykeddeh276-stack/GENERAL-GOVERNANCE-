#!/usr/bin/env python3
"""BRAINK/KEX R33 execution-and-claim accountability admission gate.

This module does not own BRAINK, IL-LLM, sector runtimes, server carriers, network
protocols or product state.  It admits or refuses a proposed mutation/claim from
estate-governance policy.  Resident implementations remain authoritative inside
their owning domains.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from typing import Any, Mapping, Sequence

SCHEMA = "keddeh.accountability-admission.r33.v1"

MUTATING_ACTIONS = {"CREATE", "REPLACE", "MODIFY", "BIND", "CLAIM"}
CANDIDATE_ROLES = {
    "SOURCE", "IMPLEMENTATION", "PROJECTION", "CARRIER", "DERIVED",
    "QUEUE_OR_INDEX", "OBSERVER",
}

# Claims are intentionally predicates, not one universal maturity number.
CLAIM_REQUIREMENTS: dict[str, set[str]] = {
    "DECLARED": {"declaration"},
    "IMPLEMENTED": {"implementation_present"},
    "SIMULATED": {"simulation_readback"},
    "LOCALLY_EXECUTED": {"local_execution_readback"},
    "EDGE_BOUND": {"edge_binding_readback"},
    "INTEGRATION_EXECUTED": {"integration_execution_readback"},
    "PERSISTED_READBACK_VERIFIED": {"persistence_readback"},
    "HOST_DEPLOYED": {"host_deployment_readback"},
    "PUBLICLY_REACHABLE": {"external_boundary_readback"},
    "PRODUCTION_QUALIFIED": {
        "production_authority",
        "production_execution_readback",
        "failure_test_readback",
        "recovery_readback",
    },
}

# Evidence is scoped.  A success in one carrier cannot be promoted to another.
FORBIDDEN_SCOPE_PROMOTIONS = {
    ("github-actions://runner", "runtime://kex"),
    ("github-actions://runner", "runtime://braink"),
    ("workbook://network-intent", "network://public-bgp"),
    ("dns://private-authority", "dns://parent-delegation"),
    ("dns://private-authority", "network://public-dns"),
    ("http://loopback", "network://public-http"),
}

AUTHORITY_FORBIDDEN_ROLES = {"PROJECTION", "CARRIER", "DERIVED", "QUEUE_OR_INDEX", "OBSERVER"}


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def root(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Decision:
    schema: str
    decision: str
    subject: str
    action: str
    requested_claim: str | None
    reasons: tuple[str, ...]
    unresolved: tuple[str, ...]
    preserved_authority: str | None
    evidence_scope: str | None
    claim_scope: str | None
    receipt_root: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _present(record: Mapping[str, Any], path: str) -> Any:
    cur: Any = record
    for part in path.split("."):
        if not isinstance(cur, Mapping) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _candidate_roles(candidates: Sequence[Mapping[str, Any]]) -> list[str]:
    return [str(c.get("role", "")) for c in candidates]


def evaluate(record: Mapping[str, Any]) -> Decision:
    """Evaluate one proposed action without mutating any estate implementation."""
    reasons: list[str] = []
    unresolved: list[str] = []

    subject = str(record.get("subject") or "")
    action = str(record.get("action") or "").upper()
    requested_claim = record.get("requested_claim")
    requested_claim = str(requested_claim).upper() if requested_claim else None

    if not subject:
        reasons.append("MISSING:SUBJECT")
    if action not in MUTATING_ACTIONS:
        reasons.append("INVALID:ACTION")

    search = record.get("estate_search") if isinstance(record.get("estate_search"), Mapping) else {}
    scopes = search.get("scopes") if isinstance(search.get("scopes"), list) else []
    queries = search.get("queries") if isinstance(search.get("queries"), list) else []
    candidates = search.get("candidates") if isinstance(search.get("candidates"), list) else []
    completeness = str(search.get("completeness") or "UNRESOLVED")

    if action in MUTATING_ACTIONS:
        if not scopes:
            reasons.append("DENY:SEARCH_SCOPE_REQUIRED")
        if not queries:
            reasons.append("DENY:SEARCH_QUERY_REQUIRED")
        if completeness not in {"PARTIAL", "EXHAUSTIVE_FOR_SCOPE"}:
            reasons.append("DENY:SEARCH_COMPLETENESS_UNRESOLVED")

    braink_ref = record.get("braink_resolution_ref")
    illlm_ref = record.get("illlm_lineage_ref")
    if not braink_ref:
        reasons.append("DENY:BRAINK_RESOLUTION_REQUIRED")
    if not illlm_ref:
        reasons.append("DENY:ILLLM_LINEAGE_REQUIRED")

    authority = record.get("authority") if isinstance(record.get("authority"), Mapping) else {}
    authority_root = authority.get("current_authority_root")
    mutation_authority = authority.get("mutation_authority")
    if not authority_root:
        reasons.append("DENY:CURRENT_AUTHORITY_REQUIRED")
    if not mutation_authority:
        reasons.append("DENY:MUTATION_AUTHORITY_REQUIRED")

    roles = _candidate_roles([c for c in candidates if isinstance(c, Mapping)])
    invalid_roles = sorted({r for r in roles if r and r not in CANDIDATE_ROLES})
    if invalid_roles:
        reasons.append("DENY:UNKNOWN_CANDIDATE_ROLE:" + ",".join(invalid_roles))

    # A partial/no-result search is unresolved, never proof of absence.
    if not candidates and completeness != "EXHAUSTIVE_FOR_SCOPE":
        unresolved.append("IMPLEMENTATION_STATUS_UNRESOLVED")
        if requested_claim == "ABSENT":
            reasons.append("DENY:NOT_OBSERVED_IS_NOT_ABSENT")

    if requested_claim == "ABSENT":
        if completeness != "EXHAUSTIVE_FOR_SCOPE":
            reasons.append("DENY:ABSENCE_REQUIRES_EXHAUSTIVE_SCOPE")
        if candidates:
            reasons.append("DENY:ABSENCE_CONTRADICTED_BY_CANDIDATE")

    # Derived/projected/carrier/index objects cannot silently become state authority.
    proposed_authority_role = str(_present(record, "proposed_mutation.authority_role") or "")
    if proposed_authority_role in AUTHORITY_FORBIDDEN_ROLES:
        reasons.append(f"DENY:{proposed_authority_role}_CANNOT_BECOME_SOURCE_AUTHORITY")

    # Preserve a working implementation before any synthesized replacement.
    working = [
        c for c in candidates
        if isinstance(c, Mapping)
        and c.get("working_observed") is True
        and c.get("role") in {"SOURCE", "IMPLEMENTATION"}
    ]
    mutation = record.get("proposed_mutation") if isinstance(record.get("proposed_mutation"), Mapping) else {}
    synthesized = mutation.get("synthesized") is True
    if action == "REPLACE" and working and synthesized:
        transfer = record.get("authority_transfer") if isinstance(record.get("authority_transfer"), Mapping) else {}
        parity = transfer.get("behavioral_parity_against_original") is True
        real_readback = transfer.get("real_path_readback") is True
        explicitly_authorized = transfer.get("explicitly_authorized") is True
        original_ref = transfer.get("original_ref")
        if not (parity and real_readback and explicitly_authorized and original_ref):
            reasons.append("DENY:WORKING_SOURCE_SYNTHESIZED_REPLACEMENT_UNPROVEN")

    preservation = record.get("preservation") if isinstance(record.get("preservation"), Mapping) else {}
    if working:
        if preservation.get("source_preserved") is not True:
            reasons.append("DENY:WORKING_SOURCE_NOT_PRESERVED")
        if not preservation.get("source_ref"):
            reasons.append("DENY:WORKING_SOURCE_REFERENCE_REQUIRED")

    # Cross-domain mutation needs an already identified relation/adapter plus both authorities.
    source_domain = mutation.get("source_domain")
    target_domain = mutation.get("target_domain")
    if source_domain and target_domain and source_domain != target_domain:
        cross = record.get("cross_domain_binding") if isinstance(record.get("cross_domain_binding"), Mapping) else {}
        if not cross.get("existing_binding_ref"):
            reasons.append("DENY:CROSS_DOMAIN_EXISTING_BINDING_REQUIRED")
        if not cross.get("source_authority_ref") or not cross.get("target_authority_ref"):
            reasons.append("DENY:CROSS_DOMAIN_BILATERAL_AUTHORITY_REQUIRED")

    evidence = record.get("evidence") if isinstance(record.get("evidence"), Mapping) else {}
    predicates = set(evidence.get("predicates") or []) if isinstance(evidence.get("predicates"), list) else set()
    evidence_scope = str(evidence.get("scope") or "") or None
    claim_scope = str(record.get("claim_scope") or "") or None

    if requested_claim in CLAIM_REQUIREMENTS:
        missing = sorted(CLAIM_REQUIREMENTS[requested_claim] - predicates)
        if missing:
            reasons.append("DENY:CLAIM_EVIDENCE_MISSING:" + ",".join(missing))
    elif requested_claim and requested_claim != "ABSENT":
        reasons.append("DENY:UNKNOWN_CLAIM")

    if evidence_scope and claim_scope and evidence_scope != claim_scope:
        if (evidence_scope, claim_scope) in FORBIDDEN_SCOPE_PROMOTIONS:
            reasons.append("DENY:EVIDENCE_SCOPE_PROMOTION")
        elif evidence.get("cross_scope_readback") is not True:
            reasons.append("DENY:CROSS_SCOPE_READBACK_REQUIRED")

    # Explicit historical failure cases that must never promote unrelated authorities.
    facts = record.get("facts") if isinstance(record.get("facts"), Mapping) else {}
    if facts.get("github_actions_runner_id") == 0 and claim_scope in {"runtime://kex", "runtime://braink"}:
        reasons.append("DENY:GITHUB_RUNNER_FACT_CANNOT_DESCRIBE_KEX_BRAINK_RUNTIME")
    if facts.get("workbook_network_intent") is True and requested_claim in {"PUBLICLY_REACHABLE", "PRODUCTION_QUALIFIED"}:
        if "external_boundary_readback" not in predicates:
            reasons.append("DENY:WORKBOOK_INTENT_IS_NOT_PUBLIC_NETWORK_EXECUTION")
    if facts.get("private_da_authority_readback") is True and claim_scope in {"dns://parent-delegation", "network://public-dns"}:
        if "external_boundary_readback" not in predicates:
            reasons.append("DENY:PRIVATE_DA_READBACK_IS_NOT_PUBLIC_DELEGATION")

    # Distinguish unresolved from denied: unresolved search/authority knowledge defers work;
    # invariant violations deny it.
    deny = any(r.startswith("DENY:") or r.startswith("INVALID:") or r.startswith("MISSING:") for r in reasons)
    if deny:
        decision = "DENY"
    elif unresolved:
        decision = "DEFER"
    else:
        decision = "ALLOW"

    preserved_authority = str(authority_root) if authority_root else None
    body = {
        "schema": SCHEMA,
        "decision": decision,
        "subject": subject,
        "action": action,
        "requested_claim": requested_claim,
        "reasons": sorted(set(reasons)),
        "unresolved": sorted(set(unresolved)),
        "preserved_authority": preserved_authority,
        "evidence_scope": evidence_scope,
        "claim_scope": claim_scope,
    }
    receipt_root = root(body)
    return Decision(receipt_root=receipt_root, **{**body, "reasons": tuple(body["reasons"]), "unresolved": tuple(body["unresolved"])})


def main() -> int:
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    result = evaluate(json.loads(args.record.read_text(encoding="utf-8")))
    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    return 0 if result.decision == "ALLOW" else 3


if __name__ == "__main__":
    raise SystemExit(main())
