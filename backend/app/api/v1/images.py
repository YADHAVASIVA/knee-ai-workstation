from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from app.services.image_service import ImagePreprocessingService

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    result = await ImagePreprocessingService.save_uploaded_file(file)
    # Remove internal_filename before returning to client
    result.pop("internal_filename", None)
    return result

@router.post("/preprocess/{image_id}")
async def preprocess_image(image_id: str):
    result = ImagePreprocessingService.preprocess_image(image_id)
    return result

@router.get("/{image_id}/preview")
async def get_image_preview(image_id: str):
    preview_path = ImagePreprocessingService.get_preview_path(image_id)
    return FileResponse(preview_path, media_type="image/jpeg")

@router.get("/{image_id}/metadata")
async def get_image_metadata(image_id: str):
    import os, json
    from app.core.config import settings
    from fastapi import HTTPException
    
    meta_path = os.path.join(settings.UPLOAD_DIR, f"{image_id}_meta.json")
    if not os.path.exists(meta_path):
        raise HTTPException(status_code=404, detail="Metadata not found")
        
    with open(meta_path, "r") as f:
        metadata = json.load(f)
        
    # Safe subset of metadata for frontend (privacy filter)
    safe_metadata = {
        "image_id": metadata.get("image_id"),
        "format": metadata.get("format", "IMAGE"),
        "modality": metadata.get("modality", "UNKNOWN"),
        "dimensions": {
            "width": metadata.get("width", metadata.get("columns", 0)),
            "height": metadata.get("height", metadata.get("rows", 0))
        },
        "pixel_spacing": metadata.get("pixel_spacing"),
        "orientation_available": metadata.get("orientation_available", False),
        "spatial_calibration_available": metadata.get("spatial_calibration_available", False)
    }
    return safe_metadata

@router.get("/{image_id}/pipeline-status")
async def get_pipeline_status(image_id: str):
    import os, json
    from app.core.config import settings
    from fastapi import HTTPException
    
    meta_path = os.path.join(settings.UPLOAD_DIR, f"{image_id}_meta.json")
    if not os.path.exists(meta_path):
        raise HTTPException(status_code=404, detail="Image not found")
        
    with open(meta_path, "r") as f:
        metadata = json.load(f)
        
    # Return mock status pipeline for now. Since we are blocked, this reflects it.
    return {
        "upload_status": "SUCCESS",
        "pixel_load_status": "SUCCESS",
        "preprocessing_status": "SUCCESS",
        "quality_status": "SUCCESS",
        "anatomy_status": "SUCCESS",
        "model_status": "MODEL_UNAVAILABLE",
        "inference_status": "BLOCKED",
        "report_status": "BLOCKED"
    }
