import sqlite3
from pathlib import Path
from datetime import datetime


class AIMemory:

    def __init__(self, db_path="data/ai_memory.db"):
        self.db_path = Path(db_path)

        self.db_path.parent.mkdir(
            exist_ok=True
        )

        self.init_db()


    def init_db(self):

        with sqlite3.connect(self.db_path) as conn:

            conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                message TEXT,
                created_at TEXT
            )
            """)

            conn.commit()


    def save(self, role, message):

        with sqlite3.connect(self.db_path) as conn:

            conn.execute(
                """
                INSERT INTO conversations
                (role, message, created_at)
                VALUES (?, ?, ?)
                """,
                (
                    role,
                    message,
                    datetime.utcnow().isoformat()
                )
            )

            conn.commit()


    def history(self, limit=20):

        with sqlite3.connect(self.db_path) as conn:

            rows = conn.execute(
                """
                SELECT role, message, created_at
                FROM conversations
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,)
            ).fetchall()

        return [
            {
                "role": r[0],
                "message": r[1],
                "created_at": r[2]
            }
            for r in rows
        ]
