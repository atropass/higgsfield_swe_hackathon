"""Integration tests for Text-to-Image endpoints."""

import respx
from fastapi.testclient import TestClient
from httpx import Response


@respx.mock
def test_create_nano_banana_image(
    client: TestClient, auth_headers: dict[str, str], mock_job_response: dict[str, str]
) -> None:
    """Test Nano Banana T2I endpoint."""
    respx.post("https://platform.higgsfield.ai/v1/text2image/nano-banana").mock(
        return_value=Response(200, json=mock_job_response)
    )

    response = client.post(
        "/v1/t2i/nano-banana",
        json={
            "prompt": "monkey",
            "aspect_ratio": "4:3",
            "batch_size": 1,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert "request_id" in data
    assert data["job_set_id"] == "job-set-123"


@respx.mock
def test_create_t2i_batch(
    client: TestClient, auth_headers: dict[str, str], mock_job_response: dict[str, str]
) -> None:
    """Test T2I with batch size."""
    respx.post("https://platform.higgsfield.ai/v1/text2image/nano-banana").mock(
        return_value=Response(200, json=mock_job_response)
    )

    response = client.post(
        "/v1/t2i/nano-banana",
        json={
            "prompt": "sunset over mountains",
            "aspect_ratio": "16:9",
            "batch_size": 4,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

