# RAG Interview Assistant
A FastAPI-based conversational RAG with LLM-powered interview booking. 

---

## Features
- Document upload (PDF/TXT)
- Text Chunking (fixed-size + sentence-based)
- Vector search using Qdrant
- Custom RAG pipeline 
- Redis-based chat memory
- Interview booking via LLM (Ollama)
- PostgreSQL for metadata + booking info

---

## Tech Stack
- FastAPI
- PostgreSQL
- Qdrant
- Redis
- Sentence Transformers (all-MiniLM-L6-V2)
- Ollama
- Docker

---

## Architecture
Document Flow:
Documents → Chunking → Embeddings → Qdrant

Chat Flow:
Query → Embedding → Vector Search → LLM → Answer

Memory:
Chat History → Redis

Booking:
User Input → Ollama → Extract Structured Data → PostgreSQL

---

## Setup Instructions
### 1. Clone repo
'''bash
git clone <repo-url>
cd rag-assistant
'''

### 2. Create virtual environment
'''bash
python -m venv venv
venv\Scripts\activate
'''

### 3. Install dependencies
'''bash
pip install -r requirements.txt
'''

### 4. Add environment variables
Create .env file in the root directory

'''bash
APP_NAME=RAG Interview Assistant

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/rag_assistant

REDIS_HOST=localhost
REDIS_PORT=6379

QDRANT_HOST=localhost
QDRANT_PORT=6333
'bash


### 5. Start infrastructure services (Docker)
'''bash
docker compose up -d redis qdrant postgres
'''

### 6. Run FastAPI server
'''bash
uvicorn app.main:app --reload
'''

---

## Access API
API: http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs

