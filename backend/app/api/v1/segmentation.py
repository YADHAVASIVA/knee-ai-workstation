import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.ai.segmentation.service import segmentation_service
from app.ai.segmentation.schemas import SegmentationResult
from app.core.config import settings

router = APIRouter()

@router.post("/{image_id}", response_model=SegmentationResult)
async def run_segmentation(image_id: str):
    return segmentation_service.run_segmentation(image_id)

@router.get("/{image_id}/mask/{structure}")
async def get_mask(image_id: str, structure: str):
    valid_structures = {"femur", "tibia", "medial_meniscus"}
    if structure not in valid_structures:
        raise HTTPException(status_code=400, detail="Invalid structure requested.")
        
    mask_path = os.path.join(settings.MASKS_DIR, image_id, f"{structure}.png")
    if not os.path.exists(mask_path):
        raise HTTPException(status_code=404, detail="Mask not found.")
        
    return FileResponse(mask_path, media_type="image/png")
