"""Integration tests for Text-to-Video endpoints."""

import respx
from fastapi.testclient import TestClient
from httpx import Response


@respx.mock
def test_create_kling21_video(
    client: TestClient, auth_headers: dict[str, str], mock_job_response: dict[str, str]
) -> None:
    """Test Kling 2.1 T2V endpoint."""
    # Mock Higgsfield API response
    respx.post("https://platform.higgsfield.ai/v1/text2video/kling-21-master").mock(
        return_value=Response(200, json=mock_job_response)
    )

    response = client.post(
        "/v1/t2v/kling21",
        json={
            "prompt": "A cat playing piano",
            "aspect_ratio": "16:9",
            "duration_sec": 5,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert "request_id" in data
    assert data["job_set_id"] == "job-set-123"
    assert data["status"] == "queued"


@respx.mock
def test_create_t2v_without_auth(client: TestClient) -> None:
    """Test T2V endpoint without authentication."""
    response = client.post(
        "/v1/t2v/kling21",
        json={
            "prompt": "A cat playing piano",
            "aspect_ratio": "16:9",
            "duration_sec": 5,
        },
    )

    assert response.status_code == 422  # Missing header


def test_create_t2v_invalid_aspect_ratio(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    """Test T2V with invalid aspect ratio."""
    response = client.post(
        "/v1/t2v/kling21",
        json={
            "prompt": "A cat playing piano",
            "aspect_ratio": "invalid",
            "duration_sec": 5,
        },
        headers=auth_headers,
    )

    assert response.status_code == 422


@respx.mock
def test_create_minimax_video(
    client: TestClient, auth_headers: dict[str, str], mock_job_response: dict[str, str]
) -> None:
    """Test Minimax T2V endpoint."""
    respx.post("https://platform.higgsfield.ai/v1/text2video/minimax-hailuo-02").mock(
        return_value=Response(200, json=mock_job_response)
    )

    response = client.post(
        "/v1/t2v/minimax-hailuo-02",
        json={
            "prompt": "A dog running on beach",
            "aspect_ratio": "9:16",
            "duration_sec": 5,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["job_set_id"] == "job-set-123"

