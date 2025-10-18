from typing import Any, Dict
from uuid import uuid4

from pydantic import BaseModel, Field

from app.schemas.enums import JobStatus


class BaseJobRequest(BaseModel):
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Free-form metadata"
    )


class JobResponse(BaseModel):
    request_id: str = Field(
        default_factory=lambda: str(uuid4()), description="Our internal request ID"
    )
    job_set_id: str = Field(..., description="Higgsfield job set ID")
    status: str = Field(default=JobStatus.QUEUED.value, description="Initial job status")
    message: str = Field(default="Job submitted successfully")


class ErrorResponse(BaseModel):
    error: Dict[str, Any] = Field(..., description="Error details")


class HealthResponse(BaseModel):
    status: str = Field(default="healthy")
    version: str = Field(default="1.0.0")
    service: str = Field(default="higgsfield-api")

