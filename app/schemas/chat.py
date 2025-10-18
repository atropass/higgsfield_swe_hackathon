from typing import Any, Dict, List, Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"] = Field(
        ..., description="Message role"
    )
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    message: str = Field(..., description="User message", min_length=1)
    conversation_history: List[ChatMessage] = Field(
        default_factory=list, description="Previous conversation history"
    )


class JobDetails(BaseModel):
    job_set_id: str = Field(..., description="Higgsfield job set ID")
    status: str = Field(..., description="Job status (queued, processing, completed, failed)")
    job_type: str = Field(..., description="Type: text-to-image, text-to-video, image-to-video")
    model: str = Field(..., description="Model used")
    parameters: Dict[str, Any] = Field(..., description="Generation parameters")
    estimated_time: str = Field(default="2-5 minutes", description="Estimated completion time")


class ChatResponse(BaseModel):
    message: str = Field(..., description="Assistant response message")
    job_details: JobDetails | None = Field(
        default=None, description="Detailed job information if generation was initiated"
    )
    action_performed: str | None = Field(
        default=None, description="Action performed: generate_image, generate_video, check_status, etc."
    )
