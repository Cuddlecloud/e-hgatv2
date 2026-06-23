#!/bin/bash
# Parallel driver for the faithful-guidance (Req 2+3) matrix on the VM.
# Each config is an independent 1-thread process; the box has ~122 usable cores.
# Budget is matched across all methods (P=p_mult*N per population; GAT/BRKGA pop=4P).
set -u
cd /workspace/e-hgatv2
source /venv/main/bin/activate
OUT=experiments/fused_tape_guided
mkdir -p "$OUT/logs"

COMMON="--seeds 5 --gens 40 --screening 2 --p-mult 5 \
  --core-samples 800 --core-epochs 40 --fused-samples 600 --fused-epochs 40 \
  --faith-samples 30 --ref-gens 50 --device cuda"

run() {  # tag, extra-args...
  local tag="$1"; shift
  OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 KMP_DUPLICATE_LIB_OK=TRUE \
    nohup python scripts/run_tape_guided_bench.py "$@" $COMMON \
    > "$OUT/logs/$tag.log" 2>&1 &
  echo "launched $tag (pid $!)"
}

# uncoupled scaling
run toy5  --instance toy:5
run toy8  --instance toy:8
run toy10 --instance toy:10
run toy15 --instance toy:15
run toy20 --instance toy:20
# coupled (peak-power) -- the "GNN necessary" regime
run toy10_pp30 --instance toy:10 --peak-power 30
run toy20_pp30 --instance toy:20 --peak-power 30
# real published L-instances (loading set)
run L07 --instance L07
run L15 --instance L15
run L21 --instance L21
run L35 --instance L35

echo "all launched at $(date +%s); waiting ..."
wait
echo "MATRIX_DONE at $(date +%s)"
