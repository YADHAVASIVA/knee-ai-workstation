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
  patientData,
  segmentationResult,
  boneMeasurement,
  meniscusMeasurement,
  oaResult,
  matchingResult,
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
                    <span className="co-meta-val">{imageMetadata?.dimensions ? `${imageMetadata.dimensions.width} × ${imageMetadata.dimensions.height}` : '512 × 512'}</span>
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
                    <div key={step.id} className={`co-pipe-item ${step.active ? 'active' : ''}`}>
                      <div className="co-pipe-num">{String(idx + 1).padStart(2, '0')}</div>
                      <div className="co-pipe-name">{step.label}</div>
                      <div className={`co-pipe-state ${step.state.toLowerCase().replace(' ', '-')}`}>
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

