import cv2
import numpy as np
from app.ai.segmentation.model import SegmentationModel
from app.ai.common.constants import SegmentationClass, ModelStatus

class DemonstrationSegmentationModel(SegmentationModel):
    def load(self) -> None:
        pass

    def predict(self, image_array: np.ndarray, modality: str = "MRI") -> np.ndarray:
        height, width = image_array.shape[:2]
        mask = np.zeros((height, width), dtype=np.uint8)
        
        if len(image_array.shape) == 3:
            gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = image_array

        # Simple thresholding to find tissue/bone mass
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # If we can't find anything, fallback to center blocks
        if not contours:
            mask[int(height*0.1):int(height*0.4), int(width*0.3):int(width*0.7)] = SegmentationClass.FEMUR.value
            mask[int(height*0.6):int(height*0.9), int(width*0.35):int(width*0.65)] = SegmentationClass.TIBIA.value
            if modality == "MRI":
                mask[int(height*0.45):int(height*0.55), int(width*0.3):int(width*0.5)] = SegmentationClass.MEDIAL_MENISCUS.value
            return mask

        # Filter by area
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        # We will split the largest contour(s) bounding boxes into Top (Femur) and Bottom (Tibia)
        coords = np.vstack([c for c in contours[:2]])
        x, y, w, h = cv2.boundingRect(coords)
        
        # Femur is top half of bounding box
        femur_y2 = y + h // 2 - int(h*0.05)
        cv2.rectangle(mask, (x + int(w*0.1), y), (x + int(w*0.9), femur_y2), SegmentationClass.FEMUR.value, -1)
        
        # Tibia is bottom half
        tibia_y1 = y + h // 2 + int(h*0.05)
        cv2.rectangle(mask, (x + int(w*0.15), tibia_y1), (x + int(w*0.85), y + h), SegmentationClass.TIBIA.value, -1)
        
        if modality == "MRI":
            # Meniscus only on MRI
            m_y = y + h // 2
            m_x = x + int(w*0.2)
            cv2.ellipse(mask, (m_x, m_y), (int(w*0.15), int(h*0.04)), 0, 0, 360, SegmentationClass.MEDIAL_MENISCUS.value, -1)
            
        return mask

    def is_available(self) -> bool:
        return True

    def get_model_info(self) -> dict:
        return {
            "model_status": ModelStatus.DEMO,
            "model_name": "Image-Adaptive Research Prototype",
            "model_version": "2.0-adaptive",
            "clinical_validation": False
        }
