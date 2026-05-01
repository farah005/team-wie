from backend.services.pipeline import run_full_pipeline

def test_pipeline():
    result = run_full_pipeline("journaliste")

    assert "top_events" in result
    assert "recommendations" in result