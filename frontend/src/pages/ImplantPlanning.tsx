import React from 'react';
import { Card } from '../components/ui/Card';
import { SectionHeader } from '../components/ui/SectionHeader';
import { StatusBadge } from '../components/ui/StatusBadge';
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
        <SectionHeader 
          title="IMPLANT PLANNING" 
          description="Compare patient anatomy against the implant database to find potential matches." 
        />
        <div className="planning-empty-action mt-5">
          <Button variant="primary" onClick={onMatch} disabled={!boneMeasurement}>
            {boneMeasurement ? 'FIND POTENTIAL MATCHES' : 'Waiting for measurements...'}
          </Button>
        </div>
      </div>
    );
  }

  if (isProcessing) {
    return (
      <div className="planning-empty">
        <SectionHeader title="PROCESSING IMPLANT MATCHES" description="Querying database and calculating geometrical fit..." />
      </div>
    );
  }

  const femoralCandidates = matchingResult?.femoral_candidates || [];

  return (
    <div className="planning-page">
      <div className="planning-header">
        <h2 className="planning-title">IMPLANT PLANNING</h2>
        <p className="planning-subtitle">Potential anatomical matches based on geometric analysis.</p>
      </div>

      <div className="planning-workspace">
        <div className="planning-col-left">
          <Card className="ui-card">
            <h3 className="ui-card-title">PATIENT ANATOMY</h3>
            {boneMeasurement?.femur && (
              <div className="planning-measure-group">
                <h4 className="planning-measure-title">FEMUR</h4>
                <div className="planning-measure-row">
                  <span className="planning-measure-label">Width</span>
                  <span className="planning-measure-value">
                    {boneMeasurement.femur.width_mm ? `${boneMeasurement.femur.width_mm.toFixed(1)} mm` : 'N/A'}
                  </span>
                </div>
                <div className="planning-measure-row">
                  <span className="planning-measure-label">AP Dimension</span>
                  <span className="planning-measure-value">
                    {boneMeasurement.femur.ap_dimension_mm ? `${boneMeasurement.femur.ap_dimension_mm.toFixed(1)} mm` : 'N/A'}
                  </span>
                </div>
              </div>
            )}
          </Card>

          <Card className="ui-card">
            <h3 className="ui-card-title">DATABASE</h3>
            <div className="mt-2">
              <StatusBadge status="DEMO" label="DEMONSTRATION DATABASE" />
              <p className="planning-demo-text mt-3 text-muted" style={{ fontSize: '12px' }}>
                Synthetic specifications. Not for clinical or surgical use.
              </p>
            </div>
          </Card>
        </div>

        <div className="planning-col-right">
          <Card className="ui-card planning-results-card">
            <div className="planning-results-header">
              <h3 className="ui-card-title mb-0 border-0">POTENTIAL MATCHES (FEMORAL)</h3>
              <StatusBadge 
                status={matchingResult?.calibration_available ? 'CALIBRATED' : 'UNCALIBRATED'} 
                label={matchingResult?.calibration_available ? 'Physical scale verified' : 'Pixel approximation'} 
              />
            </div>

            {femoralCandidates.length === 0 ? (
              <div className="planning-no-match">
                <h4>NO POTENTIAL MATCH FOUND</h4>
                <p>No components in the database fit the patient\'s anatomical parameters.</p>
              </div>
            ) : (
              <div className="planning-table-wrapper mt-4">
                <table className="planning-table">
                  <thead>
                    <tr>
                      <th className="rank-col">RANK</th>
                      <th>COMPONENT</th>
                      <th className="num-col">WIDTH (mm)</th>
                      <th className="num-col">AP (mm)</th>
                      <th className="num-col">SCORE</th>
                    </tr>
                  </thead>
                  <tbody>
                    {femoralCandidates.map((c: any, idx: number) => (
                      <tr key={c.implant.id} className={idx === 0 ? 'top-match' : ''}>
                        <td className="rank-col">{String(idx + 1).padStart(2, '0')}</td>
                        <td>
                          <div className="comp-name">Femoral Size {c.implant.size_designation}</div>
                          <div className="comp-meta">{c.implant.manufacturer}</div>
                        </td>
                        <td className="num-col">
                          <div className="comp-val">{c.implant.width_mm.toFixed(1)}</div>
                          <div className="comp-diff">
                            Δ {Math.abs(c.implant.width_mm - boneMeasurement.femur.width_mm).toFixed(1)}
                          </div>
                        </td>
                        <td className="num-col">
                          <div className="comp-val">{c.implant.ap_dimension_mm.toFixed(1)}</div>
                          <div className="comp-diff">
                            Δ {Math.abs(c.implant.ap_dimension_mm - boneMeasurement.femur.ap_dimension_mm).toFixed(1)}
                          </div>
                        </td>
                        <td className="num-col">
                          <div className="comp-score">{(c.score * 100).toFixed(1)}</div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
};
