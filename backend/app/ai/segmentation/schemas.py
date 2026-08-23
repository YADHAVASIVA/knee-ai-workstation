from pydantic import BaseModel
from typing import Dict, Optional

class StructureResult(BaseModel):
    detected: bool
    confidence: Optional[float]

class SegmentationResult(BaseModel):
    image_id: str
    model_status: str
    model_name: str
    model_version: str
    is_demo: bool  # NEW
    clinical_validation: bool
    structures: Dict[str, StructureResult]
