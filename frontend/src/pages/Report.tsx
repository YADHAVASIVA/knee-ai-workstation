import React from 'react';
import { Button } from '../components/ui/Button';
import './Report.css';

interface ReportProps {
  modality?: string;
  analysisId: string | null;
  imageMetadata: any;
  boneMeasurement: any;
  meniscusMeasurement: any;
  matchingResult: any;
  onNavigate: (route: string) => void;
}

export const Report: React.FC<ReportProps> = ({
  analysisId,
  imageMetadata,
  boneMeasurement,
  meniscusMeasurement,
  matchingResult,
  onNavigate
}) => {
  return (
    <div className="report-workspace">
      <div className="report-controls">
        <Button variant="secondary" onClick={() => onNavigate('overview')}>Back</Button>
        <Button variant="primary" onClick={() => window.print()}>Print</Button>
      </div>

      <div className="report-document">
        <div className="report-header">
          <h1>Report Preview</h1>
        </div>

        <div className="report-section">
          <h2>CASE</h2>
          <div className="report-grid">
            <div><strong>Case ID:</strong> {analysisId?.split('-')[0].toUpperCase()}</div>
            <div><strong>Modality:</strong> {imageMetadata?.modality || 'Unavailable'}</div>
            <div><strong>Dimensions:</strong> {imageMetadata?.dimensions ? `${imageMetadata.dimensions.width} × ${imageMetadata.dimensions.height}` : 'Unavailable'}</div>
            <div><strong>Calibration:</strong> {imageMetadata?.pixel_spacing ? 'Available' : 'Unavailable'}</div>
          </div>
        </div>

        <div className="report-section">
          <h2>ANATOMICAL FINDINGS</h2>
          <div className="report-grid-3">
            <div>
              <h3>Femur</h3>
              <p>Width: {boneMeasurement?.femur?.width_mm ? `${boneMeasurement.femur.width_mm.toFixed(2)} mm` : 'Not measured'}</p>
              <p>AP: {boneMeasurement?.femur?.ap_dimension_mm ? `${boneMeasurement.femur.ap_dimension_mm.toFixed(2)} mm` : 'Not measured'}</p>
            </div>
            <div>
              <h3>Tibia</h3>
              <p>Width: {boneMeasurement?.tibia?.width_mm ? `${boneMeasurement.tibia.width_mm.toFixed(2)} mm` : 'Not measured'}</p>
              <p>AP: {boneMeasurement?.tibia?.ap_dimension_mm ? `${boneMeasurement.tibia.ap_dimension_mm.toFixed(2)} mm` : 'Not measured'}</p>
            </div>
            <div>
              <h3>Meniscus</h3>
              <p>Mean Thickness: {meniscusMeasurement?.mean_thickness_mm ? `${meniscusMeasurement.mean_thickness_mm.toFixed(2)} mm` : 'Not measured'}</p>
            </div>
          </div>
        </div>

        <div className="report-section">
          <h2>POTENTIAL ANATOMICAL MATCHES</h2>
          {matchingResult?.femoral_candidates?.length > 0 ? (
            <ul>
              {matchingResult.femoral_candidates.slice(0, 3).map((c: any, i: number) => (
                <li key={i}>
                  Rank #{i+1}: Size {c.implant.size_designation} (Score: {(c.score*100).toFixed(1)})
                </li>
              ))}
            </ul>
          ) : (
            <p>No matches generated.</p>
          )}
        </div>

        <div className="report-warning">
          <strong>RESEARCH PROTOTYPE</strong>
          <p>This report is generated from a demonstration/research system and must not be used for clinical or surgical decision-making.</p>
        </div>
      </div>
    </div>
  );
};
