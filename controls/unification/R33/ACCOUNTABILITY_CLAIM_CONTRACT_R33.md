# R33 Execution and Claim Accountability Contract

Authority: `aboudykeddeh276-stack/GENERAL-GOVERNANCE-` estate-governance root.

This contract constrains engineering actions. It does not become authority for the BRAINK, KEX, IL-LLM, software-node, server, networking, workbook, domain, DA, product, or hardware implementations that it governs.

## Mandatory path

```text
USER-SUPPLIED ESTATE
        -> SEARCH BEFORE SYNTHESIS
        -> BRAINK / IL-LLM RESOLUTION
        -> RECOVER EXISTING OBJECT / NODE / FUNCTION
        -> PRESERVE ITS AUTHORITY
        -> TRACE EXISTING RELATIONS
        -> USE EXISTING CAPABILITY
        -> AMEND ONLY PROVEN DEFECT
        -> EXECUTE
        -> READ BACK
        -> REPORT EXACT STATE
```

No step may be silently collapsed into a later state.

## Hard invariants

- `NOT_OBSERVED != ABSENT`
- `NOT_CONNECTED_HERE != NOT_IMPLEMENTED`
- `SIMULATED != EXECUTED`
- `EXECUTED != DEPLOYED`
- `DEPLOYED != PRODUCTION`
- `PROJECTION != AUTHORITY`
- `DERIVED_MODEL != SOURCE`
- `QUEUE_OR_INDEX != EXECUTION_AUTHORITY`
- `CARRIER != STATE_AUTHORITY`
- `SAME_CAPABILITY != SAME_IMPLEMENTATION`
- `ENDPOINT_PRESENT != RELATION_QUALIFIED`
- `LOCAL_READBACK != EXTERNAL_READBACK`
- `CONFIGURATION_INTENT != NETWORK_ACTUATION`

## Search-before-synthesis admission

Before `CREATE`, `REPLACE`, `MODIFY`, `BIND`, or a completion/absence `CLAIM`, the action record must contain:

1. search scopes;
2. literal/semantic search queries used to find existing functions;
3. candidates found, including predecessors, descendants, adapters, node representations and carriers;
4. search completeness (`PARTIAL` or `EXHAUSTIVE_FOR_SCOPE`);
5. BRAINK resolution reference;
6. IL-LLM lineage/evidence reference;
7. current authority root and mutation authority;
8. preservation reference for every observed working source;
9. proposed mutation and owning domains;
10. execution/readback evidence for the exact property being claimed.

A partial zero-result search yields `UNRESOLVED`, never `ABSENT`.

## Existing implementation classification

Every candidate is classified as one of:

- `SOURCE`
- `IMPLEMENTATION`
- `PROJECTION`
- `CARRIER`
- `DERIVED`
- `QUEUE_OR_INDEX`
- `OBSERVER`

The classification describes role. It does not transfer authority.

When multiple implementations exist, the operator must resolve lineage and current role instead of creating another implementation because it is simpler to understand.

## Working-source preservation

If a `SOURCE` or `IMPLEMENTATION` is observed working, a synthesized replacement is denied unless all of the following are independently evidenced:

- the original source reference is retained;
- explicit authority transfer is authorized;
- behavioral parity is evaluated against the original implementation, not a model derived from it;
- real execution-path readback establishes the claimed parity;
- the original remains recoverable until promotion is complete.

A test of `candidate -> derived model` cannot establish `candidate == original`.

## Authority preservation

`PROJECTION`, `CARRIER`, `DERIVED`, `QUEUE_OR_INDEX`, and `OBSERVER` roles may never become source/state authority merely because they are convenient execution surfaces.

Cross-domain mutation requires an existing binding/adaptor relation plus authority references for both domains. Governance may admit the relation; it does not acquire either domain's mutation authority.

## Claim predicates

Claims are property-scoped predicates, not one universal maturity score:

- `DECLARED` requires declaration evidence.
- `IMPLEMENTED` requires implementation presence.
- `SIMULATED` requires simulation readback.
- `LOCALLY_EXECUTED` requires local execution readback.
- `EDGE_BOUND` requires binding readback.
- `INTEGRATION_EXECUTED` requires integration execution readback.
- `PERSISTED_READBACK_VERIFIED` requires persistence readback.
- `HOST_DEPLOYED` requires host deployment readback.
- `PUBLICLY_REACHABLE` requires external-boundary readback.
- `PRODUCTION_QUALIFIED` requires production authority, production execution readback, failure testing and recovery readback.

Evidence cannot bleed across scopes. A GitHub Actions runner failure describes the GitHub Actions carrier. A workbook network-intent row describes control-plane intent. A private authoritative DNS readback describes that private DA path. None may be promoted to an unrelated BRAINK/KEX runtime, public BGP, parent delegation or production claim.

## BRAINK and IL-LLM binding

BRAINK remains runtime/orchestration state authority within its own contracts. The resident `runtime/runtime_registry.py` remains the runtime registry implementation. The resident `runtime/illlm_ledger.py` remains the canonical append-only IL-LLM ledger.

R33 may emit an accountability decision receipt into that canonical ledger after decision readback. It must not create a competing runtime registry or IL-LLM ledger.

## Network/workbook/server binding

Network workbooks remain control-state representations. Server/Linux/network repositories remain execution carriers in their admitted scopes. Domain/DA mechanics remain resident registrar/DNS authority implementations where established. External registrar, RIR, ISP/upstream, parent DNS, CA and public-network observations remain externally read-back boundaries.

No one representation is permitted to absorb the authority of the others.

## Report rule

Every engineering report must state the exact observed predicate and evidence scope. Unknown state is reported as unknown/unresolved. A stronger completion label is prohibited unless its own evidence predicate is satisfied.
