import React from 'react';
import './shell.css';

interface SidebarProps {
  activeRoute: string;
  onNavigate: (route: string) => void;
  analysisId: string | null;
  routes: Array<{ id: string; label: string; category: string; disabled?: boolean }>;
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
  const sections = routes.reduce((acc, route) => {
    if (!acc[route.category]) acc[route.category] = [];
    acc[route.category].push(route);
    return acc;
  }, {} as Record<string, typeof routes>);

  return (
    <aside className="app-sidebar">
      <div className="sidebar-brand">
        <div className="brand-title">KNEE AI</div>
        <div className="brand-subtitle">Medical Imaging Workstation</div>
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
            {imageMetadata?.modality || 'MRI'} &bull; {imageMetadata?.dimensions ? `${imageMetadata.dimensions.width} × ${imageMetadata.dimensions.height}` : 'Unavailable'}
          </div>
          <div className={`case-context-meta ${isCalibrated ? 'success' : 'warning'}`}>
            &bull; {isCalibrated ? 'Calibrated' : 'Uncalibrated'}
          </div>
        </div>
      )}
    </aside>
  );
};
