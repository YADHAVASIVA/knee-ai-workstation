import React, { useRef, useState, useEffect } from 'react';
import './MedicalImageViewer.css';
import type { MeasurementLocation } from '../services/api';
import { Button } from './ui/Button';

interface Overlay {
  id: string;
  url: string;
  name: string;
  visible: boolean;
  color: string;
}

interface MedicalImageViewerProps {
  imageUrl: string;
  overlays?: Overlay[];
  measurements?: MeasurementLocation[];
  boneResult?: any;
  onToggleOverlay?: (id: string) => void;
  onToggleAll?: (show: boolean) => void;
  showMeasurements?: boolean;
  onToggleMeasurements?: (show: boolean) => void;
  showBoneMeasurements?: boolean;
  onToggleBoneMeasurements?: (show: boolean) => void;
}

export const MedicalImageViewer: React.FC<MedicalImageViewerProps> = ({ 
  imageUrl, 
  overlays = [],
  measurements = [],
  boneResult,
  showMeasurements = true,
  showBoneMeasurements = true,
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [lastPos, setLastPos] = useState({ x: 0, y: 0 });
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [opacity, setOpacity] = useState(0.7);

  // Wheel zoom
  const handleWheel = (e: React.WheelEvent) => {
    e.preventDefault();
    const zoomSensitivity = 0.001;
    const delta = -e.deltaY * zoomSensitivity;
    setScale(prev => Math.min(Math.max(prev + delta, 0.25), 4));
  };

  // Pointer panning
  const handlePointerDown = (e: React.PointerEvent) => {
    setIsDragging(true);
    setLastPos({ x: e.clientX, y: e.clientY });
    e.currentTarget.setPointerCapture(e.pointerId);
  };

  const handlePointerMove = (e: React.PointerEvent) => {
    if (!isDragging) return;
    const dx = e.clientX - lastPos.x;
    const dy = e.clientY - lastPos.y;
    setPan(prev => ({ x: prev.x + dx, y: prev.y + dy }));
    setLastPos({ x: e.clientX, y: e.clientY });
  };

  const handlePointerUp = (e: React.PointerEvent) => {
    setIsDragging(false);
    e.currentTarget.releasePointerCapture(e.pointerId);
  };

  const handleZoomIn = () => setScale(prev => Math.min(prev + 0.25, 4));
  const handleZoomOut = () => setScale(prev => Math.max(prev - 0.25, 0.25));
  const handleReset = () => {
    setScale(1);
    setPan({ x: 0, y: 0 });
  };

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      containerRef.current?.requestFullscreen().catch(err => {
        console.error("Error attempting to enable fullscreen:", err);
      });
    } else {
      document.exitFullscreen();
    }
  };

  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };
    document.addEventListener('fullscreenchange', handleFullscreenChange);
    return () => document.removeEventListener('fullscreenchange', handleFullscreenChange);
  }, []);

  return (
    <div className={`miv-wrapper ${isFullscreen ? 'fullscreen' : ''}`} ref={containerRef}>
      <div className="miv-toolbar">
        <div className="miv-toolbar-group">
          <Button variant="secondary" onClick={handleReset} size="sm">Fit</Button>
          <Button variant="secondary" onClick={handleZoomOut} size="sm">−</Button>
          <span className="miv-zoom-level">{Math.round(scale * 100)}%</span>
          <Button variant="secondary" onClick={handleZoomIn} size="sm">+</Button>
          <Button variant="secondary" onClick={handleReset} size="sm">Reset</Button>
        </div>
        <div className="miv-toolbar-group">
          <div className="miv-opacity-control">
            <label>Opacity</label>
            <input 
              type="range" min="0" max="1" step="0.1" 
              value={opacity} 
              onChange={(e) => setOpacity(parseFloat(e.target.value))} 
            />
          </div>
          <Button variant="ghost" onClick={toggleFullscreen} size="sm">⛶</Button>
        </div>
      </div>

      <div className="miv-workspace">
        {/* VIEWPORT */}
        <div 
          className="miv-viewport"
          onWheel={handleWheel}
          onPointerDown={handlePointerDown}
          onPointerMove={handlePointerMove}
          onPointerUp={handlePointerUp}
          onPointerCancel={handlePointerUp}
        >
          <div 
            className="miv-canvas"
            style={{
              transform: `translate(${pan.x}px, ${pan.y}px) scale(${scale})`
            }}
          >
            <img src={imageUrl} alt="Medical Image" className="miv-base-image" draggable={false} />
            
            {overlays.map(overlay => (
              <img
                key={overlay.id}
                src={overlay.url}
                alt={overlay.name}
                className={`miv-overlay-image ${overlay.visible ? 'visible' : 'hidden'}`}
                style={{ opacity: opacity }}
                draggable={false}
              />
            ))}

            {showMeasurements && measurements.map(m => (
              <div 
                key={m.name} 
                className="miv-measurement-marker"
                style={{ 
                  left: `${m.x}px`, 
                  top: `${m.y - (m.thickness_pixels / 2)}px`,
                  height: `${m.thickness_pixels}px`
                }}
              >
                <div className="miv-line"></div>
                <div className="miv-label">
                  {m.thickness_mm !== null ? `${m.thickness_mm.toFixed(1)} mm` : `${m.thickness_pixels.toFixed(1)} px`}
                </div>
              </div>
            ))}

            {showBoneMeasurements && boneResult && (
              <>
                {boneResult.femur && (
                  <div className="miv-bone-line width-line" style={{
                    left: `${boneResult.femur.width_line.start_x}px`,
                    top: `${boneResult.femur.width_line.start_y}px`,
                    width: `${boneResult.femur.width_pixels}px`
                  }}>
                    <div className="miv-label">F: {boneResult.femur.width_mm ? `${boneResult.femur.width_mm.toFixed(1)}mm` : `${boneResult.femur.width_pixels.toFixed(1)}px`}</div>
                  </div>
                )}
                {boneResult.femur && (
                  <div className="miv-bone-line ap-line" style={{
                    left: `${boneResult.femur.ap_line.start_x}px`,
                    top: `${boneResult.femur.ap_line.start_y}px`,
                    height: `${boneResult.femur.ap_dimension_pixels}px`
                  }} />
                )}
                {boneResult.tibia && (
                  <div className="miv-bone-line width-line" style={{
                    left: `${boneResult.tibia.width_line.start_x}px`,
                    top: `${boneResult.tibia.width_line.start_y}px`,
                    width: `${boneResult.tibia.width_pixels}px`
                  }}>
                    <div className="miv-label">T: {boneResult.tibia.width_mm ? `${boneResult.tibia.width_mm.toFixed(1)}mm` : `${boneResult.tibia.width_pixels.toFixed(1)}px`}</div>
                  </div>
                )}
                {boneResult.tibia && (
                  <div className="miv-bone-line ap-line" style={{
                    left: `${boneResult.tibia.ap_line.start_x}px`,
                    top: `${boneResult.tibia.ap_line.start_y}px`,
                    height: `${boneResult.tibia.ap_dimension_pixels}px`
                  }} />
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
