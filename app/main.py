from fastapi import FastAPI

app = FastAPI(
    title="RAG Interview Assistant",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "RAG Interview Assistant API"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
