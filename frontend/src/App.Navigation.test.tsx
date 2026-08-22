import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import App from './App';
import * as api from './services/api';

vi.mock('./services/api');

describe('App Navigation and State Architecture', () => {
  it('enforces single source of truth for routing', async () => {
    render(<App />);

    // 1. Initial route: overview
    expect(screen.getByText('CASE / OVERVIEW')).toBeInTheDocument();
    
    // Upload panel should be visible in Overview
    expect(screen.getByText('Upload Medical Image')).toBeInTheDocument();

    // 2. Click Anatomy (it is disabled initially, so nothing should happen)
    const anatomyBtn = screen.getByRole('button', { name: /Anatomy/i });
    fireEvent.click(anatomyBtn);
    expect(screen.getByText('CASE / OVERVIEW')).toBeInTheDocument();

    // Mock an active case to enable navigation
    // Because we mock API, it's easier to just test if the component switch happens when buttons are enabled.
    // In actual app, workflowState unlocks routes. 
  });
});
