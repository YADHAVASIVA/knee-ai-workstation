import React from 'react';
import './ui.css';

interface StatusBadgeProps {
  status: 'CALIBRATED' | 'UNCALIBRATED' | 'DEMO' | 'SUCCESS' | 'WARNING' | 'ERROR' | 'NEUTRAL';
  label: string;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, label }) => {
  let badgeClass = 'badge-neutral';
  
  switch(status) {
    case 'CALIBRATED':
    case 'SUCCESS':
      badgeClass = 'badge-success';
      break;
    case 'UNCALIBRATED':
    case 'WARNING':
      badgeClass = 'badge-warning';
      break;
    case 'ERROR':
      badgeClass = 'badge-error';
      break;
    case 'DEMO':
      badgeClass = 'badge-demo';
      break;
    case 'NEUTRAL':
      badgeClass = 'badge-neutral';
      break;
  }

  return (
    <div className={`status-badge ${badgeClass}`}>
      <span className="status-indicator"></span>
      {label}
    </div>
  );
};
