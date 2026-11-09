
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "messages.db"


def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                conversation_id TEXT PRIMARY KEY,
                title TEXT,
                message_url TEXT,
                first_detected TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

    print("Message database initialized successfully!")


def is_new_message(conversation_id, title, message_url):
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            "SELECT 1 FROM messages WHERE conversation_id = ?",
            (conversation_id,)
        )

        if cursor.fetchone():
            return False

        connection.execute(
            """INSERT INTO messages
            (conversation_id, title, message_url)
            VALUES (?, ?, ?)""",
            (conversation_id, title, message_url)
        )

        return True


if __name__ == "__main__":
    initialize_database()
    print("Database ready!")
