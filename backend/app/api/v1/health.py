from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def get_health():
    return {
        "status": "healthy",
        "service": "knee-ai-analysis",
        "version": "1.0.0"
    }
