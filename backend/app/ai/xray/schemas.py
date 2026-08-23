from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

class XRayQuality(BaseModel):
    status: str
    score: float
    limitations: list[str] = []

class KLProbabilities(BaseModel):
    KL0: float = Field(..., alias="KL0")
    KL1: float = Field(..., alias="KL1")
    KL2: float = Field(..., alias="KL2")
    KL3: float = Field(..., alias="KL3")
    KL4: float = Field(..., alias="KL4")
    
    class Config:
        populate_by_name = True

class XRayInferenceOutput(BaseModel):
    status: str
    image_id: str
    predicted_kl_grade: Optional[int] = None
    probabilities: Optional[KLProbabilities] = None
    confidence: Optional[float] = None
    model_version: Optional[str] = None
    inference_device: Optional[str] = None
    message: str = ""
