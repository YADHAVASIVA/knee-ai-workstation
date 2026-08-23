from fastapi import APIRouter
from app.api.v1 import health, system, images, segmentation, measurements, oa_analysis, implants, implant_matching, inference, xray, debug

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(system.router, prefix="/system", tags=["system"])
api_router.include_router(images.router, prefix="/images", tags=["images"])
api_router.include_router(segmentation.router, prefix="/segmentation", tags=["segmentation"])
api_router.include_router(measurements.router, prefix="/measurements", tags=["measurements"])
api_router.include_router(oa_analysis.router, prefix="/oa-analysis", tags=["oa-analysis"])
api_router.include_router(implants.router, prefix="/implants", tags=["implants"])
api_router.include_router(implant_matching.router, prefix="/implant-matching", tags=["implant-matching"])
api_router.include_router(inference.router, prefix="/inference", tags=["inference"])

api_router.include_router(xray.router, prefix="/xray", tags=["xray"])

api_router.include_router(debug.router, prefix="/debug", tags=["debug"])
