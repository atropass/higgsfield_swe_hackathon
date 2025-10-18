from typing import Optional

from pydantic import Field, field_validator

from app.schemas.common import BaseJobRequest
from app.schemas.enums import VALID_ASPECT_RATIOS


class T2IRequest(BaseJobRequest):
    prompt: str = Field(
        ..., description="Text prompt for image generation", min_length=1, max_length=2000
    )
    aspect_ratio: str = Field(
        default="1:1",
        description="Image aspect ratio",
        examples=["1:1", "16:9", "9:16", "4:3", "3:4"],
    )
    batch_size: int = Field(
        default=1, description="Number of images to generate", ge=1, le=4
    )

    @field_validator("aspect_ratio")
    @classmethod
    def validate_aspect_ratio(cls, v: str) -> str:
        if v not in VALID_ASPECT_RATIOS:
            raise ValueError(f"aspect_ratio must be one of {VALID_ASPECT_RATIOS}")
        return v.strip()


class NanoBananaT2IRequest(T2IRequest):
    negative_prompt: Optional[str] = Field(
        default=None, description="Negative prompt to avoid certain features"
    )


class Seedream4T2IRequest(T2IRequest):
    negative_prompt: Optional[str] = Field(
        default=None, description="Negative prompt to avoid certain features"
    )
