import { render, screen } from '@testing-library/react';
import { describe, test, expect, vi, beforeEach } from 'vitest';
import App from './App';
import * as api from './services/api';

vi.mock('./services/api');

describe('App Component (Integrated Dashboard)', () => {
  beforeEach(() => {
    vi.resetAllMocks();
    vi.mocked(api.getSystemInfo).mockResolvedValue({
      application: "Knee AI Analysis",
      backend: "FastAPI",
      ai_status: "Initialized",
      database_status: "connected",
      implant_database: "Demo-v1",
      environment: "test"
    });
    vi.mocked(api.getFemoralImplants).mockResolvedValue([]);
    vi.mocked(api.getTibialImplants).mockResolvedValue([]);
    vi.mocked(api.matchImplants).mockResolvedValue({
      image_id: "test",
      matching_status: "success",
      data_status: "demo",
      calibration_available: true,
      orientation_status: "unknown",
      femoral_candidates: [],
      tibial_candidates: [],
      warning: "Demo"
    });
  });

  test('renders application titles via TopBar', async () => {
    render(<App />);
    // TopBar shows "Overview" as current title
    expect(screen.getAllByText('Overview').length).toBeGreaterThan(0);
    expect(screen.getByText('RESEARCH PROTOTYPE')).toBeInTheDocument();
  });

  test('renders empty state Case Overview', async () => {
    render(<App />);
    
    // Check CaseOverview empty state
    expect(screen.getByText('NO ACTIVE CASE')).toBeInTheDocument();
    expect(screen.getByText(/Upload a DICOM, PNG, or JPEG study/i)).toBeInTheDocument();
  });

  test('renders navigation Sidebar', async () => {
    render(<App />);
    
    // Check sidebar links
    expect(screen.getByText('CASE')).toBeInTheDocument();
    expect(screen.getByText('ANATOMY')).toBeInTheDocument();
    
    // Initial state should have disabled analysis links
    const anatomyBtn = screen.getByRole('button', { name: 'Anatomy' });
    expect(anatomyBtn).toBeDisabled();
  });
});
