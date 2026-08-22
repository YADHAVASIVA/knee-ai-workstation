from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from enum import Enum

class SexEnum(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    UNKNOWN = "Unknown"

class OAStatusEnum(str, Enum):
    OA = "OA"
    NON_OA = "NON_OA"
    UNKNOWN = "Unknown"

class PatientData(BaseModel):
    age: Optional[int] = Field(None, ge=1, le=120, description="Patient age in years")
    sex: SexEnum = SexEnum.UNKNOWN
    oa_status: OAStatusEnum = OAStatusEnum.UNKNOWN

class DemoDatasetRecord(BaseModel):
    patient_id: str
    age: int
    sex: str
    oa_status: str
    meniscus_thickness_pixels: float
    is_demo: bool

class AnalysisStats(BaseModel):
    sample_count: int
    mean_thickness: float
    median_thickness: float
    std_thickness: float

class OAVsNonOAComparison(BaseModel):
    oa_stats: Optional[AnalysisStats]
    non_oa_stats: Optional[AnalysisStats]
    statistical_test: str
    p_value: Optional[float]
    conclusion: str

class MaleVsFemaleComparison(BaseModel):
    male_stats: Optional[AnalysisStats]
    female_stats: Optional[AnalysisStats]

class AgeAnalysis(BaseModel):
    correlation_coefficient: Optional[float]
    conclusion: str

class ClassifierExplanation(BaseModel):
    feature: str
    contribution: float

class ClassifierResult(BaseModel):
    model_status: str
    prediction_probability: Optional[float]
    prediction_label: Optional[str]
    explanation: List[ClassifierExplanation]

class OAAnalysisResult(BaseModel):
    image_id: str
    analysis_status: str
    data_status: str
    model_status: str
    patient: PatientData
    meniscus_measurement: Dict[str, Any]
    oa_vs_non_oa: Optional[OAVsNonOAComparison]
    male_vs_female: Optional[MaleVsFemaleComparison]
    age_association: Optional[AgeAnalysis]
    classifier_result: Optional[ClassifierResult]
    warning: str
