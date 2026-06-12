import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app import app


def test_health_endpoint():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_home_page():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"BrightWave Policy Assistant" in response.data


def test_chat_endpoint():
    client = app.test_client()

    response = client.post(
        "/chat",
        json={
            "question": "How many PTO days do employees receive?"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "answer" in data
    assert "sources" in data
    assert len(data["sources"]) > 0