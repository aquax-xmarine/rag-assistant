from pydantic import BaseModel
from enum import Enum

class ChunkStrategy(str, Enum):
    fixed = "fixed"
    sentence = "sentence"

class UploadResponse(BaseModel):
    document_id: int
    filename: str
    chunk_strategy: ChunkStrategy
    chunks_created: int


