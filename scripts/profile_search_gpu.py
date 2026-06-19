"""End-to-end attention-NSGA-II throughput: surrogate on CPU vs GPU.

The attention-guided mutation now issues ONE batched ``model.attention`` per generation
(``_batch_attention_signals``) instead of one serial forward per child, so placing the
model on CUDA makes the surrogate the GPU's load. The exact ``evaluate`` fitness stays on
CPU (it is the ground-truth judge), so this measures the realisable end-to-end speedup.

Run:  PYTHONPATH=src python scripts/profile_search_gpu.py
"""

from __future__ import annotations

import time

import torch

from ehgat.environment.instance import build_toy_instance
from ehgat.search.attention_nsga2 import AttentionNSGA2Config, run_attention_nsga2
from ehgat.surrogate.ehgatv2 import EHGATv2, EHGATv2Config


def _run(model: EHGATv2, inst, cfg: AttentionNSGA2Config) -> float:
    t0 = time.perf_counter()
    run_attention_nsga2(inst, model, cfg)
    if next(model.parameters()).device.type == "cuda":
        torch.cuda.synchronize()
    return time.perf_counter() - t0


def main() -> None:
    has_cuda = torch.cuda.is_available()
    print(f"cuda={has_cuda}  device={torch.cuda.get_device_name(0) if has_cuda else 'cpu'}\n")

    for n in (20, 50):
        inst = build_toy_instance(num_tasks=n)
        cfg = AttentionNSGA2Config(
            pop_size=20 * n,
            generations=8,
            operator_selection="attention",
            operator_granularity="per_task",
            seed=0,
        )
        base = EHGATv2(EHGATv2Config()).eval()

        cpu_t = _run(base, inst, cfg)
        line = f"N={n:<4} pop={20*n} gens={cfg.generations}  CPU: {cpu_t:.2f}s"
        if has_cuda:
            gpu_t = _run(base.to("cuda"), inst, cfg)
            base.to("cpu")
            line += f"   GPU: {gpu_t:.2f}s   speedup: {cpu_t / gpu_t:.2f}x"
        print(line, flush=True)


if __name__ == "__main__":
    main()
