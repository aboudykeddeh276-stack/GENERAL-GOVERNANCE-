from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, List, Any, Optional
import hashlib, json


def _canon(v: Any) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _root(v: Any) -> str:
    return hashlib.sha256(_canon(v).encode()).hexdigest()


@dataclass(frozen=True)
class Sector:
    sector: str
    canonical_repo: str
    authority: str
    status: str = "EXISTS"
    transitional_repo: Optional[str] = None


@dataclass(frozen=True)
class Handoff:
    source: str
    target: str
    operation: str
    required_payload: List[str]
    mutation_owner: str
    proof_required: List[str]


class KeddehCrossSectorRecursiveAdapter:
    """Resolve sector ownership and recursively carry one immutable work envelope across sector boundaries.

    The adapter does not pretend to execute a sector's implementation. It determines who owns the next
    mutation, preserves identity/state/lineage/proof references, and produces the exact next handoff.
    """

    SECTORS: Dict[str, Sector] = {
        "LEGAL_GOVERNANCE": Sector("LEGAL_GOVERNANCE", "aboudykeddeh276-stack/GENERAL-GOVERNANCE-", "legal/business identity and estate governance"),
        "BRAINK": Sector("BRAINK", "aboudykeddeh276-stack/BRAINK", "core runtime, Observer², orchestration, VFS state/proof mechanics"),
        "KEX": Sector("KEX", "aboudykeddeh276-stack/KEX", "coordinate/addressing, execution semantics, signal propagation, kernel mechanics", "MISSING_NAMED_REPO", "aboudykeddeh276-stack/BRAINK"),
        "SERVERS": Sector("SERVERS", "aboudykeddeh276-stack/SERVERS-KEDDEHSYSTEMS", "server runtimes, DA server process execution, host bindings, ingress, server qualification"),
        "DOMAIN_AUTHORITY": Sector("DOMAIN_AUTHORITY", "aboudykeddeh276-stack/DOMAIN-AUTHORITY", "registrar logic, zone/delegation semantics, DNSSEC, authority receipts", "MISSING_NAMED_REPO", "aboudykeddeh276-stack/SERVERS-KEDDEHSYSTEMS"),
        "NETWORK_FABRIC": Sector("NETWORK_FABRIC", "aboudykeddeh276-stack/NETWORK-FABRIC", "routers, bridges, mesh, VPN/TL, NAT, anycast, load balancing", "MISSING_NAMED_REPO", "aboudykeddeh276-stack/KEDDEH-CLOUD-SERVERS-ID-1"),
        "CLOUD_INFRASTRUCTURE": Sector("CLOUD_INFRASTRUCTURE", "aboudykeddeh276-stack/CLOUD-INFRASTRUCTURE", "public compute, runtime allocation, cloud/edge substrates", "MISSING_NAMED_REPO", "aboudykeddeh276-stack/KEDDEH-CLOUD-SERVERS-ID-1"),
        "K_DRIVE": Sector("K_DRIVE", "aboudykeddeh276-stack/K-DRIVE", "storage abstraction, logical volumes, persistence/VFS substrate", "MISSING_NAMED_REPO", "aboudykeddeh276-stack/VIRTUALISED_MEMORY"),
        "IL_LLM": Sector("IL_LLM", "aboudykeddeh276-stack/IL-LLM", "language/runtime model, dictionaries, ontology, workbook mechanics", "MISSING_NAMED_REPO", "aboudykeddeh276-stack/BRAINK"),
        "WORKBOOK_OS": Sector("WORKBOOK_OS", "aboudykeddeh276-stack/WORKBOOK-OS", "workbook-native execution and ledgers", "MISSING_NAMED_REPO", "aboudykeddeh276-stack/VIRTUALISED_MEMORY"),
        "WEB_FABRIC": Sector("WEB_FABRIC", "aboudykeddeh276-stack/WEB-FABRIC", "sites, frontages, deployment surfaces, domain-to-site projection", "MISSING_NAMED_REPO", "aboudykeddeh276-stack/BRAINK-CONSOLE-PLUS"),
        "SECURITY_AUTHORITY": Sector("SECURITY_AUTHORITY", "aboudykeddeh276-stack/SECURITY-AUTHORITY", "identity/signature/certificates/trust anchors/audit policy", "MISSING_NAMED_REPO", "aboudykeddeh276-stack/BRAINK"),
        "AGENTS_ORCHESTRATION": Sector("AGENTS_ORCHESTRATION", "aboudykeddeh276-stack/AGENTS-ORCHESTRATION", "agents, routing, workforce/process orchestration", "MISSING_NAMED_REPO", "aboudykeddeh276-stack/KEDDEH_SOFTWARE_NODES"),
        "EVIDENCE_LEDGER": Sector("EVIDENCE_LEDGER", "aboudykeddeh276-stack/EVIDENCE-LEDGER", "qualifications, receipts, benchmarks, conformance", "MISSING_NAMED_REPO", "aboudykeddeh276-stack/BRAINK"),
    }

    PROCESS_CHAINS = {
        "PUBLIC_DOMAIN_SERVICE": ["LEGAL_GOVERNANCE", "BRAINK", "DOMAIN_AUTHORITY", "SERVERS", "NETWORK_FABRIC", "CLOUD_INFRASTRUCTURE", "SECURITY_AUTHORITY", "WEB_FABRIC", "EVIDENCE_LEDGER"],
        "CUSTOMER_SERVICE_DELIVERY": ["LEGAL_GOVERNANCE", "BRAINK", "AGENTS_ORCHESTRATION", "K_DRIVE", "IL_LLM", "EVIDENCE_LEDGER"],
        "WORKBOOK_RUNTIME": ["LEGAL_GOVERNANCE", "BRAINK", "IL_LLM", "WORKBOOK_OS", "K_DRIVE", "SERVERS", "EVIDENCE_LEDGER"],
        "SOFTWARE_RELEASE": ["LEGAL_GOVERNANCE", "BRAINK", "KEX", "SECURITY_AUTHORITY", "SERVERS", "WEB_FABRIC", "EVIDENCE_LEDGER"],
    }

    REQUIRED_ENVELOPE = ["work_id", "organisation_identity", "operating_identity", "intent", "state", "lineage", "evidence", "continuation"]

    def new_envelope(self, work_id: str, intent: str, payload: Optional[dict] = None) -> dict:
        env = {
            "work_id": work_id,
            "organisation_identity": "organisation://the-layna-company",
            "operating_identity": "business-name://keddeh-systems",
            "intent": intent,
            "state": payload or {},
            "lineage": [],
            "evidence": [],
            "continuation": {"epoch": 1, "status": "READY"},
        }
        env["envelope_root"] = _root(env)
        return env

    def verify(self, envelope: dict) -> bool:
        missing = [k for k in self.REQUIRED_ENVELOPE if k not in envelope]
        if missing:
            raise ValueError(f"missing envelope fields: {missing}")
        claimed = envelope.get("envelope_root")
        actual = _root({k: v for k, v in envelope.items() if k != "envelope_root"})
        if claimed and claimed != actual:
            raise ValueError("envelope integrity mismatch")
        return True

    def resolve_sector(self, name: str) -> dict:
        s = self.SECTORS[name]
        d = asdict(s)
        d["execution_repo"] = s.canonical_repo if s.status == "EXISTS" else s.transitional_repo
        return d

    def handoff(self, envelope: dict, source: str, target: str, operation: str, proof_required: Optional[List[str]] = None) -> dict:
        self.verify(envelope)
        src = self.resolve_sector(source)
        dst = self.resolve_sector(target)
        next_env = json.loads(json.dumps(envelope))
        next_env["lineage"].append({
            "source": source,
            "target": target,
            "operation": operation,
            "source_repo": src["execution_repo"],
            "target_repo": dst["execution_repo"],
            "canonical_target_repo": dst["canonical_repo"],
            "target_repo_state": dst["status"],
            "mutation_owner": target,
        })
        next_env["continuation"]["epoch"] += 1
        next_env["continuation"]["status"] = "HANDED_OFF"
        if proof_required:
            next_env["state"].setdefault("required_proof", []).extend(proof_required)
        next_env["envelope_root"] = _root({k: v for k, v in next_env.items() if k != "envelope_root"})
        return next_env

    def recurse(self, process: str, envelope: dict) -> dict:
        chain = self.PROCESS_CHAINS[process]
        current = envelope
        for i in range(len(chain) - 1):
            current = self.handoff(
                current,
                chain[i],
                chain[i + 1],
                operation=f"{process}:{chain[i]}->{chain[i+1]}",
                proof_required=[f"receipt://{chain[i+1].lower()}/{current['work_id']}"],
            )
        current["continuation"]["status"] = "AWAITING_SECTOR_EXECUTION_READBACK"
        current["envelope_root"] = _root({k: v for k, v in current.items() if k != "envelope_root"})
        return current


if __name__ == "__main__":
    a = KeddehCrossSectorRecursiveAdapter()
    e = a.new_envelope("WORK-001", "PUBLIC_DOMAIN_SERVICE", {"domain": "braink.com.au"})
    print(json.dumps(a.recurse("PUBLIC_DOMAIN_SERVICE", e), indent=2))
