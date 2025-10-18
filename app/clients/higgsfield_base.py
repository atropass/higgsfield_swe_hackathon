from typing import Any, Dict, Optional

import httpx

from app.core.config import settings
from app.core.errors import UpstreamAPIError
from app.core.logging import get_logger
from app.utils.retry import retry_with_backoff

logger = get_logger(__name__)


class HiggsFieldBaseClient:
    def __init__(self) -> None:
        self.base_url = settings.hf_base_url
        self.timeout = httpx.Timeout(
            connect=settings.request_timeout_connect,
            read=settings.request_timeout_read,
            write=settings.request_timeout_read,
            pool=5.0,
        )

    def _get_headers(self) -> Dict[str, str]:
        return {
            "hf-api-key": settings.hf_api_key,
            "hf-secret": settings.hf_secret,
            "Content-Type": "application/json",
        }

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()

        async def _request() -> Dict[str, Any]:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(
                    "higgsfield_request",
                    method=method,
                    url=url,
                    has_data=data is not None,
                )

                try:
                    response = await client.request(
                        method=method,
                        url=url,
                        json=data,
                        params=params,
                        headers=headers,
                    )

                    logger.info(
                        "higgsfield_response",
                        status_code=response.status_code,
                        url=url,
                    )

                    if response.status_code < 400:
                        return response.json()

                    # Handle error response
                    try:
                        error_data = response.json()
                        error_detail = error_data.get("message") or error_data.get("error") or "Unknown error"
                    except Exception:
                        error_data = {"raw_response": response.text}
                        error_detail = f"HTTP {response.status_code}: {response.text[:200]}"

                    logger.error(
                        "higgsfield_error",
                        status_code=response.status_code,
                        error=error_detail,
                    )

                    raise UpstreamAPIError(
                        message=error_detail,
                        upstream_status=response.status_code,
                        upstream_response=error_data,
                    )

                except httpx.TimeoutException as e:
                    logger.error("higgsfield_timeout", url=url, error=str(e))
                    raise UpstreamAPIError(
                        message="Request to Higgsfield API timed out",
                        status_code=504,
                    ) from e
                except httpx.NetworkError as e:
                    logger.error("higgsfield_network_error", url=url, error=str(e))
                    raise UpstreamAPIError(
                        message="Network error connecting to Higgsfield API",
                        status_code=502,
                    ) from e

        return await retry_with_backoff(_request)

    async def post(
        self, endpoint: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        return await self._make_request("POST", endpoint, data=data)

    async def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        return await self._make_request("GET", endpoint, params=params)

