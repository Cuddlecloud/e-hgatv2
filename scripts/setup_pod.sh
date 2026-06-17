#!/usr/bin/env bash
# scripts/setup_pod.sh -- one-shot, idempotent RunPod environment rebuild for E-HGATv2.
#
# WHY THIS EXISTS: On RunPod, only the /workspace network volume survives a pod
# stop/relaunch. The container filesystem ($HOME, apt, and pip installs) is EPHEMERAL,
# so a relaunch wipes the repo + venv. This script reinstalls everything into a
# PERSISTENT location so the next relaunch is a no-op (just re-source the venv).
#
# It is safe to re-run: it pulls latest, reuses an existing venv, and re-checks imports.
#
# Usage (on the pod, after copying this one file over or pasting it):
#   GH_TOKEN=ghp_xxx bash setup_pod.sh          # CPU torch (default; deterministic)
#   GPU=1 GH_TOKEN=ghp_xxx bash setup_pod.sh    # CUDA torch build
#   BRANCH=main bash setup_pod.sh               # if the repo is already cloned (SSH auth)
#
# Auth options for the PRIVATE repo:
#   - GH_TOKEN=<github PAT>  -> clones via https then strips the token from .git/config
#   - or pre-configure an SSH deploy key and let it clone git@github.com:...
set -euo pipefail

REPO_SLUG="Cuddlecloud/e-hgatv2"
BRANCH="${BRANCH:-main}"

# 1. Pick a PERSISTENT workdir. /workspace is the RunPod network volume.
if [ -d /workspace ]; then
  WORKDIR="/workspace"
else
  WORKDIR="$HOME"
  echo "WARNING: /workspace not found -> using $HOME, which is NOT persistent across"
  echo "         a pod relaunch. Attach a RunPod network volume at /workspace to fix this."
fi
REPO_DIR="$WORKDIR/E-HGATv2"
echo "==> Workdir: $REPO_DIR (persistent=$([ "$WORKDIR" = /workspace ] && echo yes || echo NO))"

# 2. Clone or update the repo.
if [ -d "$REPO_DIR/.git" ]; then
  echo "==> Repo present; fetching latest $BRANCH"
  git -C "$REPO_DIR" fetch --all --prune
  git -C "$REPO_DIR" checkout "$BRANCH"
  git -C "$REPO_DIR" pull --ff-only
else
  echo "==> Cloning $REPO_SLUG@$BRANCH"
  if [ -n "${GH_TOKEN:-}" ]; then
    git clone --branch "$BRANCH" "https://${GH_TOKEN}@github.com/${REPO_SLUG}.git" "$REPO_DIR"
    # SECURITY: never leave the token embedded in the stored remote URL.
    git -C "$REPO_DIR" remote set-url origin "https://github.com/${REPO_SLUG}.git"
  else
    git clone --branch "$BRANCH" "git@github.com:${REPO_SLUG}.git" "$REPO_DIR"
  fi
fi
cd "$REPO_DIR"

# 3. Create / reuse the venv inside the persistent dir.
PY="${PYTHON:-python3}"
if [ ! -d "$REPO_DIR/.venv" ]; then
  echo "==> Creating venv with $("$PY" --version)"
  "$PY" -m venv "$REPO_DIR/.venv"
fi
# shellcheck disable=SC1091
source "$REPO_DIR/.venv/bin/activate"
python -m pip install --upgrade pip wheel

# 4. Torch first, so the correct CPU/CUDA build is pinned before PyG resolves it.
if [ "${GPU:-0}" = "1" ]; then
  echo "==> Installing CUDA torch (cu124)"
  pip install torch --index-url https://download.pytorch.org/whl/cu124
else
  echo "==> Installing CPU torch (deterministic; ideal for this CPU-bound workload)"
  pip install torch --index-url https://download.pytorch.org/whl/cpu
fi

# 5. Project + heavy extras (torch-geometric, xgboost, shap, sklearn, matplotlib).
echo "==> Installing E-HGATv2 with [learn,viz] extras"
pip install -e ".[learn,viz]"

# 6. Smoke check: imports + a 1-line surrogate-free sanity import.
python - <<'PY'
import torch, torch_geometric
import ehgat  # noqa: F401
print("torch", torch.__version__, "| cuda", torch.cuda.is_available(),
      "| pyg", torch_geometric.__version__)
print("ehgat import OK")
PY

echo
echo "SETUP COMPLETE."
echo "  repo : $REPO_DIR"
echo "  venv : source $REPO_DIR/.venv/bin/activate"
echo "  cores: $(nproc)"
