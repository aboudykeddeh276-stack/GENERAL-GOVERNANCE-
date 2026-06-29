#!/usr/bin/env bash
set -euo pipefail

python -m pip install -e .
python -m pytest -q
python -m virtual_brain_pc.cli build --target linux
