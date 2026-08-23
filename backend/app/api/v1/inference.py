from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.ai.inference_service import MedicalImageInferenceService
from app.services.image_service import ImagePreprocessingService
import os
from app.core.config import settings

router = APIRouter()

@router.post("/{image_id}")
async def run_inference(image_id: str, case_id: str = "default_case", task: str = "OA_CLASSIFICATION"):
    """
    Run the unified inference pipeline on a specific image.
    """
    # 1. Locate the image and metadata
    img_path = os.path.join(settings.UPLOAD_DIR, "images", f"{image_id}.png")
    if not os.path.exists(img_path):
        # Maybe it's jpg or dicom
        img_path = os.path.join(settings.UPLOAD_DIR, "images", f"{image_id}.jpg")
        if not os.path.exists(img_path):
            img_path = os.path.join(settings.UPLOAD_DIR, "dicom", f"{image_id}.dcm")
            
    if not os.path.exists(img_path):
        raise HTTPException(status_code=404, detail="Image not found")

    import json
    meta_path = os.path.join(settings.UPLOAD_DIR, f"{image_id}_meta.json")
    metadata = {}
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            metadata = json.load(f)

    # 2. Run inference orchestrator
    result = MedicalImageInferenceService.run_inference(
        case_id=case_id,
        image_id=image_id,
        filepath=img_path,
        metadata=metadata,
        target_task=task
    )

    return result
