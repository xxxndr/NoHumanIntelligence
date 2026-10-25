from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator

Message = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=4000)
]


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: Message
    conversation_id: UUID | None = None

    @field_validator("message")
    @classmethod
    def no_null_bytes(cls, v: str) -> str:
        if "\x00" in v:
            raise ValueError("il messaggio contiene caratteri nulli")
        return v


class Source(BaseModel):
    document: str
    snippet: str


class ChatResponse(BaseModel):
    conversation_id: UUID
    answer: str
    sources: list[Source] = []
    escalate: bool = False
