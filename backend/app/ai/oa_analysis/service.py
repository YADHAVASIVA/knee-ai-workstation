import os
import pandas as pd
from typing import Dict, Any
from fastapi import HTTPException

from app.core.config import settings
from app.ai.oa_analysis.schemas import PatientData, OAAnalysisResult
from app.ai.oa_analysis.statistics import compare_oa_groups, compare_sex_groups, analyze_age
from app.ai.oa_analysis.classifier import OAClassifier

class OAAnalysisService:
    def __init__(self):
        self.dataset_path = os.path.join(settings.DATA_DIR, "demo", "oa_demo_dataset.csv")
        self.classifier = OAClassifier()

    def load_dataset(self) -> pd.DataFrame:
        if not os.path.exists(self.dataset_path):
            raise HTTPException(status_code=500, detail="Demo dataset not found.")
        try:
            df = pd.read_csv(self.dataset_path)
            # basic validation
            required = {"age", "sex", "oa_status", "meniscus_thickness_pixels"}
            if not required.issubset(df.columns):
                raise ValueError("Dataset missing required columns.")
            return df
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load dataset: {str(e)}")

    def run_analysis(self, image_id: str, patient_data: PatientData, measurement: Dict[str, Any]) -> OAAnalysisResult:
        df = self.load_dataset()
        
        # Add current patient to analysis if fully populated
        thickness_pixels = measurement.get("mean_thickness_pixels", 0.0)
        
        # Classifier Prediction if we have minimal data
        clf_result = None
        if patient_data.age is not None and patient_data.sex != "Unknown":
            clf_result = self.classifier.predict(patient_data.age, patient_data.sex.value, thickness_pixels)

        return OAAnalysisResult(
            image_id=image_id,
            analysis_status="success",
            data_status="demo",
            model_status="demo",
            patient=patient_data,
            meniscus_measurement=measurement,
            oa_vs_non_oa=compare_oa_groups(df),
            male_vs_female=compare_sex_groups(df),
            age_association=analyze_age(df),
            classifier_result=clf_result,
            warning="Demonstration analysis — not a clinical diagnosis. DEMONSTRATION DATA."
        )
