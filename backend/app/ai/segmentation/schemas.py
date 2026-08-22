from pydantic import BaseModel
from typing import Dict, Optional
from app.ai.common.constants import ModelStatus

class StructureResult(BaseModel):
    detected: bool
    confidence: Optional[float]

class SegmentationResult(BaseModel):
    image_id: str
    model_status: str
    model_name: str
    model_version: str
    clinical_validation: bool
    structures: Dict[str, StructureResult]
