$ErrorActionPreference = "Stop"

python -m pip install -e . pytest
python -m pytest -q
python -m virtual_brain_pc.cli build --target windows
python -m virtual_brain_pc.cli braink-run --tick-id 0 --system ci_windows --environment ci
python -m virtual_brain_pc.cli organism-run --tick-id 0
python -m virtual_brain_pc.cli ops-run --tick-id 0
