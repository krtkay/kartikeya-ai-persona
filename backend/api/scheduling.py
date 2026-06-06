from fastapi import APIRouter

from backend.scheduler.service import (
    SchedulerService
)

from backend.scheduler.availability import (
    is_slot_available
)

try:

    from backend.calendar.google_calendar import (
        GoogleCalendarService
    )

    calendar = GoogleCalendarService()

except Exception:

    calendar = None


router = APIRouter()

scheduler = SchedulerService()


@router.get("/availability")
def availability():

    bookings = (
        scheduler.get_all_bookings()
    )

    return {
        "bookings": bookings
    }


@router.post("/book")
def book(
    payload: dict
):

    start_time = payload["start_time"]

    end_time = payload["end_time"]

    available = is_slot_available(
        start_time,
        end_time
    )

    calendar_busy = False

    if calendar:

        calendar_busy = (
            calendar.is_slot_busy(
                start_time,
                end_time
            )
        )

    if calendar_busy:

        return {
            "success": False,
            "message":
                "Google Calendar conflict"
        }

    if not available:

        return {
            "success": False,
            "message":
                "Slot unavailable"
        }

    event_id = None

    if calendar:

        event_id = (
            calendar.create_event(
                company_name=
                    payload["company_name"],

                role_name=
                    payload["role_name"],

                start_time=
                    start_time,

                end_time=
                    end_time
            )
        )

    scheduler.create_booking(

        company_name=
            payload["company_name"],

        role_name=
            payload["role_name"],

        start_time=
            start_time,

        end_time=
            end_time,

        google_event_id=
            event_id
    )

    return {
        "success": True,
        "message":
            "Interview booked",

        "event_id":
            event_id
    }


@router.get("/bookings")
def get_bookings():

    bookings = (
        scheduler.get_all_bookings()
    )

    return {
        "count": len(bookings),
        "bookings": bookings
    }


@router.delete(
    "/book/{booking_id}"
)
def delete_booking(
    booking_id: int
):

    booking = (
        scheduler.get_booking_by_id(
            booking_id
        )
    )

    if booking is None:

        return {
            "success": False,
            "message":
                "Booking not found"
        }

    scheduler.delete_booking(
        booking_id
    )

    return {
        "success": True,
        "message":
            "Booking deleted"
    }

@router.get("/debug-db")
def debug_db():

    from backend.scheduler.db import (
        get_connection
    )

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """
    )

    tables = cursor.fetchall()

    conn.close()

    return {
        "tables": tables
    }