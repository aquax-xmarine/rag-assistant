import json

import ollama

from app.schemas.booking import (
    BookingExtraction
)

from app.db.models import (
    InterviewBooking
)

from app.utils.date_parser import parse_date, parse_time

class BookingService:

    @staticmethod
    def extract_booking(
        message: str
    ) -> BookingExtraction | None:

        prompt = f"""
You are an intent detection and information extraction assistant.

Return ONLY valid JSON.

Schema:

{{
    "intent": "booking",
    "name": null,
    "email": null,
    "date": null,
    "time": null
}}

Valid intents:
- booking
- question
- unknown

Rules:
- Return valid JSON only
- No markdown
- No explanations
- Missing fields should be null

Message:
{message}
"""

        response = ollama.chat(
            model="llama3:latest",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a JSON extraction engine. "
                        "Always return valid JSON only."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = (
            response["message"]["content"]
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        try:

            data = json.loads(content)

            return BookingExtraction(
                **data
            )

        except (json.JSONDecodeError, ValueError):
            return None
        


    

    @staticmethod
    def save_booking(
        booking_data: BookingExtraction,
        db
    ):

        if not all([
            booking_data.name,
            booking_data.email,
            booking_data.date,
            booking_data.time
        ]):
            raise ValueError(
                "Missing booking fields"
            )
        
        parsed_date = parse_date(booking_data.date)
        parsed_time = parse_time(booking_data.time)

        if not parsed_date or not parsed_time:
            raise ValueError("INVALID_BOOKING_FORMAT")

        booking = InterviewBooking(
            name=booking_data.name,
            email=booking_data.email,
            date=parsed_date,
            time=parsed_time
        )

     
                    

        db.add(booking)

        db.commit()

        db.refresh(booking)

        return booking