import React from 'react';
import { WorkflowState } from '../hooks/useAnalysisWorkflow';
import { Button } from '../components/ui/Button';
import './CaseOverview.css';

interface CaseOverviewProps {
  workflowState: WorkflowState;
  analysisId: string | null;
  imageMetadata: any;
  previewUrl: string | null;
  patientData: any;
  segmentationResult: any;
  boneMeasurement: any;
  meniscusMeasurement: any;
  oaResult: any;
  matchingResult: any;
  onNavigate: (route: any) => void;
  onUpload: (file: File) => void;
  onReset: () => void;
}

export const CaseOverview: React.FC<CaseOverviewProps> = ({
  workflowState,
  analysisId,
  imageMetadata,
  previewUrl,
  boneMeasurement,
  onNavigate,
  onUpload,
}) => {
  const isIdle = workflowState === WorkflowState.IDLE;
  
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  };

  const stateOrder = Object.values(WorkflowState);
  const currentIndex = stateOrder.indexOf(workflowState);
  const getIndex = (key: string) => stateOrder.indexOf(WorkflowState[key as keyof typeof WorkflowState]);

  const getProcessingSteps = () => {
    return [
      { id: 'img', label: 'Image Intake', state: currentIndex > getIndex('IDLE') ? 'COMPLETE' : 'READY' },
      { id: 'pre', label: 'Preprocessing', state: currentIndex >= getIndex('READY_FOR_SEGMENTATION') ? 'COMPLETE' : (workflowState === WorkflowState.PREPROCESSING ? 'RUNNING' : 'LOCKED') },
      { id: 'seg', label: 'Anatomical Segmentation', state: currentIndex >= getIndex('SEGMENTATION_COMPLETE') ? 'COMPLETE' : (workflowState === WorkflowState.SEGMENTING ? 'RUNNING' : 'LOCKED') },
      { id: 'meas', label: 'Geometric Measurements', state: currentIndex >= getIndex('BONE_MEASUREMENTS_COMPLETE') ? 'COMPLETE' : ((workflowState === WorkflowState.MEASURING_MENISCUS || workflowState === WorkflowState.MEASURING_BONES) ? 'RUNNING' : 'LOCKED') },
    ];
  };

  const isReady = currentIndex >= getIndex('BONE_MEASUREMENTS_COMPLETE');

  if (isIdle) {
    return (
      <div className="co-page">
        <div className="co-header">
          <div className="co-breadcrumb">Analysis / Overview</div>
          <h1 className="co-title">CASE OVERVIEW</h1>
          <p className="co-subtitle">Medical image case intake and analysis readiness.</p>
        </div>

        <div className="co-empty-state">
          <div className="co-empty-left">
            <div className="co-abstract-art">
              <svg viewBox="0 0 100 100" className="co-abstract-svg">
                <circle cx="50" cy="50" r="40" stroke="var(--light-border-strong)" strokeWidth="1" fill="none" opacity="0.5"/>
                <path d="M50 10 L50 90 M10 50 L90 50" stroke="var(--light-border-strong)" strokeWidth="1" opacity="0.3"/>
                <circle cx="50" cy="50" r="2" fill="var(--color-primary)"/>
              </svg>
            </div>
          </div>
          <div className="co-empty-right">
            <h2 className="co-empty-title">NO ACTIVE CASE</h2>
            <p className="co-empty-desc">Start a new knee imaging analysis.<br/>Upload a DICOM, PNG, or JPEG study to begin.</p>
            
            <div className="co-upload-panel">
              <div className="co-upload-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="17 8 12 3 7 8"></polyline>
                  <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
              </div>
              <h3 className="co-upload-title">Upload Medical Image</h3>
              <p className="co-upload-text">Drag and drop your study here or</p>
              
              <div className="co-upload-action">
                <input 
                  type="file" 
                  id="file-upload" 
                  className="co-file-input" 
                  accept=".dcm,.png,.jpg,.jpeg"
                  onChange={handleFileChange}
                />
                <label htmlFor="file-upload" className="co-btn-primary">Browse Files</label>
              </div>
              
              <div className="co-upload-footer">
                Supported: DICOM • PNG • JPEG<br/>
                Maximum: 10 MB
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="co-page">
      <div className="co-header">
        <div className="co-breadcrumb">Analysis / Overview</div>
        <h1 className="co-title">CASE OVERVIEW</h1>
        <p className="co-subtitle">Review the uploaded study and analysis readiness.</p>
      </div>

      <div className="co-summary-bar">
        <div className="co-summary-item">
          <div className="co-summary-label">IMAGE</div>
          <div className="co-summary-val">{imageMetadata?.modality || 'MRI'}</div>
        </div>
        <div className="co-summary-item">
          <div className="co-summary-label">DIMENSIONS</div>
          <div className="co-summary-val">{imageMetadata?.dimensions ? `${imageMetadata.dimensions.width} × ${imageMetadata.dimensions.height}` : '512 × 512'}</div>
        </div>
        <div className="co-summary-item">
          <div className="co-summary-label">CALIBRATION</div>
          <div className="co-summary-val">{boneMeasurement?.calibration_available ? 'Available' : 'Pending'}</div>
        </div>
        <div className="co-summary-item">
          <div className="co-summary-label">CASE ID</div>
          <div className="co-summary-val">{analysisId ? analysisId.split('-')[0].toUpperCase() : '---'}</div>
        </div>
      </div>

      <div className="co-main-grid">
        <div className="co-preview-col">
          <div className="co-image-preview">
            {previewUrl ? (
              <>
                <img src={previewUrl} alt="Medical Preview" className="co-preview-img" />
                <div className="co-preview-overlay">
                  <div>{imageMetadata?.modality || 'MRI'} • {imageMetadata?.dimensions ? `${imageMetadata.dimensions.width}x${imageMetadata.dimensions.height}` : ''}</div>
                  <div>DICOM</div>
                </div>
              </>
            ) : (
              <div className="co-preview-placeholder">Loading image...</div>
            )}
          </div>
        </div>
        
        <div className="co-readiness-col">
          <div className="co-card">
            <h3 className="co-card-title">ANALYSIS PIPELINE</h3>
            <div className="co-pipeline">
              {getProcessingSteps().map((step, idx) => (
                <div key={step.id} className="co-pipeline-step">
                  <div className={`co-step-indicator co-step-${step.state.toLowerCase()}`}>
                    {step.state === 'COMPLETE' && '●'}
                    {step.state === 'RUNNING' && '●'}
                    {step.state === 'READY' && '●'}
                    {step.state === 'LOCKED' && '○'}
                  </div>
                  <div className="co-step-content">
                    <div className="co-step-num">0{idx + 1}</div>
                    <div className="co-step-label">{step.label}</div>
                  </div>
                  <div className={`co-step-status text-${step.state.toLowerCase()}`}>{step.state}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="co-next-action">
            <h3 className="co-action-title">NEXT STEP</h3>
            {isReady ? (
              <>
                <p className="co-action-desc">Review anatomical segmentation and measurements.</p>
                <Button variant="primary" onClick={() => onNavigate('anatomy')}>Open Anatomy Workspace</Button>
              </>
            ) : (
              <p className="co-action-desc">Processing anatomical structures. Please wait...</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

