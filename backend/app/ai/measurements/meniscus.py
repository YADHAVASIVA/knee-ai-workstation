import os
import json
import numpy as np
from PIL import Image
from fastapi import HTTPException

from app.core.config import settings
from app.ai.common.constants import SegmentationClass
from app.ai.measurements.calibration import CalibrationService
from app.ai.measurements.geometry import calculate_meniscus_thickness
from app.ai.measurements.schemas import MeasurementResult, MeasurementLocation

class MeniscusMeasurementService:
    @staticmethod
    def measure_thickness(image_id: str) -> MeasurementResult:
        # 1. Validate image and segmentation existence
        processed_path = os.path.join(settings.PROCESSED_DIR, f"{image_id}.png")
        if not os.path.exists(processed_path):
            raise HTTPException(status_code=404, detail="Source image not found.")
            
        result_json_path = os.path.join(settings.MASKS_DIR, image_id, "result.json")
        if not os.path.exists(result_json_path):
            raise HTTPException(status_code=404, detail="Segmentation result not found.")
            
        meniscus_mask_path = os.path.join(settings.MASKS_DIR, image_id, "medial_meniscus.png")
        if not os.path.exists(meniscus_mask_path):
            raise HTTPException(status_code=404, detail="Medial meniscus mask not found.")

        # Load segmentation metadata to check model status
        with open(result_json_path, "r") as f:
            seg_meta = json.load(f)
            model_status = seg_meta.get("model_status", "unknown")

        # 3. Load Medial Meniscus mask
        with Image.open(meniscus_mask_path) as img:
            # Mask is RGBA where meniscus is colored. We can extract the alpha channel or presence of color
            mask_rgba = np.array(img)
            # Create a 2D binary mask where the pixel is non-zero (since the mask was saved as colored overlay)
            # Actually, the original segmentation array is not saved.
            # I can reconstruct it from the colored mask: if alpha > 0, it belongs to meniscus.
            binary_mask = (mask_rgba[:, :, 3] > 0).astype(np.uint8)

        # Ensure mask dimensions match source
        with Image.open(processed_path) as src_img:
            src_width, src_height = src_img.size
            
        mask_height, mask_width = binary_mask.shape
        if mask_width != src_width or mask_height != src_height:
            raise HTTPException(status_code=400, detail="Mask dimensions do not match source image.")

        if not np.any(binary_mask):
            raise HTTPException(status_code=400, detail="Medial meniscus mask is empty.")

        # 4. Measure
        raw_measurements = calculate_meniscus_thickness(binary_mask, 1) # target_class=1 because binary_mask is 1
        
        if len(raw_measurements) == 0:
            raise HTTPException(status_code=400, detail="Unable to calculate measurements on provided mask.")

        # 5. Calibrate
        calibration = CalibrationService(image_id)
        
        locations = []
        for rm in raw_measurements:
            loc = MeasurementLocation(
                name=rm["name"],
                x=rm["x"],
                y=rm["y"],
                thickness_pixels=rm["thickness_pixels"],
                thickness_mm=calibration.pixels_to_mm_y(rm["thickness_pixels"])
            )
            locations.append(loc)

        # 6. Mean Thickness
        valid_pixel_thicknesses = [loc.thickness_pixels for loc in locations]
        mean_pixels = sum(valid_pixel_thicknesses) / len(valid_pixel_thicknesses) if valid_pixel_thicknesses else 0.0
        
        mean_mm = calibration.pixels_to_mm_y(mean_pixels)

        warning_msg = None
        if not calibration.is_calibrated():
            warning_msg = "Physical calibration unavailable."
        
        if model_status == "demo":
            warning_msg = (warning_msg + " | " if warning_msg else "") + "Measurement based on demonstration segmentation."

        result = MeasurementResult(
            image_id=image_id,
            measurement_type="medial_meniscus_thickness",
            measurement_status="success",
            segmentation_model_status=model_status,
            calibration_available=calibration.is_calibrated(),
            locations=locations,
            mean_thickness_pixels=mean_pixels,
            mean_thickness_mm=mean_mm,
            unit="pixels" if not calibration.is_calibrated() else "mm",
            warning=warning_msg
        )

        return result
