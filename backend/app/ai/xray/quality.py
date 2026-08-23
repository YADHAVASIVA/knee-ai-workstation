import numpy as np
from app.ai.xray.schemas import XRayQuality

class XRayQualityAssessor:
    @staticmethod
    def assess(pixels: np.ndarray) -> XRayQuality:
        # Example naive quality check based on contrast
        std = np.std(pixels)
        if std < 0.05:
            return XRayQuality(status="INSUFFICIENT", score=float(std), limitations=["Extremely low contrast"])
        return XRayQuality(status="ACCEPTABLE", score=float(std), limitations=[])
