import os
import numpy as np
import pydicom
from PIL import Image
from typing import Tuple, Dict, Any

class InvalidImageError(Exception):
    pass

class XRayImageLoader:
    @staticmethod
    def load_pixels(filepath: str) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Loads pixel data and calculates basic statistics for validation.
        """
        if not os.path.exists(filepath):
            raise InvalidImageError("File does not exist.")
            
        ext = os.path.splitext(filepath)[1].lower()
        metadata = {}
        
        try:
            if ext == '.dcm':
                ds = pydicom.dcmread(filepath)
                if not hasattr(ds, 'pixel_array'):
                    raise InvalidImageError("DICOM has no pixel array.")
                pixels = ds.pixel_array.astype(np.float32)
                # Store some DICOM info
                metadata['PhotometricInterpretation'] = getattr(ds, 'PhotometricInterpretation', None)
                metadata['WindowCenter'] = getattr(ds, 'WindowCenter', None)
                metadata['WindowWidth'] = getattr(ds, 'WindowWidth', None)
            else:
                with Image.open(filepath) as img:
                    img = img.convert("L")  # Convert to grayscale
                    pixels = np.array(img).astype(np.float32)
        except Exception as e:
            raise InvalidImageError(f"Failed to load image: {str(e)}")
            
        if pixels.size == 0:
            raise InvalidImageError("Empty pixel array.")
            
        # Image Pixel Verification (Step 3)
        min_val = float(np.min(pixels))
        max_val = float(np.max(pixels))
        
        if min_val == max_val:
            raise InvalidImageError("Completely uniform image (all pixels have the same value).")
            
        stats = {
            "width": int(pixels.shape[1]),
            "height": int(pixels.shape[0]),
            "channels": 1,
            "dtype": str(pixels.dtype),
            "minimum_pixel_value": min_val,
            "maximum_pixel_value": max_val,
            "mean_pixel_value": float(np.mean(pixels)),
            "standard_deviation": float(np.std(pixels)),
            "non_zero_ratio": float(np.count_nonzero(pixels) / pixels.size)
        }
        
        metadata['stats'] = stats
        return pixels, metadata
