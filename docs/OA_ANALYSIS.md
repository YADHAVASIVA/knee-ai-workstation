# Osteoarthritis-Associated Analysis

## 1. Purpose
This module investigates the relationship between medial meniscus thickness, patient age, sex, and clinically-labelled Osteoarthritis (OA) status. It satisfies Phase 6 of the development plan.

## 2. Inputs
- Internal `image_id` referencing the segmented and measured knee image.
- `mean_thickness_pixels` from the meniscus measurement engine.
- Patient metadata (Age, Sex, OA Status).

## 3. Demonstration Mode & Limitations
Currently, there is no real clinical dataset or trained OA model loaded into the repository.
As a result:
- The system explicitly operates using a synthetic demonstration dataset `oa_demo_dataset.csv`.
- The outputs do **not** represent a real clinical diagnosis.
- Any statistics, charts, or classifier outputs are heavily disclaimed as "Demonstration Data".

## 4. Dataset Structure
The demo dataset contains deterministic mock points designed purely to test the statistical logic path. It is labeled explicitly with `is_demo=true`.

## 5. Statistical Methods
- `compare_oa_groups()`: Averages and summarizes thickness grouped by OA vs NON_OA.
- `compare_sex_groups()`: Groups values by Male vs Female demographics.
- `analyze_age()`: Performs standard Pearson correlation (via pandas) linking numerical age to numerical meniscus thickness.

## 6. Classifier Architecture
- The abstract base `OAClassifier` provides a foundation for future sklearn or PyTorch classification models.
- The active demo classifier produces a deterministic prediction based on simple threshold logic (e.g., adding probabilities if age > 50 or thickness < 8px) purely to demonstrate the "Prediction" and "Feature Explanation" UI panels.

## 7. Clinical Safety Considerations
- Unknowns are explicitly permitted. A clinician cannot be forced to label a patient as OA.
- Missing values in spatial calibration (`thickness_mm = null`) are handled gracefully, failing back to pixels while refusing to misleadingly convert them to millimeters without valid `pixel_spacing`.
