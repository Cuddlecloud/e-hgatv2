"""Module 3: the E-HGATv2 surrogate (heterogeneous max-plus GATv2) + XGBoost baseline.

Submodules import Torch / PyTorch-Geometric, which are part of the optional ``learn``
extra. They are therefore imported lazily (``import ehgat.surrogate.graph``) rather than
eagerly here, so the environment / oracle / BRKGA layers stay Torch-free.
"""
