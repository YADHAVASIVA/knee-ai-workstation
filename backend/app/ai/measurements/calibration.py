import os
import json
from typing import Optional, Dict, Any
from app.core.config import settings

class CalibrationService:
    def __init__(self, image_id: str):
        self.image_id = image_id
        self.metadata = self._load_metadata()
        self.pixel_spacing = self.metadata.get("pixel_spacing")

    def _load_metadata(self) -> Dict[str, Any]:
        meta_path = os.path.join(settings.UPLOAD_DIR, f"{self.image_id}_meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                return json.load(f)
        return {}

    def is_calibrated(self) -> bool:
        return self.metadata.get("spatial_calibration_available", False) and self.pixel_spacing is not None

    def get_pixel_spacing(self) -> Optional[Dict[str, float]]:
        return self.pixel_spacing

    def pixels_to_mm_x(self, pixels: float) -> Optional[float]:
        if not self.is_calibrated():
            return None
        return pixels * self.pixel_spacing["column_mm"]

    def pixels_to_mm_y(self, pixels: float) -> Optional[float]:
        if not self.is_calibrated():
            return None
        return pixels * self.pixel_spacing["row_mm"]

    def measurement_pixels_to_mm(self, pixels: float, axis: str) -> Optional[float]:
        """axis: 'x' or 'y'"""
        if axis == 'x':
            return self.pixels_to_mm_x(pixels)
        elif axis == 'y':
            return self.pixels_to_mm_y(pixels)
        return None

class OrientationService:
    def __init__(self, image_id: str):
        self.image_id = image_id
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict[str, Any]:
        meta_path = os.path.join(settings.UPLOAD_DIR, f"{self.image_id}_meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                return json.load(f)
        return {}

    def is_orientation_available(self) -> bool:
        return self.metadata.get("orientation_available", False)
        
    def get_orientation(self) -> Optional[list]:
        return self.metadata.get("image_orientation")
        
    def describe_orientation(self) -> str:
        status = self.metadata.get("orientation_status", "UNKNOWN")
        if status == "AVAILABLE":
            return "Known DICOM orientation"
        return "Orientation unknown/unavailable"
