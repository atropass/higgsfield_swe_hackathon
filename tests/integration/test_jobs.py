"""Integration tests for job management endpoints."""

import respx
from fastapi.testclient import TestClient
from httpx import Response


@respx.mock
def test_get_job_status(
    client: TestClient, auth_headers: dict[str, str], mock_job_status: dict[str, object]
) -> None:
    """Test get job status endpoint."""
    job_set_id = "job-set-123"

    respx.get(f"https://platform.higgsfield.ai/v1/job-sets/{job_set_id}").mock(
        return_value=Response(200, json=mock_job_status)
    )

    response = client.get(f"/v1/jobs/{job_set_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == job_set_id
    assert data["status"] == "processing"
    assert len(data["jobs"]) == 1


@respx.mock
def test_refresh_job_status(
    client: TestClient, auth_headers: dict[str, str], mock_job_status: dict[str, object]
) -> None:
    """Test refresh job status endpoint."""
    job_set_id = "job-set-123"

    respx.get(f"https://platform.higgsfield.ai/v1/job-sets/{job_set_id}").mock(
        return_value=Response(200, json=mock_job_status)
    )

    response = client.post(f"/v1/jobs/{job_set_id}/refresh", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == job_set_id

