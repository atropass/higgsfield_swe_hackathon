
from fastapi import APIRouter

from app.schemas.common import JobResponse
from app.schemas.t2v import MinimaxT2VRequest, SeedanceT2VRequest
from app.services.t2v_service import t2v_service

router = APIRouter(prefix="/v1/t2v", tags=["text-to-video"])


@router.post("/minimax-hailuo-02", response_model=JobResponse)
async def create_minimax_video(
    request: MinimaxT2VRequest,
) -> JobResponse:
    return await t2v_service.create_video("minimax-hailuo-02", request)


@router.post("/seedance-v1-lite", response_model=JobResponse)
async def create_seedance_video(
    request: SeedanceT2VRequest,
) -> JobResponse:
    return await t2v_service.create_video("seedance-v1-lite", request)
