from fastapi import APIRouter
from app.ai.measurements.meniscus import MeniscusMeasurementService
from app.ai.measurements.schemas import MeasurementResult
from app.ai.measurements.bone import BoneMeasurementService
from app.ai.measurements.bone_schemas import BoneMeasurementResult

router = APIRouter()

@router.post("/meniscus/{image_id}", response_model=MeasurementResult)
async def measure_meniscus(image_id: str):
    service = MeniscusMeasurementService()
    return service.measure_thickness(image_id)

@router.post("/bones/{image_id}", response_model=BoneMeasurementResult)
async def measure_bones(image_id: str):
    service = BoneMeasurementService()
    return service.measure_bones(image_id)
