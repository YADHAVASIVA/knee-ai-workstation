import React from 'react';
import './ui.css';

interface CardProps {
  children: React.ReactNode;
  variant?: 'default' | 'elevated' | 'warning';
  className?: string;
  noPadding?: boolean;
}

export const Card: React.FC<CardProps> = ({ 
  children, 
  variant = 'default',
  className = '',
  noPadding = false
}) => {
  const padClass = noPadding ? 'ui-card-no-padding' : 'ui-card-padded';
  return (
    <div className={`ui-card ui-card-${variant} ${padClass} ${className}`}>
      {children}
    </div>
  );
};
