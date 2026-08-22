from fastapi import APIRouter
from pydantic import BaseModel
import platform
import os
from typing import Optional

from app.core.config import settings

router = APIRouter()

class SystemInfoResponse(BaseModel):
    os: str
    python_version: str
    environment: str
    data_dir_exists: bool
    database_status: str = "connected"
    implant_database: str = "demo"

@router.get("/info", response_model=SystemInfoResponse)
async def get_system_info():
    return SystemInfoResponse(
        os=platform.system(),
        python_version=platform.python_version(),
        environment=settings.ENVIRONMENT,
        data_dir_exists=os.path.exists(settings.DATA_DIR),
        database_status="connected",
        implant_database="demo"
    )
