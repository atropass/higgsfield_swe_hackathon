from typing import Any, Dict

from app.clients.higgsfield_base import HiggsFieldBaseClient


class I2VClient(HiggsFieldBaseClient):
    ENDPOINTS = {
        "kling25": "/generate/kling-2-5",
        "minimax": "/v1/image2video/minimax",
        "seedance": "/v1/image2video/seedance",
        "veo3": "/v1/image2video/veo3",
        "wan25-fast": "/generate/wan-25-fast",
    }

    async def generate_video(
        self, model: str, request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        endpoint = self.ENDPOINTS.get(model)
        if not endpoint:
            raise ValueError(f"Unknown I2V model: {model}")

        return await self.post(endpoint, request_data)


i2v_client = I2VClient()
