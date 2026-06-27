#!/usr/bin/env bash
# R4 parallel driver: compute each instance's front data in its own process so the
# independent, CPU-bound per-instance pipelines (core+fused training, NSGA-II, TAPE)
# run concurrently across the VM's many cores, then pool the caches and fit the
# predictor in a final cheap stage-2 step.
#
# Usage:
#   scripts/run_front_parallel.sh "<train specs>" "<test specs>" [jobs] [extra args...]
# Example (leave-one-QC-count-out: train spans qc∈{2,3,4,6}, hold out qc=5 + L07):
#   scripts/run_front_parallel.sh \
#     "toy:24:2:2 toy:40:2:3 toy:18:3:2 toy:36:3:3 toy:30:4:3 toy:48:4:4 toy:36:6:4 toy:54:6:5" \
#     "toy:30:5:3 toy:45:5:4 L07" 16 --pop 120 --gens 40
set -euo pipefail

TRAIN="${1:?train specs}"
TEST="${2:?test specs}"
JOBS="${3:-16}"
shift 3 || shift $#
EXTRA=("$@")

CACHE_DIR="experiments/front_learning/cache"
LOG_DIR="/tmp/r4_logs"
mkdir -p "$LOG_DIR"

ALL=$(echo "$TRAIN $TEST" | tr ' ' '\n' | sed '/^$/d' | sort -u)
echo "=== Stage 1: computing $(echo "$ALL" | wc -l | tr -d ' ') instances, ${JOBS} at a time ==="
echo "$ALL"

# Fan out one process per instance; xargs -P caps concurrency at $JOBS.
echo "$ALL" | xargs -P "$JOBS" -I {} bash -c '
  spec="$1"; shift
  safe=$(echo "$spec" | tr ":/" "__")
  log="'"$LOG_DIR"'/${safe}.log"
  cache="'"$CACHE_DIR"'/front_${safe}.json"
  if [ -s "$cache" ]; then echo "[skip]  $spec (cached)"; exit 0; fi
  echo "[start] $spec -> $log"
  if uv run python scripts/run_front_learning.py \
       --compute-instance "$spec" --cache-dir "'"$CACHE_DIR"'" "$@" >"$log" 2>&1; then
    echo "[done]  $spec"
  else
    echo "[FAIL]  $spec (see $log)"; tail -3 "$log"
  fi
' _ {} "${EXTRA[@]}"

echo "=== Stage 2: pooling caches and fitting predictor ==="
uv run python scripts/run_front_learning.py \
  --train-instances $TRAIN --test-instances $TEST \
  --cache-dir "$CACHE_DIR" "${EXTRA[@]}"