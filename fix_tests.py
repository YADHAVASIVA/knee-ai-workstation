import os

def fix_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('frontend/src/App.test.tsx', """import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from './App';

describe('App Component', () => {
  it('renders without crashing and shows the sidebar navigation', () => {
    render(<App />);
    expect(screen.getByText('Overview')).toBeInTheDocument();
    expect(screen.getByText('Imaging')).toBeInTheDocument();
    expect(screen.getByText('Anatomy')).toBeInTheDocument();
  });
});
""")

fix_file('frontend/src/pages/CaseOverview.test.tsx', """import { describe, it, expect, vi } from 'vitest';
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
    render(<CaseOverview patient={mockPatient} onChange={vi.fn()} onNext={vi.fn()} />);
    expect(screen.getByText('Case Overview')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Test')).toBeInTheDocument();
  });
});
""")
