from backend.mock_modules import *
from backend.schemas import EnrichedEvent


def run_full_pipeline(persona: str):
    posts = collect()
    events = detect(posts)
    events = compute(events)

    emotions = analyze(events)
    fake = check(events)

    enriched = []

    for e in events:
        enriched.append(
            EnrichedEvent(
                event_id=e.event_id,
                keywords=e.keywords,
                category=e.category,
                region=e.region,
                volume=e.volume,
                growth=e.growth,
                engagement=e.engagement,
                viral_score=e.viral_score,
                emotion=emotions[e.event_id],
                fake_score=fake[e.event_id]
            )
        )

    return generate(enriched, persona)