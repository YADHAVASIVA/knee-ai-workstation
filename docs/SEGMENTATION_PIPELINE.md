# AI Segmentation Pipeline

## 1. Input
The segmentation module takes the internal UUID (`image_id`) generated during the upload phase. It requires the image to have been successfully preprocessed into a standard RGB PNG representation.

## 2. Preprocessing
Images are read from `data/processed/{image_id}.png`. Since they are already normalized during the image input phase, no further heavy preprocessing occurs before inference except standard numpy array conversion.

## 3. Model Interface
The pipeline uses the abstract base class `SegmentationModel`.
This allows hot-swapping between:
- Demonstration models (currently active)
- Future clinical models (e.g., U-Net, MONAI)

## 4. Segmentation Classes
Classes are defined globally in `app.ai.common.constants.SegmentationClass`:
- 0: BACKGROUND
- 1: FEMUR
- 2: TIBIA
- 3: MEDIAL_MENISCUS

## 5. Inference
For the current MVP, because no real model or labelled dataset was provided, the `DemonstrationSegmentationModel` is active. It draws deterministic, non-clinical masks based on the image size to demonstrate the full application workflow. 

## 6. Postprocessing
The service checks the mask array dimensions and ensures only valid class labels exist. It then generates colored RGBA transparent PNGs for visualization.

## 7. Mask Storage
Outputs are stored in `data/masks/{image_id}/`:
- `femur.png` (Red mask)
- `tibia.png` (Blue mask)
- `medial_meniscus.png` (Green mask)
- `result.json` (Structured output data and metadata)

## 8. Visualization
The `MedicalImageViewer` React component layers these PNG masks absolutely over the base image. A legend controls the visibility state of each mask dynamically.

## 9. Confidence Handling
Because this is a demonstration model, confidence is returned as `null`. The UI handles this safely by displaying "Confidence unavailable" rather than fabricating a percentage.

## 10. Demo Mode
The UI aggressively disclaims the results as "Demonstration Mode - Not a clinical AI result." when the demo model is active.

## 11. Real-Model Integration Process
To integrate a real model in the future:
1. Upload weights to `models/` directory.
2. Create `RealSegmentationModel(SegmentationModel)` in `backend/app/ai/segmentation/model.py`.
3. Load the model via PyTorch/ONNX in `load()`.
4. Swap the instantiation in `SegmentationService`.

## 12. Current Limitations
- **NO CLINICAL ACCURACY**: The current output is 100% mocked demonstration logic.
- Requires all three structures to be handled by a single model rather than a cascade.
