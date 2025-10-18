"""Pytest configuration and fixtures."""

import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient

# Set test environment variables before importing app
os.environ["APP_ENV"] = "test"
os.environ["APP_API_KEY"] = "test-key"
os.environ["HF_API_KEY"] = "test-hf-key"
os.environ["HF_SECRET"] = "test-hf-secret"
os.environ["RATE_LIMIT_ENABLED"] = "false"

from app.main import app  # noqa: E402


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Create test client."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers() -> dict[str, str]:
    """Authentication headers for tests."""
    return {"x-api-key": "test-key"}


@pytest.fixture
def mock_job_response() -> dict[str, str]:
    """Mock job response from Higgsfield."""
    return {
        "id": "job-set-123",
        "status": "queued",
    }


@pytest.fixture
def mock_job_status() -> dict[str, object]:
    """Mock job status response."""
    return {
        "id": "job-set-123",
        "status": "processing",
        "jobs": [
            {
                "id": "job-1",
                "status": "processing",
                "progress": 50.0,
                "result": None,
                "error": None,
            }
        ],
        "created_at": "2025-01-01T00:00:00Z",
        "updated_at": "2025-01-01T00:01:00Z",
        "metadata": {},
    }

