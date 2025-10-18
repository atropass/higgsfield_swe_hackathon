"""Tools for the chat agent to interact with Higgsfield APIs."""

import json
from typing import Annotated, Any, Dict

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState

from app.core.logging import get_logger
from app.schemas.i2v import I2VRequest, InputImage, Motion
from app.schemas.t2i import T2IRequest
from app.schemas.t2v import MinimaxT2VRequest, SeedanceT2VRequest
from app.services.i2v_service import i2v_service
from app.services.jobs_service import jobs_service
from app.services.t2i_service import t2i_service
from app.services.t2v_service import t2v_service

logger = get_logger(__name__)


@tool
async def generate_text_to_image(
    prompt: str,
    aspect_ratio: str = "1:1",
    batch_size: int = 1,
    model: str = "nano-banana",
    state: Annotated[Dict[str, Any], InjectedState] = {},
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
    - 1:1 (square): Social media posts, profile pictures, general images
    - 16:9 (landscape): Wallpapers, presentations, wide scenes
    - 9:16 (portrait): Mobile wallpapers, stories, vertical content
    - 4:3, 3:4, 2:3, 3:2: Standard photo formats

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

    tool_result = {
        "action": "generate_image",
        "job_set_id": result.job_set_id,
        "status": result.status,
        "job_type": "text-to-image",
        "model": model,
        "parameters": {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "batch_size": batch_size,
        },
        "estimated_time": "1-3 minutes",
        "message": f"Image generation started! Creating {batch_size} image(s) with {model}.",
    }

    return f"TOOL_RESULT: {json.dumps(tool_result)}"


@tool
async def generate_text_to_video(
    prompt: str,
    aspect_ratio: str = "16:9",
    duration: int = 5,
    model: str = "minimax-hailuo-02",
    resolution: str = "768",
    state: Annotated[Dict[str, Any], InjectedState] = {},
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
    - 16:9 (landscape): YouTube, horizontal videos, cinematic
    - 9:16 (portrait): TikTok, Instagram Reels, vertical videos
    - 1:1 (square): Social media, Instagram feed
    - 4:3, 3:4: Standard video formats

    Args:
        prompt: Detailed description of the video scene and action
        aspect_ratio: Video aspect ratio (default: 16:9)
        duration: Video length in seconds, 1-10 (default: 5)
        model: Which model to use (default: minimax-hailuo-02)
        resolution: Video quality - 768/1280 for minimax, 480/720 for seedance

    Returns:
        Job set ID and status message
    """
    print(f"\n{'='*60}")
    print(f"TEXT-TO-VIDEO TOOL CALLED")
    print(f"{'='*60}")
    print(f"Prompt: {prompt}")
    print(f"Model: {model}")
    print(f"Aspect Ratio: {aspect_ratio}")
    print(f"Duration: {duration}s")
    print(f"Resolution: {resolution}")
    print(f"{'='*60}\n")

    logger.info(
        "t2v_tool_called",
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        duration=duration,
        model=model,
    )

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

    # Return structured JSON for frontend parsing
    tool_result = {
        "action": "generate_video",
        "job_set_id": result.job_set_id,
        "status": result.status,
        "job_type": "text-to-video",
        "model": model,
        "parameters": {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "duration": duration,
            "resolution": resolution,
        },
        "estimated_time": "2-5 minutes",
        "message": f"🎬 Video generation started! Creating a {duration}s video with {model}.",
    }

    return f"TOOL_RESULT: {json.dumps(tool_result)}"


@tool
async def generate_image_to_video(
    image_url: str,
    prompt: str,
    aspect_ratio: str = "9:16",
    model: str = "kling25",
    motion_presets: str | None = None,
    state: Annotated[Dict[str, Any], InjectedState] = {},
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
    Use format "preset_name:strength" (strength 0.0-1.0)
    - objects_around:0.7 - Camera orbits around subject
    - zoom_in:0.5 - Camera zooms into scene
    - pan_left:0.6 - Camera pans left

    ASPECT RATIOS:
    - 9:16 (portrait): TikTok, Instagram Stories, vertical
    - 16:9 (landscape): YouTube, cinematic
    - 1:1 (square): Instagram feed

    Args:
        image_url: URL of the image to animate (must be valid HTTP/HTTPS URL)
        prompt: Description of the motion/animation you want
        aspect_ratio: Video aspect ratio (default: 9:16)
        model: Which model to use (default: kling25)
        motion_presets: Optional motion control (e.g., "objects_around:0.7")

    Returns:
        Job set ID and status message
    """
    print(f"\n{'='*60}")
    print(f"IMAGE-TO-VIDEO TOOL CALLED")
    print(f"{'='*60}")
    print(f"Image URL: {image_url}")
    print(f"Prompt: {prompt}")
    print(f"Model: {model}")
    print(f"Aspect Ratio: {aspect_ratio}")
    print(f"Motion Presets: {motion_presets or 'None'}")
    print(f"{'='*60}\n")

    logger.info(
        "i2v_tool_called",
        image_url=image_url,
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        model=model,
    )

    # Parse motion presets if provided
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

    tool_result = {
        "action": "generate_video_from_image",
        "job_set_id": result.job_set_id,
        "status": result.status,
        "job_type": "image-to-video",
        "model": model,
        "parameters": {
            "image_url": image_url,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "motion_presets": motion_presets,
        },
        "estimated_time": "2-4 minutes",
        "message": f"Image-to-video generation started! Animating your image with {model}.",
    }

    return f"TOOL_RESULT: {json.dumps(tool_result)}"


@tool
async def check_job_status(
    job_set_id: str,
    state: Annotated[Dict[str, Any], InjectedState] = {},
) -> str:
    """
    Check the current status and progress of a generation job.

    WHEN TO USE:
    - User asks about job status ("how's my job doing?", "is it ready?")
    - User provides a job_set_id and wants an update
    - User asks to check on a previous generation
    - After creating a job, user wants to know progress

    JOB STATUSES:
    - queued: Job is waiting to be processed
    - processing: Job is currently being generated (may show progress %)
    - completed: Job is done! Result URLs will be available
    - failed: Job encountered an error

    WHAT YOU'LL GET:
    - Overall job set status
    - Individual job progress (if multiple jobs in batch)
    - Result URLs when completed
    - Progress percentage when processing

    Args:
        job_set_id: The job set ID to check (format: hf-job-set-xxx or similar)

    Returns:
        Detailed status, progress, and result URLs if available
    """
    print(f"\n{'='*60}")
    print(f"CHECK JOB STATUS TOOL CALLED")
    print(f"{'='*60}")
    print(f"Job Set ID: {job_set_id}")
    print(f"{'='*60}\n")

    logger.info("job_status_tool_called", job_set_id=job_set_id)

    result = await jobs_service.get_job_status(job_set_id)

    status = result.get("status", "unknown")
    jobs = result.get("jobs", [])

    # Collect result URLs if completed
    result_urls = []
    progress_info = []

    for idx, job in enumerate(jobs, 1):
        job_status = job.get("status", "unknown")
        progress = job.get("progress", 0)

        job_info = {
            "job_number": idx,
            "status": job_status,
            "progress": progress
        }

        if job_status == "completed" and job.get("result"):
            result_data = job["result"]
            if result_data.get("url"):
                result_urls.append(result_data["url"])
                job_info["result_url"] = result_data["url"]

        progress_info.append(job_info)

    print(f"Status Retrieved: {status}")
    print(f"Number of Jobs: {len(jobs)}\n")

    tool_result = {
        "action": "check_status",
        "job_set_id": job_set_id,
        "status": status,
        "jobs": progress_info,
        "result_urls": result_urls,
        "completed": status == "completed",
        "message": f"📊 Job status: {status}" + (f" - {len(result_urls)} result(s) ready!" if result_urls else "")
    }

    return f"TOOL_RESULT: {json.dumps(tool_result)}"


@tool
async def refresh_job_status(
    job_set_id: str,
    state: Annotated[Dict[str, Any], InjectedState] = {},
) -> str:
    """
    Refresh and get the latest status of a generation job (force update).

    WHEN TO USE:
    - User explicitly asks to "refresh" or "update" job status
    - User wants the most recent information after waiting
    - Previous check showed "processing" and user wants latest progress

    This is similar to check_job_status but explicitly refreshes from server.
    Use check_job_status for normal status checks.

    Args:
        job_set_id: The job set ID to refresh

    Returns:
        Latest status and progress information
    """
    print(f"\n{'='*60}")
    print(f"REFRESH JOB STATUS TOOL CALLED")
    print(f"{'='*60}")
    print(f"Job Set ID: {job_set_id}")
    print(f"{'='*60}\n")

    logger.info("refresh_job_status_tool_called", job_set_id=job_set_id)

    result = await jobs_service.refresh_job_status(job_set_id)

    status = result.get("status", "unknown")
    jobs = result.get("jobs", [])

    # Collect result URLs if completed
    result_urls = []
    progress_info = []

    for idx, job in enumerate(jobs, 1):
        job_status = job.get("status", "unknown")
        progress = job.get("progress", 0)

        job_info = {
            "job_number": idx,
            "status": job_status,
            "progress": progress
        }

        if job_status == "completed" and job.get("result"):
            result_data = job["result"]
            if result_data.get("url"):
                result_urls.append(result_data["url"])
                job_info["result_url"] = result_data["url"]

        progress_info.append(job_info)

    print(f"Refreshed Status: {status}")
    print(f"Number of Jobs: {len(jobs)}\n")

    tool_result = {
        "action": "refresh_status",
        "job_set_id": job_set_id,
        "status": status,
        "jobs": progress_info,
        "result_urls": result_urls,
        "completed": status == "completed",
        "message": f"[REFRESHED] Job status: {status}" + (f" - {len(result_urls)} result(s) ready!" if result_urls else "")
    }

    return f"TOOL_RESULT: {json.dumps(tool_result)}"


# List of all tools
CHAT_TOOLS = [
    generate_text_to_image,
    generate_text_to_video,
    generate_image_to_video,
    check_job_status,
    refresh_job_status,
]

