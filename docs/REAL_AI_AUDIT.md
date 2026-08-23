# Real AI Audit

## backend/app/ai/findings_schema.py
- `AIFinding` has `confidence` and `is_demo`. (STATUS: DEMO/STUB artifact)
- `InferenceReport` has `is_demo`. (STATUS: DEMO/STUB artifact)

## backend/app/ai/inference_service.py
- Uses `is_demo`. Checks for `DEMO` model status. (STATUS: DEMO artifact)
- OA inference has hardcoded `confidence = 0.85 if is_demo else 0.95`. (STATUS: STUB)
- Explicitly states: "Run Inference (stubbed to route to specific task logic)". (STATUS: STUB)

## backend/app/ai/registry.py
- Pre-registers `demo_xray_oa_v1` ("Heuristic OA Demo Classifier") with dataset "synthetic". (STATUS: DEMO/STUB)
- Pre-registers `demo_mri_seg_v1` ("Heuristic MRI Segmenter"). (STATUS: DEMO/STUB)

## backend/app/ai/validation.py
- Anatomy classification has `return ("KNEE", 0.95)` (STATUS: STUB / hard-coded)
- Quality check has `return (ImageQuality.ACCEPTABLE, "ACCEPTABLE", ...)` (STATUS: STUB / hard-coded)
- Modality classification uses a fallback logic but is mostly a stub. (STATUS: STUB)

## backend/ai/training/train.py & evaluate.py
- Both scripts just print "STUB: In production...". (STATUS: STUB)

## backend/app/ai/oa_analysis/classifier.py
- Implements `OAClassifier.predict` using age, sex, and meniscus thickness heuristics. (STATUS: HEURISTIC / DEMO)
- Uses `random`, hard-coded probabilities `0.2, 0.3, 0.4`. (STATUS: HEURISTIC / STUB)

## backend/app/ai/oa_analysis/service.py
- Uses `oa_demo_dataset.csv`. (STATUS: DEMO)
- Explicitly sets `data_status="demo"` and `is_demo=is_demo`. (STATUS: DEMO)

## frontend/src/pages/Analysis.tsx
- Explicitly looks for `is_demo` and `REVIEW REQUIRED`. (STATUS: DEMO artifact support)

## frontend/src/services/api.ts
- Exposes `is_demo` in schemas. (STATUS: DEMO artifact support)

**Conclusion:** The pipeline architecture exists, but the models, logic, and data backing it are DEMO/STUB implementations.
