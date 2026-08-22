from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.repositories.implant_repository import ImplantRepository
from app.db.models.implant import ImplantComponent
from app.ai.measurements.bone import BoneMeasurementService
from app.ai.implant_matching.schemas import MatchingResult, RankedCandidate
from app.ai.implant_matching.scoring import calculate_errors_and_score, MINIMUM_MATCH_SCORE

class ImplantMatchingService:
    def __init__(self, db: Session):
        self.db = db
        self.implant_repo = ImplantRepository(db)
        self.bone_service = BoneMeasurementService()

    def match_implants(self, image_id: str, synthetic_pixel_spacing: float = None) -> MatchingResult:
        # 1. Fetch patient anatomy (re-measure or fetch, currently we measure dynamically)
        try:
            bone_result = self.bone_service.measure_bones(image_id)
        except HTTPException as e:
            raise HTTPException(status_code=400, detail=f"Cannot perform matching: {e.detail}")
            
        # 2. Calibration & Unit validation
        calibration_available = bone_result.calibration_available
        
        # Override for DEMO bypass
        if synthetic_pixel_spacing and synthetic_pixel_spacing > 0:
            calibration_available = True
            # apply synthetic calibration to measurements
            if bone_result.femur:
                bone_result.femur.width_mm = bone_result.femur.width_pixels * synthetic_pixel_spacing
                bone_result.femur.ap_dimension_mm = bone_result.femur.ap_dimension_pixels * synthetic_pixel_spacing
            if bone_result.tibia:
                bone_result.tibia.width_mm = bone_result.tibia.width_pixels * synthetic_pixel_spacing
                bone_result.tibia.ap_dimension_mm = bone_result.tibia.ap_dimension_pixels * synthetic_pixel_spacing
                
        if not calibration_available:
            return MatchingResult(
                image_id=image_id,
                matching_status="calibration_required",
                data_status="demo",
                calibration_available=False,
                orientation_status=bone_result.orientation_status,
                femoral_candidates=[],
                tibial_candidates=[],
                warning="Physical calibration is required before anatomical implant matching."
            )
            
        # 3. Missing anatomy validation
        if not bone_result.femur or not bone_result.tibia:
            return MatchingResult(
                image_id=image_id,
                matching_status="insufficient_data",
                data_status="demo",
                calibration_available=True,
                orientation_status=bone_result.orientation_status,
                femoral_candidates=[],
                tibial_candidates=[],
                warning="Insufficient anatomical measurements."
            )
            
        femur_mm = bone_result.femur
        tibia_mm = bone_result.tibia
        
        if femur_mm.width_mm is None or femur_mm.ap_dimension_mm is None or tibia_mm.width_mm is None or tibia_mm.ap_dimension_mm is None:
            return MatchingResult(
                image_id=image_id,
                matching_status="insufficient_data",
                data_status="demo",
                calibration_available=True,
                orientation_status=bone_result.orientation_status,
                femoral_candidates=[],
                tibial_candidates=[],
                warning="Insufficient anatomical measurements (missing mm values)."
            )

        # 4. Fetch candidates
        all_femoral = self.implant_repo.get_all(component_type="femoral")
        all_tibial = self.implant_repo.get_all(component_type="tibial")
        
        if not all_femoral and not all_tibial:
            return MatchingResult(
                image_id=image_id,
                matching_status="no_candidates_in_db",
                data_status="demo",
                calibration_available=True,
                orientation_status=bone_result.orientation_status,
                femoral_candidates=[],
                tibial_candidates=[],
                warning="No candidates available in the implant database."
            )

        # 5. Matching & Ranking logic
        femoral_candidates = self._rank_candidates(femur_mm.width_mm, femur_mm.ap_dimension_mm, all_femoral)
        tibial_candidates = self._rank_candidates(tibia_mm.width_mm, tibia_mm.ap_dimension_mm, all_tibial)
        
        if not femoral_candidates and not tibial_candidates:
            matching_status = "no_match"
            warning = "No sufficiently similar demonstration component found."
        else:
            matching_status = "success"
            
            warning = "DEMONSTRATION MATCH. Synthetic implant specifications and demonstration calibration are used. This result is NOT for clinical or surgical use."
            if bone_result.orientation_status == "unknown":
                warning = "Anatomical orientation unavailable for validated implant matching. " + warning

        return MatchingResult(
            image_id=image_id,
            matching_status=matching_status,
            data_status="demo",
            calibration_available=True,
            orientation_status=bone_result.orientation_status,
            femoral_candidates=femoral_candidates[:3],
            tibial_candidates=tibial_candidates[:3],
            warning=warning
        )

    def _rank_candidates(self, pat_width: float, pat_ap: float, implants: List[ImplantComponent]) -> List[RankedCandidate]:
        candidates = []
        for imp in implants:
            try:
                score, w_diff, ap_diff, explanation = calculate_errors_and_score(
                    patient_width=pat_width,
                    patient_ap=pat_ap,
                    implant_width=imp.width,
                    implant_ap=imp.ap_dimension
                )
                if score >= MINIMUM_MATCH_SCORE:
                    candidates.append({
                        "implant": imp,
                        "score": score,
                        "w_diff": w_diff,
                        "ap_diff": ap_diff,
                        "explanation": explanation
                    })
            except ValueError:
                continue
                
        # Sort by score descending
        candidates.sort(key=lambda x: x["score"], reverse=True)
        
        # Format as RankedCandidate
        ranked = []
        for i, c in enumerate(candidates):
            ranked.append(RankedCandidate(
                rank=i + 1,
                implant_id=c["implant"].id,
                size=c["implant"].size,
                score=c["score"],
                width_difference=c["w_diff"],
                ap_difference=c["ap_diff"],
                explanation=c["explanation"],
                is_demo=True,
                source_type="synthetic_demo"
            ))
            
        return ranked
