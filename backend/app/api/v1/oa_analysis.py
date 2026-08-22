import os
import json
from fastapi import APIRouter, HTTPException
from typing import Dict, Any

from app.core.config import settings
from app.ai.oa_analysis.schemas import PatientData, OAAnalysisResult
from app.ai.oa_analysis.service import OAAnalysisService
from app.ai.measurements.meniscus import MeniscusMeasurementService

router = APIRouter()

@router.post("/{image_id}", response_model=OAAnalysisResult)
async def run_oa_analysis(image_id: str, patient: PatientData):
    # Retrieve meniscus measurement result
    measurement_service = MeniscusMeasurementService()
    try:
        measurement_result = measurement_service.measure_thickness(image_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Measurement required before OA analysis. {str(e)}")
        
    measurement_dict = {
        "mean_thickness_pixels": measurement_result.mean_thickness_pixels,
        "mean_thickness_mm": measurement_result.mean_thickness_mm,
        "calibration_available": measurement_result.calibration_available
    }
    
    service = OAAnalysisService()
    return service.run_analysis(image_id, patient, measurement_dict)
