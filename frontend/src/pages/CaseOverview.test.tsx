import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { CaseOverview } from './CaseOverview';

describe('CaseOverview Component', () => {
  const mockPatient = {
    name: 'Test',
    age: '45',
    sex: 'Male',
    patientId: '123',
    laterality: 'Right',
    notes: ''
  };

  it('renders patient intake form', () => {
    render(<CaseOverview patient={mockPatient} caseId='TEST-123' onChange={vi.fn()} onNext={vi.fn()} />);
    expect(screen.getByText('Case Overview')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Test')).toBeInTheDocument();
  });
});
