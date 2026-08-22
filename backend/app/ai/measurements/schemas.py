from pydantic import BaseModel
from typing import List, Optional

class MeasurementLocation(BaseModel):
    name: str
    x: float
    y: float
    thickness_pixels: float
    thickness_mm: Optional[float]

class MeasurementResult(BaseModel):
    image_id: str
    measurement_type: str
    measurement_status: str
    segmentation_model_status: str
    calibration_available: bool
    locations: List[MeasurementLocation]
    mean_thickness_pixels: float
    mean_thickness_mm: Optional[float]
    unit: str
    warning: Optional[str]
