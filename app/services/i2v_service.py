from typing import Any, Dict
from uuid import uuid4

from app.clients.i2v_client import i2v_client
from app.core.logging import get_logger
from app.schemas.common import JobResponse
from app.schemas.i2v import I2VRequest

logger = get_logger(__name__)


class I2VService:
    async def create_video(
        self, model: str, request: I2VRequest
    ) -> JobResponse:
        request_id = str(uuid4())

        logger.info(
            "i2v_request",
            request_id=request_id,
            model=model,
            num_images=len(request.input_images),
        )

        payload: Dict[str, Any] = {
            "params": {
                "input_image": {
                    "type": request.input_images[0].type,
                    "image_url": str(request.input_images[0].image_url)
                },
                "prompt": request.prompt,
                "aspect_ratio": request.aspect_ratio,
            }
        }

        if hasattr(request, 'camera_control') and request.camera_control:
            payload["params"]["camera_control"] = request.camera_control

        if request.motions:
            payload["params"]["motions"] = [
                {"id": motion.id, "strength": motion.strength}
                for motion in request.motions
            ]

        if request.metadata:
            payload["metadata"] = request.metadata

        response = await i2v_client.generate_video(model, payload)

        job_set_id = response.get("id") or response.get("job_set_id")

        logger.info(
            "i2v_job_created",
            request_id=request_id,
            job_set_id=job_set_id,
            model=model,
        )

        return JobResponse(
            request_id=request_id,
            job_set_id=job_set_id,
            status="queued",
            message="I2V job submitted successfully",
        )


i2v_service = I2VService()
