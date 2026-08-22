import React from 'react';
import { MedicalImageViewer } from '../components/MedicalImageViewer';
import { Card } from '../components/ui/Card';
import { SectionHeader } from '../components/ui/SectionHeader';
import { StatusBadge } from '../components/ui/StatusBadge';
import type { MeasurementLocation } from '../services/api';
import './Anatomy.css';

interface AnatomyProps {
  previewUrl: string | null;
  overlays: any[];
  measurements: MeasurementLocation[];
  boneMeasurement: any;
  onToggleOverlay: (id: string) => void;
  showMeasurements: boolean;
  onToggleMeasurements: (show: boolean) => void;
  showBoneMeasurements: boolean;
  onToggleBoneMeasurements: (show: boolean) => void;
  isDemo: boolean;
}

export const Anatomy: React.FC<AnatomyProps> = ({
  previewUrl,
  overlays,
  measurements,
  boneMeasurement,
  onToggleOverlay,
  showMeasurements,
  onToggleMeasurements,
  showBoneMeasurements,
  onToggleBoneMeasurements,
  isDemo
}) => {
  if (!previewUrl) {
    return (
      <div className="anatomy-empty">
        <SectionHeader title="ANATOMY UNAVAILABLE" description="No active image to display." />
      </div>
    );
  }

  const isCalibrated = boneMeasurement?.calibration_available;

  return (
    <div className="anatomy-page">
      <div className="anatomy-header">
        <div>
          <h2 className="anatomy-title">ANATOMY WORKSPACE</h2>
          <p className="anatomy-subtitle">Anatomical structures and geometric measurements.</p>
        </div>
      </div>

      <div className="anatomy-workspace">
        {/* HERO VIEWER */}
        <div className="anatomy-hero">
          <MedicalImageViewer 
            imageUrl={previewUrl}
            overlays={overlays}
            measurements={measurements}
            boneResult={boneMeasurement}
            onToggleOverlay={onToggleOverlay}
            showMeasurements={showMeasurements}
            onToggleMeasurements={onToggleMeasurements}
            showBoneMeasurements={showBoneMeasurements}
            onToggleBoneMeasurements={onToggleBoneMeasurements}
          />
        </div>

        {/* ANALYTICAL SIDE PANEL */}
        <div className="anatomy-panel">
          
          <Card className="ana-card">
            <h3 className="ana-card-title">IMAGE LAYERS</h3>
            <div className="ana-layers">
              {overlays.map(overlay => (
                <label key={overlay.id} className="ana-layer-item">
                  <input 
                    type="checkbox" 
                    checked={overlay.visible} 
                    onChange={() => onToggleOverlay(overlay.id)}
                  />
                  <span className="ana-color-box" style={{ backgroundColor: overlay.color }}></span>
                  <span className="ana-layer-name">{overlay.name}</span>
                </label>
              ))}
              <label className="ana-layer-item">
                <input 
                  type="checkbox" 
                  checked={showMeasurements} 
                  onChange={(e) => onToggleMeasurements(e.target.checked)}
                />
                <span className="ana-color-box" style={{ backgroundColor: 'var(--color-success)' }}></span>
                <span className="ana-layer-name">Meniscus Measurements</span>
              </label>
              <label className="ana-layer-item">
                <input 
                  type="checkbox" 
                  checked={showBoneMeasurements} 
                  onChange={(e) => onToggleBoneMeasurements(e.target.checked)}
                />
                <span className="ana-color-box" style={{ backgroundColor: 'var(--color-primary)' }}></span>
                <span className="ana-layer-name">Bone Measurements</span>
              </label>
            </div>
          </Card>

          <Card className="ana-card">
            <h3 className="ana-card-title">ANATOMICAL MEASUREMENTS</h3>
            
            <div className="ana-measure-group">
              <h4 className="ana-measure-title">MEDIAL MENISCUS</h4>
              {measurements.map(m => (
                <div className="ana-measure-row" key={m.name}>
                  <span className="ana-measure-label">Location {m.name}</span>
                  <span className="ana-measure-value">
                    {m.thickness_mm !== null ? `${m.thickness_mm.toFixed(2)} mm` : `${m.thickness_pixels.toFixed(1)} px`}
                  </span>
                </div>
              ))}
            </div>

            {boneMeasurement?.femur && (
              <div className="ana-measure-group">
                <h4 className="ana-measure-title">FEMUR</h4>
                <div className="ana-measure-row">
                  <span className="ana-measure-label">Width</span>
                  <span className="ana-measure-value">
                    {boneMeasurement.femur.width_mm ? `${boneMeasurement.femur.width_mm.toFixed(2)} mm` : `${boneMeasurement.femur.width_pixels.toFixed(1)} px`}
                  </span>
                </div>
                <div className="ana-measure-row">
                  <span className="ana-measure-label">AP Dimension</span>
                  <span className="ana-measure-value">
                    {boneMeasurement.femur.ap_dimension_mm ? `${boneMeasurement.femur.ap_dimension_mm.toFixed(2)} mm` : `${boneMeasurement.femur.ap_dimension_pixels.toFixed(1)} px`}
                  </span>
                </div>
              </div>
            )}

            {boneMeasurement?.tibia && (
              <div className="ana-measure-group">
                <h4 className="ana-measure-title">TIBIA</h4>
                <div className="ana-measure-row">
                  <span className="ana-measure-label">Width</span>
                  <span className="ana-measure-value">
                    {boneMeasurement.tibia.width_mm ? `${boneMeasurement.tibia.width_mm.toFixed(2)} mm` : `${boneMeasurement.tibia.width_pixels.toFixed(1)} px`}
                  </span>
                </div>
                <div className="ana-measure-row">
                  <span className="ana-measure-label">AP Dimension</span>
                  <span className="ana-measure-value">
                    {boneMeasurement.tibia.ap_dimension_mm ? `${boneMeasurement.tibia.ap_dimension_mm.toFixed(2)} mm` : `${boneMeasurement.tibia.ap_dimension_pixels.toFixed(1)} px`}
                  </span>
                </div>
              </div>
            )}
          </Card>

          <Card className="ana-card">
            <h3 className="ana-card-title">STATUS</h3>
            <div className="ana-status-row">
              <span className="ana-status-label">Spatial Calibration</span>
              <StatusBadge 
                status={isCalibrated ? 'CALIBRATED' : 'UNCALIBRATED'} 
                label={isCalibrated ? 'Available' : 'Review Required'} 
              />
            </div>
            {isDemo && (
              <div className="ana-status-row mt-3">
                <span className="ana-status-label">Model Status</span>
                <StatusBadge status="DEMO" label="RESEARCH MODEL" />
              </div>
            )}
          </Card>

        </div>
      </div>
    </div>
  );
};
