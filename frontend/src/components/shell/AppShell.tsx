import React from 'react';
import { Sidebar } from './Sidebar';
import { TopBar } from './TopBar';
import './shell.css';

interface AppShellProps {
  children: React.ReactNode;
  activeRoute: string;
  onNavigate: (route: string) => void;
  analysisId: string | null;
  isDemo: boolean;
  isCalibrated: boolean | null;
  imageMetadata?: any;
  routes: Array<{ id: string; label: string; category: string; disabled?: boolean }>;
}

export const AppShell: React.FC<AppShellProps> = ({
  children,
  activeRoute,
  onNavigate,
  analysisId,
  isDemo,
  isCalibrated,
  imageMetadata,
  routes
}) => {
  // Anatomy route uses the Dark Workspace (World B)
  const isDarkWorkspace = activeRoute === 'anatomy';
  const workspaceClass = isDarkWorkspace ? 'workspace-dark' : 'workspace-light';

  return (
    <div className="app-layout">
      <Sidebar 
        activeRoute={activeRoute} 
        onNavigate={onNavigate} 
        analysisId={analysisId}
        routes={routes}
        imageMetadata={imageMetadata}
        isCalibrated={isCalibrated}
      />
      <div className="app-main-wrapper">
        <TopBar 
          activeRoute={activeRoute} 
          analysisId={analysisId} 
          isDemo={isDemo} 
          isCalibrated={isCalibrated}
          imageMetadata={imageMetadata}
        />
        <main className={`app-main-content ${workspaceClass}`}>
          <div className="content-container">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};
