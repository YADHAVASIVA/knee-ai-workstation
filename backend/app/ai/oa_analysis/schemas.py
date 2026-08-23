from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from enum import Enum

class BiologicalSex(str, Enum):
    MALE = "Male"
    FEMALE = "Female"

class PatientData(BaseModel):
    name: str = ""
    age: Optional[int] = None
    sex: BiologicalSex = BiologicalSex.MALE
    laterality: str = "Unknown"
    notes: str = ""

class ClassifierExplanation(BaseModel):
    feature: str
    contribution: float

class ClassifierResult(BaseModel):
    prediction_label: str
    prediction_probability: float
    explanation: str

class AnalysisStats(BaseModel):
    sample_count: int
    mean_thickness: float
    median_thickness: float
    std_thickness: float

class OAVsNonOAComparison(BaseModel):
    oa_stats: Optional[AnalysisStats] = None
    non_oa_stats: Optional[AnalysisStats] = None
    statistical_test: str = ""
    p_value: Optional[float] = None
    conclusion: str = ""

class MaleVsFemaleComparison(BaseModel):
    male_stats: Optional[AnalysisStats] = None
    female_stats: Optional[AnalysisStats] = None
    statistical_test: str = ""
    p_value: Optional[float] = None
    conclusion: str = ""

class AgeAnalysis(BaseModel):
    correlation: Optional[float] = None
    statistical_test: str = ""
    p_value: Optional[float] = None
    conclusion: str = ""

class OAAnalysisResult(BaseModel):
    image_id: str
    analysis_status: str
    data_status: str
    model_status: str
    is_demo: bool
    patient: PatientData
    meniscus_measurement: Dict[str, Any]
    oa_vs_non_oa: Optional[OAVsNonOAComparison] = None
    male_vs_female: Optional[MaleVsFemaleComparison] = None
    age_association: Optional[AgeAnalysis] = None
    classifier_result: Optional[ClassifierResult] = None
    warning: str
    patient_findings: Dict[str, str] = {}
