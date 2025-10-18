from fastapi import APIRouter

from app.schemas.common import JobResponse
from app.schemas.t2i import NanoBananaT2IRequest, Seedream4T2IRequest
from app.services.t2i_service import t2i_service

router = APIRouter(prefix="/v1/t2i", tags=["text-to-image"])


@router.post("/nano-banana", response_model=JobResponse)
async def create_nano_banana_image(
    request: NanoBananaT2IRequest,
) -> JobResponse:
    return await t2i_service.create_image("nano-banana", request)


@router.post("/seedream4", response_model=JobResponse)
async def create_seedream4_image(
    request: Seedream4T2IRequest,
) -> JobResponse:
    return await t2i_service.create_image("seedream4", request)
