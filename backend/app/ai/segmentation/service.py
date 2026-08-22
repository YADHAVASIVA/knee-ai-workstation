import os
import json
import time
from typing import Dict, Any
import numpy as np
from PIL import Image
from fastapi import HTTPException

from app.core.config import settings
from app.ai.segmentation.demo import DemonstrationSegmentationModel
from app.ai.segmentation.schemas import SegmentationResult, StructureResult
from app.ai.common.constants import SegmentationClass

class SegmentationService:
    def __init__(self):
        # Determine if real model is available. 
        # For now, we strictly use the demo model since no real model exists in repo.
        self.model = DemonstrationSegmentationModel()
        self.model.load()

    def run_segmentation(self, image_id: str) -> SegmentationResult:
        processed_path = os.path.join(settings.PROCESSED_DIR, f"{image_id}.png")
        if not os.path.exists(processed_path):
            raise HTTPException(status_code=404, detail="Processed image not found for segmentation.")
        
        try:
            # 1. Load image
            with Image.open(processed_path) as img:
                img_array = np.array(img)
            
            start_time = time.time()
            
            # 2. Model Inference
            mask_array = self.model.predict(img_array)
            
            # 3. Basic Quality Checks
            if mask_array.shape[:2] != img_array.shape[:2]:
                raise ValueError("Mask dimensions do not match image dimensions.")
                
            unique_labels = np.unique(mask_array)
            valid_labels = {c.value for c in SegmentationClass}
            if not set(unique_labels).issubset(valid_labels):
                raise ValueError("Invalid classes detected in segmentation mask.")
            
            # 4. Generate colored masks for frontend visualization
            self._save_visualization_masks(image_id, mask_array)
            
            # 5. Extract structured result
            structures = {
                "femur": StructureResult(
                    detected=SegmentationClass.FEMUR in unique_labels,
                    confidence=None # Demo model doesn't compute real confidence
                ),
                "tibia": StructureResult(
                    detected=SegmentationClass.TIBIA in unique_labels,
                    confidence=None
                ),
                "medial_meniscus": StructureResult(
                    detected=SegmentationClass.MEDIAL_MENISCUS in unique_labels,
                    confidence=None
                )
            }
            
            model_info = self.model.get_model_info()
            
            result = SegmentationResult(
                image_id=image_id,
                model_status=model_info["model_status"],
                model_name=model_info["model_name"],
                model_version=model_info["model_version"],
                clinical_validation=model_info["clinical_validation"],
                structures=structures
            )
            
            # 6. Save result JSON
            result_path = os.path.join(settings.MASKS_DIR, image_id, "result.json")
            with open(result_path, "w") as f:
                f.write(result.json())
                
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Segmentation failed: {str(e)}")

    def _save_visualization_masks(self, image_id: str, mask_array: np.ndarray):
        """Saves separate transparent PNGs for each structure for overlay."""
        out_dir = os.path.join(settings.MASKS_DIR, image_id)
        os.makedirs(out_dir, exist_ok=True)
        
        height, width = mask_array.shape
        
        # Colors: RGBA
        colors = {
            SegmentationClass.FEMUR: [255, 0, 0, 128],       # Red
            SegmentationClass.TIBIA: [0, 0, 255, 128],       # Blue
            SegmentationClass.MEDIAL_MENISCUS: [0, 255, 0, 128]  # Green
        }
        
        for cls, color in colors.items():
            # Create RGBA blank image
            rgba_img = np.zeros((height, width, 4), dtype=np.uint8)
            
            # Apply color where mask matches
            target_area = (mask_array == cls.value)
            if np.any(target_area):
                rgba_img[target_area] = color
            
            img = Image.fromarray(rgba_img, mode="RGBA")
            name_map = {
                SegmentationClass.FEMUR: "femur",
                SegmentationClass.TIBIA: "tibia",
                SegmentationClass.MEDIAL_MENISCUS: "medial_meniscus"
            }
            img.save(os.path.join(out_dir, f"{name_map[cls]}.png"), format="PNG")

segmentation_service = SegmentationService()
