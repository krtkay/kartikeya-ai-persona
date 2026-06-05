from backend.calendar.google_calendar import (
    GoogleCalendarService
)

calendar = (
    GoogleCalendarService()
)

print(
    calendar.is_slot_busy(
        "2026-06-10T15:00:00",
        "2026-06-10T16:00:00"
    )
)