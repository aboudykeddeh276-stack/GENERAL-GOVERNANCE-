from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any
import hashlib, json


def _canon(v: Any) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _root(v: Any) -> str:
    return hashlib.sha256(_canon(v).encode()).hexdigest()


@dataclass(frozen=True)
class LegalEntity:
    identity: str
    legal_name: str
    entity_type: str
    acn: str
    abn: str
    jurisdiction: str


@dataclass(frozen=True)
class BusinessIdentity:
    identity: str
    business_name: str
    business_name_class: str
    legal_holder: str
    operating_authority: str
    jurisdiction: str


class KeddehLegalIdentityAdapter:
    """Canonical legal-to-operating identity resolver for the Keddeh Systems estate."""

    LEGAL = LegalEntity(
        identity="organisation://the-layna-company",
        legal_name="THE LAYNA COMPANY PTY LIMITED",
        entity_type="AUSTRALIAN_PRIVATE_COMPANY",
        acn="691036236",
        abn="79691036236",
        jurisdiction="AUSTRALIA/SA",
    )

    BUSINESS = BusinessIdentity(
        identity="business-name://keddeh-systems",
        business_name="Keddeh Systems",
        business_name_class="REGISTERED_BUSINESS_NAME",
        legal_holder=LEGAL.identity,
        operating_authority="KEDDEH_SYSTEMS",
        jurisdiction="AUSTRALIA/SA",
    )

    def resolve(self, identity: str) -> Dict[str, Any]:
        if identity in {self.LEGAL.identity, self.LEGAL.acn, self.LEGAL.abn}:
            payload = {"class": "LEGAL_ENTITY", **asdict(self.LEGAL)}
        elif identity in {self.BUSINESS.identity, self.BUSINESS.business_name, self.BUSINESS.operating_authority}:
            payload = {
                "class": "BUSINESS_IDENTITY",
                **asdict(self.BUSINESS),
                "legal_entity": asdict(self.LEGAL),
            }
        else:
            raise KeyError(identity)
        payload["identity_root"] = _root(payload)
        return payload

    def operating_to_legal(self) -> Dict[str, Any]:
        return {
            "operating_identity": self.BUSINESS.identity,
            "legal_holder": self.LEGAL.identity,
            "abn": self.LEGAL.abn,
            "acn": self.LEGAL.acn,
            "relationship": "BUSINESS_NAME_HELD_BY_LEGAL_ENTITY",
            "root": _root({"business": asdict(self.BUSINESS), "legal": asdict(self.LEGAL)}),
        }

    def bind_transaction_identity(self, transaction_class: str) -> Dict[str, str]:
        legal_classes = {"contract", "invoice", "tax", "regulatory", "banking", "legal_notice"}
        if transaction_class.lower() in legal_classes:
            return {"primary": self.LEGAL.identity, "trading_as": self.BUSINESS.identity}
        return {"primary": self.BUSINESS.identity, "legal_holder": self.LEGAL.identity}


if __name__ == "__main__":
    print(json.dumps(KeddehLegalIdentityAdapter().resolve("KEDDEH_SYSTEMS"), indent=2))
