from typing import Any, Dict

from app.clients.higgsfield_base import HiggsFieldBaseClient


class JobsClient(HiggsFieldBaseClient):
    async def get_job_set_status(self, job_set_id: str) -> Dict[str, Any]:
        endpoint = f"/v1/job-sets/{job_set_id}"
        return await self.get(endpoint)


jobs_client = JobsClient()
