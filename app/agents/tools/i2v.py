import json

from langchain_core.tools import tool

from app.core.logging import get_logger
from app.schemas.i2v import I2VRequest, InputImage, Motion
from app.services.i2v_service import i2v_service

logger = get_logger(__name__)


@tool
async def generate_image_to_video(
    image_url: str,
    prompt: str,
    aspect_ratio: str = "9:16",
    model: str = "kling25",
    motion_presets: str | None = None,
) -> str:
    """
    Animate a static image - bring photos and images to life with AI-generated motion.

    WHEN TO USE:
    - User provides an image URL and wants to animate it
    - User wants to add motion to an existing photo/image
    - User says "make this image move" or "animate this picture"
    - User wants to create video from a specific starting frame

    MODELS:
    - kling25 (DEFAULT - Kling 2.5): Best overall quality and motion realism
      * Best for: Professional animations, realistic motion, character animation
      * Supports camera control and motion presets

    - minimax: Good balance of speed and quality
      * Best for: General purpose animations, quick results

    - veo3 (Veo 3): High-end video generation
      * Best for: Premium quality, complex scenes

    - wan25-fast (Wan 2.5 Fast): Fastest processing
      * Best for: Quick iterations, testing, speed priority
      * Supports custom duration (1-10 seconds)

    - seedance: Alternative animation model
      * Best for: Artistic effects, creative animations

    MOTION PRESETS (optional):
    Format: "preset_name:strength" where strength is 0.0-1.0
    Available presets:
    - objects_around:0.7 - Camera orbits around the subject
    - zoom_in:0.5 - Camera zooms into the scene
    - zoom_out:0.5 - Camera zooms out from the scene
    - pan_left:0.6 - Camera pans to the left
    - pan_right:0.6 - Camera pans to the right
    - tilt_up:0.6 - Camera tilts upward
    - tilt_down:0.6 - Camera tilts downward

    ASPECT RATIOS:
    - 9:16 (portrait): TikTok, Instagram Stories, vertical content
    - 16:9 (landscape): YouTube, cinematic, horizontal videos
    - 1:1 (square): Instagram feed, balanced composition
    - 4:3 / 3:4: Traditional video formats

    Args:
        image_url: URL of the image to animate (must be valid HTTP/HTTPS URL)
        prompt: Description of the motion/animation you want
        aspect_ratio: Video aspect ratio (default: 9:16)
        model: Which model to use (default: kling25)
        motion_presets: Optional motion control (e.g., "objects_around:0.7")

    Returns:
        JSON string with job details
    """
    logger.info("i2v_tool_called", prompt=prompt[:50], model=model)

    motions = None
    if motion_presets:
        try:
            motion_id, strength_str = motion_presets.split(":")
            motions = [Motion(id=motion_id.strip(), strength=float(strength_str))]
        except Exception:
            pass

    request = I2VRequest(
        input_images=[InputImage(image_url=image_url)],  # type: ignore
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        motions=motions,
    )

    result = await i2v_service.create_video(model, request)

    return json.dumps({
        "_higgsfield_job": True,
        "job_set_id": result.job_set_id,
        "job_type": "image-to-video",
        "model": model,
        "status": result.status,
        "parameters": {
            "image_url": image_url,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "motion_presets": motion_presets,
        },
    })

