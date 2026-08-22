import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { CaseOverview } from './CaseOverview';
import { WorkflowState } from '../hooks/useAnalysisWorkflow';

describe('CaseOverview Component', () => {
  const defaultProps: any = {
    workflowState: WorkflowState.IDLE,
    analysisId: null,
    imageMetadata: null,
    previewUrl: null,
    patientData: null,
    segmentationResult: null,
    boneMeasurement: null,
    meniscusMeasurement: null,
    oaResult: null,
    matchingResult: null,
    onNavigate: vi.fn(),
    onUpload: vi.fn(),
    onReset: vi.fn()
  };

  it('renders idle state with upload area', () => {
    render(<CaseOverview {...defaultProps} />);
    
    
  });

  it('renders processing state correctly', () => {
    const props = {
      ...defaultProps,
      workflowState: WorkflowState.SEGMENTING,
      analysisId: 'uuid-1234',
      previewUrl: 'blob:mock',
      imageMetadata: { modality: 'MRI', dimensions: { width: 512, height: 512 } }
    };
    render(<CaseOverview {...props} />);
    
    expect(screen.getAllByText('MRI')[0]).toBeInTheDocument();
    // Pipeline indicators
    expect(screen.getByText('Imaging')).toBeInTheDocument();
  });

  it('shows next action button when ready', () => {
    const props = {
      ...defaultProps,
      workflowState: WorkflowState.BONE_MEASUREMENTS_COMPLETE,
      analysisId: 'uuid-1234',
      previewUrl: 'blob:mock'
    };
    render(<CaseOverview {...props} />);
    const nextBtn = screen.getByRole('button', { name: /Review Anatomy/i });
    expect(nextBtn).toBeInTheDocument();
    fireEvent.click(nextBtn);
    expect(props.onNavigate).toHaveBeenCalledWith('anatomy');
  });

});
