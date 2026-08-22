import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { ImplantDatabasePanel } from './ImplantDatabasePanel';
import * as api from '../services/api';

vi.mock('../services/api', () => ({
  getFemoralImplants: vi.fn(),
  getTibialImplants: vi.fn()
}));

const mockFemoralData = [
  {
    id: "f1",
    component_type: "femoral",
    size: "1",
    width: 55,
    ap_dimension: 50,
    manufacturer: "Demonstration",
    model_name: "Demo",
    source_type: "synthetic_demo",
    dataset_version: "demo-v1",
    is_demo: true,
    created_at: "2023-01-01T00:00:00Z"
  }
];

const mockTibialData = [
  {
    id: "t1",
    component_type: "tibial",
    size: "2",
    width: 60,
    ap_dimension: 45,
    manufacturer: "Demonstration",
    model_name: "Demo",
    source_type: "synthetic_demo",
    dataset_version: "demo-v1",
    is_demo: true,
    created_at: "2023-01-01T00:00:00Z"
  }
];

describe('ImplantDatabasePanel Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', () => {
    vi.mocked(api.getFemoralImplants).mockReturnValue(new Promise(() => {}));
    vi.mocked(api.getTibialImplants).mockReturnValue(new Promise(() => {}));
    
    render(<ImplantDatabasePanel />);
    expect(screen.getByText('Loading Implant Database...')).toBeInTheDocument();
  });

  it('renders database tables and demo warning', async () => {
    vi.mocked(api.getFemoralImplants).mockResolvedValue(mockFemoralData);
    vi.mocked(api.getTibialImplants).mockResolvedValue(mockTibialData);
    
    render(<ImplantDatabasePanel />);
    
    await waitFor(() => {
      expect(screen.getByText('DEMONSTRATION IMPLANT DATABASE')).toBeInTheDocument();
    });

    expect(screen.getByText('Femoral Components')).toBeInTheDocument();
    expect(screen.getByText('Tibial Components')).toBeInTheDocument();
    
    // Check femoral data
    expect(screen.getByText('55.0')).toBeInTheDocument();
    expect(screen.getByText('50.0')).toBeInTheDocument();

    // Check tibial data
    expect(screen.getByText('60.0')).toBeInTheDocument();
    expect(screen.getByText('45.0')).toBeInTheDocument();

    // Check demo badges
    const demoBadges = screen.getAllByText('DEMO');
    expect(demoBadges.length).toBe(2);
  });

  it('renders error state on API failure', async () => {
    vi.mocked(api.getFemoralImplants).mockRejectedValue(new Error("API Error"));
    vi.mocked(api.getTibialImplants).mockRejectedValue(new Error("API Error"));
    
    render(<ImplantDatabasePanel />);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to load implant database.')).toBeInTheDocument();
    });
  });
});
