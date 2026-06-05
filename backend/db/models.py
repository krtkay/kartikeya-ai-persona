from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from .database import Base


class Booking(Base):

    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)

    candidate_name = Column(String)

    candidate_email = Column(String)

    start_time = Column(DateTime)

    end_time = Column(DateTime)

    source = Column(String)

    google_event_id = Column(String)

    status = Column(String)