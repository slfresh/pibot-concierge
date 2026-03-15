from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import rag
import llm

app = FastAPI(title="Hotel Concierge AI")

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Step 1: Retrieve relevant context from ChromaDB
    context = rag.retrieve(request.query)

    # Step 2: Pass context and query to local AI
    answer = llm.answer_question(request.query, context)

    return ChatResponse(answer=answer)

# Mount the static directory to serve index.html
app.mount("/", StaticFiles(directory="static", html=True), name="static")
