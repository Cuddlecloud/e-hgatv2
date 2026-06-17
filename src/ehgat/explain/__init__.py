"""Graph-native explainability utilities for E-HGATv2."""

from ehgat.explain.event_dag import EventDag, assemble_event_dag, extract_precedence
from ehgat.explain.fused_ehgat import FusedEHGATv2, FusedPrediction
from ehgat.explain.fused_explainer import (
    FaithfulnessReport,
    explain_fused,
    explain_fused_schedules,
    faithfulness_report,
    fused_pareto_tension_scores,
)
from ehgat.explain.pts_calculator import ParetoPoint, pareto_tension_scores
from ehgat.explain.tape_explainer import TapeExplanation, explain_schedule, explain_schedules
from ehgat.explain.tropical_dp import TropicalMaxPlus, tropical_longest_path, tropical_makespan

__all__ = [
    "EventDag",
    "FaithfulnessReport",
    "FusedEHGATv2",
    "FusedPrediction",
    "ParetoPoint",
    "TapeExplanation",
    "TropicalMaxPlus",
    "assemble_event_dag",
    "explain_fused",
    "explain_fused_schedules",
    "explain_schedule",
    "explain_schedules",
    "extract_precedence",
    "faithfulness_report",
    "fused_pareto_tension_scores",
    "pareto_tension_scores",
    "tropical_longest_path",
    "tropical_makespan",
]
