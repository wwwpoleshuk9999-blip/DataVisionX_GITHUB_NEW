import sqlite3
import os
import time


DB_PATH = "data/events.db"



def init_db():

    os.makedirs(
        "data",
        exist_ok=True
    )

    conn = sqlite3.connect(DB_PATH)

    cur = conn.cursor()


    cur.execute(
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



def add_event(
    action,
    plugin=None,
    user="system"
):

    conn = sqlite3.connect(
        DB_PATH
    )

    cur = conn.cursor()


    cur.execute(
        """
        INSERT INTO events
        (
            time,
            action,
            plugin,
            user
        )

        VALUES
        (?,?,?,?)
        """,

        (
            time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            action,
            plugin,
            user
        )
    )


    conn.commit()

    conn.close()



def get_events():

    conn = sqlite3.connect(
        DB_PATH
    )

    cur = conn.cursor()


    cur.execute(
        """
        SELECT
        time,
        action,
        plugin,
        user

        FROM events

        ORDER BY id DESC

        LIMIT 50
        """
    )


    rows = cur.fetchall()


    conn.close()


    events = []


    for row in rows:

        events.append(
            {
                "time": row[0],
                "action": row[1],
                "plugin": row[2],
                "user": row[3]
            }
        )


    return events



init_db()
