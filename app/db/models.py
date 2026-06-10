from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    DateTime
)

from app.db.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)

    filename = Column(String, nullable=False)

    chunk_strategy = Column(
        String,
        nullable=False
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class InterviewBooking(Base):
    __tablename__ = "interview_bookings"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    email = Column(String, nullable=False)

    date = Column(Date)

    time = Column(Time)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )