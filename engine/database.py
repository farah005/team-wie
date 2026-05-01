# database.py
import sqlite3
from datetime import datetime

DB_PATH = "pulseTN.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # retourne des dicts
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_type TEXT NOT NULL,
            region_preference TEXT DEFAULT 'national',
            interest_category TEXT DEFAULT 'general',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            post_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    """)

    conn.commit()
    conn.close()

# --- Fonctions POSTS ---

def insert_post(region, platform, source, content, category="", 
                emotion="", viral_score=0, fake_score=0):
    conn = get_connection()
    conn.execute("""
        INSERT INTO posts (region, platform, source, content, category,
                           emotion, viral_score, fake_score, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (region, platform, source, content, category,
          emotion, viral_score, fake_score, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_recent_posts(limit=50, region=None):
    conn = get_connection()
    if region:
        rows = conn.execute("""
            SELECT * FROM posts WHERE region = ?
            ORDER BY timestamp DESC LIMIT ?
        """, (region, limit)).fetchall()
    else:
        rows = conn.execute("""
            SELECT * FROM posts
            ORDER BY timestamp DESC LIMIT ?
        """, (limit,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_posts_by_category(category, limit=20):
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM posts WHERE category = ?
        ORDER BY viral_score DESC LIMIT ?
    """, (category, limit)).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_top_viral_posts(limit=10):
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM posts
        ORDER BY viral_score DESC LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]

# --- Fonctions USERS ---

def insert_user(persona_type, region_preference="national", 
                interest_category="general"):
    conn = get_connection()
    cursor = conn.execute("""
        INSERT INTO users (persona_type, region_preference, interest_category)
        VALUES (?, ?, ?)
    """, (persona_type, region_preference, interest_category))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def get_user(user_id):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM users WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None

if __name__ == "__main__":
    create_tables()
    print("✅ Base de données créée avec succès")