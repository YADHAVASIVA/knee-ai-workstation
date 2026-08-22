import numpy as np
from app.ai.segmentation.model import SegmentationModel
from app.ai.common.constants import SegmentationClass, ModelStatus

class DemonstrationSegmentationModel(SegmentationModel):
    def load(self) -> None:
        pass

    def predict(self, image_array: np.ndarray) -> np.ndarray:
        """
        Creates a deterministic demonstration mask based on image dimensions.
        DO NOT interpret this as a clinical prediction.
        """
        height, width = image_array.shape[:2]
        mask = np.zeros((height, width), dtype=np.uint8)
        
        # Draw fake femur (top center)
        mask[int(height*0.1):int(height*0.4), int(width*0.3):int(width*0.7)] = SegmentationClass.FEMUR
        
        # Draw fake tibia (bottom center)
        mask[int(height*0.6):int(height*0.9), int(width*0.35):int(width*0.65)] = SegmentationClass.TIBIA
        
        # Draw fake medial meniscus (between them on one side)
        mask[int(height*0.45):int(height*0.55), int(width*0.3):int(width*0.5)] = SegmentationClass.MEDIAL_MENISCUS
        
        return mask

    def is_available(self) -> bool:
        return True

    def get_model_info(self) -> dict:
        return {
            "model_status": ModelStatus.DEMO,
            "model_name": "Demonstration Segmentation Model",
            "model_version": "1.0-demo",
            "clinical_validation": False
        }
