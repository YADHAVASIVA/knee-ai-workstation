import React, { useState } from 'react';
import type { PatientInfo } from '../types/case';
import { Button } from '../components/ui/Button';
import './CaseOverview.css';

interface CaseOverviewProps {
  patient: PatientInfo;
  caseId: string;
  onChange: (patient: PatientInfo) => void;
  onNext: () => void;
}

export const CaseOverview: React.FC<CaseOverviewProps> = ({ patient, caseId, onChange, onNext }) => {
  const [touched, setTouched] = useState<Record<string, boolean>>({});

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    onChange({ ...patient, [e.target.name]: e.target.value });
  };

  const handleBlur = (e: React.FocusEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setTouched({ ...touched, [e.target.name]: true });
  };

  const isNameValid = patient.name.trim() !== '';
  const isPatientIdValid = patient.patientId.trim() !== '';
  const isAgeValid = patient.age.trim() !== '';
  const isLateralityValid = patient.laterality.trim() !== '';

  const isValid = isNameValid && isPatientIdValid && isAgeValid && isLateralityValid;

  return (
    <div className="co-container fade-in">
      <div className="co-header">
        <h2 className="co-title">Case Overview</h2>
        <p className="co-subtitle">Create a patient case before imaging</p>
      </div>

      <div className="co-card">
        <h3 className="co-section-title">PATIENT INFORMATION</h3>
        <div className="co-form-grid">
          
          <div className="co-form-group">
            <label>Patient Name *</label>
            <input 
              type="text" name="name" 
              value={patient.name} 
              onChange={handleChange} 
              onBlur={handleBlur}
              placeholder="Enter patient name" 
              className={touched.name && !isNameValid ? 'error' : ''}
            />
            {touched.name && !isNameValid && <span className="co-error-text">Patient name is required.</span>}
          </div>

          <div className="co-form-group">
            <label>Patient / Case ID *</label>
            <input 
              type="text" name="patientId" 
              value={patient.patientId} 
              onChange={handleChange}
              onBlur={handleBlur}
              placeholder={caseId} 
              className={touched.patientId && !isPatientIdValid ? 'error' : ''}
            />
            {touched.patientId && !isPatientIdValid && <span className="co-error-text">Patient / Case ID is required.</span>}
          </div>

          <div className="co-form-group">
            <label>Age *</label>
            <input 
              type="number" name="age" 
              value={patient.age} 
              onChange={handleChange}
              onBlur={handleBlur}
              placeholder="Enter age" 
              className={touched.age && !isAgeValid ? 'error' : ''}
            />
            {touched.age && !isAgeValid && <span className="co-error-text">Age is required.</span>}
          </div>

          <div className="co-form-group">
            <label>Sex</label>
            <select name="sex" value={patient.sex} onChange={handleChange}>
              <option value="">Select</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
              <option value="Not specified">Not specified</option>
            </select>
          </div>

          <div className="co-form-group">
            <label>Laterality *</label>
            <select 
              name="laterality" 
              value={patient.laterality} 
              onChange={handleChange}
              onBlur={handleBlur}
              className={touched.laterality && !isLateralityValid ? 'error' : ''}
            >
              <option value="">Select</option>
              <option value="Left">Left</option>
              <option value="Right">Right</option>
              <option value="Bilateral">Bilateral</option>
              <option value="Not specified">Not specified</option>
            </select>
            {touched.laterality && !isLateralityValid && <span className="co-error-text">Laterality is required.</span>}
          </div>

          <div className="co-form-group">
            <label>Clinical Notes</label>
            <textarea 
              name="notes" 
              value={patient.notes} 
              onChange={handleChange} 
              placeholder="Optional clinical notes" 
              rows={1} 
            />
          </div>

        </div>
      </div>

      <div className="co-card co-notice-card">
        <h3 className="co-section-title">PRIVACY / RESEARCH NOTICE</h3>
        <p className="co-privacy-text">
          This application is a research and demonstration prototype. Do not enter real PHI.
        </p>
      </div>

      <div className="co-actions">
        <Button variant="primary" onClick={onNext} disabled={!isValid} className="co-next-btn">
          Continue to Imaging &rarr;
        </Button>
      </div>
    </div>
  );
};
