"""Profile where the search time goes at N=160: exact-eval (CPU, un-GPU-able) vs
GNN screening (GPU-able). Times mp-BRKGA (pure CPU exact) and TAPE-guided on CPU vs CUDA
for a few generations, plus raw evaluate() throughput. Extrapolates a full 40-gen run.

    python scripts/profile_n160.py --n 160 --gens 4
"""
from __future__ import annotations

import argparse
import os
import time

os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=160)
    ap.add_argument("--gens", type=int, default=4)
    ap.add_argument("--p-mult", type=int, default=5)
    ap.add_argument("--screening", type=int, default=2)
    ap.add_argument("--full-gens", type=int, default=40)
    args = ap.parse_args()

    import torch

    from ehgat.baselines.mp_brkga import MpBRKGAConfig, run_mp_brkga
    from ehgat.environment.decoder import NUM_BLOCKS, decode
    from ehgat.environment.evaluator import evaluate
    from ehgat.environment.instance import build_toy_instance, scaled_fleet
    from ehgat.explain.train_fused import FusedTrainConfig, build_core, train_fused
    from ehgat.search.attention_nsga2 import AttentionNSGA2Config, run_attention_nsga2
    from ehgat.utils.seeding import make_rng

    n = args.n
    agvs, qcs = scaled_fleet(n)
    inst = build_toy_instance(num_tasks=n, qcs=tuple(f"QC{i+1}" for i in range(qcs)),
                              num_agvs=agvs)
    base = args.p_mult * n
    matched = 4 * base
    G = args.gens
    print(f"N={n} fleet=({agvs}agv,{qcs}qc) base_pop={base} matched_pop={matched} "
          f"gens={G} screening={args.screening} cuda={torch.cuda.is_available()}", flush=True)

    # raw exact-eval throughput
    rng = make_rng(1)
    scheds = [decode(rng.random(NUM_BLOCKS * n), inst) for _ in range(200)]
    t = time.perf_counter()
    for s in scheds:
        evaluate(s, inst)
    dt = time.perf_counter() - t
    eps = 200 / dt
    print(f"[exact-eval] {eps:.0f} evals/s at N={n}  ({dt*1000/200:.2f} ms/eval)", flush=True)

    # cheap valid model (timing doesn't need accuracy)
    core = build_core(inst, seed=0, num_samples=120, epochs=3, device="cpu")
    fused = train_fused(inst, core, FusedTrainConfig(num_samples=100, epochs=3, seed=0)).model

    def time_run(fn):
        t0 = time.perf_counter()
        fn()
        if torch.cuda.is_available():
            torch.cuda.synchronize()
        return time.perf_counter() - t0

    # mp-BRKGA (pure CPU exact)
    mp_t = time_run(lambda: run_mp_brkga(inst, MpBRKGAConfig(pop_size=base, generations=G, seed=0)))
    print(f"[mp-BRKGA]   {mp_t:.1f}s / {G} gens  -> ~{mp_t/G*args.full_gens:.0f}s at {args.full_gens} gens", flush=True)

    # TAPE-guided CPU
    fcpu = fused.cpu()
    cfg = AttentionNSGA2Config(matched, G, seed=0, guidance="tape", screening_factor=args.screening)
    cpu_t = time_run(lambda: run_attention_nsga2(inst, None, cfg, fused_model=fcpu))
    print(f"[TAPE-cpu]   {cpu_t:.1f}s / {G} gens  -> ~{cpu_t/G*args.full_gens:.0f}s at {args.full_gens} gens", flush=True)

    # TAPE-guided CUDA
    if torch.cuda.is_available():
        fgpu = fused.to("cuda")
        gpu_t = time_run(lambda: run_attention_nsga2(inst, None, cfg, fused_model=fgpu))
        print(f"[TAPE-cuda]  {gpu_t:.1f}s / {G} gens  -> ~{gpu_t/G*args.full_gens:.0f}s at {args.full_gens} gens  "
              f"(speedup {cpu_t/gpu_t:.2f}x)", flush=True)


if __name__ == "__main__":
    main()
