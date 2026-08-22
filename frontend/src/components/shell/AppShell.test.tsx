import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { AppShell } from './AppShell';

describe('AppShell Component', () => {
  const mockRoutes: any = [
    { id: 'overview', label: 'Overview', category: 'CASE' },
    { id: 'anatomy', label: 'Anatomy', category: 'ANATOMY' },
    { id: 'planning', label: 'Planning', category: 'PLANNING', disabled: true }
  ];

  it('renders topbar and sidebar', () => {
    render(
      <AppShell 
        activeRoute="overview"
        onNavigate={vi.fn()}
        analysisId="uuid-1234"
        isDemo={true}
        isCalibrated={true}
        routes={mockRoutes}
      >
        <div>Content Data</div>
      </AppShell>
    );
    
    expect(screen.getByText('Content Data')).toBeInTheDocument();
    expect(screen.getAllByText('Overview').length).toBeGreaterThan(0);
    expect(screen.getByText(/Case uuid/i)).toBeInTheDocument(); 
    expect(screen.getByText('RESEARCH PROTOTYPE')).toBeInTheDocument();
  });

  it('calls onNavigate when clicking active route', () => {
    const onNav = vi.fn();
    render(
      <AppShell 
        activeRoute="overview"
        onNavigate={onNav}
        analysisId={null}
        isDemo={false}
        isCalibrated={null}
        routes={mockRoutes}
      >
        <div>Content Data</div>
      </AppShell>
    );

    const anatBtn = screen.getByRole('button', { name: 'Anatomy' });
    fireEvent.click(anatBtn);
    expect(onNav).toHaveBeenCalledWith('anatomy');
  });

  it('disabled routes cannot be clicked', () => {
    const onNav = vi.fn();
    render(
      <AppShell 
        activeRoute="overview"
        onNavigate={onNav}
        analysisId={null}
        isDemo={false}
        isCalibrated={null}
        routes={mockRoutes}
      >
        <div>Content Data</div>
      </AppShell>
    );

    const planBtn = screen.getByRole('button', { name: 'Planning' });
    expect(planBtn).toBeDisabled();
    fireEvent.click(planBtn);
    expect(onNav).not.toHaveBeenCalled();
  });
});
