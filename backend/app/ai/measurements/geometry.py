import numpy as np
from typing import List, Tuple, Dict, Any

def calculate_meniscus_thickness(mask_array: np.ndarray, target_class: int) -> List[Dict[str, Any]]:
    """
    Calculates meniscus thickness at prototype predefined locations A, B, and C.
    Methodology:
    1. Find bounding box of the meniscus mask.
    2. Define sample columns at 25%, 50%, 75% of the width.
    3. Calculate vertical distance (thickness) between top and bottom pixels in these columns.
    Returns deterministic coordinates and pixel thicknesses.
    """
    # Create binary mask for the target class
    binary_mask = (mask_array == target_class).astype(np.uint8)
    
    # Find bounding box
    rows = np.any(binary_mask, axis=1)
    cols = np.any(binary_mask, axis=0)
    
    if not np.any(rows) or not np.any(cols):
        return [] # Empty mask
        
    ymin, ymax = np.where(rows)[0][[0, -1]]
    xmin, xmax = np.where(cols)[0][[0, -1]]
    
    width = xmax - xmin
    
    if width < 10:
        return [] # Mask too small to measure reliably
    
    # Predefined location fractions
    locations = [
        {"name": "A", "fraction": 0.25},
        {"name": "B", "fraction": 0.50},
        {"name": "C", "fraction": 0.75}
    ]
    
    results = []
    
    for loc in locations:
        col_idx = int(xmin + width * loc["fraction"])
        col_data = binary_mask[:, col_idx]
        
        y_indices = np.where(col_data)[0]
        if len(y_indices) > 0:
            top_y = int(y_indices[0])
            bottom_y = int(y_indices[-1])
            thickness = float(bottom_y - top_y + 1)
            
            # Central y coordinate for visualization anchor
            center_y = top_y + (thickness / 2.0)
            
            results.append({
                "name": loc["name"],
                "x": float(col_idx),
                "y": float(center_y),
                "thickness_pixels": thickness,
                "top_y": top_y,
                "bottom_y": bottom_y
            })
            
    return results
