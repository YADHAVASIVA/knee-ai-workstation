import React from 'react';
import './GlobalWarnings.css';

interface GlobalWarningsProps {
  calibrationAvailable: boolean | undefined;
  orientationStatus: string | undefined;
}

export const GlobalWarnings: React.FC<GlobalWarningsProps> = ({ calibrationAvailable, orientationStatus }) => {
  return (
    <div className="global-warnings-container">
      <div className="demo-banner">
        <strong>DEMONSTRATION / RESEARCH PROTOTYPE</strong>
        <p>This application currently uses synthetic/demo components and is NOT intended for clinical diagnosis, treatment, or surgical decision-making.</p>
      </div>

      {calibrationAvailable === false && (
        <div className="warning-banner">
          <strong>PHYSICAL CALIBRATION UNAVAILABLE</strong>
          <p>Current measurements are image-plane pixel measurements. Physical millimeter measurements and validated implant matching require appropriate spatial calibration.</p>
        </div>
      )}

      {orientationStatus === 'unknown' && (
        <div className="warning-banner">
          <strong>ANATOMICAL ORIENTATION UNKNOWN</strong>
          <p>Current femoral/tibial AP values represent image-plane geometry rather than validated anatomical AP measurements.</p>
        </div>
      )}
    </div>
  );
};
