from langchain_core.tools import tool

from app.core.logging import get_logger
from app.services.jobs_service import jobs_service

logger = get_logger(__name__)


@tool
async def check_job_status(
    job_set_id: str,
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

    IMPORTANT:
    - Extract the job_set_id from the conversation history (look for the JSON with _higgsfield_job)
    - The job_set_id was returned when the generation job was created

    Args:
        job_set_id: The job set ID to check (required, find it in conversation history)

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

    result_urls = []

    for job in jobs:
        job_status = job.get("status", "unknown")

        if job_status == "completed":
            results = job.get("results") or job.get("result")
            if results:
                url = None
                if isinstance(results, dict):
                    if results.get("raw", {}).get("url"):
                        url = results["raw"]["url"]
                    elif results.get("min", {}).get("url"):
                        url = results["min"]["url"]
                    elif results.get("url"):
                        url = results["url"]
                elif isinstance(results, str):
                    url = results

                if url:
                    result_urls.append(url)

    print(f"Status: {status}")
    print(f"Result URLs: {len(result_urls)}\n")

    if status == "completed" and result_urls:
        message = "Great news! Your content is ready!\n\n"
        for url in result_urls:
            message += f"Download: {url}\n"
    elif status == "processing":
        message = "Still processing... hang tight!"
    elif status == "queued":
        message = "Your job is queued and will start soon!"
    elif status == "failed":
        message = "Unfortunately, the job failed."
    else:
        message = f"Status: {status}"

    return message


@tool
async def refresh_job_status(
    job_set_id: str,
) -> str:
    """
    Force refresh the latest status of a generation job.

    WHEN TO USE:
    - User explicitly asks to "refresh" or "update" status
    - Previous check showed "processing" and user wants latest progress

    IMPORTANT:
    - Extract the job_set_id from the conversation history (look for the JSON with _higgsfield_job)
    - The job_set_id was returned when the generation job was created

    Args:
        job_set_id: The job set ID to refresh (required, find it in conversation history)

    Returns:
        Latest status message with download URLs if completed
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

    result_urls = []

    for job in jobs:
        job_status = job.get("status", "unknown")

        if job_status == "completed":
            results = job.get("results") or job.get("result")
            if results:
                url = None
                if isinstance(results, dict):
                    if results.get("raw", {}).get("url"):
                        url = results["raw"]["url"]
                    elif results.get("min", {}).get("url"):
                        url = results["min"]["url"]
                    elif results.get("url"):
                        url = results["url"]
                elif isinstance(results, str):
                    url = results

                if url:
                    result_urls.append(url)

    print(f"Refreshed Status: {status}")
    print(f"Result URLs: {len(result_urls)}\n")

    if status == "completed" and result_urls:
        message = "Great news! Your content is ready!\n\n"
        for url in result_urls:
            message += f"Download: {url}\n"
    elif status == "processing":
        message = "Still processing... almost there!"
    elif status == "queued":
        message = "Your job is queued and will start soon!"
    elif status == "failed":
        message = "The job failed."
    else:
        message = f"Status: {status}"

    return message
