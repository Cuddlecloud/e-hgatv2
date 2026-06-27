#!/usr/bin/env bash
# Stage-1 fan-out: compute & cache front data for each instance spec passed as args,
# one process per instance, $JOBS at a time. Skips specs already cached. Designed for
# the high-core VM so independent per-instance pipelines run concurrently.
#
# Usage: JOBS=24 scripts/compute_front_cache.sh L01 L02 ... [-- <extra run_front_learning args>]
set -euo pipefail

JOBS="${JOBS:-16}"
CACHE_DIR="${CACHE_DIR:-experiments/front_learning/cache}"
LOG_DIR="${LOG_DIR:-/tmp/r4_logs}"
mkdir -p "$LOG_DIR" "$CACHE_DIR"

SPECS=()
EXTRA=()
seen_dd=0
for a in "$@"; do
  if [ "$a" = "--" ]; then seen_dd=1; continue; fi
  if [ "$seen_dd" -eq 1 ]; then EXTRA+=("$a"); else SPECS+=("$a"); fi
done

printf '%s\n' "${SPECS[@]}" | xargs -P "$JOBS" -I {} bash -c '
  spec="$1"; shift
  safe=$(echo "$spec" | tr ":/" "__")
  cache="'"$CACHE_DIR"'/front_${safe}.json"
  log="'"$LOG_DIR"'/${safe}.log"
  if [ -s "$cache" ]; then echo "[skip] $spec"; exit 0; fi
  if uv run python scripts/run_front_learning.py \
       --compute-instance "$spec" --cache-dir "'"$CACHE_DIR"'" "$@" >"$log" 2>&1; then
    echo "[done] $spec"
  else
    echo "[FAIL] $spec"; tail -2 "$log"
  fi
' _ {} "${EXTRA[@]}"
echo "=== stage-1 fan-out complete ==="
