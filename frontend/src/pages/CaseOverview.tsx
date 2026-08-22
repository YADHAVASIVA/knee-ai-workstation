import React from 'react';
import type { PatientInfo } from '../types/case';
import { Button } from '../components/ui/Button';
import './CaseOverview.css';

interface CaseOverviewProps {
  patient: PatientInfo;
  onChange: (patient: PatientInfo) => void;
  onNext: () => void;
}

export const CaseOverview: React.FC<CaseOverviewProps> = ({ patient, onChange, onNext }) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    onChange({ ...patient, [e.target.name]: e.target.value });
  };

  const isValid = patient.name.trim() !== '' && patient.patientId.trim() !== '';

  return (
    <div className="co-container fade-in">
      <div className="co-header">
        <h2 className="co-title">Case Overview</h2>
        <p className="co-subtitle">Create a patient case before uploading imaging studies.</p>
      </div>

      <div className="co-card">
        <h3 className="co-section-title">Patient Information</h3>
        <div className="co-form-grid">
          <div className="co-form-group">
            <label>Patient Name</label>
            <input type="text" name="name" value={patient.name} onChange={handleChange} placeholder="e.g. Arun Kumar" />
          </div>
          <div className="co-form-group">
            <label>Age</label>
            <input type="number" name="age" value={patient.age} onChange={handleChange} placeholder="e.g. 45" />
          </div>
          <div className="co-form-group">
            <label>Sex</label>
            <select name="sex" value={patient.sex} onChange={handleChange}>
              <option value="">Select...</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>
          <div className="co-form-group">
            <label>Patient ID / Case ID</label>
            <input type="text" name="patientId" value={patient.patientId} onChange={handleChange} placeholder="e.g. KNEE-2026-001" />
          </div>
          <div className="co-form-group">
            <label>Laterality</label>
            <select name="laterality" value={patient.laterality} onChange={handleChange}>
              <option value="">Select...</option>
              <option value="Left">Left</option>
              <option value="Right">Right</option>
              <option value="Bilateral">Bilateral</option>
            </select>
          </div>
          <div className="co-form-group full-width">
            <label>Clinical Notes</label>
            <textarea name="notes" value={patient.notes} onChange={handleChange} placeholder="Knee pain for 6 months..." rows={3} />
          </div>
        </div>
      </div>

      <div className="co-card">
        <h3 className="co-section-title">Privacy Notice</h3>
        <p className="co-privacy-text">
          This is a research/demonstration prototype. Please do not enter real Protected Health Information (PHI). 
          Any uploaded DICOM images will be stripped of identifying metadata during processing.
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
