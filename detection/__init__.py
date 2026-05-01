"""
PulseTN Persona - Detection Package
Membre 2 : Event Detection + Viral Score Engine
"""

from .event_detector import (
    analyze_posts,
    detect_region,
    categorize_event,
    detect_signal_strength,
    enrich_post,
    get_top_events
)

from .viral_score import (
    calculate_viral_score,
    normalize
)

__all__ = [
    "analyze_posts",
    "detect_region",
    "categorize_event",
    "detect_signal_strength",
    "enrich_post",
    "get_top_events",
    "calculate_viral_score",
    "normalize"
]