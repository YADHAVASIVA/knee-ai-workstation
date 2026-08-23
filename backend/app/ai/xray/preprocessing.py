import numpy as np
from typing import Dict, Any

class XRayPreprocessor:
    PREPROCESSING_VERSION = "v1.0"

    @staticmethod
    def preprocess(pixels: np.ndarray, metadata: Dict[str, Any]) -> np.ndarray:
        """
        Applies standard X-Ray preprocessing:
        - DICOM Windowing if applicable
        - Intensity normalization
        - Resizing (stubbed conceptually)
        """
        # Step 5 - Windowing
        wc = metadata.get('WindowCenter')
        ww = metadata.get('WindowWidth')
        
        processed = np.copy(pixels)
        
        if wc is not None and ww is not None:
            # Handle MultiValue
            if isinstance(wc, list) or type(wc).__name__ == "MultiValue":
                wc = wc[0]
            if isinstance(ww, list) or type(ww).__name__ == "MultiValue":
                ww = ww[0]
                
            wc = float(wc)
            ww = float(ww)
            
            lower = wc - (ww / 2.0)
            upper = wc + (ww / 2.0)
            processed = np.clip(processed, lower, upper)
            
        # Normalize to [0, 1]
        p_min = processed.min()
        p_max = processed.max()
        if p_max > p_min:
            processed = (processed - p_min) / (p_max - p_min)
            
        return processed
