from backend.scheduler.db import (
    get_connection
)


class SchedulerService:

    def create_booking(
        self,
        company_name,
        role_name,
        start_time,
        end_time,
        google_event_id=None
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO interviews(

                company_name,
                role_name,

                start_time,
                end_time,

                google_event_id,
                status

            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                company_name,
                role_name,

                start_time,
                end_time,

                google_event_id,

                "confirmed"
            )
        )

        conn.commit()

        conn.close()

    def get_all_bookings(self):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM interviews
            """
        )

        rows = cursor.fetchall()

        conn.close()

        return rows

    def delete_booking(
        self,
        booking_id
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM interviews
            WHERE id = ?
            """,
            (booking_id,)
        )

        conn.commit()

        conn.close()

    def get_booking_by_id(
        self,
        booking_id
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM interviews
            WHERE id = ?
            """,
            (booking_id,)
        )

        row = cursor.fetchone()

        conn.close()

        return row