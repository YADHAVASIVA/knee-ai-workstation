# X-Ray AI Task Specification

## Exact Task
**KNEE X-RAY OSTEOARTHRITIS GRADING (Kellgren-Lawrence Grade)**

## Description
The model will receive a 2D knee X-ray (radiograph) and output a probability distribution over the 5 Kellgren-Lawrence (KL) grades for osteoarthritis severity:
- KL 0: None
- KL 1: Doubtful
- KL 2: Minimal
- KL 3: Moderate
- KL 4: Severe

## Modality and Projection
- **Modality:** X-Ray
- **Projection:** AP (Anteroposterior) and PA (Posteroanterior)

## Rationale
KL grading is the clinically validated and globally recognized standard for diagnosing and assessing knee osteoarthritis on radiographs. Binary OA classification is insufficient for detailed clinical assessment, and attempting to classify all possible knee pathologies simultaneously is out of scope for a reliable first model.
