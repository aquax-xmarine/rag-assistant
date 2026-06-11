import os
import fitz

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends
)

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Document

from app.schemas.document import ChunkStrategy
from app.services.chunking_service import (
    ChunkingService
)

from app.services.embedding_service import (
    EmbeddingService
)

from app.services.vector_service import (
    VectorService
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


def extract_text(path: str) -> str:

    if path.endswith(".txt"):

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:
            return f.read()

    if path.endswith(".pdf"):

        with fitz.open(path) as pdf:
            text = ""

            for page in pdf:
                text += page.get_text()

            return text

    raise ValueError(
        "Unsupported file type"
    )


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    chunk_strategy: ChunkStrategy = Form(...),
    db: Session = Depends(get_db)
):

    file_path = os.path.join(
        "uploads",
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(
            await file.read()
        )

    text = extract_text(file_path)

    if chunk_strategy == ChunkStrategy.fixed:

        chunks = ChunkingService.fixed_chunking(text)

    elif chunk_strategy == ChunkStrategy.sentence:

        chunks = ChunkingService.sentence_chunking(text)

    else:
        raise ValueError(
            "Invalid chunk strategy"
        )

    document = Document(
        filename=file.filename,
        chunk_strategy=chunk_strategy
    )

    db.add(document)

    db.commit()

    db.refresh(document)


    embeddings = [
        EmbeddingService.embed(chunk)
        for chunk in chunks
    ]

    VectorService().store_chunks(
        document.id,
        chunks,
        embeddings
    )

    return {
        "document_id": document.id,
        "filename": document.filename,
        "chunk_strategy": chunk_strategy,
        "chunks_created": len(chunks),
    }
