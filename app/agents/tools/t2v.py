import json

from langchain_core.tools import tool

from app.core.logging import get_logger
from app.schemas.t2v import MinimaxT2VRequest, SeedanceT2VRequest
from app.services.t2v_service import t2v_service

logger = get_logger(__name__)


@tool
async def generate_text_to_video(
    prompt: str,
    aspect_ratio: str = "16:9",
    duration: int = 5,
    model: str = "minimax-hailuo-02",
    resolution: str = "768",
) -> str:
    """
    Generate videos from text descriptions - create moving scenes and animations from scratch.

    WHEN TO USE:
    - User wants to create/generate a video from text description
    - User describes a scene with motion (e.g., "cat walking", "waves crashing")
    - User wants animated content without providing an image
    - User asks for cinematic scenes, action sequences, or dynamic content

    MODELS:
    - minimax-hailuo-02 (DEFAULT): High-quality cinematic video generation
      * Resolutions: 768 (fast) or 1280 (high quality)
      * Best for: Realistic scenes, detailed motion, professional content
      * Default duration: 6 seconds

    - seedance-v1-lite: Alternative video model
      * Resolutions: 480 (fast) or 720 (standard)
      * Best for: Quick iterations, artistic content
      * Has camera_fixed option
      * Default duration: 5 seconds

    ASPECT RATIOS:
    - 16:9 (landscape): YouTube, horizontal videos, cinematic (BEST FOR: wide scenes)
    - 9:16 (portrait): TikTok, Instagram Reels, vertical videos (BEST FOR: mobile)
    - 1:1 (square): Social media, Instagram feed (BEST FOR: balanced composition)
    - 4:3 / 3:4: Traditional video/photo formats

    DURATIONS:
    - 1-10 seconds supported (default: 5 for seedance, 6 for minimax)
    - Longer = more processing time but more action

    RESOLUTIONS (quality vs speed):
    - minimax-hailuo-02: 768 (faster) or 1280 (higher quality)
    - seedance-v1-lite: 480 (faster) or 720 (higher quality)

    Args:
        prompt: Detailed description of the video scene and action
        aspect_ratio: Video aspect ratio (default: 16:9)
        duration: Video length in seconds, 1-10 (default: 5)
        model: Which model to use (default: minimax-hailuo-02)
        resolution: Video quality - 768/1280 for minimax, 480/720 for seedance

    Returns:
        JSON string with job details
    """
    logger.info("t2v_tool_called", prompt=prompt[:50], model=model, duration=duration)

    if model == "minimax-hailuo-02":
        request = MinimaxT2VRequest(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            duration=duration,
            resolution=resolution,
        )
    else:  # seedance-v1-lite
        request = SeedanceT2VRequest(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            duration=duration,
            resolution=resolution,
        )

    result = await t2v_service.create_video(model, request)

    return json.dumps({
        "_higgsfield_job": True,
        "job_set_id": result.job_set_id,
        "job_type": "text-to-video",
        "model": model,
        "status": result.status,
        "parameters": {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "resolution": resolution,
        },
    })

