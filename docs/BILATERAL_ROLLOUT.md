# Bilateral Multi-Repo Rollout

This repository includes a rollout script to apply the BRAINK doctrine and calibration stack across multiple repositories in a consistent way.

## Scope Applied to Target Repositories

- docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.3.md
- docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.4.md
- src/virtual_brain_pc/material_calibration.py
- src/virtual_brain_pc/spike_calibration.py
- src/virtual_brain_pc/registry.py
- tests/test_smoke.py (if present in source)

## Script

Path:

- scripts/bilateral_rollout.sh

Requirements:

- gh CLI authenticated
- git
- rsync

Run example:

```bash
chmod +x scripts/bilateral_rollout.sh
scripts/bilateral_rollout.sh owner/repo-one owner/repo-two owner/repo-three
```

Behavior:

1. Clones each target repo into a temporary rollout folder.
2. Copies doctrine and calibration modules.
3. Creates branch braink/bilateral-rollout-v14.
4. Commits and pushes changes.
5. Opens a PR against main if one does not already exist.

## Bilateral Intent

Bilateral means each target receives the same doctrine and executable calibration lane so runtime proofs and failure-ledger semantics stay aligned across repositories.
