from typing import List, Dict, Any
from app.ai.oa_analysis.schemas import ClassifierResult, ClassifierExplanation
import random

class OAClassifier:
    def __init__(self):
        self.model_status = "demo"

    def predict(self, age: int, sex: str, meniscus_thickness: float) -> ClassifierResult:
        # Mock deterministic prediction for demo
        base_prob = 0.2
        if age > 50:
            base_prob += 0.3
        if meniscus_thickness < 8.0:
            base_prob += 0.4

        prob = min(max(base_prob, 0.0), 1.0)
        label = "OA" if prob > 0.5 else "NON_OA"

        explanations = [
            f"Age contribution: {0.3 if age > 50 else 0.0}",
            f"Meniscus contribution: {0.4 if meniscus_thickness < 8.0 else 0.0}"
        ]

        return ClassifierResult(
            prediction_probability=prob,
            prediction_label=label,
            explanation=", ".join(explanations)
        )
