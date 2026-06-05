from backend.scheduler.db import (
    get_connection
)


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interviews (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_name TEXT,

        role_name TEXT,

        start_time TEXT,

        end_time TEXT,

        google_event_id TEXT,

        status TEXT
    )
    """)

    conn.commit()

    conn.close()