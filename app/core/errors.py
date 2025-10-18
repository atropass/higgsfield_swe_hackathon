from typing import Any, Dict

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse


class HiggsFieldAPIError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class RateLimitExceeded(HiggsFieldAPIError):
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = 60) -> None:
        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            details={"retry_after": retry_after},
        )


class UpstreamAPIError(HiggsFieldAPIError):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_502_BAD_GATEWAY,
        upstream_status: int | None = None,
        upstream_response: Dict[str, Any] | None = None,
    ) -> None:
        details = {}
        if upstream_status:
            details["upstream_status"] = upstream_status
        if upstream_response:
            details["upstream_response"] = upstream_response

        super().__init__(message=message, status_code=status_code, details=details)


class JobNotFoundError(HiggsFieldAPIError):
    def __init__(self, job_set_id: str) -> None:
        super().__init__(
            message=f"Job set {job_set_id} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            details={"job_set_id": job_set_id},
        )


class IdempotencyConflictError(HiggsFieldAPIError):
    def __init__(self, idempotency_key: str) -> None:
        super().__init__(
            message="Idempotency key reused with different parameters",
            status_code=status.HTTP_409_CONFLICT,
            details={"idempotency_key": idempotency_key},
        )


class ValidationError(HiggsFieldAPIError):
    def __init__(self, message: str, field: str | None = None) -> None:
        details = {"field": field} if field else {}
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details,
        )


async def higgsfield_api_error_handler(
    request: Request, exc: HiggsFieldAPIError
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "code": exc.__class__.__name__,
                "details": exc.details,
            }
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "code": "HTTPException",
            }
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": "Internal server error",
                "code": "InternalServerError",
            }
        },
    )

