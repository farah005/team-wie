# interfaces.py — Membre 5 : Backend
# =====================================
# Définit les contrats (signatures) entre tous les membres.
# Chaque membre implémente sa fonction ici.

from typing import List, Dict
from backend.schemas import Post, Event, EmotionScore, EnrichedEvent, Dashboard

# ──────────────────────────────────────────
# Membre 1 — Data Collection
# ──────────────────────────────────────────
def collect() -> List[Post]:
    """Retourne la liste des posts collectés depuis les sources."""
    pass


# ──────────────────────────────────────────
# Membre 2 — Event Detection
# ──────────────────────────────────────────
def detect(posts: List[Post]) -> List[Event]:
    """Détecte les événements à partir des posts."""
    pass


def compute(events: List[Event]) -> List[Event]:
    """Calcule le viral score et enrichit les events."""
    pass


# ──────────────────────────────────────────
# Membre 3 — Analysis
# ──────────────────────────────────────────
def analyze(events: List[Event]) -> Dict[str, EmotionScore]:
    """Retourne les émotions par event_id."""
    pass


def check(events: List[Event]) -> Dict[str, float]:
    """Retourne fake news score par event_id."""
    pass


# ──────────────────────────────────────────
# Membre 4 — Persona Engine  ← BRANCHÉ ICI
# ──────────────────────────────────────────
def generate(events: List[EnrichedEvent], persona: str) -> dict:
    """
    Génère le dashboard personnalisé selon le persona.
    Délègue à persona_engine.generate() du Membre 4.
    """
    import sys
    import os
    # Ajoute le dossier engine/ au path pour importer persona_engine
    engine_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "engine")
    if engine_path not in sys.path:
        sys.path.insert(0, engine_path)

    from persona_engine import generate as persona_generate
    return persona_generate(events, persona)