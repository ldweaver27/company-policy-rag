import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import app as flask_app_module


def test_health_endpoint():
    client = flask_app_module.app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_home_page():
    client = flask_app_module.app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"BrightWave Policy Assistant" in response.data


def test_chat_endpoint(monkeypatch):
    def mock_answer_question(question):
        return {
            "question": question,
            "answer": "Employees receive 20 days of PTO per calendar year.",
            "sources": [
                {
                    "title": "Paid Time Off (PTO) Policy",
                    "source": "pto_policy.md",
                    "text": "Employees receive 20 days of PTO per calendar year."
                }
            ],
        }

    monkeypatch.setattr(flask_app_module, "answer_question", mock_answer_question)

    client = flask_app_module.app.test_client()

    response = client.post(
        "/chat",
        json={"question": "How many PTO days do employees receive?"}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert "answer" in data
    assert "sources" in data
    assert len(data["sources"]) > 0