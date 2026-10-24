from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_chat_crea_conversation_id():
    r = client.post("/chat", json={"message": "ciao"})
    assert r.status_code == 200
    assert r.json()["conversation_id"]


def test_chat_mantiene_conversation_id():
    r = client.post("/chat", json={"message": "ciao", "conversation_id": "abc"})
    assert r.json()["conversation_id"] == "abc"


def test_chat_senza_message_422():
    assert client.post("/chat", json={}).status_code == 422
