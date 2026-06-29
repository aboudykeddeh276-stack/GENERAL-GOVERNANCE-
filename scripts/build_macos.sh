#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install -e . pytest
python3 -m pytest -q
python3 -m virtual_brain_pc.cli build --target macos
python3 -m virtual_brain_pc.cli braink-run --tick-id 0 --system ci_macos --environment ci
python3 -m virtual_brain_pc.cli organism-run --tick-id 0
python3 -m virtual_brain_pc.cli ops-run --tick-id 0
