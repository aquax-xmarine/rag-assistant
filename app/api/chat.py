from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.chat import (
    ChatRequest
)

from app.services.booking_service import BookingService
from app.services.rag_service import (
    RAGService
)
from app.services.redis_service import RedisService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post("")
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    
    redis_service = RedisService()

    redis_service.save_message(
        request.session_id,
        "user",
        request.query
    )

    booking_data = (
        BookingService.extract_booking(
            request.query
        )
    )

    if (
        booking_data is not None
        and booking_data.intent == "booking"
    ):
        
        if not all([
            booking_data.name,
            booking_data.email,
            booking_data.date,
            booking_data.time
        ]):
            response_text = (
                "I understand you want to book an interview, but I need complete details.\n\n"
                "Please provide the information in this format:\n\n"
                "Name: <your name>\n"
                "Email: <your email>\n"
                "Date: YYYY-MM-DD\n"
                "Time: HH:MM (24-hour format)\n"
            )

            redis_service.save_message(
                request.session_id,
                "assistant",
                response_text
            )

            return {
                "message": response_text
            }

        booking = (
            BookingService.save_booking(
                booking_data,
                db
            )
        )

        response_text = (
            f"Interview booked successfully. "
            f"Booking ID: {booking.id}"
        )

        redis_service.save_message(
            request.session_id,
            "assistant",
            response_text
        )

        return {
            "message": response_text,
            "booking_id": booking.id
        }

    answer = (
        RAGService().answer(
            request.query,
            request.session_id
        )
    )

    redis_service.save_message(
        request.session_id,
        "assistant",
        answer
    )

    return {
        "answer": answer
    }