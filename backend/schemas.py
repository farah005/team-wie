from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional, Literal


# -------------------------
# CONSTANTES
# -------------------------

ALLOWED_CATEGORIES = ["politique", "accident", "culture", "sport", "trend"]


# -------------------------
# POST (Membre 1)
# -------------------------
class Post(BaseModel):
    id: str = Field(..., min_length=1)
    text: str = Field(..., min_length=1)
    source: str
    timestamp: datetime
    region: str
    engagement: int = Field(ge=0)

    url: Optional[str] = None
    author: Optional[str] = None


# -------------------------
# EVENT (Membre 2)
# -------------------------
class Event(BaseModel):
    event_id: str
    keywords: List[str]
    category: Literal["politique", "accident", "culture", "sport", "trend"]
    region: str

    volume: float = Field(ge=0)
    growth: float = Field(ge=0)
    engagement: float = Field(ge=0)

    viral_score: float = Field(ge=0, le=100)

    @validator("keywords")
    def keywords_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError("keywords ne peut pas être vide")
        return v


# -------------------------
# EMOTION (Membre 3)
# -------------------------
class EmotionScore(BaseModel):
    joy: float = Field(ge=0, le=100)
    anger: float = Field(ge=0, le=100)
    fear: float = Field(ge=0, le=100)
    sadness: float = Field(ge=0, le=100)


class Analysis(BaseModel):
    event_id: str
    emotion: EmotionScore
    fake_score: float = Field(ge=0, le=100)


# -------------------------
# EVENT ENRICHI (fusion M2 + M3)
# -------------------------
class EnrichedEvent(BaseModel):
    event_id: str
    keywords: List[str]
    category: Literal["politique", "accident", "culture", "sport", "trend"]
    region: str

    volume: float = Field(ge=0)
    growth: float = Field(ge=0)
    engagement: float = Field(ge=0)
    viral_score: float = Field(ge=0, le=100)

    emotion: EmotionScore
    fake_score: float = Field(ge=0, le=100)


# -------------------------
# DASHBOARD (Membre 4)
# -------------------------
class Recommendation(BaseModel):
    message: str
    priority: int = Field(ge=1, le=5)  # 1 = urgent


class Dashboard(BaseModel):
    persona: Literal[
        "journaliste",
        "entreprise",
        "influenceur",
        "citoyen",
        "ong"
    ]
    top_events: List[EnrichedEvent]
    alerts: List[str]
    recommendations: List[Recommendation]


# -------------------------
# CONFIG Pydantic (optionnel mais pro)
# -------------------------
class Config:
    orm_mode = True
    validate_assignment = True