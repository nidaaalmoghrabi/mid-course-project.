"""Tests for the application health-check endpoint."""

from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app


# TestClient sends requests directly to the FastAPI application.
client = TestClient(app)


def test_health_endpoint_returns_ok() -> None:
    """The health endpoint should return HTTP 200 and a valid timestamp."""

    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "ok"
    assert set(body) == {"status", "timestamp"}

    # Parsing succeeds only when timestamp is a valid ISO-formatted datetime.
    parsed_timestamp = datetime.fromisoformat(
        body["timestamp"].replace("Z", "+00:00")
    )

    assert parsed_timestamp.tzinfo is not None


def test_root_serves_frontend_html() -> None:
    """The app root should serve the task board frontend."""

    response = client.get("/")

    assert response.status_code == 200
    assert "Task Board" in response.text
    assert "task-card" in response.text