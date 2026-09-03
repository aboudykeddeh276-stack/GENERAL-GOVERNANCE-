# NAMING CONVENTIONS R1

## Governing rule

A named concept is a class identifier once established. Names are not loose metaphors.

## Canonical naming grammar

SYSTEM_CLASS_VERSION

Examples:
- IL_LLM_DEFINITION_V1
- KEX_COORDINATE_RUNTIME_R2
- BRAINK_RECURSIVE_COMPUTER_R26
- OBSERVER2_ENVIRONMENTAL_LOOP_R29
- DURABLE_TRANSITION_R31

## Versioning

- Vn = semantic definition or stable major specification version.
- Rn = implementation/revision lineage.
- Epics MAY span multiple R revisions but SHALL NOT redefine existing class semantics silently.

## File naming

Source: <system>_<component>_r<revision>.py
Definition: <CLASS>_DEFINITION_V<version>.json|md
Receipt: <SYSTEM>_<EVENT>_RECEIPT_<YYYY-MM-DD>.json
Qualification: <SYSTEM>_<COMPONENT>_QUALIFICATION_R<revision>.json
Benchmark: <SYSTEM>_<COMPONENT>_BENCHMARK_R<revision>.json
Control: <KEDDEH_SYSTEMS>_<CONTROL_NAME>_R<revision>.md

## Identity rules

- Use stable canonical identifier separate from display label.
- Never reuse an identifier for a semantically different class.
- Definition changes require explicit version advancement.
- Implementation revisions do not automatically change definition versions.
- Aliases MUST resolve to one canonical identifier.
- Deprecated names MUST retain redirect/migration metadata.

## Invalid naming practices

- Generic labels that erase the user-defined class boundary.
- Reusing “fabric”, “runtime”, “server”, or “agent” as substitutes for exact established classes.
- Renaming historical implementations to imply unproven promotion.
- Encoding “production”, “live”, “certified”, or “deployed” in names without corresponding evidence.
