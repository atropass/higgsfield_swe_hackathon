"""Integration tests for health endpoints."""

from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    """Test health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "higgsfield-api"


def test_root_endpoint(client: TestClient) -> None:
    """Test root endpoint."""
    response = client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

