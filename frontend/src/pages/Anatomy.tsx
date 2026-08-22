import React, { useState } from 'react';
import { MedicalImageViewer } from '../components/MedicalImageViewer';
import { MousePointer2, Move, ZoomIn, SlidersHorizontal, Eye, EyeOff } from 'lucide-react';
import './Anatomy.css';

interface AnatomyProps {
  previewUrl: string | null;
  overlays: any[];
  measurements: any[];
  boneMeasurement: any;
  onToggleOverlay: (id: string) => void;
  showMeasurements: boolean;
  onToggleMeasurements: (show: boolean) => void;
  showBoneMeasurements: boolean;
  onToggleBoneMeasurements: (show: boolean) => void;
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
  onToggleBoneMeasurements
}) => {
  const [activeTool, setActiveTool] = useState('pan');

  return (
    <div className="ana-workstation">
      <div className="ana-sidebar ana-sidebar-left">
        <div className="ana-panel">
          <div className="ana-panel-header">LAYERS</div>
          <div className="ana-layer-list">
            <div className="ana-layer-item">
              <button className="ana-layer-toggle" disabled><Eye size={16} className="text-success" /></button>
              <span>Base Image (MRI)</span>
            </div>
            {overlays.map(overlay => (
              <div key={overlay.id} className="ana-layer-item" onClick={() => onToggleOverlay(overlay.id)}>
                <button className="ana-layer-toggle">
                  {overlay.visible ? <Eye size={16} className="text-success" /> : <EyeOff size={16} className="text-muted" />}
                </button>
                <span style={{ color: overlay.color }}>{overlay.name}</span>
                <span className="ana-layer-status">Detected</span>
              </div>
            ))}
          </div>
        </div>

        <div className="ana-panel">
          <div className="ana-panel-header">TOOLS</div>
          <div className="ana-tool-list">
            <button className={`ana-tool-btn ${activeTool === 'select' ? 'active' : ''}`} disabled title="Coming soon">
              <MousePointer2 size={16} /> <span>Select (Coming soon)</span>
            </button>
            <button className={`ana-tool-btn ${activeTool === 'pan' ? 'active' : ''}`} onClick={() => setActiveTool('pan')} disabled title="Coming soon">
              <Move size={16} /> <span>Pan (Coming soon)</span>
            </button>
            <button className={`ana-tool-btn ${activeTool === 'zoom' ? 'active' : ''}`} onClick={() => setActiveTool('zoom')} disabled title="Coming soon">
              <ZoomIn size={16} /> <span>Zoom (Coming soon)</span>
            </button>
            <button className={`ana-tool-btn ${activeTool === 'window' ? 'active' : ''}`} disabled title="Coming soon">
              <SlidersHorizontal size={16} /> <span>Window/Level (Coming soon)</span>
            </button>
          </div>
        </div>
      </div>

      <div className="ana-viewer-container">
        {previewUrl ? (
          <MedicalImageViewer
            imageUrl={previewUrl}
            overlays={overlays}
            measurements={showMeasurements ? measurements : []}
            boneResult={showBoneMeasurements ? boneMeasurement : null}
          />
        ) : (
          <div className="ana-empty">
            <p>No image available.</p>
          </div>
        )}
      </div>

      <div className="ana-sidebar ana-sidebar-right">
        <div className="ana-panel">
          <div className="ana-panel-header">FINDINGS</div>
          
          <div className="ana-findings-list">
            {overlays.length > 0 ? overlays.map(o => (
              <div key={o.id} className="ana-finding-item">
                <span className="ana-finding-name">{o.name}</span>
                <span className="ana-finding-status">Detected</span>
              </div>
            )) : (
              <div className="ana-empty-text">No findings available</div>
            )}
          </div>
        </div>

        <div className="ana-panel">
          <div className="ana-panel-header">MEASUREMENTS</div>
          
          <div className="ana-measure-controls">
            <div className="ana-layer-item" onClick={() => onToggleMeasurements(!showMeasurements)}>
              <button className="ana-layer-toggle">
                {showMeasurements ? <Eye size={16} className="text-success" /> : <EyeOff size={16} className="text-muted" />}
              </button>
              <span>Meniscus</span>
            </div>
            <div className="ana-layer-item" onClick={() => onToggleBoneMeasurements(!showBoneMeasurements)}>
              <button className="ana-layer-toggle">
                {showBoneMeasurements ? <Eye size={16} className="text-success" /> : <EyeOff size={16} className="text-muted" />}
              </button>
              <span>Bones</span>
            </div>
          </div>

          <div className="ana-measure-summary">
            <div className="ana-summary-item">
              <div className="ana-summary-label">Femur Width</div>
              <div className="ana-summary-val">{boneMeasurement?.femur?.width_mm ? `${boneMeasurement.femur.width_mm.toFixed(1)} mm` : 'Not measured'}</div>
            </div>
            <div className="ana-summary-item">
              <div className="ana-summary-label">Femur AP</div>
              <div className="ana-summary-val">{boneMeasurement?.femur?.ap_dimension_mm ? `${boneMeasurement.femur.ap_dimension_mm.toFixed(1)} mm` : 'Not measured'}</div>
            </div>
            <div className="ana-summary-item">
              <div className="ana-summary-label">Tibia Width</div>
              <div className="ana-summary-val">{boneMeasurement?.tibia?.width_mm ? `${boneMeasurement.tibia.width_mm.toFixed(1)} mm` : 'Not measured'}</div>
            </div>
            <div className="ana-summary-item">
              <div className="ana-summary-label">Tibia AP</div>
              <div className="ana-summary-val">{boneMeasurement?.tibia?.ap_dimension_mm ? `${boneMeasurement.tibia.ap_dimension_mm.toFixed(1)} mm` : 'Not measured'}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
