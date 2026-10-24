from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


class Source(BaseModel):
    document: str
    snippet: str


class ChatResponse(BaseModel):
    conversation_id: str
    answer: str
    sources: list[Source] = []
    escalate: bool = False
