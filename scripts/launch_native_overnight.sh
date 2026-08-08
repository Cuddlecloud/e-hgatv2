#!/usr/bin/env bash
# Overnight native-budget (P=20N) optimization scaling to N=160, both regimes.
# Run inside tmux so it survives SSH disconnect:
#   tmux new-session -d -s native 'bash scripts/launch_native_overnight.sh'
# NOTE: no `set -u` -- venv activate references unset vars and would abort the script.
cd /workspace/e-hgatv2
source /venv/main/bin/activate

export TOTAL_SEEDS=8 PER_SHARD=1 GENS=40 REFGENS=15 SEARCH_DEV=cpu
export NS="10 20 40 80 160"

echo "[native] $(date) starting both regimes: NS=[$NS] seeds=$TOTAL_SEEDS gens=$GENS refgens=$REFGENS"

bash scripts/run_opt_scaling.sh unc  experiments/fused_tape_guided/scaling_natfull_unc \
    > experiments/fused_tape_guided/scaling_natfull_unc.log  2>&1 &
UNC=$!
bash scripts/run_opt_scaling.sh pp30 experiments/fused_tape_guided/scaling_natfull_pp30 \
    > experiments/fused_tape_guided/scaling_natfull_pp30.log 2>&1 &
PP=$!

wait "$UNC"; echo "[native] $(date) uncoupled done"
wait "$PP";  echo "[native] $(date) coupled done"
echo "[native] $(date) ALL DONE"
