# KEDDEH SYSTEMS ARCHITECTURAL INTENT BINDING R32

Authority: THE LAYNA COMPANY PTY LIMITED trading as KEDDEH SYSTEMS  
Lead Systems Architect: Aboudy Keddeh  
Governance parent: `00_ESTATE_DEPENDENCY_FEDERATION_R32.md`  
Estate graph parent: `01_ESTATE_DEPENDENCY_GRAPH_R32.json`

## Purpose

This binding places the BRAINK × KEX × DATA × IL-LLM × NODE × VFS × MESH architectural intent under the existing R32 estate-governance spine without creating a competing authority model.

It preserves the R32 rule that repository names, carriers, manifests, projections and declarations do not independently establish runtime authority.

## Governing relation

```text
IDENTITY != IMPLEMENTATION != CARRIER != EXECUTION != EVIDENCE
```

A relation between those classes must be explicit. No class is silently promoted into another.

## Core system classes

| Class | Architectural responsibility | Authority boundary |
|---|---|---|
| BRAINK | orchestration, Observer², resident-root/state coordination, continuation | does not replace KEX execution/address semantics or physical persistence |
| KEX | coordinate/address resolution, execution/transition semantics, machine mechanics | does not inherit BRAINK orchestration merely because mechanics share a carrier |
| DATA | canonical typed information and state contracts | data identity does not establish execution or storage authority |
| IL-LLM | semantic resolution, ontology, relation traversal, multilingual/code-list interpretation | semantic identity does not establish physical carrier authority |
| NODE | executable identity, lifecycle state and capability binding | promotion stage does not itself establish health or physical-host verification |
| VFS | logical namespace and resolver | resolver is not storage medium, capacity authority or persistence proof |
| MESH | distributed membership, routing/replication relations and peer state | membership does not make local state authoritative |
| K-DRIVE | encoded-medium/controller/persistence surface | owns storage mechanics, not VFS logical identity |
| WORKBOOK-OS | workbook-native registers, formula/state topology, scheduler/ledger bindings | workbook carrier is distinct from evaluator/runtime execution |
| EVIDENCE | receipts, hashes, qualification and readback | proves only the property actually observed by the evidence source |

## Enterprise invariants

### A. Persistent IPC

Ordinary request execution must not spawn a new process per request. Long-lived UDS, TCP, shared-memory or equivalent daemon channels are the normal execution substrate.

### B. Anti-mock / epistemic integrity

No mock, manifest, projection, return value or declared state may be promoted as evidence of a physical runtime property. Verification is bound to the owning implementation surface.

Canonical distinction:

```text
DECLARED != MATERIALIZED != CONSTRUCTED != RUNNING != RESPONSIVE != VERIFIED != ACTIVE
```

### C. Typed decomposition

```text
Controller
  -> Domain Service
  -> DAO / Runtime Adapter / Hardware Bridge
  -> Physical or Virtual Substrate
```

Cross-boundary data is schema-validated and canonicalized.

### D. Substrate-first lifecycle

```text
Hardware / virtual substrate
  -> kernel / execution runtime
  -> persistent service
  -> verified IPC/socket liveness
  -> domain service
  -> API/gateway
  -> projection/HCI
```

A higher layer cannot establish authority for an absent lower layer.

## Workbook execution boundary

`.xlsx` is a structured carrier of registers, formulas, state, matrices, manifests and ledgers. Execution authority belongs to the evaluator/runtime that reads and evaluates that carrier.

```text
WORKBOOK = REGISTER + FORMULA + STATE + TOPOLOGY CARRIER
EVALUATOR = EXECUTION + MUTATION + PERSISTENCE CONTROL
```

A workbook may therefore participate in the CPU substrate while remaining distinct from the runtime engine that performs computation.

## Persistent transition contract

The architectural seven-stage mutation sequence is:

```text
1 MOUNT
2 VERIFY
3 HYDRATE
4 RESOLVE
5 MUTATE
6 WRITE-BACK
7 PROOF
```

