#!/usr/bin/env bash
# Thesis data collection driver, run unattended on the compute instance.
#
# Three campaigns in increasing cost order, so the cheap and most load-bearing evidence lands
# first and a later failure cannot cost the earlier results:
#
#   1. L   -- the 35 published loading instances, whose boundaries can be checked against the
#             book chapter's exact MILP optima.
#   2. DL  -- the author's ten large instances on his own recovered geometry.
#   3. fleet -- the vehicle-per-crane sweep. This is the one the front-behaviour claim rests on:
#             the published sets hold the ratio nearly fixed, and the transport share only moves
#             when the ratio does.
#
# Every campaign writes its own JSON, so partial completion is still usable.

set -u  # a failing campaign must not abort the ones after it, so -e is deliberately omitted

cd /workspace/ehgat
source /venv/main/bin/activate

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export THREADS_PER_WORKER=1

WORKERS="${WORKERS:-88}"
SEEDS="${SEEDS:-10}"
GENS="${GENS:-300}"
LOGS=experiments/thesis/logs
mkdir -p "$LOGS"

echo "=== driver start $(date -u +%FT%TZ) | workers=$WORKERS seeds=$SEEDS Gmax=$GENS ==="

echo "--- [1/3] L set (35 instances) ---"
python scripts/run_thesis_experiments.py \
    --set L --seeds "$SEEDS" --generations "$GENS" \
    --workers "$WORKERS" --tag L_full > "$LOGS/L_full.log" 2>&1
echo "L set rc=$? $(date -u +%FT%TZ)"

echo "--- [2/3] DL set (10 instances) ---"
python scripts/run_thesis_experiments.py \
    --set DL --seeds "$SEEDS" --generations "$GENS" \
    --workers "$WORKERS" --tag DL_full > "$LOGS/DL_full.log" 2>&1
echo "DL set rc=$? $(date -u +%FT%TZ)"

# Fleet sizes span A/Q from 1/6 to 6 across these four instances (2, 3, 6 and 8 cranes), which
# brackets the author's own published range of 0.67-2.33 on both sides.
echo "--- [3/3] fleet sweep ---"
python scripts/run_thesis_experiments.py \
    --set fleet --instances L15 L21 L35 DL01 \
    --agv-sweep 1 2 3 4 6 8 12 --seeds 5 --generations "$GENS" \
    --workers "$WORKERS" --tag fleet_sweep > "$LOGS/fleet_sweep.log" 2>&1
echo "fleet sweep rc=$? $(date -u +%FT%TZ)"

echo "=== driver done $(date -u +%FT%TZ) ==="
ls -la experiments/thesis/*.json
