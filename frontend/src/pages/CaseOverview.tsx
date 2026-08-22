import React, { useRef } from 'react';
import { WorkflowState } from '../hooks/useAnalysisWorkflow';
import { Button } from '../components/ui/Button';
import './CaseOverview.css';

interface CaseOverviewProps {
  workflowState: string;
  analysisId: string | null;
  imageMetadata: any;
  previewUrl: string | null;
  onNavigate: (route: string) => void;
  onUpload: (file: File) => void;
  onReset?: () => void;
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
      { id: 'image', label: 'Imaging', state: isIdle ? 'Waiting' : 'Complete', active: !isIdle },
      { id: 'anatomy', label: 'Anatomy', state: isSegDone || isOADone ? 'Complete' : (isReady ? 'Running' : 'Waiting'), active: isSegDone },
      { id: 'analysis', label: 'Analysis', state: isOADone ? 'Complete' : (isSegDone ? 'Ready' : 'Waiting'), active: isOADone },
      { id: 'planning', label: 'Planning', state: isMatchDone ? 'Complete' : (isOADone ? 'Ready' : 'Waiting'), active: isMatchDone }
    ];
  };

  const pipeline = getPipelineStatus();

  return (
    <div className="co-page">
      {workflowState === WorkflowState.IDLE ? (
        <div className="co-intake-workspace">
          <div className="co-intake-header">
            <h1 className="co-title">CASE OVERVIEW</h1>
            <p className="co-subtitle">Start a new imaging analysis</p>
          </div>
          <div className="co-dropzone" onClick={() => fileInputRef.current?.click()}>
            <div className="co-drop-title">Upload a knee MRI study to begin.</div>
            <div className="co-drop-subtitle">Drop DICOM / image here or Browse files</div>
            <div className="co-drop-meta">Supported: DICOM &bull; PNG &bull; JPG &bull; JPEG</div>
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
          <div className="co-header">
            <h1 className="co-title">Case Overview</h1>
            <div className="co-header-meta">
              <span className="mono">{analysisId?.split('-')[0].toUpperCase()}</span>
              <span>&bull;</span>
              <span>{imageMetadata?.modality || 'MRI'}</span>
            </div>
            {onReset && (
              <Button variant="ghost" className="co-reset-btn" onClick={onReset}>
                Reset / New Case
              </Button>
            )}
          </div>
          
          <div className="co-grid">
            <div className="co-col">
              <div className="co-image-preview">
                {previewUrl ? <img src={previewUrl} alt="MRI" /> : <div className="co-placeholder">Image Unavailable</div>}
              </div>
            </div>

            <div className="co-col">
              <div className="co-panel">
                <h3 className="co-panel-title">Case Information</h3>
                <div className="co-info-grid">
                  <div className="co-info-item">
                    <span className="co-info-label">Modality</span>
                    <span className="co-info-val">{imageMetadata?.modality || 'Unavailable'}</span>
                  </div>
                  <div className="co-info-item">
                    <span className="co-info-label">Dimensions</span>
                    <span className="co-info-val">{imageMetadata?.dimensions ? `${imageMetadata.dimensions.width} × ${imageMetadata.dimensions.height}` : 'Unavailable'}</span>
                  </div>
                  <div className="co-info-item">
                    <span className="co-info-label">Pixel Spacing</span>
                    <span className="co-info-val">{imageMetadata?.pixel_spacing ? `${imageMetadata.pixel_spacing[0].toFixed(3)} / ${imageMetadata.pixel_spacing[1].toFixed(3)} mm` : 'Unavailable'}</span>
                  </div>
                  <div className="co-info-item">
                    <span className="co-info-label">Calibration</span>
                    <span className="co-info-val">{imageMetadata?.pixel_spacing ? 'Available' : 'Unavailable'}</span>
                  </div>
                </div>
              </div>

              <div className="co-panel mt-6">
                <h3 className="co-panel-title">Analysis Pipeline</h3>
                <div className="co-pipeline-list">
                  {pipeline.map((step, idx) => (
                    <div key={step.id} className={`co-pipe-item ${step.active ? 'active' : ''}`}>
                      <div className="co-pipe-num">{String(idx + 1).padStart(2, '0')}</div>
                      <div className="co-pipe-name">{step.label}</div>
                      <div className={`co-pipe-state ${step.state.toLowerCase().replace(' ', '-')}`}>
                        {step.state}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="co-next-action mt-6">
                <Button variant="primary" onClick={() => onNavigate('anatomy')}>
                  Review Anatomy →
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
