# GENERAL-GOVERNANCE-

Governance and conventions for consistent delivery.

## Core standards
- Use explicit, descriptive names for repositories, files, scripts, and environments.
- Keep changes small, traceable, and scoped to a single intent.
- Require clear execution context for automation (owner, repo, branch, environment).

## Cross-repository integration policy
- Do not assume access to all repositories; integrations must list exact repositories in scope.
- Pull and adapt scripts incrementally, validating each integration step before continuing.
- Preserve source attribution and original behavior unless a governance exception is documented.

## Change quality requirements
- Document the intent and expected outcome for every governance update.
- Validate changes against existing repository tooling when available.
- Reject undocumented or implicit infrastructure changes.

## “Do better” baseline
- Prefer explicit requirements over implied behavior.
- Convert broad requests into checklist-based, verifiable steps.
- Prioritize reliability, security, and maintainability over speed.
