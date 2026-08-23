import React from 'react';
import { Activity } from 'lucide-react';
import './shell.css';

interface SidebarProps {
  activeRoute: string;
  onNavigate: (route: string) => void;
  analysisId: string | null;
  routes: Array<{ id: string; label: string; category: string; disabled?: boolean; icon?: React.ReactNode }>;
}

export const Sidebar: React.FC<SidebarProps> = ({ 
  activeRoute, 
  onNavigate, 
  routes
}) => {
  const sections = routes.reduce((acc, route) => {
    if (!acc[route.category]) acc[route.category] = [];
    acc[route.category].push(route);
    return acc;
  }, {} as Record<string, typeof routes>);

  return (
    <aside className="app-sidebar">
      <div className="sidebar-brand">
        <div className="brand-logo">
          <Activity size={24} style={{ color: 'var(--color-primary)' }} />
          <div className="brand-text">
            <div className="brand-title">KNEE AI</div>
            <div className="brand-subtitle">Clinical Workstation</div>
          </div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {Object.entries(sections).map(([category, items]) => (
          <div key={category} className="nav-section">
            <h3 className="nav-section-title">{category}</h3>
            <ul className="nav-list">
              {items.map(item => (
                <li key={item.id}>
                  <button
                    className={`nav-btn ${activeRoute === item.id ? 'active' : ''}`}
                    onClick={() => onNavigate(item.id)}
                    disabled={item.disabled}
                  >
                    <span className="nav-icon">{item.icon}</span>
                    <span className="nav-label">{item.label}</span>
                  </button>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </nav>
    </aside>
  );
};
