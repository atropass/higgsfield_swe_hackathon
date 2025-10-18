from typing import Any, Dict, Union
from uuid import uuid4

from app.clients.t2v_client import t2v_client
from app.core.logging import get_logger
from app.schemas.common import JobResponse
from app.schemas.t2v import MinimaxT2VRequest, SeedanceT2VRequest

logger = get_logger(__name__)


class T2VService:
    async def create_video(
        self, model: str, request: Union[MinimaxT2VRequest, SeedanceT2VRequest]
    ) -> JobResponse:
        request_id = str(uuid4())

        logger.info(
            "t2v_request",
            request_id=request_id,
            model=model,
            prompt_length=len(request.prompt),
        )

        if isinstance(request, MinimaxT2VRequest):
            payload: Dict[str, Any] = {
                "params": {
                    "prompt": request.prompt,
                    "duration": request.duration,
                    "resolution": request.resolution,
                    "enable_prompt_optimizier": request.enable_prompt_optimizer,
                }
            }
        else:
            payload = {
                "params": {
                    "prompt": request.prompt,
                    "duration": request.duration,
                    "resolution": request.resolution,
                    "aspect_ratio": request.aspect_ratio,
                    "camera_fixed": request.camera_fixed,
                }
            }

        if request.metadata:
            payload["metadata"] = request.metadata

        response = await t2v_client.generate_video(model, payload)

        job_set_id = response.get("id") or response.get("job_set_id")

        logger.info(
            "t2v_job_created",
            request_id=request_id,
            job_set_id=job_set_id,
            model=model,
        )

        return JobResponse(
            request_id=request_id,
            job_set_id=job_set_id,
            status="queued",
            message="T2V job submitted successfully",
        )


t2v_service = T2VService()
