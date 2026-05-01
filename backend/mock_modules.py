from backend.schemas import Post, Event, EmotionScore


def collect():
    return [
        Post(
            id="1",
            text="Accident à Tunis",
            source="facebook",
            timestamp="2026-01-01T10:00:00",
            region="Tunis",
            engagement=120
        )
    ]


def detect(posts):
    return [
        Event(
            event_id="e1",
            keywords=["accident"],
            category="accident",
            region="Tunis",
            volume=50,
            growth=10,
            engagement=200,
            viral_score=80
        )
    ]


def compute(events):
    return events


def analyze(events):
    return {
        "e1": EmotionScore(joy=10, anger=70, fear=60, sadness=30)
    }


def check(events):
    return {
        "e1": 20
    }


def generate(events, persona):
    return {
        "persona": persona,
        "top_events": events,
        "alerts": ["Test alert"],
        "recommendations": [
            {"message": "Suivre l’événement", "priority": 1}
        ]
    }