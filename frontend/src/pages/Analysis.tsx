import React from 'react';
import { Card } from '../components/ui/Card';
import { SectionHeader } from '../components/ui/SectionHeader';
import { StatusBadge } from '../components/ui/StatusBadge';
import { Button } from '../components/ui/Button';
import type { PatientData } from '../services/api';
import './Analysis.css';

interface AnalysisProps {
  patientData: PatientData;
  oaResult: any;
  boneMeasurement: any;
  meniscusMeasurement: any;
  onAnalyze: () => void;
  isProcessing: boolean;
}

export const Analysis: React.FC<AnalysisProps> = ({
  patientData,
  oaResult,
  boneMeasurement,
  meniscusMeasurement,
  onAnalyze,
  isProcessing
}) => {
  if (!oaResult && !isProcessing) {
    return (
      <div className="analysis-empty">
        <SectionHeader 
          title="OA ANALYSIS" 
          description="Analyze the anatomical measurements against population data." 
        />
        <div className="analysis-empty-action mt-5">
          <Button variant="primary" onClick={onAnalyze} disabled={!boneMeasurement}>
            {boneMeasurement ? 'START OA ANALYSIS' : 'Waiting for measurements...'}
          </Button>
        </div>
      </div>
    );
  }

  if (isProcessing) {
    return (
      <div className="analysis-empty">
        <SectionHeader title="PROCESSING OA ANALYSIS" description="Comparing patient anatomy to population references..." />
      </div>
    );
  }

  return (
    <div className="analysis-page">
      <div className="analysis-header">
        <h2 className="analysis-title">OSTEOARTHRITIS-ASSOCIATED ANALYSIS</h2>
        <p className="analysis-subtitle">Population comparison and structural findings.</p>
      </div>

      <div className="analysis-workspace">
        {/* LEFT COLUMN: PATIENT CONTEXT & MEASUREMENTS */}
        <div className="analysis-col-left">
          <Card className="ui-card">
            <h3 className="ui-card-title">PATIENT CONTEXT</h3>
            <div className="analysis-metric-grid">
              <div className="analysis-metric">
                <span className="analysis-metric-label">Age</span>
                <span className="analysis-metric-value">{patientData.age !== null ? patientData.age : 'UNKNOWN'}</span>
              </div>
              <div className="analysis-metric">
                <span className="analysis-metric-label">Sex</span>
                <span className="analysis-metric-value">{patientData.sex || 'UNKNOWN'}</span>
              </div>
              <div className="analysis-metric">
                <span className="analysis-metric-label">Clinical OA Status</span>
                <span className="analysis-metric-value">{patientData.oa_status || 'UNKNOWN'}</span>
              </div>
            </div>
          </Card>

          <Card className="ui-card">
            <h3 className="ui-card-title">KEY MEASUREMENTS</h3>
            <div className="analysis-measure-list">
              <div className="analysis-measure-item">
                <span className="analysis-measure-label">Meniscus Mean Thickness</span>
                <span className="analysis-measure-value">
                  {meniscusMeasurement?.mean_thickness_mm ? `${meniscusMeasurement.mean_thickness_mm.toFixed(2)} mm` : 'Unavailable'}
                </span>
              </div>
              <div className="analysis-measure-item">
                <span className="analysis-measure-label">Femoral Width</span>
                <span className="analysis-measure-value">
                  {boneMeasurement?.femur?.width_mm ? `${boneMeasurement.femur.width_mm.toFixed(2)} mm` : 'Unavailable'}
                </span>
              </div>
              <div className="analysis-measure-item">
                <span className="analysis-measure-label">Tibial Width</span>
                <span className="analysis-measure-value">
                  {boneMeasurement?.tibia?.width_mm ? `${boneMeasurement.tibia.width_mm.toFixed(2)} mm` : 'Unavailable'}
                </span>
              </div>
            </div>
          </Card>

          <Card className="ui-card">
            <h3 className="ui-card-title">DATA SOURCE</h3>
            <div className="mt-2">
              <StatusBadge status="DEMO" label="DEMONSTRATION DATA" />
              <p className="analysis-demo-text mt-3 text-muted" style={{ fontSize: '12px' }}>
                Comparisons are generated using a synthetic research dataset. Not for clinical diagnostic use.
              </p>
            </div>
          </Card>
        </div>

        {/* RIGHT COLUMN: COMPARISONS */}
        <div className="analysis-col-right">
          <Card className="ui-card analysis-results-card">
            <h3 className="ui-card-title">POPULATION COMPARISON</h3>
            
            <div className="analysis-section mt-4">
              <h4 className="analysis-section-title">OA vs Non-OA (Male)</h4>
              <p className="text-muted text-sm mb-3">Comparing meniscus thickness against male population averages.</p>
              
              <div className="analysis-chart-mock">
                {/* Minimal CSS Bar Chart Mock */}
                <div className="chart-bar-group">
                  <div className="chart-label">Non-OA Avg</div>
                  <div className="chart-track">
                    <div className="chart-fill bg-secondary" style={{ width: '85%' }}></div>
                    <div className="chart-val">5.8 mm</div>
                  </div>
                </div>
                <div className="chart-bar-group">
                  <div className="chart-label">OA Avg</div>
                  <div className="chart-track">
                    <div className="chart-fill bg-warning" style={{ width: '55%' }}></div>
                    <div className="chart-val">3.4 mm</div>
                  </div>
                </div>
                <div className="chart-bar-group highlight-group">
                  <div className="chart-label">Patient</div>
                  <div className="chart-track">
                    <div className="chart-fill bg-primary" style={{ width: `${Math.min(((meniscusMeasurement?.mean_thickness_mm || 0) / 6.5) * 100, 100)}%` }}></div>
                    <div className="chart-val">{meniscusMeasurement?.mean_thickness_mm?.toFixed(2) || '?'} mm</div>
                  </div>
                </div>
              </div>
            </div>

            <div className="analysis-section mt-6">
              <h4 className="analysis-section-title">Age Association</h4>
              <p className="text-muted text-sm mb-3">Thickness trend across age groups.</p>
              <div className="analysis-chart-mock text-muted text-center p-4 border-dashed rounded">
                [ Age Association Scatter Plot ]
                <br/>
                <span className="text-xs">Recharts integration placeholder</span>
              </div>
            </div>
            
          </Card>
        </div>
      </div>
    </div>
  );
};
