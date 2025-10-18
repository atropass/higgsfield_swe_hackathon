"""Job management schemas."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class JobResult(BaseModel):
    """Individual job result."""

    url: Optional[str] = Field(default=None, description="Result URL")
    min_url: Optional[str] = Field(default=None, description="Minimized result URL")
    raw_url: Optional[str] = Field(default=None, description="Raw result URL")
    duration: Optional[float] = Field(default=None, description="Duration in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Job(BaseModel):
    """Individual job in a job set."""

    id: str = Field(..., description="Job ID")
    status: str = Field(..., description="Job status")
    progress: Optional[float] = Field(default=None, description="Progress percentage")
    result: Optional[JobResult] = Field(default=None, description="Job result")
    error: Optional[str] = Field(default=None, description="Error message if failed")
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)


class JobSetStatus(BaseModel):
    """Job set status response."""

    id: str = Field(..., description="Job set ID")
    status: str = Field(..., description="Overall status")
    jobs: List[Job] = Field(default_factory=list, description="Individual jobs")
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WebhookPayload(BaseModel):
    """Webhook callback payload from Higgsfield."""

    job_set_id: str = Field(..., description="Job set ID")
    status: str = Field(..., description="Job status")
    jobs: List[Job] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

