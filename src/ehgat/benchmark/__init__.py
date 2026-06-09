"""Module 5: the effectiveness benchmark (multi-seed runs, faithfulness, plots).

Submodules import Torch (the surrogate), ``scipy``/``matplotlib`` and the optional
``viz`` extra, so they are imported lazily (``import ehgat.benchmark.runner``) to keep the
Torch-free environment / oracle / BRKGA layers importable on their own.
"""
