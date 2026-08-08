#!/usr/bin/env bash
# Simultaneous k-ablation: does cranking screening (k=8,16) tip the large-N ties vs mp-BRKGA?
# Config is IDENTICAL to the running native sweep (launch_native_overnight.sh / run_opt_scaling
# COMMON) except --screening, so k=8/16 are apples-to-apples with the k=2 native baseline on the
# SAME seeds (0-3). `nice -n 15` so it yields cores to the running native sweep.
cd /workspace/e-hgatv2
source /venv/main/bin/activate

OUT=experiments/fused_tape_guided/kabl_natfull
mkdir -p "$OUT/logs"

# matched to native sweep COMMON (p-mult 5 => native budget, gens 40, ref-gens 15)
COMMON="--gens 40 --p-mult 5 --core-samples 800 --core-epochs 40 \
  --fused-samples 600 --fused-epochs 40 --faith-samples 30 --ref-gens 15 \
  --device cpu --search-device cpu --seeds 4 --seed-start 0"

launch() {  # mode N k
  local mode=$1 n=$2 k=$3 pp=""
  [[ "$mode" == pp* ]] && pp="--peak-power ${mode#pp}"
  local tag="${mode}_n${n}_k${k}"
  OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 KMP_DUPLICATE_LIB_OK=TRUE \
    nohup nice -n 15 python scripts/run_tape_guided_bench.py \
      --instance "toy:$n" $pp --screening "$k" $COMMON \
      --out-tag "$tag" --out-dir "$OUT" \
      > "$OUT/logs/$tag.log" 2>&1 &
  echo "  launched $tag (pid $!)"
}

echo "[kabl] $(date) launching k-ablation into $OUT"
for mode in unc pp30; do
  for n in 40 80; do
    for k in 8 16; do
      launch "$mode" "$n" "$k"
    done
  done
done
echo "[kabl] all 8 processes launched (nice 15, 4 seeds each)."
