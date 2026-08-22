import os

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

write_file('frontend/src/components/shell/Sidebar.tsx', '''
import React from 'react';
import './shell.css';

interface SidebarProps {
  activeRoute: string;
  onNavigate: (route: string) => void;
  analysisId: string | null;
  routes: Array<{ id: string; label: string; category: string; disabled?: boolean }>;
  imageMetadata?: any;
  isCalibrated?: boolean | null;
}

export const Sidebar: React.FC<SidebarProps> = ({ 
  activeRoute, 
  onNavigate, 
  analysisId,
  routes,
  imageMetadata,
  isCalibrated
}) => {
  const sections = routes.reduce((acc, route) => {
    if (!acc[route.category]) acc[route.category] = [];
    acc[route.category].push(route);
    return acc;
  }, {} as Record<string, typeof routes>);

  return (
    <aside className="app-sidebar">
      <div className="sidebar-brand">
        <div className="brand-logo-area">
          <div className="brand-text">
            <span className="brand-title">KNEE AI</span>
          </div>
        </div>
        <div className="brand-subtitle">Imaging Workstation</div>
      </div>

      <nav className="sidebar-nav">
        {Object.entries(sections).map(([category, items]) => (
          <div key={category} className="nav-section">
            <h3 className="nav-section-title">{category}</h3>
            <ul className="nav-list">
              {items.map(item => (
                <li key={item.id}>
                  <button
                    className={
av-btn }
                    onClick={() => onNavigate(item.id)}
                    disabled={item.disabled}
                  >
                    <span className="nav-label">{item.label}</span>
                  </button>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </nav>

      {analysisId && (
        <div className="sidebar-case-context">
          <div className="case-context-title">CURRENT CASE</div>
          <div className="case-context-id">{analysisId.split('-')[0].toUpperCase()}</div>
          <div className="case-context-meta">
            {imageMetadata?.modality || 'MRI'} &bull; {imageMetadata?.dimensions ? ${imageMetadata.dimensions.width} x  : '512 x 512'}
          </div>
          {isCalibrated && (
            <div className="case-context-meta case-calibrated-dot">
              &bull; Calibrated
            </div>
          )}
        </div>
      )}
    </aside>
  );
};
''')

write_file('frontend/src/components/shell/TopBar.tsx', '''
import React from 'react';
import { StatusBadge } from '../ui/StatusBadge';
import './shell.css';

interface TopBarProps {
  activeRoute: string;
  analysisId: string | null;
  isDemo: boolean;
  isCalibrated: boolean | null;
  imageMetadata?: any;
}

export const TopBar: React.FC<TopBarProps> = ({ 
  activeRoute, 
  analysisId,
  isDemo,
  isCalibrated,
  imageMetadata
}) => {
  const getContextName = () => {
    switch(activeRoute) {
      case 'overview': return 'Overview';
      case 'anatomy': return 'Anatomy';
      case 'analysis': return 'OA Analysis';
      case 'planning': return 'Implant Planning';
      case 'report': return 'Report';
      default: return '';
    }
  };

  return (
    <header className="app-topbar">
      <div className="topbar-left">
        <div className="topbar-brand-inline">KNEE AI</div>
        <div className="topbar-breadcrumb">
          Case <span className="breadcrumb-slash">/</span> {getContextName()}
        </div>
      </div>
      
      <div className="topbar-right">
        {analysisId && (
          <div className="topbar-case-id">{analysisId.split('-')[0].toUpperCase()}</div>
        )}
        {imageMetadata?.modality && (
          <div className="topbar-meta-item">
            <div className="topbar-meta-dot"></div>
            {imageMetadata.modality}
          </div>
        )}
        {isCalibrated !== null && (
          <div className={	opbar-meta-item }>
            <div className="topbar-meta-dot"></div>
            {isCalibrated ? 'Calibrated' : 'Uncalibrated'}
          </div>
        )}
        {isDemo && (
          <StatusBadge status="DEMO" label="DEMO" />
        )}
      </div>
    </header>
  );
};
''')

write_file('frontend/src/pages/Anatomy.tsx', '''
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
                className={na-tool-btn }
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
            boneMeasurement={showBoneMeasurements ? boneMeasurement : null}
            mode={activeTool as any}
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
''')

