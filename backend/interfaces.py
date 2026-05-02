from typing import List, Dict
from backend.schemas import (
    Post,
    Event,
    EmotionScore,
    EnrichedEvent,
    Dashboard
)

# -------------------------
# Membre 1 — Data Collection
# -------------------------
def collect() -> List[Post]:
    """
    Retourne la liste des posts collectés depuis les sources.
    """
    pass


# -------------------------
# Membre 2 — Event Detection
# -------------------------
def detect(posts: List[Post]) -> List[Event]:
    """
    Détecte les événements à partir des posts.
    """
    pass


def compute(events: List[Event]) -> List[Event]:
    """
    Calcule le viral score et enrichit les events.
    """
    pass


# -------------------------
# Membre 3 — Analysis
# -------------------------
def analyze(events: List[Event]) -> Dict[str, EmotionScore]:
    """
    Retourne les émotions par event_id.
    """
    pass


def check(events: List[Event]) -> Dict[str, float]:
    """
    Retourne fake news score par event_id.
    """
    pass


# -------------------------
# Membre 4 — Persona Engine
# -------------------------
def generate(events: List[EnrichedEvent], persona: str) -> Dashboard:
    """
    Génère le dashboard personnalisé selon le persona.
    """
    pass