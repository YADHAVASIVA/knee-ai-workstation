from app.ai.implant_matching.schemas import CandidateExplanation

WEIGHT_WIDTH = 0.5
WEIGHT_AP = 0.5
MINIMUM_MATCH_SCORE = 50.0

def calculate_errors_and_score(patient_width: float, patient_ap: float, implant_width: float, implant_ap: float):
    if implant_width <= 0 or implant_ap <= 0:
        raise ValueError("Implant dimensions must be strictly positive.")
        
    width_diff = patient_width - implant_width
    ap_diff = patient_ap - implant_ap
    
    width_error = abs(width_diff) / implant_width
    ap_error = abs(ap_diff) / implant_ap
    
    combined_error = (WEIGHT_WIDTH * width_error) + (WEIGHT_AP * ap_error)
    score = max(0.0, 100.0 * (1.0 - combined_error))
    
    explanation = CandidateExplanation(
        patient_width=patient_width,
        implant_width=implant_width,
        width_difference=width_diff,
        width_error=width_error,
        patient_ap=patient_ap,
        implant_ap=implant_ap,
        ap_difference=ap_diff,
        ap_error=ap_error,
        combined_normalized_error=combined_error,
        contribution_to_score=score
    )
    
    return score, width_diff, ap_diff, explanation
