import React from 'react';
import type { CaseState, CaseImage } from '../types/case';
import { Button } from '../components/ui/Button';
import './Analysis.css';
import * as api from '../services/api';

interface AnalysisProps {
  caseState: CaseState;
  setCaseState: React.Dispatch<React.SetStateAction<CaseState>>;
  onBack: () => void;
  onNext: () => void;
}

export const Analysis: React.FC<AnalysisProps> = ({ caseState, setCaseState, onBack, onNext }) => {
  const handleRunOaAnalysis = async () => {
    // If not already run, maybe pick an image to run against or run against case ID
    // For now we run OA on the active image or first valid one
    const targetImage = caseState.images.find(img => img.id === caseState.activeImageId) || caseState.images[0];
    if (!targetImage) return;

    const oaRes = await api.analyzeOA(targetImage.id, {
      age: parseInt(caseState.patient.age),
      sex: caseState.patient.sex || 'Not provided',
      oa_status: 'Unknown'
    });

    setCaseState(prev => ({ ...prev, oaAnalysis: oaRes }));
  };

  const renderImageMeasurements = (img: CaseImage) => {
    
    const isMRI = img.metadata?.modality === 'MRI';

    return (
      <div key={img.id} className="an-card">
        <h4>{img.metadata?.modality} • {img.file?.name}</h4>
        
        <div className="an-measure-grid">
          <div className="an-measure-col">
            <h5>Femur</h5>
            <div className="an-measure-val">
              {img.measurements.bones?.femur?.width_mm 
                ? `${img.measurements.bones.femur?.width_mm.toFixed(1)} mm` 
                : 'N/A'}
            </div>
          </div>
          <div className="an-measure-col">
            <h5>Tibia</h5>
            <div className="an-measure-val">
              {img.measurements.bones?.tibia?.width_mm 
                ? `${img.measurements.bones.tibia?.width_mm.toFixed(1)} mm` 
                : 'N/A'}
            </div>
          </div>
          {isMRI && (
            <div className="an-measure-col">
              <h5>Medial Meniscus</h5>
              <div className="an-measure-val">
                {img.measurements.meniscus?.mean_thickness_mm 
                  ? `${img.measurements.meniscus.mean_thickness_mm.toFixed(2)} mm` 
                  : 'N/A'}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="an-container fade-in">
      <div className="an-header">
        <h2 className="an-title">Case Analysis Summary</h2>
        <p className="an-subtitle">Aggregated findings from {caseState.images.length} imaging studies.</p>
      </div>

      <div className="an-layout">
        <div className="an-main-col">
          <h3 className="an-section-title">Anatomical Measurements</h3>
          {caseState.images.filter(img => img.segmentation !== null).map(renderImageMeasurements)}
        </div>
        
        <div className="an-side-col">
          <div className="an-card">
            <h3 className="an-section-title">OA-Associated Analysis</h3>
            {!caseState.oaAnalysis ? (
              <div className="an-empty-state">
                <p>Run analysis to detect potential OA indicators across studies.</p>
                {caseState.patient.age && caseState.patient.sex ? (
                  <Button onClick={handleRunOaAnalysis}>Run Case OA Analysis</Button>
                ) : (
                  <div className="an-warning-box">Patient age and sex are required to run OA-associated analysis. Please update them in the Case Overview.</div>
                )}
              </div>
            ) : (
              <div className="an-oa-results">
                <div className="an-oa-row">
                  <span>Joint Space Narrowing</span>
                  <strong>{caseState.oaAnalysis.patient_findings.joint_space_narrowing}</strong>
                </div>
                <div className="an-oa-row">
                  <span>Osteophytes</span>
                  <strong>{caseState.oaAnalysis.patient_findings.osteophytes}</strong>
                </div>
                <div className="an-oa-row">
                  <span>Sclerosis</span>
                  <strong>{caseState.oaAnalysis.patient_findings.sclerosis}</strong>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="an-actions">
        <Button variant="ghost" onClick={onBack}>&larr; Back to Anatomy</Button>
        <Button variant="primary" onClick={onNext}>Continue to Implant Planning &rarr;</Button>
      </div>
    </div>
  );
};
