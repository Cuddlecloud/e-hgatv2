"""Throughput profiler for the E-HGATv2 surrogate inference path (graphs/sec).

Measures the three regimes that matter for making the GPU the load-bearer of the
attention-guided NSGA-II search:

  1. build        -- HeteroData construction (pure-Python, CPU) per schedule
  2. serial-cpu   -- model.predict / .attention one graph at a time (what the search does now)
  3. batch-cpu    -- one forward over a PyG mini-batch on CPU
  4. batch-gpu    -- one forward over a PyG mini-batch on CUDA (incl. H2D transfer + sync)

Run on the box:  PYTHONPATH=src python scripts/profile_gpu_inference.py
"""

from __future__ import annotations

import time

import numpy as np
import torch
from torch_geometric.data import Batch

from ehgat.environment.decoder import NUM_BLOCKS, decode
from ehgat.environment.instance import build_toy_instance
from ehgat.surrogate.ehgatv2 import EHGATv2, EHGATv2Config
from ehgat.surrogate.graph import build_hetero_graph


def _sync(device: torch.device) -> None:
    if device.type == "cuda":
        torch.cuda.synchronize()


def _time(fn, *, device: torch.device, repeats: int, warmup: int = 2) -> float:
    for _ in range(warmup):
        fn()
    _sync(device)
    t0 = time.perf_counter()
    for _ in range(repeats):
        fn()
    _sync(device)
    return (time.perf_counter() - t0) / repeats


def _make_pool(inst, k: int, seed: int = 0) -> list:
    rng = np.random.default_rng(seed)
    chrom = NUM_BLOCKS * inst.num_tasks
    return [build_hetero_graph(decode(rng.random(chrom), inst), inst) for _ in range(k)]


def main() -> None:
    has_cuda = torch.cuda.is_available()
    gpu = torch.device("cuda") if has_cuda else None
    cpu = torch.device("cpu")
    print(f"torch {torch.__version__}  cuda={has_cuda}  "
          f"devices={torch.cuda.device_count() if has_cuda else 0}")
    if has_cuda:
        print(f"gpu0 = {torch.cuda.get_device_name(0)}")
    print()

    model = EHGATv2(EHGATv2Config()).eval()
    pool_size = 2048
    cpu_batches = (64, 256)
    gpu_batches = (256, 1024, 4096, 8192)

    for n in (10, 20, 50, 100):
        inst = build_toy_instance(num_tasks=n)
        # --- build throughput (CPU, per-graph) ---
        rng = np.random.default_rng(0)
        chrom = NUM_BLOCKS * n
        scheds = [decode(rng.random(chrom), inst) for _ in range(256)]
        t_build = _time(
            lambda: [build_hetero_graph(s, inst) for s in scheds],
            device=cpu, repeats=2,
        ) / len(scheds)
        print(f"N={n:<4} build: {1.0/t_build:,.0f} graphs/s  ({t_build*1e3:.3f} ms/graph)", flush=True)

        pool = _make_pool(inst, pool_size)

        # --- serial CPU predict (the current search regime) ---
        sub = pool[:128]
        t_serial = _time(
            lambda: [model.predict(g) for g in sub], device=cpu, repeats=2,
        ) / len(sub)
        print(f"        serial-cpu predict: {1.0/t_serial:,.0f} graphs/s", flush=True)

        # --- batched CPU + GPU across batch sizes ---
        for dev in ([cpu, gpu] if has_cuda else [cpu]):
            m = model.to(dev)
            batches = gpu_batches if dev.type == "cuda" else cpu_batches
            for bs in batches:
                reps = max(bs // pool_size, 1)  # tile the pool if bs > pool
                graphs = (pool * reps)[:bs] if bs > pool_size else pool[:bs]

                def run_pred() -> None:
                    batch = Batch.from_data_list(graphs).to(dev)
                    with torch.no_grad():
                        m.predict(batch)

                def run_attn() -> None:
                    batch = Batch.from_data_list(graphs).to(dev)
                    with torch.no_grad():
                        m.attention(batch)

                t_p = _time(run_pred, device=dev, repeats=5)
                t_a = _time(run_attn, device=dev, repeats=5)
                tag = "batch-gpu" if dev.type == "cuda" else "batch-cpu"
                print(f"        {tag} bs={bs:<5} predict: {bs/t_p:,.0f} g/s   "
                      f"attention: {bs/t_a:,.0f} g/s", flush=True)
        model = model.to(cpu)
        print(flush=True)


if __name__ == "__main__":
    main()
