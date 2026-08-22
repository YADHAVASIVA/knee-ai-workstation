# Hackathon Demo Flow (120 Seconds)

## Target Audience
Hackathon Judges (Technical + Clinical). They have extremely limited time and need to see the entire pipeline instantly while trusting the mathematical/AI credibility.

## 0:00 - 0:15 | Case Ingestion & Calibration
1. **Action:** Drag and drop a Synthetic DICOM file into the `CASE OVERVIEW` screen.
2. **Narration:** "The system ingests native DICOM, instantly extracting metadata."
3. **Visual Hook:** The metadata card populates, and a green badge lights up: `Physical Calibration: Available (0.5 x 0.5 mm)`.

## 0:15 - 0:40 | Anatomical Segmentation & Image Verification
1. **Action:** Switch to `ANATOMY` tab.
2. **Narration:** "Our AI immediately segments the femur, tibia, and medial meniscus. We built an interactive clinical viewer so surgeons can verify the AI."
3. **Visual Hook:** Toggle the layers on and off. Pan and zoom into the meniscus to show that the interactive viewer is a true workstation, not a static web image.

## 0:40 - 0:55 | Quantitative Analysis
1. **Action:** Switch to `ANALYSIS` tab.
2. **Narration:** "We mathematically measure the meniscus thickness and correlate it with the patient's demographics to identify OA associations."
3. **Visual Hook:** Input Age/Sex. The graphs update immediately, showing the patient's risk profile against the baseline cohort.

## 0:55 - 1:10 | Explainable Implant Matching
1. **Action:** Switch to `IMPLANT PLANNING` tab.
2. **Narration:** "Finally, using the physical calibration from the DICOM, we measure the bone geometries and rank them against an implant database."
3. **Visual Hook:** Expand the #1 Ranked Match. Show the visual error bars detailing exactly *why* this implant was selected (e.g., "Width difference: 0.5mm"). 

## 1:10 - 1:20 | Final Report
1. **Action:** Click `GENERATE REPORT`.
2. **Narration:** "The entire workflow is packaged into a printable clinical summary."
3. **Visual Hook:** The clean, printable layout showing the image, demographics, measurements, and selected implant.
