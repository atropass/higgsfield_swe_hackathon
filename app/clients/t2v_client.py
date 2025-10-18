from typing import Any, Dict

from app.clients.higgsfield_base import HiggsFieldBaseClient


class T2VClient(HiggsFieldBaseClient):
    ENDPOINTS = {
        "minimax-hailuo-02": "/generate/minimax-t2v",
        "seedance-v1-lite": "/generate/seedance-v1-lite-t2v",
    }

    async def generate_video(
        self, model: str, request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        endpoint = self.ENDPOINTS.get(model)
        if not endpoint:
            raise ValueError(f"Unknown T2V model: {model}")

        return await self.post(endpoint, request_data)


t2v_client = T2VClient()
