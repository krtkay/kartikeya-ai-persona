from backend.scheduler.db import (
    get_connection
)


def is_slot_available(
    start_time,
    end_time
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM interviews
        WHERE
            start_time < ?
        AND
            end_time > ?
        """,
        (
            end_time,
            start_time
        )
    )

    result = cursor.fetchall()

    conn.close()

    return len(result) == 0