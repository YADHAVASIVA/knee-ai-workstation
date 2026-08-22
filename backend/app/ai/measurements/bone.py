import os
import numpy as np
from PIL import Image
from typing import Optional, Tuple
from fastapi import HTTPException

from app.core.config import settings
from app.ai.measurements.calibration import CalibrationService
from app.ai.measurements.bone_schemas import BoneMeasurementResult, BoneMetrics, LineCoordinate

class BoneMeasurementService:
    def get_mask_path(self, image_id: str, structure_name: str) -> str:
        return os.path.join(settings.DATA_DIR, "masks", image_id, f"{structure_name}.png")

    def load_mask(self, image_id: str, structure_name: str) -> np.ndarray:
        path = self.get_mask_path(image_id, structure_name)
        if not os.path.exists(path):
            raise ValueError(f"Mask for structure {structure_name} not found.")
        # Load as RGBA, check alpha > 0
        with Image.open(path) as img:
            img = img.convert("RGBA")
            rgba_array = np.array(img)
            binary_mask = (rgba_array[:, :, 3] > 0).astype(np.uint8)
        return binary_mask

    def calculate_bone_metrics(self, mask_array: np.ndarray, calibration: CalibrationService) -> Optional[BoneMetrics]:
        rows, cols = np.where(mask_array > 0)
        
        if len(rows) == 0:
            return None
            
        min_y, max_y = np.where(mask_array > 0)[0][[0, -1]]
        min_x, max_x = np.where(mask_array > 0)[1][[0, -1]]
        
        width_pixels = float(max_x - min_x + 1)
        ap_pixels = float(max_y - min_y + 1)
        
        mid_x = (min_x + max_x) // 2
        mid_y = (min_y + max_y) // 2
        
        width_mm = calibration.pixels_to_mm_x(width_pixels)
        ap_mm = calibration.pixels_to_mm_y(ap_pixels)
        
        return BoneMetrics(
            width_pixels=width_pixels,
            ap_dimension_pixels=ap_pixels,
            width_mm=width_mm,
            ap_dimension_mm=ap_mm,
            width_line=LineCoordinate(start_x=float(min_x), start_y=float(mid_y), end_x=float(max_x), end_y=float(mid_y)),
            ap_line=LineCoordinate(start_x=float(mid_x), start_y=float(min_y), end_x=float(mid_x), end_y=float(max_y))
        )

    def measure_bones(self, image_id: str) -> BoneMeasurementResult:
        from app.ai.measurements.calibration import OrientationService
        
        try:
            femur_mask = self.load_mask(image_id, "femur")
            tibia_mask = self.load_mask(image_id, "tibia")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
            
        calibration = CalibrationService(image_id)
        orientation = OrientationService(image_id)
        
        femur_metrics = self.calculate_bone_metrics(femur_mask, calibration)
        tibia_metrics = self.calculate_bone_metrics(tibia_mask, calibration)
        
        warning = None
        if not calibration.is_calibrated():
            warning = "Uncalibrated image. Providing image-plane pixel measurements only."
        elif not orientation.is_orientation_available():
            warning = "Anatomical orientation unknown. AP values represent vertical image-plane geometry."
            
        return BoneMeasurementResult(
            image_id=image_id,
            femur=femur_metrics,
            tibia=tibia_metrics,
            calibration_available=calibration.is_calibrated(),
            orientation_status=orientation.describe_orientation() if orientation.is_orientation_available() else "unknown",
            warning=warning,
            segmentation_model_status="demo",
            measurement_status="success"
        )
