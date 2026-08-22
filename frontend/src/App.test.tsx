import { describe, it, expect } from 'vitest';
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
