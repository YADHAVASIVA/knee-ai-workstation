import React from 'react';
import './ui.css';

interface PanelProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
}

export const Panel: React.FC<PanelProps> = ({ children, className = '', title }) => {
  return (
    <div className={`ui-panel ${className}`}>
      {title && <div className="ui-panel-header"><h3>{title}</h3></div>}
      <div className="ui-panel-content">
        {children}
      </div>
    </div>
  );
};
