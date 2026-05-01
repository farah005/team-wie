from backend.schemas import Post, Event, EmotionScore, Analysis

# ✅ Test Post valide
post = Post(
    id="1",
    text="Accident à Tunis",
    source="facebook",
    timestamp="2026-01-01T10:00:00",
    region="Tunis",
    engagement=120
)

print("Post OK:", post)


# ✅ Test Event valide
event = Event(
    event_id="e1",
    keywords=["accident", "tunis"],
    category="accident",
    region="Tunis",
    volume=50,
    growth=10,
    engagement=200,
    viral_score=85
)

print("Event OK:", event)


# ✅ Test Analysis valide
analysis = Analysis(
    event_id="e1",
    emotion=EmotionScore(
        joy=10,
        anger=70,
        fear=60,
        sadness=30
    ),
    fake_score=20
)

print("Analysis OK:", analysis)