# utils/db_connection.py
from sqlalchemy import create_engine

# Create SQLite DB (file will be created in your project folder as 'cricbuzz.db')
engine = create_engine("sqlite:///cricbuzz.db", echo=True)

def test_connection():
    """Test if SQLite database connection works"""
    try:
        with engine.connect() as conn:
            result = conn.execute("SELECT sqlite_version();")
            version = result.fetchone()
            print("✅ Connected to SQLite DB, version:", version[0])
            return True
    except Exception as e:
        print("❌ Database connection failed:", e)
        return False
