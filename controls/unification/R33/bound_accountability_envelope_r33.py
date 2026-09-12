#!/usr/bin/env python3
"""Bind an R33 admission decision to the exact request it evaluated.

This prevents a valid governance decision from being replayed against a different
mutation, carrier or authority target.  It imports the existing R33 gate; it does
not reimplement policy.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from accountability_admission_gate_r33 import evaluate, root

SCHEMA = "keddeh.accountability-bound-envelope.r33.v1"


def bind_request(record: Mapping[str, Any]) -> dict[str, Any]:
    decision = evaluate(record)
    decision_dict = decision.to_dict()
    if decision.decision != "ALLOW":
        raise PermissionError("ACCOUNTABILITY_DECISION_NOT_ALLOW")

    mutation = record.get("proposed_mutation") if isinstance(record.get("proposed_mutation"), Mapping) else {}
    authority = record.get("authority") if isinstance(record.get("authority"), Mapping) else {}
    body = {
        "schema": SCHEMA,
        "request_root": root(record),
        "decision_receipt": decision_dict,
        "subject": record.get("subject"),
        "action": record.get("action"),
        "source_domain": mutation.get("source_domain"),
        "target_domain": mutation.get("target_domain"),
        "current_authority_root": authority.get("current_authority_root"),
        "mutation_authority": authority.get("mutation_authority"),
        "claim_scope": record.get("claim_scope"),
        "evidence_root": root(record.get("evidence") or {}),
        "preservation_root": root(record.get("preservation") or {}),
    }
    return {**body, "envelope_root": root(body)}


def verify_envelope(envelope: Mapping[str, Any], record: Mapping[str, Any]) -> None:
    if envelope.get("schema") != SCHEMA:
        raise ValueError("ACCOUNTABILITY_ENVELOPE_SCHEMA_INVALID")
    supplied = str(envelope.get("envelope_root") or "")
    body = {k: v for k, v in envelope.items() if k != "envelope_root"}
    if not supplied or root(body) != supplied:
        raise ValueError("ACCOUNTABILITY_ENVELOPE_ROOT_INVALID")
    if envelope.get("request_root") != root(record):
        raise ValueError("ACCOUNTABILITY_REQUEST_ROOT_MISMATCH")
    expected = evaluate(record).to_dict()
    if expected.get("decision") != "ALLOW":
        raise PermissionError("ACCOUNTABILITY_REEVALUATION_NOT_ALLOW")
    if envelope.get("decision_receipt") != expected:
        raise ValueError("ACCOUNTABILITY_DECISION_RECEIPT_MISMATCH")


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    record = json.loads(args.record.read_text(encoding="utf-8"))
    print(json.dumps(bind_request(record), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
