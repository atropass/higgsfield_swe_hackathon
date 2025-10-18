from pydantic import Field, field_validator

from app.schemas.common import BaseJobRequest
from app.schemas.enums import VALID_VIDEO_ASPECT_RATIOS


class T2VRequest(BaseJobRequest):
    prompt: str = Field(
        ..., description="Text prompt for video generation", min_length=1, max_length=2000
    )
    aspect_ratio: str = Field(
        default="16:9",
        description="Video aspect ratio",
        examples=["16:9", "9:16", "1:1"],
    )
    duration: int = Field(
        default=5, description="Video duration in seconds", ge=1, le=10
    )

    @field_validator("aspect_ratio")
    @classmethod
    def validate_aspect_ratio(cls, v: str) -> str:
        if v not in VALID_VIDEO_ASPECT_RATIOS:
            raise ValueError(f"aspect_ratio must be one of {VALID_VIDEO_ASPECT_RATIOS}")
        return v.strip()


class MinimaxT2VRequest(T2VRequest):
    resolution: str = Field(
        default="768",
        description="Video resolution (768 or 1280)",
        examples=["768", "1280"],
    )
    enable_prompt_optimizer: bool = Field(
        default=True, description="Enable prompt optimization"
    )
    duration: int = Field(
        default=6, description="Video duration in seconds", ge=1, le=10
    )


class SeedanceT2VRequest(T2VRequest):
    resolution: str = Field(
        default="720",
        description="Video resolution (480 or 720)",
        examples=["480", "720"],
    )
    camera_fixed: bool = Field(
        default=False, description="Keep camera fixed (no movement)"
    )
    duration: int = Field(
        default=5, description="Video duration in seconds", ge=1, le=10
    )

