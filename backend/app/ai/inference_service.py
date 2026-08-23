from typing import Dict, Any
from app.ai.registry import ModelRegistry, ModelStatus, ModelMetadata
from app.ai.validation import ValidationService, ImageQuality
from app.ai.xray.service import XRayInferenceService

class MedicalImageInferenceService:
    @staticmethod
    def run_inference(
        case_id: str, 
        image_id: str, 
        filepath: str, 
        metadata: Dict[str, Any], 
        target_task: str
    ) -> Dict[str, Any]:
        """
        Main entry point for AI inference on a single image.
        """
        # We delegate X-Ray tasks entirely to the new X-Ray pipeline
        if target_task == "OA_CLASSIFICATION":
            result = XRayInferenceService.process_image(image_id, filepath, target_task)
            return result.model_dump()
            
        return {"status": "UNSUPPORTED_TASK", "message": "Task not implemented."}
