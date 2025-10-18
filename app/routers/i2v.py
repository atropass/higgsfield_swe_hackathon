from fastapi import APIRouter

from app.schemas.common import JobResponse
from app.schemas.i2v import (
    Kling25I2VRequest,
    MinimaxI2VRequest,
    Veo3I2VRequest,
    Wan25FastI2VRequest,
    I2VRequest,
)
from app.services.i2v_service import i2v_service

router = APIRouter(prefix="/v1/i2v", tags=["image-to-video"])


@router.post("/kling25", response_model=JobResponse)
async def create_kling25_video(
    request: Kling25I2VRequest,
) -> JobResponse:
    return await i2v_service.create_video("kling25", request)


@router.post("/minimax", response_model=JobResponse)
async def create_minimax_video(
    request: MinimaxI2VRequest,
) -> JobResponse:
    return await i2v_service.create_video("minimax", request)


@router.post("/seedance", response_model=JobResponse)
async def create_seedance_video(
    request: I2VRequest,
) -> JobResponse:
    return await i2v_service.create_video("seedance", request)


@router.post("/veo3", response_model=JobResponse)
async def create_veo3_video(
    request: Veo3I2VRequest,
) -> JobResponse:
    return await i2v_service.create_video("veo3", request)


@router.post("/wan25-fast", response_model=JobResponse)
async def create_wan25_video(
    request: Wan25FastI2VRequest,
) -> JobResponse:
    return await i2v_service.create_video("wan25-fast", request)
