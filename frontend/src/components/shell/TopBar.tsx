import React from 'react';
import './shell.css';

interface TopBarProps {
  activeRoute: string;
  analysisId: string | null;
  isDemo: boolean;
  isCalibrated: boolean | null;
  imageMetadata?: any;
}

export const TopBar: React.FC<TopBarProps> = ({ 
  activeRoute, 
  analysisId,
  isDemo,
  isCalibrated,
  imageMetadata
}) => {
  const getContextName = () => {
    switch(activeRoute) {
      case 'overview': return 'Overview';
      case 'anatomy': return 'Anatomy';
      case 'analysis': return 'OA Analysis';
      case 'planning': return 'Implant Planning';
      case 'report': return 'Report';
      default: return '';
    }
  };

  return (
    <header className="app-topbar">
      <div className="topbar-left">
        <span className="topbar-brand">KNEE AI</span>
        <span className="breadcrumb-slash">/</span>
        <span className="topbar-route">{getContextName()}</span>
      </div>
      
      <div className="topbar-right">
        {analysisId && (
          <>
            <span className="topbar-meta">{analysisId.split('-')[0].toUpperCase()}</span>
            <span className="topbar-divider"></span>
            <span className="topbar-meta">{imageMetadata?.modality || 'MRI'}</span>
            <span className="topbar-divider"></span>
            <span className={`topbar-meta ${isCalibrated ? 'calibrated' : ''}`}>
              &bull; {isCalibrated ? 'Calibrated' : 'Uncalibrated'}
            </span>
          </>
        )}
        {isDemo && (
          <>
            <span className="topbar-divider"></span>
            <span className="topbar-demo-badge">DEMO</span>
          </>
        )}
      </div>
    </header>
  );
};
