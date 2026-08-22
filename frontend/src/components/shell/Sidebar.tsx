import React from 'react';
import './shell.css';

export type RouteId = 'overview' | 'anatomy' | 'analysis' | 'planning' | 'report';

interface SidebarProps {
  activeRoute: string;
  onNavigate: (route: RouteId) => void;
  analysisId: string | null;
  routes: Array<{ id: RouteId; label: string; category: string; disabled?: boolean }>;
  imageMetadata?: any;
  isCalibrated?: boolean | null;
}

export const Sidebar: React.FC<SidebarProps> = ({ 
  activeRoute, 
  onNavigate, 
  analysisId,
  routes,
  imageMetadata,
  isCalibrated
}) => {
  // Group routes by category
  const sections = routes.reduce((acc, route) => {
    if (!acc[route.category]) acc[route.category] = [];
    acc[route.category].push(route);
    return acc;
  }, {} as Record<string, typeof routes>);

  return (
    <aside className="app-sidebar">
      <div className="sidebar-brand">
        <div className="brand-logo-area">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
          <div className="brand-text">
            <span className="brand-title">KNEE<br/>AI</span>
          </div>
        </div>
        <div className="brand-subtitle">ORTHOPEDIC ANALYSIS</div>
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
                    <span className="nav-label">{item.label}</span>
                  </button>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </nav>

      {analysisId && (
        <div className="sidebar-case-context">
          <div className="case-context-title">CURRENT CASE</div>
          <div className="case-context-id">{analysisId.split('-')[0].toUpperCase()}</div>
          <div className="case-context-meta">
            {imageMetadata?.modality || 'UNKNOWN'}
            {isCalibrated && <span className="case-calibrated-dot">• CALIBRATED</span>}
          </div>
        </div>
      )}
    </aside>
  );
};
