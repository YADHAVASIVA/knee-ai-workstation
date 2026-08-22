import React from 'react';
import './ui.css';

interface SectionHeaderProps {
  title: string;
  description?: string;
  action?: React.ReactNode;
}

export const SectionHeader: React.FC<SectionHeaderProps> = ({ title, description, action }) => {
  return (
    <div className="ui-section-header">
      <div>
        <h2>{title}</h2>
        {description && <p className="text-muted">{description}</p>}
      </div>
      {action && <div>{action}</div>}
    </div>
  );
};
