import sqlite3

conn = sqlite3.connect("cricbuzz.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

for table in ["players", "player_stats", "matches", "venues", "series"]:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"{table} rows:", cursor.fetchone()[0])
    except:
        print(f"{table} ❌ not found")

conn.close()

