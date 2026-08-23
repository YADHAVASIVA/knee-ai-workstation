# Phase 12.3 Final Report

1. **Does the system read actual X-ray pixel data?**
   Yes. `backend/app/ai/xray/image_loader.py` reads `ds.pixel_array` for DICOM and uses PIL for standard images. It extracts full image statistics (min, max, mean, std, nonzero) to verify the image is not empty or uniform.

2. **Where is the pixel array loaded?**
   `XRayImageLoader.load_pixels(filepath)` inside `backend/app/ai/xray/image_loader.py`.

3. **What preprocessing is applied?**
   `XRayPreprocessor.preprocess` handles DICOM windowing (`WindowCenter`, `WindowWidth`) and robust intensity normalization. Resizing and advanced projection-specific normalization are stubbed to await specific model parameters.

4. **What model receives the tensor?**
   None currently. The pipeline is ready to feed `processed_pixels` to `XRayInferenceEngine.run_inference`, but without real weights, it halts execution and raises a `ModelUnavailableError`.

5. **Where are the model weights?**
   They are missing. They are expected to be downloaded or trained and placed in `models/xray/...` with `.pth` or `.onnx` extensions.

6. **What dataset trained the model?**
   None currently. The task is strictly defined as Kellgren-Lawrence Grading in `docs/XRAY_AI_TASK_SPECIFICATION.md`, awaiting a real dataset (like the OAI dataset).

7. **What are the actual test metrics?**
   None. `evaluate.py` will generate them when a dataset and model are available.

8. **Does prediction change based on image input?**
   Inference is currently blocked entirely. If weights were present, the architecture guarantees a fresh forward pass of the unique image tensor on every request.

9. **Does image_id isolate results?**
   Yes. Each API request routes uniquely via `image_id`. A multi-view check is strictly decoupled.

10. **Does the final report use the actual inference result?**
    Yes. The report pulls from the `caseState.oaAnalysis` state which directly matches the API response. When the model is unavailable, it reports `MODEL_UNAVAILABLE` rather than generating a fake finding.

11. **Does Grad-CAM work?**
    No. Grad-CAM requires backpropagation on an actual PyTorch computation graph, which does not exist until model weights are loaded.

12. **What remains blocked?**
    **REAL MODEL BLOCKED — DATASET REQUIRED.**
    We require a real dataset (with KL grading labels), a trained PyTorch checkpoint, and a configuration file denoting the input tensor size and preprocessing expectations for that exact model.
