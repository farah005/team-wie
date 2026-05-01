import sqlite3

DB_PATH = "data/raw_data.db"
conn = None

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM posts")
    total_posts = cursor.fetchone()[0]

    print(f"\n📊 TOTAL POSTS DANS LA BASE : {total_posts}")

    print("\n📍 POSTS PAR RÉGION :")
    cursor.execute("""
        SELECT region, COUNT(*)
        FROM posts
        GROUP BY region
        ORDER BY COUNT(*) DESC
    """)

    region_total = 0
    for region, count in cursor.fetchall():
        print(f"- {region}: {count}")
        region_total += count

    print(f"\n🔢 TOTAL CALCULÉ VIA RÉGIONS : {region_total}")

    if total_posts == region_total:
        print("\n✅ Base cohérente : total = somme des régions")
    else:
        print("\n❌ Incohérence détectée")

    print("\n📰 TOP SOURCES :")
    cursor.execute("""
        SELECT source, COUNT(*)
        FROM posts
        GROUP BY source
        ORDER BY COUNT(*) DESC
    """)

    for source, count in cursor.fetchall():
        print(f"- {source}: {count}")

    print("\n🧪 EXEMPLES DE POSTS :")
    cursor.execute("""
        SELECT content, source, region, platform, engagement
        FROM posts
        LIMIT 10
    """)

    for content, source, region, platform, engagement in cursor.fetchall():
        print(f"- [{platform} | {source} | {region}] {content[:120]}... | Engagement: {engagement}")

except sqlite3.Error as e:
    print(f"❌ Erreur SQLite : {e}")

finally:
    if conn:
        conn.close()