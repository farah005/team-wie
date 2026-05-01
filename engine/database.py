# database.py — Membre 4 : Persona Engine
# =========================================
# Gère la base de données pulseTN.db (tables users + posts)
# et peut également lire raw_data.db du Membre 1.

import sqlite3
import os
from datetime import datetime

# ── Chemins absolus (indépendants du répertoire de lancement) ──────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))   # .../engine/
PROJECT_DIR = os.path.dirname(BASE_DIR)                    # .../pulseTN/

# Base principale du Membre 4 (users + posts enrichis)
DB_PATH = os.path.join(BASE_DIR, "pulseTN.db")

# Base du Membre 1 (posts bruts collectés)
RAW_DB_PATH = os.path.join(PROJECT_DIR, "data", "raw_data.db")


def get_connection(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id           INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_type      TEXT    NOT NULL,
            region_preference TEXT    DEFAULT 'national',
            interest_category TEXT    DEFAULT 'general',
            created_at        TEXT    DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            post_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            region      TEXT,
            platform    TEXT,
            source      TEXT,
            content     TEXT,
            category    TEXT,
            emotion     TEXT,
            viral_score REAL    DEFAULT 0,
            fake_score  REAL    DEFAULT 0,
            timestamp   TEXT    DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print(f"✅ Tables créées dans : {DB_PATH}")


# ── CRUD Posts ─────────────────────────────────────────────────────────────────

def insert_post(region, platform, source, content,
                category="", emotion="", viral_score=0, fake_score=0):
    conn = get_connection()
    conn.execute("""
        INSERT INTO posts
            (region, platform, source, content, category,
             emotion, viral_score, fake_score, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (region, platform, source, content, category,
          emotion, viral_score, fake_score, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_recent_posts(limit: int = 50, region: str = None) -> list:
    conn = get_connection()
    if region:
        rows = conn.execute("""
            SELECT * FROM posts WHERE region = ?
            ORDER BY timestamp DESC LIMIT ?
        """, (region, limit)).fetchall()
    else:
        rows = conn.execute("""
            SELECT * FROM posts ORDER BY timestamp DESC LIMIT ?
        """, (limit,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_posts_by_category(category: str, limit: int = 20) -> list:
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM posts WHERE category = ?
        ORDER BY viral_score DESC LIMIT ?
    """, (category, limit)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_top_viral_posts(limit: int = 10) -> list:
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM posts ORDER BY viral_score DESC LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ── Lecture raw_data.db du Membre 1 ───────────────────────────────────────────

def get_raw_posts(limit: int = 100, region: str = None) -> list:
    """
    Lit les posts bruts depuis raw_data.db (Membre 1).
    Colonnes : post_id, platform, source, region, content, timestamp, engagement, url
    """
    if not os.path.exists(RAW_DB_PATH):
        print(f"⚠️  raw_data.db introuvable : {RAW_DB_PATH}")
        return []

    conn = get_connection(RAW_DB_PATH)
    tables = [t["name"] for t in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()]

    if "Posts" not in tables:
        print(f"⚠️  Table 'Posts' absente dans raw_data.db. Tables : {tables}")
        conn.close()
        return []

    if region:
        rows = conn.execute("""
            SELECT * FROM Posts WHERE region = ?
            ORDER BY timestamp DESC LIMIT ?
        """, (region, limit)).fetchall()
    else:
        rows = conn.execute("""
            SELECT * FROM Posts ORDER BY timestamp DESC LIMIT ?
        """, (limit,)).fetchall()

    conn.close()
    return [dict(row) for row in rows]


def load_raw_posts_into_engine(limit: int = 100) -> int:
    """
    Importe les posts bruts du Membre 1 dans pulseTN.db.
    emotion/viral_score/fake_score = 0 (enrichis ensuite par Membres 2 et 3).
    """
    raw_posts = get_raw_posts(limit=limit)
    if not raw_posts:
        print("ℹ️  Aucun post brut à importer.")
        return 0

    conn = get_connection()
    imported = 0
    for p in raw_posts:
        exists = conn.execute(
            "SELECT 1 FROM posts WHERE source = ? AND content = ?",
            (p.get("source", ""), p.get("content", ""))
        ).fetchone()

        if not exists:
            conn.execute("""
                INSERT INTO posts
                    (region, platform, source, content,
                     category, emotion, viral_score, fake_score, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p.get("region", "Tunis"),
                p.get("platform", "rss"),
                p.get("source", ""),
                p.get("content", ""),
                "", "", 0, 0,
                p.get("timestamp", datetime.now().isoformat())
            ))
            imported += 1

    conn.commit()
    conn.close()
    print(f"✅ {imported} posts importés depuis raw_data.db → pulseTN.db")
    return imported


# ── CRUD Users ─────────────────────────────────────────────────────────────────

def insert_user(persona_type: str,
                region_preference: str = "national",
                interest_category: str = "general") -> int:
    conn = get_connection()
    cursor = conn.execute("""
        INSERT INTO users (persona_type, region_preference, interest_category)
        VALUES (?, ?, ?)
    """, (persona_type, region_preference, interest_category))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def get_user(user_id: int):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM users WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


if __name__ == "__main__":
    create_tables()
    print(f"\n📂 Base principale : {DB_PATH}")
    print(f"📂 Base Membre 1   : {RAW_DB_PATH}")
    n = load_raw_posts_into_engine(limit=20)
    print(f"   → {n} posts importés")