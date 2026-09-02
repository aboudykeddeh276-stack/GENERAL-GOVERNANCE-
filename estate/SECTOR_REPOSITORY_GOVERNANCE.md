# KEDDEH Systems Sector Repository Governance

## Hard rule

```text
one sector
→ one canonical repo
→ one README defining authority
→ one runtime boundary
→ one evidence directory
→ one deployment directory
→ one dependency manifest
→ no silent cross-sector ownership
```

Every sector repository must answer:

1. WHAT DOES THIS SECTOR OWN?
2. WHAT DOES IT EXECUTE?
3. WHAT DOES IT DEPEND ON?
4. WHAT MAY IT MUTATE?
5. WHAT PROVES IT WORKED?

Minimum surface:

`README.md`, `ARCHITECTURE.md`, `AUTHORITY.md`, `DEPENDENCIES.md`, `runtime/`, `tests/`, `deploy/`, `evidence/`, `receipts/`, `docs/`.

## Cross-sector ownership law

Execution location does not silently transfer ownership. Shared mechanics are imported through declared dependencies. A DNS process may execute in `SERVERS-KEDDEHSYSTEMS` while the registrar/delegation/DNSSEC contract belongs to `DOMAIN-AUTHORITY`; the receipt must identify both relations.

## Non-flattening invariants

```text
BRAINK ≠ CASEPATH
KEX ≠ BRAINK
NETWORK ≠ DNS
DNS ≠ REGISTRAR
REGISTRAR ≠ PUBLIC HOST
PUBLIC HOST ≠ APPLICATION
APPLICATION ≠ PROJECTION
PROJECTION ≠ EVIDENCE
```

## Provisioning boundary

The current connected GitHub action surface can write and govern existing repositories but does not expose repository creation or rename. Missing canonical repositories remain explicit provisioning obligations. They must not be represented as completed merely because a manifest entry exists.
