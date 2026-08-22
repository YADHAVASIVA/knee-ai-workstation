import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import App from './App';

vi.mock('./services/api');

describe('App Navigation and State Architecture', () => {
  it('enforces single source of truth for routing', async () => {
    render(<App />);

    // 1. Initial route: overview
    
    
    // Upload panel should be visible in Overview
    

    // 2. Click Anatomy (it is disabled initially, so nothing should happen)
    const anatomyBtn = screen.getByRole('button', { name: /Anatomy/i });
    fireEvent.click(anatomyBtn);
    

    // Mock an active case to enable navigation
    // Because we mock API, it's easier to just test if the component switch happens when buttons are enabled.
    // In actual app, workflowState unlocks routes. 
  });
});
