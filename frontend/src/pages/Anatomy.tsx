import React, { useState } from 'react';
import type { CaseImage } from '../types/case';
import { MedicalImageViewer } from '../components/MedicalImageViewer';
import { Eye, EyeOff, MousePointer2, Move, ZoomIn, Contrast, RefreshCcw } from 'lucide-react';
import { Button } from '../components/ui/Button';
import './Anatomy.css';

interface AnatomyProps {
  images: CaseImage[];
  activeImageId: string | null;
  setActiveImageId: (id: string) => void;
  onBack: () => void;
  onNext: () => void;
  onProcessImage: (id: string) => void;
}

export const Anatomy: React.FC<AnatomyProps> = ({ images, activeImageId, setActiveImageId, onBack, onNext, onProcessImage }) => {
  const [activeTool, setActiveTool] = useState('pan');
  const [showMeasurements, setShowMeasurements] = useState(true);
  const [showBoneMeasurements, setShowBoneMeasurements] = useState(true);

  const activeImage = images.find(img => img.id === activeImageId);

  const getMaskUrl = (id: string, structure: string) =>
    `http://localhost:8000/api/v1/segmentation/${id}/mask/${structure}`;

  const renderLeftPanel = () => (
    <div className="ana-left-panel">
      <h3 className="ana-panel-title">Studies</h3>
      <div className="ana-study-list">
        {images.map(img => (
          <div
            key={img.id}
            className={`ana-study-item ${activeImageId === img.id ? 'active' : ''}`}
            onClick={() => setActiveImageId(img.id)}
          >
            <div className="ana-study-thumb">
              {img.previewUrl
                ? <img src={img.previewUrl} alt="" />
                : <span style={{ fontSize: 10, color: 'var(--color-text-muted)' }}>{img.metadata?.modality || '?'}</span>
              }
            </div>
            <div className="ana-study-info">
              <span className="ana-study-modality">{img.metadata?.modality || 'UNKNOWN'}</span>
              <span className="ana-study-filename" title={img.file?.name}>{img.file?.name || 'Image'}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderCenterPanel = () => {
    if (!activeImage) {
      return (
        <div className="ana-center-panel empty">
          <p style={{ color: 'var(--color-text-secondary)', fontSize: '14px' }}>Select an image from the Studies panel</p>
        </div>
      );
    }

    if (activeImage.status === 'FAILED') {
      return (
        <div className="ana-center-panel empty">
          <p style={{ color: 'var(--color-danger)', fontSize: '14px' }}>[!] Image processing failed. Remove and re-upload.</p>
        </div>
      );
    }

    const overlays: { id: string; url: string; visible: boolean; name: string; color: string }[] = [];

    if (activeImage.segmentation?.structures.femur?.detected) {
      overlays.push({ id: 'femur', url: getMaskUrl(activeImage.id, 'femur'), visible: true, name: 'Femur', color: '#3b82f6' });
    }
    if (activeImage.segmentation?.structures.tibia?.detected) {
      overlays.push({ id: 'tibia', url: getMaskUrl(activeImage.id, 'tibia'), visible: true, name: 'Tibia', color: '#10b981' });
    }
    if (activeImage.metadata?.modality === 'MRI' && activeImage.segmentation?.structures.medial_meniscus?.detected) {
      overlays.push({ id: 'meniscus', url: getMaskUrl(activeImage.id, 'medial_meniscus'), visible: true, name: 'Meniscus', color: '#f59e0b' });
    }

    const mList = activeImage.measurements.meniscus?.locations || [];
    const boneRes = activeImage.measurements.bones;

    return (
      <div className="ana-center-panel">
        <div className="ana-toolbar">
          <div className="ana-tools">
            <button className={`ana-tool-btn ${activeTool === 'pan' ? 'active' : ''}`} onClick={() => setActiveTool('pan')} title="Pan">
              <Move size={18} />
            </button>
            <button className={`ana-tool-btn ${activeTool === 'zoom' ? 'active' : ''}`} onClick={() => setActiveTool('zoom')} title="Zoom">
              <ZoomIn size={18} />
            </button>
            <button className={`ana-tool-btn ${activeTool === 'select' ? 'active' : ''}`} onClick={() => setActiveTool('select')} title="Select">
              <MousePointer2 size={18} />
            </button>
            <button className={`ana-tool-btn ${activeTool === 'window' ? 'active' : ''}`} onClick={() => setActiveTool('window')} title="Window/Level">
              <Contrast size={18} />
            </button>
            <div className="ana-tool-separator" />
            <button className="ana-tool-btn" onClick={() => { setActiveTool('reset_trigger'); setTimeout(() => setActiveTool('pan'), 50); }} title="Reset View">
              <RefreshCcw size={18} />
            </button>
          </div>
        </div>

        <div className="ana-viewer-container">
          <MedicalImageViewer
            imageUrl={activeImage.previewUrl!}
            overlays={overlays}
            measurements={showMeasurements ? mList : []}
            boneResult={showBoneMeasurements ? (boneRes || undefined) : undefined}
            activeTool={activeTool}
          />
        </div>

        {!activeImage.segmentation && (
          <div className="ana-analyze-prompt">
              <p>{activeImage.status === "PROCESSING" ? "Processing Anatomy..." : "No segmentation yet for this image."}</p>
              <Button onClick={() => onProcessImage(activeImage.id)} variant="primary" disabled={activeImage.status === "PROCESSING"}>
                {activeImage.status === "PROCESSING" ? "Analyzing..." : "Analyze This Image"}
              </Button>
            </div>
        )}
      </div>
    );
  };

  const renderRightPanel = () => {
    if (!activeImage) return <div className="ana-right-panel" />;

    const modality = activeImage.metadata?.modality || 'UNKNOWN';
    const seg = activeImage.segmentation;
    const boneRes = activeImage.measurements.bones;

    return (
      <div className="ana-right-panel">
        <h3 className="ana-panel-title">Findings</h3>

        <div className="ana-findings-list">
          <div className="ana-finding-item">
            <h4>Tibia</h4>
            <div className="ana-finding-val">
              {seg ? (seg.structures.tibia?.detected ? "Detected" : "Not Detected") : "Pending analysis"}
            </div>
            {boneRes?.tibia && (
              <div style={{ marginTop: 4, fontSize: 12, color: "var(--shell-text)" }}>
                {boneRes.tibia.width_mm != null 
                  ? `${boneRes.tibia.width_mm.toFixed(1)} mm`
                  : `${boneRes.tibia.width_pixels.toFixed(1)} px (Uncalibrated)`}
              </div>
            )}
          </div>
          {modality === "MRI" ? (
            <div className="ana-finding-item">
              <h4>Medial Meniscus</h4>
              <div className="ana-finding-val">
                {seg ? (seg.structures.medial_meniscus?.detected ? "Detected" : "Not Detected") : "Pending analysis"}
              </div>
              {activeImage.measurements.meniscus && (
                <div style={{ marginTop: 4, fontSize: 12, color: "var(--shell-text)" }}>
                  {activeImage.measurements.meniscus.mean_thickness_mm != null 
                    ? `${activeImage.measurements.meniscus.mean_thickness_mm.toFixed(2)} mm`
                    : `${activeImage.measurements.meniscus.mean_thickness_pixels.toFixed(1)} px (Uncalibrated)`}
                </div>
              )}
            </div>
          ) : (
            <div className="ana-finding-item disabled">
              <h4>Medial Meniscus</h4>
              <div className="ana-finding-val">Not Applicable (X-Ray)</div>
            </div>
          )}
        </div>

        <h3 className="ana-panel-title" style={{ marginTop: 8 }}>Visibility</h3>
        <div className="ana-layer-list">
          <div className="ana-layer-item" onClick={() => setShowBoneMeasurements(v => !v)}>
            <button className="ana-layer-toggle">
              {showBoneMeasurements
                ? <Eye size={16} style={{ color: 'var(--color-success)' }} />
                : <EyeOff size={16} style={{ color: 'var(--color-text-muted)' }} />
              }
            </button>
            <span>Bone Measurements</span>
          </div>
          {modality === 'MRI' && (
            <div className="ana-layer-item" onClick={() => setShowMeasurements(v => !v)}>
              <button className="ana-layer-toggle">
                {showMeasurements
                  ? <Eye size={16} style={{ color: 'var(--color-success)' }} />
                  : <EyeOff size={16} style={{ color: 'var(--color-text-muted)' }} />
                }
              </button>
              <span>Meniscus Measurements</span>
            </div>
          )}
        </div>
      </div>
    );
  };

  const isValid = images.length > 0 && images.some(img => img.segmentation !== null);

  return (
    <div className="ana-container fade-in">
      <div className="ana-layout">
        {renderLeftPanel()}
        {renderCenterPanel()}
        {renderRightPanel()}
      </div>
      <div className="ana-actions">
        <Button variant="ghost" onClick={onBack}>&larr; Back to Imaging</Button>
        <Button variant="primary" onClick={onNext} disabled={!isValid}>
          Continue to Analysis &rarr;
        </Button>
      </div>
    </div>
  );
};








