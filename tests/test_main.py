import uuid

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.errors import PROBLEM_JSON, VALIDATION_TYPE, install_error_handlers
from app.main import app

client = TestClient(app)


def assert_problem(r, status: int) -> dict:
    assert r.status_code == status
    assert r.headers["content-type"] == PROBLEM_JSON
    body = r.json()
    assert body["status"] == status
    return body


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_chat_crea_conversation_id():
    r = client.post("/chat", json={"message": "ciao"})
    assert r.status_code == 200
    uuid.UUID(r.json()["conversation_id"])


def test_chat_mantiene_conversation_id():
    cid = str(uuid.uuid4())
    r = client.post("/chat", json={"message": "ciao", "conversation_id": cid})
    assert r.json()["conversation_id"] == cid


def test_chat_message_viene_ripulito():
    assert client.post("/chat", json={"message": "  ciao  "}).status_code == 200


def test_chat_senza_message_422():
    body = assert_problem(client.post("/chat", json={}), 422)
    assert body["type"] == VALIDATION_TYPE
    assert body["instance"] == "/chat"
    assert body["errors"][0]["pointer"] == "/body/message"


@pytest.mark.parametrize(
    ("payload", "pointer"),
    [
        ({"message": ""}, "/body/message"),
        ({"message": "   "}, "/body/message"),
        ({"message": "x" * 4001}, "/body/message"),
        ({"message": "a\x00b"}, "/body/message"),
        ({"message": "ciao", "conversation_id": "abc"}, "/body/conversation_id"),
        ({"message": "ciao", "extra": 1}, "/body/extra"),
    ],
)
def test_chat_input_non_valido_422(payload, pointer):
    body = assert_problem(client.post("/chat", json=payload), 422)
    assert pointer in [e["pointer"] for e in body["errors"]]


def test_route_inesistente_404_problem():
    assert_problem(client.get("/non-esiste"), 404)


def test_metodo_non_consentito_405_problem():
    r = client.get("/chat")
    assert_problem(r, 405)
    assert "POST" in r.headers["allow"]


def test_errore_non_gestito_500_senza_dettagli_interni():
    boom = FastAPI()
    install_error_handlers(boom)

    @boom.get("/boom")
    def _boom():
        raise RuntimeError("segreto")

    r = TestClient(boom, raise_server_exceptions=False).get("/boom")
    body = assert_problem(r, 500)
    assert "segreto" not in r.text
    assert body["detail"] == "Errore interno del server."
