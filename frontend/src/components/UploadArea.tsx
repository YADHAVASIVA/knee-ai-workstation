import React, { useRef, useState } from 'react';
import './UploadArea.css';

interface UploadAreaProps {
  onFileSelect: (file: File) => void;
  isProcessing: boolean;
  statusMessage: string;
}

export const UploadArea: React.FC<UploadAreaProps> = ({ onFileSelect, isProcessing, statusMessage }) => {
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file: File) => {
    onFileSelect(file);
  };

  const onButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div 
      className={`upload-area ${dragActive ? 'drag-active' : ''} ${isProcessing ? 'disabled' : ''}`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <input 
        ref={fileInputRef}
        type="file" 
        accept=".png,.jpg,.jpeg,.dcm" 
        onChange={handleChange} 
        disabled={isProcessing}
        data-testid="file-upload"
      />
      
      {isProcessing ? (
        <div className="upload-content">
          <div className="spinner"></div>
          <p>{statusMessage}</p>
        </div>
      ) : (
        <div className="upload-content">
          <p className="primary-text">Drag and drop image here</p>
          <p className="secondary-text">or</p>
          <button type="button" className="upload-btn" onClick={onButtonClick}>Browse Files</button>
          <div className="supported-formats">
            Supported: PNG / JPG / JPEG / DICOM<br/>
            Max size: 10MB
          </div>
        </div>
      )}
    </div>
  );
};
