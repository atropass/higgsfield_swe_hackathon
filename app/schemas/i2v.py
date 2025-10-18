from typing import List, Literal, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.schemas.common import BaseJobRequest


class InputImage(BaseModel):
    type: Literal["image_url"] = Field(default="image_url", description="Image input type")
    image_url: HttpUrl = Field(..., description="URL of the input image")


class Motion(BaseModel):
    id: str = Field(..., description="Motion preset ID")
    strength: float = Field(default=0.7, description="Motion strength", ge=0.0, le=1.0)


class I2VRequest(BaseJobRequest):
    input_images: List[InputImage] = Field(
        ..., description="Input images for video generation", min_length=1, max_length=10
    )
    prompt: str = Field(
        ..., description="Text prompt for video generation", min_length=1, max_length=2000
    )
    aspect_ratio: str = Field(
        default="9:16",
        description="Video aspect ratio",
        examples=["16:9", "9:16", "1:1"],
    )
    motions: Optional[List[Motion]] = Field(
        default=None, description="Optional motion presets"
    )

    @field_validator("aspect_ratio")
    @classmethod
    def validate_aspect_ratio(cls, v: str) -> str:
        valid_ratios = ["16:9", "9:16", "1:1", "4:3", "3:4"]
        if v not in valid_ratios:
            raise ValueError(f"aspect_ratio must be one of {valid_ratios}")
        return v


class Kling25I2VRequest(I2VRequest):
    camera_control: Optional[str] = Field(
        default=None, description="Camera control preset"
    )


class MinimaxI2VRequest(I2VRequest):
    pass


class Veo3I2VRequest(I2VRequest):
    pass


class Wan25FastI2VRequest(I2VRequest):
    duration_sec: int = Field(default=5, description="Video duration", ge=1, le=10)

