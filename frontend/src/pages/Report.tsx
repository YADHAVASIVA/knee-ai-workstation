import React from 'react';
import { Button } from '../components/ui/Button';
import './Report.css';

interface ReportProps {
  analysisId: string | null;
  patientData: any;
  imageMetadata: any;
  boneMeasurement: any;
  meniscusMeasurement: any;
  oaResult: any;
  matchingResult: any;
  onPrint: () => void;
}

export const Report: React.FC<ReportProps> = ({
  analysisId,
  patientData,
  imageMetadata,
  boneMeasurement,
  meniscusMeasurement,
  matchingResult,
  onPrint
}) => {
  if (!matchingResult) {
    return (
      <div className="report-empty">
        <h2>REPORT UNAVAILABLE</h2>
        <p>Complete the analysis pipeline to generate a final report.</p>
      </div>
    );
  }

  const dateStr = new Date().toLocaleDateString();
  const timeStr = new Date().toLocaleTimeString();

  return (
    <div className="report-page">
      <div className="report-toolbar">
        <Button variant="primary" onClick={onPrint}>PRINT REPORT</Button>
      </div>

      <div className="report-document" id="printable-report">
        <div className="report-header">
          <div className="report-header-left">
            <h1 className="report-title">KNEE AI ANALYSIS REPORT</h1>
            <div className="report-meta">Case ID: {analysisId}</div>
            <div className="report-meta">Generated: {dateStr} {timeStr}</div>
          </div>
          <div className="report-header-right">
            <div className="report-badge">RESEARCH PROTOTYPE</div>
          </div>
        </div>

        <div className="report-section">
          <h2 className="report-section-title">PATIENT CONTEXT</h2>
          <table className="report-table">
            <tbody>
              <tr>
                <td className="rt-label">Age</td>
                <td className="rt-value">{patientData.age || 'UNKNOWN'}</td>
                <td className="rt-label">Sex</td>
                <td className="rt-value">{patientData.sex || 'UNKNOWN'}</td>
                <td className="rt-label">Clinical Label</td>
                <td className="rt-value">{patientData.oa_status || 'UNKNOWN'}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="report-section">
          <h2 className="report-section-title">IMAGE INFORMATION</h2>
          <table className="report-table">
            <tbody>
              <tr>
                <td className="rt-label">Modality</td>
                <td className="rt-value">{imageMetadata?.modality || 'UNKNOWN'}</td>
                <td className="rt-label">Calibration</td>
                <td className="rt-value">{boneMeasurement?.calibration_available ? 'CALIBRATED (Physical)' : 'UNCALIBRATED (Pixel)'}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="report-section">
          <h2 className="report-section-title">ANATOMICAL MEASUREMENTS</h2>
          <div className="report-measurements">
            <div className="rm-group">
              <h3>MEDIAL MENISCUS</h3>
              <p>Mean Thickness: {meniscusMeasurement?.mean_thickness_mm ? `${meniscusMeasurement.mean_thickness_mm.toFixed(2)} mm` : 'N/A'}</p>
            </div>
            <div className="rm-group">
              <h3>FEMUR</h3>
              <p>Width: {boneMeasurement?.femur?.width_mm ? `${boneMeasurement.femur.width_mm.toFixed(2)} mm` : 'N/A'}</p>
              <p>AP: {boneMeasurement?.femur?.ap_dimension_mm ? `${boneMeasurement.femur.ap_dimension_mm.toFixed(2)} mm` : 'N/A'}</p>
            </div>
            <div className="rm-group">
              <h3>TIBIA</h3>
              <p>Width: {boneMeasurement?.tibia?.width_mm ? `${boneMeasurement.tibia.width_mm.toFixed(2)} mm` : 'N/A'}</p>
              <p>AP: {boneMeasurement?.tibia?.ap_dimension_mm ? `${boneMeasurement.tibia.ap_dimension_mm.toFixed(2)} mm` : 'N/A'}</p>
            </div>
          </div>
        </div>

        <div className="report-section">
          <h2 className="report-section-title">POTENTIAL IMPLANT MATCHES</h2>
          {matchingResult?.femoral_candidates?.length > 0 ? (
            <table className="report-match-table">
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Component</th>
                  <th>Width (mm)</th>
                  <th>AP (mm)</th>
                  <th>Score</th>
                </tr>
              </thead>
              <tbody>
                {matchingResult.femoral_candidates.slice(0, 3).map((c: any, idx: number) => (
                  <tr key={c.implant.id}>
                    <td>{idx + 1}</td>
                    <td>Femoral Size {c.implant.size_designation}</td>
                    <td>{c.implant.width_mm.toFixed(1)}</td>
                    <td>{c.implant.ap_dimension_mm.toFixed(1)}</td>
                    <td>{(c.score * 100).toFixed(1)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="rt-value">No potential matches found in the database.</p>
          )}
        </div>

        <div className="report-footer">
          <p className="report-disclaimer">
            <strong>DISCLAIMER:</strong> This report is generated by a demonstration research prototype. 
            It is not intended for clinical, diagnostic, or surgical use. The implant database is synthetic 
            and the automated anatomical segmentation has not been clinically validated.
          </p>
        </div>
      </div>
    </div>
  );
};
