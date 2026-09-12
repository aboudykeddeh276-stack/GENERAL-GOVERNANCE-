#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from dataclasses import asdict
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"MODULE_LOAD_FAILED:{path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def probe(braink_root: Path, nodes_root: Path) -> dict:
    braink_root = braink_root.resolve()
    nodes_root = nodes_root.resolve()
    sys.path.insert(0, str(braink_root))

    node_mod = load_module("braink_r33_node_transition", braink_root / "runtime" / "node_transition_r33.py")
    binding_mod = load_module("keddeh_r33_node_binding", nodes_root / "federation" / "R33" / "node_binding_adapter.py")
    active_nodes = nodes_root / "federation" / "R16" / "ACTIVE_SECTOR_NODES_R16.json"

    node = node_mod.materialize_agent_process(
        "FUNCTION_RND_ENGINEERING",
        {"objective": "R33 executable edge qualification", "mode": "preserve-existing-authority"},
        authority_root="authority:r33:qualification",
        sector_id="ENTERPRISE_AUTOMATION",
    )
    original = asdict(node)
    binding = binding_mod.bind(original, path=active_nodes)
    if binding["status"] != "EDGE_BOUND":
        return {
            "schema": "keddeh.estate-node-edge-probe.r33/v1",
            "status": "HOLD",
            "node_id": node.node_id,
            "node_state": node.state,
            "binding": binding,
            "authority_switch_authorized": False,
        }

    bound = node_mod.transition(
        node,
        "EDGE_BOUND",
        evidence_ref=f"software-nodes://binding/{binding['receipt_root']}",
        state_definition="Existing ENTERPRISE_AUTOMATION sector node accepted the BRAINK node identity; no downstream effect claimed.",
    )

    checks = {
        "node_id_preserved": bound.node_id == node.node_id,
        "source_root_preserved": bound.source_root == node.source_root,
        "payload_root_preserved": bound.payload_root == node.payload_root,
        "authority_root_preserved": bound.authority_root == node.authority_root,
        "adjacent_state_only": node.state == "NODE_MATERIALIZED" and bound.state == "EDGE_BOUND",
        "binding_did_not_mutate_node_authority": binding["node_authority_mutated"] is False,
        "sector_bound": binding["sector_id"] == "ENTERPRISE_AUTOMATION",
    }
    status = "PASS_EDGE_BOUND_ONLY" if all(checks.values()) else "FAIL"
    return {
        "schema": "keddeh.estate-node-edge-probe.r33/v1",
        "status": status,
        "node_id": bound.node_id,
        "source_uri": bound.source_uri,
        "source_root": bound.source_root,
        "payload_root": bound.payload_root,
        "authority_root": bound.authority_root,
        "sector_id": bound.sector_id,
        "capability": bound.capability,
        "state_before": node.state,
        "state_after": bound.state,
        "binding_receipt_root": binding["receipt_root"],
        "transition_root": bound.transition_root,
        "checks": checks,
        "stronger_states_not_claimed": ["TRANSITION_PROPAGATED", "EFFECT_READBACK", "QUALIFIED", "PRODUCTION_PROMOTED"],
        "authority_switch_authorized": False,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--braink-root", required=True)
    ap.add_argument("--nodes-root", required=True)
    ap.add_argument("--out")
    args = ap.parse_args()
    result = probe(Path(args.braink_root), Path(args.nodes_root))
    text = json.dumps(result, indent=2, sort_keys=True)
    print(text)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    return 0 if result["status"] == "PASS_EDGE_BOUND_ONLY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
