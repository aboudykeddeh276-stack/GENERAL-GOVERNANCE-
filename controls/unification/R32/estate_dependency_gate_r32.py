#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, hashlib
from pathlib import Path

REQUIRED_INVARIANTS = {
    "CARRIER_IS_PROJECTION_NOT_IDENTITY",
    "RESIDENT_ROOT_BEFORE_CARRIER_TRUST",
    "STRUCTURAL_QUALIFICATION_NE_PHYSICAL_VERIFICATION",
    "TRUST_BOUND_NE_PHYSICAL_VERIFIED",
    "VFS_ROLE_RESOLVER_ONLY",
    "EXTERNAL_CLAIM_REQUIRES_ACTUATION_AND_READBACK",
}
FORBIDDEN_AUTO_PROMOTIONS = {"PROMOTED", "ACTIVE_CANONICAL_BY_R32", "EXTERNALLY_VERIFIED"}

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode()

def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()

def load(path):
    return json.loads(Path(path).read_text())

def validate(graph, bindings):
    failures=[]
    graph_repos={r["repo"]:r for r in graph.get("repositories",[])}
    if not REQUIRED_INVARIANTS.issubset(set(graph.get("invariants",[]))):
        failures.append("GRAPH_REQUIRED_INVARIANTS_MISSING")
    if graph.get("r32_action") != "DEPENDENCIES_BOUND; NO DESTRUCTIVE MIGRATION OR AUTHORITY SWITCH IMPLIED":
        failures.append("GRAPH_FAIL_CLOSED_ACTION_MISSING")
    seen=set(); results=[]
    for b in bindings:
        repo=b.get("repository")
        if not repo:
            failures.append("BINDING_REPOSITORY_REQUIRED"); continue
        if repo in seen: failures.append(f"DUPLICATE_BINDING:{repo}")
        seen.add(repo)
        if repo not in graph_repos: failures.append(f"UNREGISTERED_REPOSITORY:{repo}")
        state=b.get("authority_state","")
        if state in FORBIDDEN_AUTO_PROMOTIONS: failures.append(f"FORBIDDEN_AUTO_PROMOTION:{repo}:{state}")
        status=b.get("status","")
        if "PROMOTED" in status and "NOT_" not in status:
            failures.append(f"PROMOTION_STATUS_FORBIDDEN:{repo}:{status}")
        results.append({"repository":repo,"authority_state":state,"binding_status":status,"binding_sha256":digest(b),"registered":repo in graph_repos})
    expected={r for r in graph_repos if r != "aboudykeddeh276-stack/BRAINK"}
    for repo in sorted(expected-seen): failures.append(f"MISSING_BINDING:{repo}")
    return {"schema":"keddah.estate-dependency-gate.r32.receipt/v1","graph_sha256":digest(graph),"binding_count":len(bindings),"expected_supporting_binding_count":len(expected),"results":results,"failures":failures,"status":"PASS_FAIL_CLOSED" if not failures else "REJECTED","promotion_authorized":False,"authority_switch_authorized":False}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--graph",required=True); ap.add_argument("--binding",action="append",default=[]); ap.add_argument("--receipt")
    a=ap.parse_args(); result=validate(load(a.graph),[load(p) for p in a.binding]); text=json.dumps(result,indent=2); print(text)
    if a.receipt: Path(a.receipt).write_text(text+"\n")
    return 0 if result["status"]=="PASS_FAIL_CLOSED" else 2

if __name__=="__main__": raise SystemExit(main())
