from typing import Any, Dict

from fastapi import APIRouter

from app.services.jobs_service import jobs_service

router = APIRouter(prefix="/v1/jobs", tags=["jobs"])


@router.get("/{job_set_id}")
async def get_job_status(
    job_set_id: str,
) -> Dict[str, Any]:
    return await jobs_service.get_job_status(job_set_id)


@router.post("/{job_set_id}/refresh")
async def refresh_job_status(
    job_set_id: str,
) -> Dict[str, Any]:
    return await jobs_service.refresh_job_status(job_set_id)
