from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.ai.implant_matching.schemas import MatchingResult
from app.ai.implant_matching.service import ImplantMatchingService

router = APIRouter()

@router.post("/{image_id}", response_model=MatchingResult)
async def match_implants(
    image_id: str,
    synthetic_pixel_spacing: Optional[float] = Query(None, description="Bypass uncalibrated status by providing a synthetic mm/px scale for demonstration."),
    db: Session = Depends(get_db)
):
    service = ImplantMatchingService(db)
    return service.match_implants(image_id, synthetic_pixel_spacing)
