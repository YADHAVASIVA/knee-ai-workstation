from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.ai.xray.service import XRayInferenceService
from app.ai.xray.schemas import XRayInferenceOutput
from app.services.image_service import ImagePreprocessingService

router = APIRouter()
service = XRayInferenceService()

@router.post("/analyze/{image_id}", response_model=XRayInferenceOutput)
async def analyze_xray(image_id: str):
    image_path = ImagePreprocessingService.get_preview_path(image_id)
    if not image_path:
        raise HTTPException(status_code=404, detail="Image not found")
        
    try:
        with open(image_path, "rb") as f:
            content = f.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not read image file")
        
    return service.analyze_image(content, image_id)
