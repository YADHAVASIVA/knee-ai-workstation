from pydantic import BaseModel
from typing import List, Optional

class CandidateExplanation(BaseModel):
    patient_width: float
    implant_width: float
    width_difference: float
    width_error: float
    
    patient_ap: float
    implant_ap: float
    ap_difference: float
    ap_error: float
    
    combined_normalized_error: float
    contribution_to_score: float

class RankedCandidate(BaseModel):
    rank: int
    implant_id: str
    size: str
    score: float
    width_difference: float
    ap_difference: float
    explanation: CandidateExplanation
    is_demo: bool = True
    source_type: str = "synthetic_demo"

class MatchingResult(BaseModel):
    image_id: str
    matching_status: str
    data_status: str
    calibration_available: bool
    orientation_status: str
    femoral_candidates: List[RankedCandidate]
    tibial_candidates: List[RankedCandidate]
    warning: str
