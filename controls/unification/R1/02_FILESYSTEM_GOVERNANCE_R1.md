# FILESYSTEM GOVERNANCE R1

## Principle

Filesystem layout is an authority map, not merely storage convenience.

## Repository ownership

Each logical sector SHALL have one canonical repository authority boundary.

Canonical target sectors:
- BRAINK
- KEX
- SERVERS-KEDDEHSYSTEMS
- DOMAIN-AUTHORITY
- NETWORK-FABRIC
- CLOUD-INFRASTRUCTURE
- K-DRIVE
- IL-LLM
- WORKBOOK-OS
- CASEPATH
- CLAIMPATH
- WEB-FABRIC
- EDGE-IOT
- SECURITY-AUTHORITY
- AGENTS-ORCHESTRATION
- EVIDENCE-LEDGER
- GENERAL-GOVERNANCE-

## Minimum repository layout

README.md
ARCHITECTURE.md
AUTHORITY.md
DEPENDENCIES.md
runtime/
tests/
deploy/
evidence/
receipts/
docs/

## Filesystem authority rules

1. A file SHALL have one canonical owner sector.
2. Shared mechanics SHALL be imported/referenced, not silently copied.
3. Transitional placement MUST declare canonical_owner, transitional_owner, migration_target, and reason.
4. Generated evidence MUST NOT overwrite source.
5. Runtime mutable state MUST NOT be confused with source-of-truth definitions.
6. Receipts/evidence SHALL be append-oriented or versioned.
7. Quarantine/recovery directories SHALL never be silently promoted back into active state.
8. Temporary files SHALL be uniquely named and atomically promoted only after validation.
9. Persistent transition state SHALL support crash-safe write/readback semantics appropriate to its class.
10. Absolute paths may be used in runtime receipts, but canonical definitions SHALL use logical identifiers where possible.

## Recommended tree inside a sector repo

definitions/
runtime/
adapters/
constructors/
transitions/
tests/
benchmarks/
deploy/
evidence/
receipts/
quarantine/
docs/

## Logical URI forms

definition://<system>/<class>/<version>
class://<sector>/<class>
runtime://<system>/<runtime-id>
process://<sector>/<process>
constructor://<system>/<constructor>
transition://<sector>/<transition-id>
evidence://<sector>/<evidence-id>
receipt://<sector>/<receipt-id>
vfs://<scope>/<object>
organisation://<identifier>
business-name://<identifier>
