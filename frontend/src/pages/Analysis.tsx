import React from 'react';
import { Button } from '../components/ui/Button';
import { AlertTriangle } from 'lucide-react';
import './Analysis.css';

interface AnalysisProps {
  boneMeasurement: any;
  meniscusMeasurement: any;
  onAnalyze: () => void;
  isProcessing: boolean;
}

export const Analysis: React.FC<AnalysisProps> = ({
  boneMeasurement,
  meniscusMeasurement,
  onAnalyze,
  isProcessing
}) => {
  if (!isProcessing && !meniscusMeasurement) {
    return (
      <div className="analysis-empty">
        <h2>OA-ASSOCIATED ANALYSIS</h2>
        <p>Analyze anatomical measurements against population references.</p>
        <div className="mt-5">
          <Button variant="primary" onClick={onAnalyze} disabled={!boneMeasurement}>
            {boneMeasurement ? 'START ANALYSIS' : 'Waiting for measurements...'}
          </Button>
        </div>
      </div>
    );
  }

  const mean_thickness = meniscusMeasurement?.mean_thickness_mm;
  const medial_thickness = meniscusMeasurement?.medial_thickness_mm;
  const lateral_thickness = meniscusMeasurement?.lateral_thickness_mm;

  return (
    <div className="analysis-page">
      <div className="analysis-header">
        <h2 className="analysis-title">OA-ASSOCIATED ANALYSIS</h2>
      </div>

      <div className="analysis-workspace">
        <div className="analysis-col-left">
          <div className="analysis-section">
            <h3 className="analysis-section-title">Patient Context</h3>
            <div className="analysis-metric-grid">
              <div className="analysis-metric">
                <span className="analysis-metric-label">Age</span>
                <span className="analysis-metric-value">65</span>
              </div>
              <div className="analysis-metric">
                <span className="analysis-metric-label">Sex</span>
                <span className="analysis-metric-value">M</span>
              </div>
              <div className="analysis-metric">
                <span className="analysis-metric-label">Clinical Status</span>
                <span className="analysis-metric-value">Moderate</span>
              </div>
            </div>
          </div>

          <div className="analysis-section mt-6">
            <h3 className="analysis-section-title">Anatomical Measurements</h3>
            
            <div className="analysis-measure-group">
              <h4>Femur</h4>
              <div className="analysis-measure-row">
                <span>Width</span>
                <span>{boneMeasurement?.femur?.width_mm ? `${boneMeasurement.femur.width_mm.toFixed(2)} mm` : 'Not measured'}</span>
              </div>
              <div className="analysis-measure-row">
                <span>AP</span>
                <span>{boneMeasurement?.femur?.ap_dimension_mm ? `${boneMeasurement.femur.ap_dimension_mm.toFixed(2)} mm` : 'Not measured'}</span>
              </div>
            </div>

            <div className="analysis-measure-group">
              <h4>Tibia</h4>
              <div className="analysis-measure-row">
                <span>Width</span>
                <span>{boneMeasurement?.tibia?.width_mm ? `${boneMeasurement.tibia.width_mm.toFixed(2)} mm` : 'Not measured'}</span>
              </div>
              <div className="analysis-measure-row">
                <span>AP</span>
                <span>{boneMeasurement?.tibia?.ap_dimension_mm ? `${boneMeasurement.tibia.ap_dimension_mm.toFixed(2)} mm` : 'Not measured'}</span>
              </div>
            </div>

            <div className="analysis-measure-group">
              <h4>Meniscus</h4>
              <div className="analysis-measure-row">
                <span>Medial</span>
                <span>{medial_thickness ? `${medial_thickness.toFixed(2)} mm` : 'Not measured'}</span>
              </div>
              <div className="analysis-measure-row">
                <span>Lateral</span>
                <span>{lateral_thickness ? `${lateral_thickness.toFixed(2)} mm` : 'Not measured'}</span>
              </div>
              <div className="analysis-measure-row">
                <span>Mean</span>
                <span>{mean_thickness ? `${mean_thickness.toFixed(2)} mm` : 'Not measured'}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="analysis-col-right">
          <div className="analysis-section">
            <h3 className="analysis-section-title">Population Comparison</h3>
            
            <div className="analysis-prototype-warning">
              <div className="warning-icon"><AlertTriangle size={16} /></div>
              <div className="warning-content">
                <strong>RESEARCH PROTOTYPE</strong>
                <p>Synthetic reference dataset &mdash; not clinical evidence.</p>
              </div>
            </div>

            <div className="analysis-comparison mt-6">
              <p className="text-sm text-muted mb-4">Patient Meniscus Mean Thickness vs Reference Population</p>
              
              {mean_thickness ? (
                <div className="comparison-visual">
                  <div className="comparison-track">
                    <span className="comp-label left">Lower</span>
                    <div className="comp-line">
                      <div className="comp-marker" style={{ left: '50%' }}>●</div>
                      <div className="comp-marker-label" style={{ left: '50%' }}>
                        Patient<br/>{mean_thickness.toFixed(2)}
                      </div>
                    </div>
                    <span className="comp-label right">Upper</span>
                  </div>
                </div>
              ) : (
                <div className="text-muted text-sm text-center">Patient measurement unavailable for comparison.</div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
