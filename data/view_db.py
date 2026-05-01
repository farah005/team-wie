import sqlite3
import os

DB_NAME = os.path.join("data", "raw_data.db")

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Voir toutes les tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables :", cursor.fetchall())

# Voir 10 posts
cursor.execute("SELECT * FROM Posts LIMIT 10;")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()