The durable write-back boundary is:

```text
serialize candidate
  -> write temporary sibling
  -> flush userspace buffers
  -> fsync(temp_fd)
  -> atomic same-filesystem replacement
  -> fsync(parent_directory_fd)
  -> reopen authoritative path
  -> read back bytes
  -> hash authoritative bytes
  -> append lineage receipt
```

Concurrent writers require exclusion, generation comparison, compare-and-swap, or an equivalent conflict mechanism. `fsync` and rename do not by themselves prevent writer races.

The resulting software property is durable, append-oriented, tamper-evident lineage. Physical immutability requires separate deployment enforcement.

## Node promotion contract

Canonical stages:

```text
01 OBSERVED
02 CLASSIFIED
03 VALIDATED
04 MATERIALIZED
05 AGENT_BOUND
06 VFS_BOUND
07 NETWORK_BOUND
08 RUNTIME_CONSTRUCTED
09 RUNTIME_RUNNING
10 LOCAL_VERIFIED
11 MESH_REGISTERED
12 SERVER_REGISTERED
13 SUBSCRIBED
14 ACTIVE
```

Health is an independent axis:

```text
READY | BLOCKED | DEGRADED | FAILED | QUARANTINED
```

A node may therefore truthfully remain at `09:RUNTIME_RUNNING` while `health=BLOCKED`; no failure condition is permitted to counterfeit later promotion stages.

## Mathematical scope controls

### Rule 110

For binary `p,q,r`, the ANF is:

```text
f(p,q,r) = q XOR r XOR qr XOR pqr
```

Workbook arithmetic projection:

```text
=MOD(B2+C2+B2*C2+A2*B2*C2,2)
```

subject to `A2=p`, `B2=q`, `C2=r` and binary-domain validation.

### ExtraNonce2 slicing

```text
E(i,k) = (i << 16) | (k & 0xFFFF)
```

is injective only within the declared domain, field width and job namespace. Collision-free slicing is therefore a scoped construction, not an unconditional statement across arbitrary protocols/jobs.

### Signed target delta

`Delta = Target - Hash` is retained as deterministic telemetry. It is not a usable optimization gradient for SHA-256 search.

### Landauer bound

At 300 K:

```text
k_B * T * ln(2) ~= 2.87098e-21 J/bit
```

This is a thermodynamic lower bound, not a claim of runtime energy efficiency.

## Evidence doctrine

Every operational claim carries an evidence class:

```text
SPECIFIED
MATERIALIZED
CONSTRUCTED
RUNNING
RESPONSIVE
VERIFIED
REGISTERED
ACTIVE
```

Examples of prohibited inference:

```text
PROJECTION_OPEN      != RUNTIME_RUNNING
CARRIER_RESOLVED     != APPLICATION_EXECUTED
HASH_MATCH           != SEMANTIC_CORRECTNESS
MESH_REGISTERED      != LOCAL_STATE_AUTHORITATIVE
TRUST_BOUND          != PHYSICAL_EXECUTION_VERIFIED
```

## R32 integration

This document does not switch authority for any repository or sector. It binds architectural meaning to the existing R32 promotion sequence:

```text
COPY / BIND
-> HASH
-> TEST
-> NEGATIVE TEST
-> FAILURE INJECTION
-> PERSIST / READBACK
-> DESCENDANT CHECK
-> INDEPENDENT EXECUTION
-> EXTERNAL ACTUATION / READBACK WHEN MATERIAL
-> AUTHORITY SWITCH
-> OPTIONAL RETIREMENT
```

Original carriers remain preserved until the owning mechanics are extracted, hashed, tested, read back and independently qualified.

## Closure rule

The system-wide transition law is:

```text
DECLARE
-> MATERIALIZE
-> EXECUTE
-> PERSIST
-> READ BACK
-> VERIFY
-> PROMOTE
```

No later verb may be inferred merely because an earlier verb succeeded.
