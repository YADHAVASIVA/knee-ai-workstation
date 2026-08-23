from typing import Dict, Any
from fastapi import HTTPException

from app.ai.oa_analysis.schemas import PatientData, OAAnalysisResult
from app.ai.registry import ModelRegistry, ModelStatus
from app.ai.inference_service import MedicalImageInferenceService

class OAAnalysisService:
    def run_analysis(self, image_id: str, patient_data: PatientData, measurement: Dict[str, Any]) -> OAAnalysisResult:
        # Check model registry for real models
        available_models = ModelRegistry.get_models_by_task("OA_CLASSIFICATION")
        real_models = [m for m in available_models if m.status == ModelStatus.VALIDATED_RESEARCH]
        
        if not real_models:
             return OAAnalysisResult(
                image_id=image_id,
                analysis_status="MODEL_UNAVAILABLE",
                data_status="unsupported",
                model_status="unsupported",
                is_demo=False,
                patient=patient_data,
                meniscus_measurement=measurement,
                oa_vs_non_oa={},
                male_vs_female={},
                age_association={},
                classifier_result=None,
                warning="No compatible validated research model is available.",
                patient_findings={}
            )

        # In a real environment, we'd delegate to MedicalImageInferenceService.
        # But since we have no real models, this path won't be hit.
        return OAAnalysisResult(
            image_id=image_id,
            analysis_status="ERROR",
            data_status="real",
            model_status="real",
            is_demo=False,
            patient=patient_data,
            meniscus_measurement=measurement,
            oa_vs_non_oa={},
            male_vs_female={},
            age_association={},
            classifier_result=None,
            warning="Inference failed.",
            patient_findings={}
        )
