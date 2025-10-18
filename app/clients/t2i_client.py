from typing import Any, Dict

from app.clients.higgsfield_base import HiggsFieldBaseClient


class T2IClient(HiggsFieldBaseClient):
    ENDPOINTS = {
        "nano-banana": "/v1/text2image/nano-banana",
        "seedream4": "/v1/text2image/seedream",
    }

    async def generate_image(
        self, model: str, request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        endpoint = self.ENDPOINTS.get(model)
        if not endpoint:
            raise ValueError(f"Unknown T2I model: {model}")

        return await self.post(endpoint, request_data)


t2i_client = T2IClient()
