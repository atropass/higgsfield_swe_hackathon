from typing import Any, Dict
from uuid import uuid4

from app.clients.t2i_client import t2i_client
from app.core.logging import get_logger
from app.schemas.common import JobResponse
from app.schemas.t2i import T2IRequest

logger = get_logger(__name__)


class T2IService:

    async def create_image(
        self, model: str, request: T2IRequest
    ) -> JobResponse:
        request_id = str(uuid4())

        logger.info(
            "t2i_request",
            request_id=request_id,
            model=model,
            prompt_length=len(request.prompt),
            batch_size=request.batch_size,
        )

        payload: Dict[str, Any] = {
            "params": {
                "prompt": request.prompt,
                "aspect_ratio": request.aspect_ratio,
                "input_images": [],
            }
        }

        if request.metadata:
            payload["metadata"] = request.metadata

        response = await t2i_client.generate_image(model, payload)

        job_set_id = response.get("id") or response.get("job_set_id")

        logger.info(
            "t2i_job_created",
            request_id=request_id,
            job_set_id=job_set_id,
            model=model,
        )

        return JobResponse(
            request_id=request_id,
            job_set_id=job_set_id,
            status="queued",
            message="T2I job submitted successfully",
        )


t2i_service = T2IService()
