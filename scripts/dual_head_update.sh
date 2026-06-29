#!/usr/bin/env bash
# dual_head_update.sh — BRAINK dual-head update with ops-mirror lane
#
# Operation:
#   1. Stages and commits all pending src/ and test changes on main (HEAD 1)
#   2. Creates or resets the 'ops-mirror' branch to current main
#   3. Runs auto_ops_commit.py on ops-mirror (HEAD 2) — per-process commits
#   4. Returns to main and fast-forward merges ops-mirror
#   5. Reports final state of both heads
#
# Usage:
#   bash scripts/dual_head_update.sh [--tick-id N] [--dry-run]
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

TICK_ID=0
DRY_RUN=false
MIRROR_BRANCH="ops-mirror"

for arg in "$@"; do
  case "$arg" in
    --tick-id=*) TICK_ID="${arg#*=}" ;;
    --tick-id)   shift; TICK_ID="$1" ;;
    --dry-run)   DRY_RUN=true ;;
  esac
done

HR="════════════════════════════════════════════════════"

echo ""
echo "$HR"
echo "  BRAINK DUAL-HEAD UPDATE"
echo "  Tick ID    : $TICK_ID"
echo "  Dry-run    : $DRY_RUN"
echo "  HEAD 1     : main"
echo "  HEAD 2     : $MIRROR_BRANCH"
echo "$HR"

# ── Ensure git identity ───────────────────────────────────────────────────
git config user.email 2>/dev/null || git config user.email "ops-bot@braink.local"
git config user.name  2>/dev/null || git config user.name  "BRAINK OPS BOT"

# ── Step 1: Stage and commit all pending source changes on main ───────────
echo ""
echo "── STEP 1: Commit pending source changes on main ──"

STAGED=$(git diff --cached --name-only)
UNSTAGED=$(git diff --name-only)
UNTRACKED=$(git ls-files --others --exclude-standard src/ tests/ scripts/)

if [[ -n "$STAGED$UNSTAGED$UNTRACKED" ]]; then
  git add src/ tests/ scripts/ pyproject.toml Makefile 2>/dev/null || true
  CHANGED=$(git diff --cached --name-only | wc -l | tr -d ' ')
  if [[ "$CHANGED" -gt 0 ]]; then
    MSG="chore: stage ops infrastructure changes [tick=$TICK_ID]

Files changed: $CHANGED
Includes: ops.py, ops_processes.py, auto_ops_commit.py, dual_head_update.sh, cli updates, test expansion"
    if $DRY_RUN; then
      echo "  [DRY-RUN] git commit -m '$MSG'"
    else
      git commit -m "$MSG"
      echo "  Committed $(git rev-parse --short HEAD) on main"
    fi
  else
    echo "  Nothing new to stage on main."
  fi
else
  echo "  Working tree clean — no pending source changes."
fi

# ── Step 2: Create / reset ops-mirror from current main ──────────────────
echo ""
echo "── STEP 2: Reset $MIRROR_BRANCH to current main ──"

if $DRY_RUN; then
  echo "  [DRY-RUN] git branch -f $MIRROR_BRANCH HEAD"
  echo "  [DRY-RUN] git checkout $MIRROR_BRANCH"
else
  git branch -f "$MIRROR_BRANCH" HEAD
  git checkout "$MIRROR_BRANCH"
  echo "  $MIRROR_BRANCH is now at $(git rev-parse --short HEAD) (same as main)"
fi

# ── Step 3: Run auto_ops_commit.py on ops-mirror ─────────────────────────
echo ""
echo "── STEP 3: Run per-process ops commits on $MIRROR_BRANCH ──"

if $DRY_RUN; then
  python3 scripts/auto_ops_commit.py --tick-id "$TICK_ID" --dry-run
else
  python3 scripts/auto_ops_commit.py --tick-id "$TICK_ID"
fi

MIRROR_SHA=""
if ! $DRY_RUN; then
  MIRROR_SHA=$(git rev-parse --short HEAD)
  echo ""
  echo "  $MIRROR_BRANCH HEAD: $MIRROR_SHA"
fi

# ── Step 4: Return to main and fast-forward merge ops-mirror ─────────────
echo ""
echo "── STEP 4: Merge $MIRROR_BRANCH into main ──"

if $DRY_RUN; then
  echo "  [DRY-RUN] git checkout main"
  echo "  [DRY-RUN] git merge --ff-only $MIRROR_BRANCH"
else
  git checkout main
  git merge --ff-only "$MIRROR_BRANCH"
  MAIN_SHA=$(git rev-parse --short HEAD)
  echo "  main HEAD: $MAIN_SHA (fast-forwarded from $MIRROR_BRANCH)"
fi

# ── Step 5: Final report ─────────────────────────────────────────────────
echo ""
echo "$HR"
echo "  DUAL-HEAD UPDATE COMPLETE"
if ! $DRY_RUN; then
  echo "  main HEAD       : $(git rev-parse --short main)"
  echo "  ops-mirror HEAD : $(git rev-parse --short $MIRROR_BRANCH)"
  echo "  Commits ahead   : $(git rev-list --count origin/main..main)"
  echo ""
  echo "  Recent log:"
  git log --oneline -6
fi
echo "$HR"
