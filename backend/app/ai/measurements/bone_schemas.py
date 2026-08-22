from pydantic import BaseModel
from typing import Optional, Dict

class LineCoordinate(BaseModel):
    start_x: int
    start_y: int
    end_x: int
    end_y: int

class BoneMetrics(BaseModel):
    width_pixels: float
    width_mm: Optional[float]
    ap_dimension_pixels: float
    ap_dimension_mm: Optional[float]
    width_line: LineCoordinate
    ap_line: LineCoordinate

class BoneMeasurementResult(BaseModel):
    image_id: str
    measurement_status: str
    segmentation_model_status: str
    calibration_available: bool
    orientation_status: str
    femur: Optional[BoneMetrics]
    tibia: Optional[BoneMetrics]
    warning: str
