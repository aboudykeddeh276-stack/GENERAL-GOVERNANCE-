# Keddeh Organisation Authority Skill

## Purpose
Resolve the Keddeh Systems operating identity to its underlying legal holder before any consequential legal, commercial, domain, repository, billing, customer, publishing, or infrastructure action.

## Mandatory decision test
Before acting, ask: **AM I DOING WHAT I SHOULD BE DOING?**

Then resolve:
1. What identity is being acted as?
2. Does the action require the operating identity or the underlying legal entity?
3. Is the legal/business relationship preserved rather than flattened?
4. Is the target sector allowed to mutate this identity, or only reference it?
5. Will the action produce an evidence receipt sufficient for the claim?

## Canonical identities
- Legal entity: `organisation://the-layna-company`
- Legal name: `THE LAYNA COMPANY PTY LIMITED`
- ACN: `691036236`
- ABN: `79691036236`
- Business identity: `business-name://keddeh-systems`
- Business name: `Keddeh Systems`
- Operating authority: `KEDDEH_SYSTEMS`
- Relationship: `BUSINESS_NAME_HELD_BY_LEGAL_ENTITY`

## Resolution rule
For product, service, repository, runtime, domain frontage, support, publishing, or technical operations, resolve primarily to `business-name://keddeh-systems` and retain `organisation://the-layna-company` as legal holder.

For contracts, invoices, tax, regulatory matters, banking, formal legal notices, or other actions requiring the legal person, resolve primarily to `organisation://the-layna-company` and attach `business-name://keddeh-systems` as the trading/operating identity where applicable.

## Authority boundary
This skill resolves identity. It does not itself:
- alter ASIC/ABR registry state;
- create legal rights;
- change tax registration;
- mutate DNS, repositories, payments, or customer records.

Those effects must be delegated to the owning sector adapter after identity resolution.

## Required evidence
Every consequential identity-bound action should record:
- operating identity;
- legal holder identity;
- ABN/ACN where required;
- target sector;
- mutation class;
- authority used;
- resulting receipt/proof root.

## Implementation
Canonical adapter:
`authority/legal_identity/KEDDEH_LEGAL_IDENTITY_ADAPTER_R1.py`

Canonical process:
`processes/KEDDEH_LEGAL_TO_OPERATING_IDENTITY_PROCESS_R1.json`
