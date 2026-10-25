import uuid

from fastapi import FastAPI

from app.errors import install_error_handlers
from app.models import ChatRequest, ChatResponse

app = FastAPI(title="NoHumanIntelligence")
install_error_handlers(app)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    # stub: l'LLM arriva nel blocco 3
    return ChatResponse(
        conversation_id=req.conversation_id or uuid.uuid4(),
        answer="Non ho ancora una risposta.",
    )
