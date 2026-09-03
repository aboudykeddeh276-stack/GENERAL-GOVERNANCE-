# PROMOTION AND EVIDENCE GATES R1

## Gate 1: Definition
Canonical class and proof conditions exist.

## Gate 2: Implementation
A concrete implementation is bound to the class.

## Gate 3: Local execution
The implementation executes in a real local runtime.

## Gate 4: Determinism and negative tests
Expected behavior and invalid inputs are tested.

## Gate 5: Failure semantics
Crash, concurrency, stale state, replay, torn state, or equivalent relevant failures are injected.

## Gate 6: Persistence/readback
State survives the required lifecycle and is independently read back.

## Gate 7: Recursive descendants
Any instantiated descendants are followed and independently qualified.

## Gate 8: Quantitative benchmark
Latency, throughput, growth, contention, or recovery costs are measured where material.

## Gate 9: CI / independent execution
Independent runner executes the same source/tests.

## Gate 10: External boundary
Where the claim concerns public/external reality, an owning actuator performs the mutation and public/external readback verifies it.

## Gate 11: Persistence of evidence
Source, test evidence, receipts, benchmark results, and package hashes are stored in canonical evidence locations.

## Promotion statuses

NOT_ASSESSED
PARTIAL
LOCALLY_VERIFIED
INDEPENDENTLY_VERIFIED
EXTERNALLY_OBSERVED
PROMOTED
