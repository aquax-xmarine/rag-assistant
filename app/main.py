from fastapi import FastAPI

from app.core.config import settings

from app.db.database import Base
from app.db.database import engine

import app.db.models

from app.api.documents import router as document_router



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0"
)

app.include_router(document_router)

@app.get("/")
async def root():
    return {
        "app": settings.app_name
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
