import json

import redis

from app.core.config import settings


class RedisService:

    def __init__(self):

        self.client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            decode_responses=True
        )

    def get_history(
        self,
        session_id: str
    ):

        data = self.client.get(
            f"chat:{session_id}"
        )

        if not data:
            return []

        return json.loads(data)

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str
    ):

        history = self.get_history(
            session_id
        )

        history.append(
            {
                "role": role,
                "content": content
            }
        )

        self.client.set(
            f"chat:{session_id}",
            json.dumps(history)
        )

    def save_booking_state(
        self,
        session_id: str,
        state: dict
    ):

        self.client.set(
            f"booking:{session_id}",
            json.dumps(state)
        )

    def get_booking_state(
        self,
        session_id: str
    ):

        data = self.client.get(
            f"booking:{session_id}"
        )

        if not data:
            return None

        return json.loads(data)
    
    def delete_booking_state(
        self,
        session_id: str
    ):

        self.client.delete(
            f"booking:{session_id}"
        )
    