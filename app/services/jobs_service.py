from typing import Any, Dict

from app.clients.jobs_client import jobs_client
from app.core.logging import get_logger

logger = get_logger(__name__)


class JobsService:
    async def get_job_status(self, job_set_id: str) -> Dict[str, Any]:
        logger.info("get_job_status", job_set_id=job_set_id)
        return await jobs_client.get_job_set_status(job_set_id)

    async def refresh_job_status(self, job_set_id: str) -> Dict[str, Any]:
        logger.info("refresh_job_status", job_set_id=job_set_id)
        # Could add cache invalidation logic here in the future
        return await jobs_client.get_job_set_status(job_set_id)


jobs_service = JobsService()

