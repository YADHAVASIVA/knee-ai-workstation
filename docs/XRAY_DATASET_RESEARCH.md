# Knee X-Ray Dataset Research

## Selected Candidate Dataset
**Dataset Name:** Knee Osteoarthritis Severity Grading Dataset
**Official Source:** Mendeley Data
**Contributor:** Pingjun Chen
**Citation:** Chen, Pingjun (2018), "Knee Osteoarthritis Severity Grading Dataset", Mendeley Data, V1, doi: 10.17632/56rmx5bjcr.1
**License/Access:** CC BY 4.0 (Attribution 4.0 International). Requires manual download via browser from Mendeley Data or Kaggle.
**Patient Count:** ~3,000+ patients (derived from Osteoarthritis Initiative - OAI)
**Image Count:** ~8,000+ knee joint images
**Labels:** Kellgren-Lawrence (KL) grades 0, 1, 2, 3, 4
**Projection:** Primarily AP/PA (Anteroposterior/Posteroanterior)
**Laterality:** Both left and right knees are typically cropped individually from bilateral standing radiographs.

## Known Limitations
- The dataset consists of pre-cropped knee joints. If a user uploads a full bilateral pelvic/lower limb X-ray, we will need a YOLO/Faster-RCNN knee detector first to crop the joint before passing it to this KL model. 
- Patient IDs must be carefully tracked. The dataset originates from OAI, so multiple images might belong to the same patient (e.g., left/right knees, or longitudinal follow-ups). We MUST group by patient ID when creating the train/val/test splits to prevent data leakage.
