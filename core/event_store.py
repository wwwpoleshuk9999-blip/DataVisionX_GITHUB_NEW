import sqlite3
import os
import time


DB_PATH = "data/events.db"


def init_event_store():

    os.makedirs(
        "data",
        exist_ok=True
    )

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            action TEXT,
            plugin TEXT,
            user TEXT
        )
        """
    )

    conn.commit()
    conn.close()



def save_event(
    action,
    plugin=None,
    user="system"
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    event_time = time.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO events
        (time, action, plugin, user)
        VALUES (?, ?, ?, ?)
        """,
        (
            event_time,
            action,
            plugin,
            user
        )
    )

    conn.commit()
    conn.close()


    return {
        "time": event_time,
        "action": action,
        "plugin": plugin,
        "user": user
    }



def get_events(limit=50):

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM events
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    conn.close()


    return [
        dict(row)
        for row in rows
    ]



init_event_store()
