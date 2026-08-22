import React, { useState } from 'react';
import { MedicalImageViewer } from '../components/MedicalImageViewer';
import { Layers, Activity, Search, ZoomIn, Maximize, Target, MousePointer2 } from 'lucide-react';
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
  isDemo?: boolean;
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
  const [activeTool, setActiveTool] = useState('pan');

  const tools = [
    { id: 'select', icon: <MousePointer2 size={16} />, label: 'Select' },
    { id: 'pan', icon: <Maximize size={16} />, label: 'Pan' },
    { id: 'zoom', icon: <ZoomIn size={16} />, label: 'Zoom' },
    { id: 'window', icon: <Target size={16} />, label: 'Window' }
  ];

  return (
    <div className="ana-workstation">
      {/* LEFT SIDEBAR - LAYERS & TOOLS */}
      <div className="ana-sidebar ana-sidebar-left">
        <div className="ana-panel">
          <div className="ana-panel-header">
            <Layers size={14} /> LAYERS
          </div>
          <div className="ana-layer-list">
            <label className="ana-layer-item">
              <input type="checkbox" checked={true} readOnly />
              <span>Base Image (MRI)</span>
            </label>
            {overlays.map(overlay => (
              <label key={overlay.id} className="ana-layer-item">
                <input 
                  type="checkbox" 
                  checked={overlay.visible}
                  onChange={() => onToggleOverlay(overlay.id)}
                />
                <span style={{ color: overlay.color }}>{overlay.name}</span>
              </label>
            ))}
          </div>
        </div>

        <div className="ana-panel">
          <div className="ana-panel-header">
            <Search size={14} /> TOOLS
          </div>
          <div className="ana-tool-list">
            {tools.map(t => (
              <button 
                key={t.id} 
                className={`ana-tool-btn ${activeTool === t.id ? 'active' : ''}`}
                onClick={() => setActiveTool(t.id)}
              >
                {t.icon} {t.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* CENTER VIEWER */}
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
            <p>No image available for anatomy workspace.</p>
          </div>
        )}
      </div>

      {/* RIGHT SIDEBAR - FINDINGS */}
      <div className="ana-sidebar ana-sidebar-right">
        <div className="ana-panel">
          <div className="ana-panel-header">
            <Activity size={14} /> FINDINGS
          </div>
          
          <div className="ana-findings-list">
            {overlays.map(o => (
              <div key={o.id} className="ana-finding-item">
                <span className="ana-finding-name">{o.name}</span>
                <span className="ana-finding-status">Detected</span>
              </div>
            ))}
          </div>
        </div>

        <div className="ana-panel">
          <div className="ana-panel-header">
            MEASUREMENTS
          </div>
          
          <div className="ana-measure-controls">
            <label className="ana-layer-item">
              <input 
                type="checkbox" 
                checked={showMeasurements}
                onChange={(e) => onToggleMeasurements(e.target.checked)}
              />
              <span>Meniscus</span>
            </label>
            <label className="ana-layer-item">
              <input 
                type="checkbox" 
                checked={showBoneMeasurements}
                onChange={(e) => onToggleBoneMeasurements(e.target.checked)}
              />
              <span>Bones</span>
            </label>
          </div>

          <div className="ana-measure-summary">
            {boneMeasurement?.femur_width_mm && (
              <div className="ana-summary-item">
                <div className="ana-summary-label">Femur Width</div>
                <div className="ana-summary-val">{boneMeasurement.femur_width_mm.toFixed(1)} mm</div>
              </div>
            )}
            {boneMeasurement?.tibia_width_mm && (
              <div className="ana-summary-item">
                <div className="ana-summary-label">Tibia Width</div>
                <div className="ana-summary-val">{boneMeasurement.tibia_width_mm.toFixed(1)} mm</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

