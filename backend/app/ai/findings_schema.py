from pydantic import BaseModel
from typing import List, Optional

class AIFinding(BaseModel):
    finding_id: str
    image_id: str
    finding_type: str
    location: str
    severity: str
    confidence: float
    evidence: str
    model: str
    is_demo: bool

class InferenceReport(BaseModel):
    case_id: str
    image_id: str
    model_id: str
    model_version: str
    dataset_version: str
    preprocessing_version: str
    timestamp: str
    modality: str
    quality_status: str
    is_demo: bool
    findings: List[AIFinding]
    limitations: List[str]
    next_clinical_workflow: str