write_file('frontend/src/pages/CaseOverview.tsx', '''
import React, { useRef } from 'react';
import { Upload, FileImage, ClipboardList, Activity } from 'lucide-react';
import { WorkflowState } from '../hooks/useAnalysisWorkflow';
import { Button } from '../components/ui/Button';
import './CaseOverview.css';

interface CaseOverviewProps {
  workflowState: string;
  analysisId: string | null;
  imageMetadata: any;
  previewUrl: string | null;
  patientData: any;
  segmentationResult: any;
  boneMeasurement: any;
  meniscusMeasurement: any;
  oaResult: any;
  matchingResult: any;
  onNavigate: (route: string) => void;
  onUpload: (file: File) => void;
  onReset: () => void;
}

export const CaseOverview: React.FC<CaseOverviewProps> = ({
  workflowState,
  analysisId,
  imageMetadata,
  previewUrl,
  onNavigate,
  onUpload,
  onReset
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onUpload(e.target.files[0]);
    }
  };

  const getPipelineStatus = () => {
    const isIdle = workflowState === WorkflowState.IDLE;
    const isReady = workflowState === WorkflowState.READY_FOR_SEGMENTATION || workflowState === WorkflowState.SEGMENTING;
    const isSegDone = workflowState === WorkflowState.SEGMENTATION_COMPLETE || workflowState === WorkflowState.MEASURING_MENISCUS || workflowState === WorkflowState.MEASURING_BONES || workflowState === WorkflowState.BONE_MEASUREMENTS_COMPLETE;
    const isOADone = workflowState === WorkflowState.OA_ANALYSIS_COMPLETE || workflowState === WorkflowState.MATCHING || workflowState === WorkflowState.MATCHING_COMPLETE;
    const isMatchDone = workflowState === WorkflowState.MATCHING_COMPLETE;

    return [
      { id: 'image', label: 'Imaging', state: isIdle ? 'Not started' : 'Complete', active: !isIdle },
      { id: 'anatomy', label: 'Anatomy', state: isSegDone || isOADone ? 'Complete' : (isReady ? 'Running' : 'Waiting'), active: isSegDone },
      { id: 'analysis', label: 'Analysis', state: isOADone ? 'Complete' : (isSegDone ? 'Ready' : 'Waiting'), active: isOADone },
      { id: 'planning', label: 'Planning', state: isMatchDone ? 'Complete' : (isOADone ? 'Ready' : 'Waiting'), active: isMatchDone }
    ];
  };

  const pipeline = getPipelineStatus();

  return (
    <div className="co-page">
      <div className="co-header">
        <h1 className="co-title">CASE OVERVIEW</h1>
        <p className="co-subtitle">MRI Knee Analysis Workspace</p>
      </div>

      {workflowState === WorkflowState.IDLE ? (
        <div className="co-intake-workspace">
          <div className="co-dropzone" onClick={() => fileInputRef.current?.click()}>
            <Upload className="co-drop-icon" size={48} />
            <div className="co-drop-title">Drop medical image here</div>
            <div className="co-drop-subtitle">or click to browse from your computer</div>
            <div className="co-drop-meta">DICOM &middot; PNG &middot; JPG &middot; JPEG</div>
            <input 
              type="file" 
              ref={fileInputRef} 
              style={{ display: 'none' }} 
              accept=".dcm,.png,.jpg,.jpeg"
              onChange={handleFileChange}
            />
          </div>
        </div>
      ) : (
        <div className="co-dashboard">
          <div className="co-grid">
            {/* Left Column */}
            <div className="co-col">
              <div className="co-panel">
                <h3 className="co-panel-title">IMAGE</h3>
                <div className="co-image-preview">
                  {previewUrl ? <img src={previewUrl} alt="MRI" /> : <div className="co-placeholder"><FileImage /></div>}
                </div>
                <div className="co-meta-grid">
                  <div className="co-meta-item">
                    <span className="co-meta-label">MODALITY</span>
                    <span className="co-meta-val">{imageMetadata?.modality || 'MRI'}</span>
                  </div>
                  <div className="co-meta-item">
                    <span className="co-meta-label">RESOLUTION</span>
                    <span className="co-meta-val">{imageMetadata?.dimensions ? ${imageMetadata.dimensions.width} x  : '512 x 512'}</span>
                  </div>
                  <div className="co-meta-item">
                    <span className="co-meta-label">FORMAT</span>
                    <span className="co-meta-val">DICOM</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Column */}
            <div className="co-col">
              <div className="co-panel">
                <h3 className="co-panel-title">CASE INFORMATION</h3>
                <div className="co-info-box">
                  <div className="co-info-row">
                    <span className="co-info-label">Case ID</span>
                    <span className="co-info-val mono">{analysisId?.split('-')[0].toUpperCase()}</span>
                  </div>
                  <div className="co-info-row">
                    <span className="co-info-label">Modality</span>
                    <span className="co-info-val">{imageMetadata?.modality || 'MRI'}</span>
                  </div>
                  <div className="co-info-row">
                    <span className="co-info-label">Calibration</span>
                    <span className="co-info-val success">&bull; Available</span>
                  </div>
                </div>
              </div>

              <div className="co-panel">
                <h3 className="co-panel-title">ANALYSIS PIPELINE</h3>
                <div className="co-pipeline-list">
                  {pipeline.map((step, idx) => (
                    <div key={step.id} className={co-pipe-item }>
                      <div className="co-pipe-num">{String(idx + 1).padStart(2, '0')}</div>
                      <div className="co-pipe-name">{step.label}</div>
                      <div className={co-pipe-state }>
                        {step.state === 'Complete' && '✓'}
                        {step.state === 'Running' && '○'}
                        {step.state === 'Waiting' && '○'}
                        {step.state === 'Not started' && '○'}
                        {step.state === 'Ready' && '○'}
                        {' '}{step.state}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="co-next-action">
                <div className="co-action-text">
                  <h4>Next Action</h4>
                  <p>Review detected anatomical structures and measurements.</p>
                </div>
                <Button variant="primary" onClick={() => onNavigate('anatomy')}>
                  Continue to Anatomy &rarr;
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
''')
