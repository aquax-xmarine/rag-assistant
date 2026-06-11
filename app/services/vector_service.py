from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter
)

from app.core.config import settings


COLLECTION_NAME = "documents"


class VectorService:

    def __init__(self):

        self.client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port
        )

    def create_collection(self):

        collections = self.client.get_collections()

        names = [
            c.name
            for c in collections.collections
        ]

        if COLLECTION_NAME not in names:

            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=384,
                    distance=Distance.COSINE
                )
            )


    def store_chunks(
        self,
        document_id: int,
        chunks: list[str],
        embeddings: list[list[float]]
    ):

        points = []

        for idx, (chunk, vector) in enumerate(
            zip(chunks, embeddings)
        ):

            points.append(
                PointStruct(
                    id=document_id * 10000 + idx,
                    vector=vector,
                    payload={
                        "document_id": document_id,
                        "chunk_text": chunk
                    }
                )
            )

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )


    def search(
        self,
        query_vector: list[float],
        limit: int = 5
    ):

        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit
        )

        return results.points
    