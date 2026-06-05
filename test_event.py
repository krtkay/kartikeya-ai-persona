from backend.calendar.google_calendar import (
    GoogleCalendarService
)

calendar = (
    GoogleCalendarService()
)

event_id = (
    calendar.create_event(
        candidate_name="Test Candidate",
        start_time=
        "2026-06-08T15:00:00",
        end_time=
        "2026-06-08T16:00:00"
    )
)

print(event_id)