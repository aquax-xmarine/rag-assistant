from app.services.embedding_service import (
    EmbeddingService
)

from app.services.redis_service import (
    RedisService
)

from app.services.vector_service import (
    VectorService
)

import requests


class RAGService:

    def answer(
        self,
        query: str,
        session_id: str
    ) -> str:

        redis_service = RedisService()

        history = (
            redis_service.get_history(
                session_id
            )
        )

        query_embedding = (
            EmbeddingService.embed(query)
        )

        results = (
            VectorService().search(
                query_embedding
            )
        )

        context = "\n\n".join(
            r.payload["chunk_text"]
            for r in results
        )

        conversation = "\n".join(
            f"{m['role']}: {m['content']}"
            for m in history
        )

        prompt = f"""
You are a helpful assistant.

Conversation History:
{conversation}

Context:
{context}

Question:
{query}

Answer using only the provided context.
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        answer = response.json()["response"]

       

        return answer