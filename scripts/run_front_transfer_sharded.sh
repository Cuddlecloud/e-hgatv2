#!/usr/bin/env bash
# Shard driver for the cross-instance front-transfer study.
#
# Each shard is one (held-out instance, seed) pair and writes its own JSON, so the
# independent CPU-bound pipelines fan across cores without contending for output.
# Per-process thread pools are pinned to one thread; oversubscribing BLAS across
# many concurrent shards degrades throughput without improving latency.
#
# Usage:
#   scripts/run_front_transfer_sharded.sh "<train specs>" "<test specs>" <seeds> [jobs] [extra...]
#
# Example (train on twelve L instances, hold out five, ten seeds, 100 workers):
#   scripts/run_front_transfer_sharded.sh \
#     "L01 L02 L03 L04 L05 L06 L08 L09 L10 L11 L12 L13" \
#     "L07 L15 L21 L28 L35" 10 100

set -euo pipefail

TRAIN="${1:?train specs}"
TEST="${2:?test specs}"
SEEDS="${3:-10}"
JOBS="${4:-16}"
shift 4 || shift $#
EXTRA=("$@")

OUT_DIR="${OUT_DIR:-experiments/front_transfer}"
LOG_DIR="${LOG_DIR:-/tmp/front_transfer_logs}"
PY="${PY:-.venv/bin/python}"
mkdir -p "$OUT_DIR" "$LOG_DIR"

export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export KMP_DUPLICATE_LIB_OK=TRUE

# Reject overlap here as well as in the script: a shard that trains and tests on
# the same instance would silently invalidate the transfer claim.
for t in $TEST; do
  for r in $TRAIN; do
    [[ "$t" == "$r" ]] && { echo "train/test overlap: $t" >&2; exit 1; }
  done
done

JOBLIST="$LOG_DIR/joblist.txt"
: >"$JOBLIST"
for spec in $TEST; do
  for ((s = 0; s < SEEDS; s++)); do
    echo "$spec $s" >>"$JOBLIST"
  done
done

N=$(wc -l <"$JOBLIST" | tr -d ' ')
echo "=== ${N} shards over ${JOBS} workers ==="
echo "train: $TRAIN"
echo "test : $TEST   seeds: 0..$((SEEDS - 1))"
date

# shellcheck disable=SC2016
awk '{print}' "$JOBLIST" | xargs -P "$JOBS" -L1 bash -c '
  spec="$1"; seed="$2"
  out="'"$OUT_DIR"'/shard_${spec}_s${seed}.json"
  log="'"$LOG_DIR"'/${spec}_s${seed}.log"
  if [[ -s "$out" ]]; then echo "skip ${spec} s${seed} (exists)"; exit 0; fi
  if '"$PY"' scripts/run_front_transfer.py \
       --train '"$TRAIN"' --test "$spec" --seed "$seed" \
       --out "$out" '"${EXTRA[*]:-}"' >"$log" 2>&1; then
    echo "ok   ${spec} s${seed}"
  else
    echo "FAIL ${spec} s${seed} -- see ${log}"
  fi
' _

echo "=== done ==="
date
ls -1 "$OUT_DIR"/shard_*.json 2>/dev/null | wc -l | xargs echo "shards written:"
grep -l . "$LOG_DIR"/*.log 2>/dev/null | wc -l | xargs echo "logs:"
