"""KEX Canonical Reference Validator  (kex-canonical v1)

BRAINK::KEX::CANONICAL::VALIDATE::v01

This module implements the executable reference for the 10 conformance
acceptance tests listed in SPEC/conformance-checklist.md.  Every function
here is derived exclusively from definitions that are **DEFINED** (not
AUTHOR TO RATIFY) in SPEC/kex-canonical.md and the committed theorem
documents.

Acceptance tests implemented here:
  AT-01  No zero active state
  AT-02  topologicalDistance(−2, 1) == 1          [AUTHOR TO RATIFY — returns None]
  AT-03  scalarDelta(−2, 1) == 3                  [AUTHOR TO RATIFY — returns None]
  AT-04  add(1, −1) → Balanced
  AT-05  Balanced projects to typed zero
  AT-06  Both operands recoverable from Balanced
  AT-07  Balanced(1,−1) ≠ Balanced(2,−2) canonically
  AT-08  Canonical encoding is byte-identical across runs
  AT-09  Invalid denominators are unconstructable     [AUTHOR TO RATIFY — returns None]
  AT-10  Every event carries identity, observer, provenance [AUTHOR TO RATIFY — partial]
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Optional

# ---------------------------------------------------------------------------
# Spec version tag
# ---------------------------------------------------------------------------

SPEC_VERSION = "kex-canonical v1"

# ---------------------------------------------------------------------------
# §1 — Active-state set
# §1.3 — NO-Zero-Axis Invariant
# ---------------------------------------------------------------------------

#: Active values defined as non-zero by §1.1.  The formal signed set
#: {−3,−2,1,+2,+3} is AUTHOR TO RATIFY (§1.2); these are the roles that ARE
#: defined in the committed theorem documents.
_DEFINED_ACTIVE_ROLES = frozenset({1, 2, -2, 3})

#: Absolute tolerance used throughout zero-detection (from zero_classifier.py).
_ZERO_TOL = 1e-10


def is_active_state(value: Any) -> bool:
    """AT-01 — Return True when *value* is a non-zero active state.

    A value is an active state if and only if it is a real number whose
    absolute value is greater than _ZERO_TOL.  Raw zero is never a live
    active weight (§1.3 / §3.1).
    """
    try:
        return abs(float(value)) > _ZERO_TOL
    except (TypeError, ValueError):
        return False


def assert_no_zero_active_state(value: Any) -> None:
    """AT-01 — Raise ValueError when *value* is a raw zero active state."""
    if not is_active_state(value):
        raise ValueError(
            f"NO-Zero-Axis invariant violated: {value!r} is zero or non-numeric. "
            "Zero is never a live active weight (kex-canonical §1.3)."
        )


# ---------------------------------------------------------------------------
# §1.2 — topologicalDistance — AUTHOR TO RATIFY
# ---------------------------------------------------------------------------

def topological_distance(a: Any, b: Any) -> Optional[int]:
    """AT-02 — Topological distance between two active-state values.

    The formal metric is AUTHOR TO RATIFY (§1.2 / §A1).
    Returns None until the author supplies the definition.
    """
    return None  # AUTHOR TO RATIFY


# ---------------------------------------------------------------------------
# §1.2 — scalarDelta — AUTHOR TO RATIFY
# ---------------------------------------------------------------------------

def scalar_delta(a: Any, b: Any) -> Optional[float]:
    """AT-03 — Scalar delta between two active-state values.

    The formal definition is AUTHOR TO RATIFY (§1.2 / §A1).
    Returns None until the author supplies the definition.
    """
    return None  # AUTHOR TO RATIFY


# ---------------------------------------------------------------------------
# §3 — Non-Erasing Arithmetic / Balanced result type
# ---------------------------------------------------------------------------

#: Tag used by the Balanced projection to identify the zero-classification kind.
#: Maps to ZERO_AS_CANCELLATION from zero_classifier.py.
BALANCED_ZERO_TAG = "ZERO_AS_CANCELLATION"


def add(left: float, right: float) -> Dict[str, Any]:
    """AT-04 / AT-05 / AT-06 / AT-07 — Non-erasing addition.

    When *left* + *right* cancels to zero the result is a **Balanced** record
    that retains both operands.  Bare zero is never returned (§3.1).

    Returns a dict with keys:
        ``balanced``       — True when cancellation occurred
        ``left_value``     — original left operand (preserved)
        ``right_value``    — original right operand (preserved)
        ``result``         — arithmetic result (may be zero, carried as a
                             typed projection, not a bare active weight)
        ``projection``     — zero-classification tag (BALANCED_ZERO_TAG when
                             balanced, otherwise ``"NO_ZERO_PRODUCED"``)
        ``power_one_preserved`` — always 1  (§3.1)
    """
    result = left + right
    produced_zero = abs(result) < _ZERO_TOL
    return {
        "left_value": left,
        "right_value": right,
        "result": result,
        "balanced": produced_zero,
        "projection": BALANCED_ZERO_TAG if produced_zero else "NO_ZERO_PRODUCED",
        "power_one_preserved": 1,
    }


def is_balanced(record: Dict[str, Any]) -> bool:
    """AT-04 — Return True when *record* represents a Balanced result."""
    return bool(record.get("balanced"))


def project_to_typed_zero(record: Dict[str, Any]) -> Optional[str]:
    """AT-05 — Return the typed-zero projection tag from a Balanced record.

    Returns the projection string (e.g. ``ZERO_AS_CANCELLATION``) when the
    record is Balanced, or None otherwise.
    """
    if is_balanced(record):
        return record.get("projection")
    return None


def recover_operands(record: Dict[str, Any]) -> Dict[str, float]:
    """AT-06 — Recover both original operands from a Balanced record.

    Raises KeyError when the record does not contain both operands.
    """
    return {
        "left_value": record["left_value"],
        "right_value": record["right_value"],
    }


def balanced_canonical_key(record: Dict[str, Any]) -> str:
    """AT-07 — Canonical key that distinguishes Balanced records by their operands.

    Balanced(1,−1) and Balanced(2,−2) are distinct because they carry different
    operands; their canonical keys will not match.
    """
    return json.dumps(
        {
            "left_value": record["left_value"],
            "right_value": record["right_value"],
            "projection": record.get("projection"),
        },
        sort_keys=True,
        separators=(",", ":"),
    )


# ---------------------------------------------------------------------------
# §5 — Canonical Event Schema / proof ledger encoding
# ---------------------------------------------------------------------------

def canonical_encode(event: Dict[str, Any]) -> bytes:
    """AT-08 — Canonical encoding of a proof-ledger event.

    Produces UTF-8-encoded, sorted-key, compact JSON.  Output is byte-identical
    across Python versions and platforms for identical inputs (§5.1).
    """
    return json.dumps(event, sort_keys=True, separators=(",", ":")).encode("utf-8")


def proof_hash(event: Dict[str, Any]) -> str:
    """Return the first 16 hex chars of SHA-256 over the canonical encoding.

    Matches the algorithm in ``braink_runtime.py → CALL_PROOF_LEDGER_COMMIT``.
    """
    return hashlib.sha256(canonical_encode(event)).hexdigest()[:16]


# ---------------------------------------------------------------------------
# §5.2 — identity / observer / provenance — AUTHOR TO RATIFY
# ---------------------------------------------------------------------------

def validate_event_provenance(event: Dict[str, Any]) -> Optional[str]:
    """AT-10 — Validate that an event carries identity, observer, and provenance.

    The exact field names are AUTHOR TO RATIFY (§5.2 / §A6).
    Returns None when the specification is pending; once ratified, this
    function must be updated to enforce the required fields.
    """
    return None  # AUTHOR TO RATIFY


# ---------------------------------------------------------------------------
# §3.2 / §4 — Invalid denominator / unconstructable states — AUTHOR TO RATIFY
# ---------------------------------------------------------------------------

def construct_active_state(value: Any) -> Dict[str, Any]:
    """AT-09 — Construct an active-state record, rejecting invalid values.

    The exact constraints on invalid denominators are AUTHOR TO RATIFY (§4/§A5).
    Currently enforces the NO-Zero-Axis invariant (§1.3): zero is rejected.
    """
    assert_no_zero_active_state(value)
    return {
        "value": float(value),
        "active": True,
        "spec_version": SPEC_VERSION,
    }
