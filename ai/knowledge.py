import sqlite3
from pathlib import Path
from datetime import datetime


class AIKnowledge:

    def __init__(self, db_path="data/ai_knowledge.db"):

        self.db_path = Path(db_path)

        self.db_path.parent.mkdir(
            exist_ok=True
        )

        self.init_db()


    def init_db(self):

        with sqlite3.connect(self.db_path) as conn:

            conn.execute("""
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                content TEXT,
                created_at TEXT
            )
            """)

            conn.commit()


    def add(self, topic, content):

        with sqlite3.connect(self.db_path) as conn:

            conn.execute(
                """
                INSERT INTO knowledge
                (topic, content, created_at)
                VALUES (?, ?, ?)
                """,
                (
                    topic,
                    content,
                    datetime.utcnow().isoformat()
                )
            )

            conn.commit()


    def search(self, query):

        with sqlite3.connect(self.db_path) as conn:

            rows = conn.execute(
                """
                SELECT topic, content, created_at
                FROM knowledge
                WHERE topic LIKE ?
                OR content LIKE ?
                ORDER BY id DESC
                """,
                (
                    f"%{query}%",
                    f"%{query}%"
                )
            ).fetchall()


        return [
            {
                "topic": r[0],
                "content": r[1],
                "created_at": r[2]
            }
            for r in rows
        ]
