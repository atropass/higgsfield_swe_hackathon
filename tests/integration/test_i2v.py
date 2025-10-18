"""Integration tests for Image-to-Video endpoints."""

import respx
from fastapi.testclient import TestClient
from httpx import Response


@respx.mock
def test_create_kling25_video(
    client: TestClient, auth_headers: dict[str, str], mock_job_response: dict[str, str]
) -> None:
    """Test Kling 2.5 I2V endpoint."""
    respx.post("https://platform.higgsfield.ai/v1/image2video/kling-2-5").mock(
        return_value=Response(200, json=mock_job_response)
    )

    response = client.post(
        "/v1/i2v/kling25",
        json={
            "input_images": [
                {"type": "url", "image_url": "https://example.com/image.jpg"}
            ],
            "prompt": "cinematic portrait with subtle camera motion",
            "aspect_ratio": "9:16",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert "request_id" in data
    assert data["job_set_id"] == "job-set-123"


@respx.mock
def test_create_i2v_with_motions(
    client: TestClient, auth_headers: dict[str, str], mock_job_response: dict[str, str]
) -> None:
    """Test I2V with motion presets."""
    respx.post("https://platform.higgsfield.ai/v1/image2video/kling-2-5").mock(
        return_value=Response(200, json=mock_job_response)
    )

    response = client.post(
        "/v1/i2v/kling25",
        json={
            "input_images": [
                {"type": "url", "image_url": "https://example.com/image.jpg"}
            ],
            "prompt": "cinematic portrait",
            "aspect_ratio": "9:16",
            "motions": [{"id": "objects_around", "strength": 0.7}],
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

