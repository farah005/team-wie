from backend.interfaces import *
from backend.schemas import EnrichedEvent, Dashboard
from backend.mock_modules import *


# -------------------------
# PIPELINE PRINCIPAL
# -------------------------
def run_pipeline(persona: str = "journaliste"):
    """
    Exécute tout le pipeline :
    collect → detect → compute → analyze → check → generate
    """

    # 1. COLLECTE
    posts = collect()

    # 2. DETECTION EVENTS
    events = detect(posts)

    # 3. VIRAL SCORE
    events = compute(events)

    # 4. ANALYSE EMOTIONNELLE
    emotions = analyze(events)

    # 5. FAKE NEWS DETECTION
    fake_scores = check(events)

    # 6. FUSION (enrichissement)
    enriched_events = []

    for event in events:
        enriched_events.append(
            EnrichedEvent(
                event_id=event.event_id,
                keywords=event.keywords,
                category=event.category,
                region=event.region,
                volume=event.volume,
                growth=event.growth,
                engagement=event.engagement,
                viral_score=event.viral_score,
                emotion=emotions.get(event.event_id),
                fake_score=fake_scores.get(event.event_id, 0)
            )
        )

    # 7. PERSONA ENGINE
    dashboard = generate(enriched_events, persona)

    return dashboard


# -------------------------
# TEST LOCAL
# -------------------------
if __name__ == "__main__":
    result = run_pipeline(persona="journaliste")

    print("\n===== DASHBOARD =====\n")
    print(result)
    