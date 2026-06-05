from backend.scheduler.service import (
    SchedulerService
)

scheduler = SchedulerService()

scheduler.create_booking(
    name="Kartikeya",
    email="kartikeya@gmail.com",
    start_time="2026-06-08T15:00:00",
    end_time="2026-06-08T16:00:00"
)

print(
    scheduler.get_all_bookings()
)