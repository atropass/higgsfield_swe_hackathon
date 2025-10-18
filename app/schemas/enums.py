from enum import Enum


class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class JobType(str, Enum):
    TEXT_TO_IMAGE = "text-to-image"
    TEXT_TO_VIDEO = "text-to-video"
    IMAGE_TO_VIDEO = "image-to-video"


class ActionType(str, Enum):
    GENERATE_IMAGE = "generate_image"
    GENERATE_VIDEO = "generate_video"
    GENERATE_VIDEO_FROM_IMAGE = "generate_video_from_image"


VALID_ASPECT_RATIOS = ["1:1", "16:9", "9:16", "4:3", "3:4", "2:3", "3:2"]
VALID_VIDEO_ASPECT_RATIOS = ["16:9", "9:16", "1:1", "4:3", "3:4"]

