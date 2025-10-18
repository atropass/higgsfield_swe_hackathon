import re

from app.core.errors import ValidationError


def validate_aspect_ratio(aspect_ratio: str) -> None:
    pattern = r"^\d+:\d+$"
    if not re.match(pattern, aspect_ratio):
        raise ValidationError(
            "Invalid aspect ratio format. Expected format: 'width:height' (e.g., '16:9')",
            field="aspect_ratio",
        )


def validate_url(url: str) -> None:
    pattern = r"^https?://.+"
    if not re.match(pattern, url):
        raise ValidationError(
            "Invalid URL format. Expected http:// or https:// URL", field="url"
        )


def validate_duration(duration: int, min_duration: int = 1, max_duration: int = 10) -> None:
    if not min_duration <= duration <= max_duration:
        raise ValidationError(
            f"Duration must be between {min_duration} and {max_duration} seconds",
            field="duration_sec",
        )


def validate_batch_size(batch_size: int, max_batch: int = 4) -> None:
    if not 1 <= batch_size <= max_batch:
        raise ValidationError(
            f"Batch size must be between 1 and {max_batch}", field="batch_size"
        )

