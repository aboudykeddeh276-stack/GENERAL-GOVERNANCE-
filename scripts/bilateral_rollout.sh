#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   scripts/bilateral_rollout.sh owner/repo1 owner/repo2 ...
#
# Requires:
#   - gh authenticated
#   - git
#   - rsync

if [[ "$#" -lt 1 ]]; then
  echo "usage: $0 owner/repo [owner/repo ...]"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="${ROOT_DIR}/.rollout_tmp"
mkdir -p "${TMP_DIR}"

copy_payload() {
  local target_dir="$1"

  mkdir -p "${target_dir}/docs"
  mkdir -p "${target_dir}/src/virtual_brain_pc"
  mkdir -p "${target_dir}/tests"
  mkdir -p "${target_dir}/scripts"

  rsync -a "${ROOT_DIR}/docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.3.md" "${target_dir}/docs/"
  rsync -a "${ROOT_DIR}/docs/KEDDEH_THEOREM_BRAINK_MASTER_v1.4.md" "${target_dir}/docs/"

  rsync -a "${ROOT_DIR}/src/virtual_brain_pc/material_calibration.py" "${target_dir}/src/virtual_brain_pc/"
  rsync -a "${ROOT_DIR}/src/virtual_brain_pc/spike_calibration.py" "${target_dir}/src/virtual_brain_pc/"
  rsync -a "${ROOT_DIR}/src/virtual_brain_pc/registry.py" "${target_dir}/src/virtual_brain_pc/"

  if [[ -f "${ROOT_DIR}/tests/test_smoke.py" ]]; then
    rsync -a "${ROOT_DIR}/tests/test_smoke.py" "${target_dir}/tests/"
  fi
}

for repo in "$@"; do
  repo_name="${repo##*/}"
  target="${TMP_DIR}/${repo_name}"

  rm -rf "${target}"
  echo "[rollout] cloning ${repo}"
  gh repo clone "${repo}" "${target}" -- -q

  echo "[rollout] copying BRAINK payload into ${repo}"
  copy_payload "${target}"

  pushd "${target}" >/dev/null
  git checkout -b "braink/bilateral-rollout-v14" >/dev/null 2>&1 || git checkout "braink/bilateral-rollout-v14"
  git add docs src tests scripts || true

  if git diff --cached --quiet; then
    echo "[rollout] no changes for ${repo}"
    popd >/dev/null
    continue
  fi

  git commit -m "Add BRAINK v1.4 bilateral calibration stack" >/dev/null
  git push -u origin "braink/bilateral-rollout-v14"

  if gh pr view --repo "${repo}" "braink/bilateral-rollout-v14" >/dev/null 2>&1; then
    echo "[rollout] PR already exists for ${repo}"
  else
    gh pr create \
      --repo "${repo}" \
      --base main \
      --head "braink/bilateral-rollout-v14" \
      --title "BRAINK v1.4 bilateral rollout" \
      --body "Rolls out BRAINK KEDDEH master doctrine v1.3/v1.4 and spike/material calibration modules."
  fi
  popd >/dev/null
done

echo "[rollout] completed"
