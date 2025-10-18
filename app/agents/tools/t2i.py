import json

from langchain_core.tools import tool

from app.core.logging import get_logger
from app.schemas.t2i import T2IRequest
from app.services.t2i_service import t2i_service

logger = get_logger(__name__)


@tool
async def generate_text_to_image(
    prompt: str,
    aspect_ratio: str = "1:1",
    batch_size: int = 1,
    model: str = "nano-banana",
) -> str:
    """
    Generate images from text descriptions using AI image generation models.

    WHEN TO USE:
    - User wants to create/generate/make an image or picture
    - User describes a scene, object, or concept they want visualized
    - User wants multiple variations (use batch_size)

    MODELS:
    - nano-banana (DEFAULT): Fast, high-quality general-purpose image generation. Best for most use cases.
    - seedream4: Alternative model, good for artistic/creative images

    ASPECT RATIOS:
    - 1:1 (square): Social media posts, profile pictures (BEST FOR: balanced scenes)
    - 16:9 (landscape): Wallpapers, presentations, wide scenes (BEST FOR: landscapes)
    - 9:16 (portrait): Mobile wallpapers, stories (BEST FOR: people, vertical subjects)
    - 4:3 / 3:4: Traditional photo formats
    - 2:3 / 3:2: Standard photo aspect ratios

    BATCH SIZE:
    - 1-4 images can be generated at once
    - More images = more variety but longer processing time
    - Use batch_size > 1 when user wants variations/options

    Args:
        prompt: Detailed text description of what to generate (be specific!)
        aspect_ratio: Image aspect ratio (default: 1:1)
        batch_size: How many images to generate (1-4, default: 1)
        model: Which model to use (default: nano-banana)

    Returns:
        Job set ID and status message
    """
    print(f"\n{'='*60}")
    print(f"TEXT-TO-IMAGE TOOL CALLED")
    print(f"{'='*60}")
    print(f"Prompt: {prompt}")
    print(f"Model: {model}")
    print(f"Aspect Ratio: {aspect_ratio}")
    print(f"Batch Size: {batch_size}")
    print(f"{'='*60}\n")

    logger.info(
        "t2i_tool_called",
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        batch_size=batch_size,
        model=model,
    )

    request = T2IRequest(
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        batch_size=batch_size,
    )

    result = await t2i_service.create_image(model, request)

    return json.dumps({
        "_higgsfield_job": True,
        "job_set_id": result.job_set_id,
        "job_type": "text-to-image",
        "model": model,
        "status": result.status,
        "parameters": {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "batch_size": batch_size,
        },
        "user_message": f"Perfect! Generating {batch_size} image(s) with {model}. Ready in 1-3 minutes.",
    })

