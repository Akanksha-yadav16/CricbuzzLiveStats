import sqlite3
import os

DB_PATH = "cricbuzz.db"
SCHEMA_FILE = "schema.sql"

def init_db():
    if not os.path.exists(SCHEMA_FILE):
        print(f"Schema file not found: {SCHEMA_FILE}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_FILE, "r") as f:
        sql_script = f.read()

    try:
        cursor.executescript(sql_script)
        conn.commit()
        print(f"Database initialized successfully at {DB_PATH}")
    except Exception as e:
        print(f"Error while creating DB: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
