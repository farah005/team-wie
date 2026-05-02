import sqlite3
from pathlib import Path

from analysis.fake_detector import process_post
from analysis.summarizer import summarize_posts
from data.source_collectors import collect_all_sources
from detection.event_detector import analyze_posts


BASE_DIR = Path(__file__).resolve().parents[2]
PULSE_DB = BASE_DIR / "engine" / "pulseTN.db"


EMOTION_LABELS = {
    "anger": "Colere",
    "panic": "Panique",
    "sadness": "Tristesse",
    "hype": "Hype",
    "humor": "Humour",
    "solidarity": "Joie",
    "neutral": "Neutre",
}


def _ensure_posts_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            post_id TEXT PRIMARY KEY,
            region TEXT,
            platform TEXT,
            source TEXT,
            content TEXT,
            category TEXT,
            emotion TEXT,
            viral_score REAL DEFAULT 0,
            fake_score REAL DEFAULT 0,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()


def _save_posts(posts):
    conn = sqlite3.connect(PULSE_DB)
    try:
        _ensure_posts_table(conn)
        columns = {row[1]: row[2].upper() for row in conn.execute("PRAGMA table_info(posts)").fetchall()}
        uses_integer_id = "INT" in columns.get("post_id", "")
        for post in posts:
            values = {
                "post_id": post.get("post_id"),
                "region": post.get("region"),
                "platform": post.get("platform"),
                "source": post.get("source"),
                "content": post.get("summary") or post.get("content"),
                "category": post.get("category"),
                "emotion": post.get("emotion"),
                "viral_score": post.get("viral_score", 0),
                "fake_score": post.get("fake_score", 0),
                "timestamp": post.get("timestamp"),
            }
            write_columns = [
                "region", "platform", "source", "content", "category",
                "emotion", "viral_score", "fake_score", "timestamp",
            ]
            if not uses_integer_id:
                write_columns.insert(0, "post_id")
            placeholders = ", ".join(["?"] * len(write_columns))
            conn.execute(
                f"INSERT OR REPLACE INTO posts ({', '.join(write_columns)}) VALUES ({placeholders})",
                [values[column] for column in write_columns],
            )
        conn.commit()
    finally:
        conn.close()


def run_real_pipeline(save=True):
    raw_posts = collect_all_sources(use_backup=True)
    detected = analyze_posts(raw_posts)
    summarized = summarize_posts(detected)

    enriched = []
    for post in summarized:
        analyzed = process_post(post)
        analyzed["summary"] = post.get("summary") or analyzed.get("content")
        analyzed["summarizer"] = post.get("summarizer", "local_nlp")
        analyzed["emotion"] = EMOTION_LABELS.get(analyzed.get("emotion"), analyzed.get("emotion", "Neutre"))
        enriched.append(analyzed)

    if save:
        _save_posts(enriched)

    return {
        "count": len(enriched),
        "mode": "simulation_backup" if any(post.get("backup") for post in enriched) else "real",
        "backup_count": sum(1 for post in enriched if post.get("backup")),
        "sources": sorted({post.get("platform", "Unknown") for post in enriched}),
        "posts": enriched,
    }
