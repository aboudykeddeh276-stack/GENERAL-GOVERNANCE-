# CONTROL CONVENTIONS R1

## Action control

Before consequential mutation:
AM I DOING WHAT I SHOULD BE DOING?

Required answer must resolve:
- target definition/class
- current observed state
- owning sector
- actor authority
- exact mechanic to invoke
- expected mutation
- readback target
- rollback/recovery path
- evidence target

## Control state vocabulary

DEFINED
BOUND
EXECUTING
COMMITTED
READ_BACK
VERIFIED
BLOCKED
QUARANTINED
RECOVERING
RECOVERED
FAILED
UNBOUND
UNPROVEN
PROMOTED

Avoid ambiguous labels such as “done”, “live”, or “ready” without class-specific proof.

## Mutation control

Every mutation SHOULD specify:
- transition_id
- work_id
- actor
- authority_scope
- epoch
- pre_state_root
- requested_change
- permitted_fields
- persistence semantics
- idempotency semantics
- rollback/recovery
- readback
- evidence

## Definition mutation control

A definition may change only by explicit versioned mutation:
OLD_DEFINITION
→ PROPOSED_DELTA
→ COMPATIBILITY ANALYSIS
→ PROOF
→ NEW_DEFINITION_VERSION

Delta MUST include:
- added properties
- removed properties
- changed invariants
- changed substrate boundary
- changed traversal rules
- changed proof conditions
- compatibility impact
- reason/evidence

## Failure control

Failures are first-class state.

Never convert:
BLOCKED → SUCCESS
UNBOUND → IMPOSSIBLE
QUEUED → GREEN
MANIFEST_EXISTS → EXECUTED
PUBLIC_READBACK_ABSENT → PROCESS_ABSENT

## Recovery control

Recovery MUST classify state before mutation:
CONSISTENT
STATE_AHEAD_OF_LEDGER
LEDGER_AHEAD_OF_STATE
CORRUPTED
UNRESOLVED

Unknown divergence MUST fail closed.
