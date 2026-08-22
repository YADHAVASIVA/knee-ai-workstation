import React from 'react';
import { Button } from '../components/ui/Button';
import './ImplantPlanning.css';

interface ImplantPlanningProps {
  matchingResult: any;
  boneMeasurement: any;
  onMatch: () => void;
  isProcessing: boolean;
}

export const ImplantPlanning: React.FC<ImplantPlanningProps> = ({
  matchingResult,
  boneMeasurement,
  onMatch,
  isProcessing
}) => {
  if (!matchingResult && !isProcessing) {
    return (
      <div className="planning-empty">
        <h2>POTENTIAL ANATOMICAL MATCHES</h2>
        <p>Dimension-based comparison against the demonstration implant database.</p>
        <div className="mt-5">
          <Button variant="primary" onClick={onMatch} disabled={!boneMeasurement}>
            {boneMeasurement ? 'FIND MATCHES' : 'Waiting for measurements...'}
          </Button>
        </div>
      </div>
    );
  }

  if (isProcessing) {
    return (
      <div className="planning-empty">
        <h2>PROCESSING MATCHES</h2>
        <p>Querying demonstration database...</p>
      </div>
    );
  }

  const femoralCandidates = matchingResult?.femoral_candidates || [];

  return (
    <div className="planning-page">
      <div className="planning-header">
        <h2 className="planning-title">POTENTIAL ANATOMICAL MATCHES</h2>
        <p className="planning-subtitle">Dimension-based comparison against the demonstration implant database.</p>
      </div>

      <div className="planning-workspace">
        <div className="planning-col-left">
          <div className="planning-section">
            <h3 className="planning-section-title">Patient Anatomy</h3>
            {boneMeasurement?.femur && (
              <div className="planning-measure-group">
                <h4>Femur</h4>
                <div className="planning-measure-row">
                  <span>Width</span>
                  <span>{boneMeasurement.femur.width_mm ? `${boneMeasurement.femur.width_mm.toFixed(2)} mm` : 'Unavailable'}</span>
                </div>
                <div className="planning-measure-row">
                  <span>AP</span>
                  <span>{boneMeasurement.femur.ap_dimension_mm ? `${boneMeasurement.femur.ap_dimension_mm.toFixed(2)} mm` : 'Unavailable'}</span>
                </div>
              </div>
            )}
            {boneMeasurement?.tibia && (
              <div className="planning-measure-group">
                <h4>Tibia</h4>
                <div className="planning-measure-row">
                  <span>Width</span>
                  <span>{boneMeasurement.tibia.width_mm ? `${boneMeasurement.tibia.width_mm.toFixed(2)} mm` : 'Unavailable'}</span>
                </div>
                <div className="planning-measure-row">
                  <span>AP</span>
                  <span>{boneMeasurement.tibia.ap_dimension_mm ? `${boneMeasurement.tibia.ap_dimension_mm.toFixed(2)} mm` : 'Unavailable'}</span>
                </div>
              </div>
            )}
          </div>
          
          <div className="planning-demo-warning mt-6">
            <strong>DEMONSTRATION DATABASE</strong>
            <p>Synthetic specifications. Not for clinical or surgical use.</p>
          </div>
        </div>

        <div className="planning-col-right">
          <div className="planning-section">
            <h3 className="planning-section-title">Potential Anatomical Matches</h3>
            
            {femoralCandidates.length === 0 ? (
              <div className="text-muted mt-4">No components found.</div>
            ) : (
              <div className="planning-matches-list">
                {femoralCandidates.map((c: any, idx: number) => (
                  <div key={c.implant.id} className="planning-match-card">
                    <div className="match-rank">Rank #{idx + 1}</div>
                    <div className="match-details">
                      <div className="match-name">Femoral Component - Size {c.implant.size_designation}</div>
                      
                      <div className="match-comparison mt-3">
                        <div className="match-comp-row">
                          <span className="match-comp-label">Patient width:</span>
                          <span className="match-comp-val">{boneMeasurement?.femur?.width_mm?.toFixed(2)} mm</span>
                        </div>
                        <div className="match-comp-row">
                          <span className="match-comp-label">Component width:</span>
                          <span className="match-comp-val">{c.implant.width_mm.toFixed(2)} mm</span>
                        </div>
                        <div className="match-comp-row border-top">
                          <span className="match-comp-label">Difference:</span>
                          <span className="match-comp-val">{Math.abs(c.implant.width_mm - (boneMeasurement?.femur?.width_mm || 0)).toFixed(2)} mm</span>
                        </div>
                      </div>

                      <div className="match-comparison mt-3">
                        <div className="match-comp-row">
                          <span className="match-comp-label">Patient AP:</span>
                          <span className="match-comp-val">{boneMeasurement?.femur?.ap_dimension_mm?.toFixed(2)} mm</span>
                        </div>
                        <div className="match-comp-row">
                          <span className="match-comp-label">Component AP:</span>
                          <span className="match-comp-val">{c.implant.ap_dimension_mm.toFixed(2)} mm</span>
                        </div>
                        <div className="match-comp-row border-top">
                          <span className="match-comp-label">Difference:</span>
                          <span className="match-comp-val">{Math.abs(c.implant.ap_dimension_mm - (boneMeasurement?.femur?.ap_dimension_mm || 0)).toFixed(2)} mm</span>
                        </div>
                      </div>
                      
                      <div className="match-score mt-3">
                        Match score: {(c.score * 100).toFixed(1)}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
