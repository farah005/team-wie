from backend.mock_modules import *
from backend.schemas import EnrichedEvent

try:
    from backend.services.real_pipeline import run_real_pipeline
except Exception:
    run_real_pipeline = None


def run_full_pipeline(persona: str):
    if run_real_pipeline:
        try:
            result = run_real_pipeline(save=True)
            top_events = sorted(
                result.get("posts", []),
                key=lambda post: float(post.get("viral_score") or 0),
                reverse=True,
            )[:10]
            return {
                "persona": persona,
                "top_events": top_events,
                "alerts": [
                    f"{post.get('region', 'Tunisie')}: {post.get('summary') or post.get('content', '')}"
                    for post in top_events[:3]
                ],
                "recommendations": [
                    {
                        "message": "Verifier les signaux a fort viral_score et fake_score avant publication.",
                        "priority": 1,
                    }
                ],
                "sources": result.get("sources", []),
                "count": result.get("count", 0),
                "mode": result.get("mode", "real"),
                "backup_count": result.get("backup_count", 0),
            }
        except Exception as exc:
            print(f"Real pipeline fallback used: {exc}")

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
