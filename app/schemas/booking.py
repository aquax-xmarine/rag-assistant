from pydantic import BaseModel
from typing import Optional


class BookingExtraction(BaseModel):
    intent: str

    name: Optional[str] = None
    email: Optional[str] = None

    date: Optional[str] = None
    time: Optional[str] = None