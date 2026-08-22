import React from 'react';
import { StatusBadge } from '../ui/StatusBadge';
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
        <div className="topbar-brand-inline">KNEE AI</div>
        <div className="topbar-breadcrumb">
          Case <span className="breadcrumb-slash">/</span> {getContextName()}
        </div>
      </div>
      
      <div className="topbar-right">
        {analysisId && (
          <div className="topbar-case-id">{analysisId.split('-')[0].toUpperCase()}</div>
        )}
        {imageMetadata?.modality && (
          <div className="topbar-meta-item">
            <div className="topbar-meta-dot"></div>
            {imageMetadata.modality}
          </div>
        )}
        {isCalibrated !== null && (
          <div className={`topbar-meta-item ${isCalibrated ? 'calibrated' : ''}`}>
            <div className="topbar-meta-dot"></div>
            {isCalibrated ? 'Calibrated' : 'Uncalibrated'}
          </div>
        )}
        {isDemo && (
          <StatusBadge status="DEMO" label="DEMO" />
        )}
      </div>
    </header>
  );
};
