import React from 'react';
import type { CaseState } from '../types/case';
import { Button } from '../components/ui/Button';
import './ImplantPlanning.css';
import * as api from '../services/api';

interface ImplantPlanningProps {
  caseState: CaseState;
  setCaseState: React.Dispatch<React.SetStateAction<CaseState>>;
  onBack: () => void;
  onNext: () => void;
}

export const ImplantPlanning: React.FC<ImplantPlanningProps> = ({ caseState, setCaseState, onBack, onNext }) => {
  const activeImage = caseState.images.find(img => img.id === caseState.activeImageId) || caseState.images[0];
  const boneRes = activeImage?.measurements.bones;
  const isCalibrated = activeImage?.metadata?.pixel_spacing != null;

  const handleMatch = async () => {
    if (!activeImage) return;
    try {
      const res = await api.matchImplants(activeImage.id);
      setCaseState(prev => ({ ...prev, implantMatches: res }));
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="ip-container fade-in">
      <div className="ip-header">
        <h2 className="ip-title">Potential Anatomical Matches</h2>
        <p className="ip-subtitle">Dimension-based comparison against the available implant dataset for {activeImage?.file?.name || 'the active study'}.</p>
      </div>

      {!isCalibrated ? (
        <div className="ip-card ip-warning">
          <h3>Calibration Required</h3>
          <p>Implant matching requires physical calibration (pixel spacing). The selected image is not calibrated.</p>
        </div>
      ) : !boneRes ? (
        <div className="ip-card ip-warning">
          <h3>Insufficient Measurements</h3>
          <p>Bone measurements are required for implant matching. Please run anatomy analysis first.</p>
        </div>
      ) : (
        <div className="ip-layout">
          <div className="ip-main-col">
            {!caseState.implantMatches ? (
              <div className="ip-empty-state">
                <Button onClick={handleMatch}>Find Potential Matches</Button>
              </div>
            ) : (
              <div className="ip-matches">
                {caseState.implantMatches.femoral_candidates.map((match, idx: number) => (
                  <div key={idx} className="ip-match-card">
                    <div className="ip-match-header">
                      <h4>Rank #{idx + 1} • {'Generic Manufacturer'}</h4>
                      <span className="ip-score">Score: {match.score.toFixed(1)}</span>
                    </div>
                    <p className="ip-match-model">{match.implant_id} (Size {match.size})</p>
                    
                    <div className="ip-match-diffs">
                      <div className="ip-diff-item">
                        <span>Femur Width Diff:</span>
                        <strong>{match.width_difference.toFixed(2)} mm</strong>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
          
          <div className="ip-side-col">
            <div className="ip-card">
              <h3>Patient Anatomy</h3>
              <div className="ip-anatomy-details">
                <div className="ip-detail-row">
                  <span>Femur Width</span>
                  <strong>{boneRes.femur?.width_mm?.toFixed(1)} mm</strong>
                </div>
                <div className="ip-detail-row">
                  <span>Tibia Width</span>
                  <strong>{boneRes.tibia?.width_mm?.toFixed(1)} mm</strong>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="ip-actions">
        <Button variant="ghost" onClick={onBack}>&larr; Back to Analysis</Button>
        <Button variant="primary" onClick={onNext}>Continue to Report &rarr;</Button>
      </div>
    </div>
  );
};
