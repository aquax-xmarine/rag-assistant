from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


class EmbeddingService:

    @staticmethod
    def embed(text: str) -> list[float]:
        return model.encode(text).tolist()