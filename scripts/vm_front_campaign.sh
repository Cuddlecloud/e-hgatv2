#!/usr/bin/env bash
# Front-behaviour campaign, run unattended on the compute instance.
#
# Three families in increasing cost order, so a later failure cannot cost the earlier results:
#   1. loading    -- Table 5 as printed, the family every prior result used
#   2. unloading  -- the same rows with origin and destination reversed
#   3. mixed      -- one loading instance concatenated with one unloading instance
#
# Each family writes its own JSON. Worker count is set from the core count rather than fixed:
# no surrogate is fitted here, so a worker holds roughly 320 MiB and memory is not the limit.

set -u

cd /workspace/ehgat
source /venv/main/bin/activate
export PYTHONPATH=/workspace/ehgat/src

CORES=$(nproc)
WORKERS=$(( CORES > 200 ? 200 : CORES ))     # past ~200 the largest mixed instances straggle
echo "[vm] $CORES cores detected, using $WORKERS workers"

python scripts/build_instance_families.py || exit 1

for FAM in loading unloading mixed; do
  echo "[vm] === $FAM ==="
  python scripts/run_front_campaign.py \
      --families "$FAM" \
      --fleet 1,2,3,4,5,6,7,8,9 \
      --seeds 10 \
      --generations 100 \
      --workers "$WORKERS" \
      --out "experiments/front_campaign/$FAM" \
      2>&1 | tail -12
  echo "[vm] $FAM done: $(date -Is)"
done

echo "[vm] all families complete"
du -sh experiments/front_campaign/*
