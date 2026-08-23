import React, { useCallback, useRef } from 'react';
import type { CaseImage } from '../types/case';
import { Button } from '../components/ui/Button';
import { X, FileImage, FileStack, AlertCircle, CheckCircle2 } from 'lucide-react';
import './ImagingStudies.css';
import * as api from '../services/api';

interface ImagingStudiesProps {
  images: CaseImage[];
  setImages: React.Dispatch<React.SetStateAction<CaseImage[]>>;
  onBack: () => void;
  onNext: () => void;
}

export const ImagingStudies: React.FC<ImagingStudiesProps> = ({ images, setImages, onBack, onNext }) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const processFile = async (file: File) => {
    // tempId declared outside try so catch can reference it
    const tempId = Math.random().toString(36).substring(7);
    try {
      const newImg: CaseImage = {
        id: tempId,
        metadata: null,
        file,
        previewUrl: null,
        status: 'PROCESSING',
        segmentation: null,
        measurements: { meniscus: null, bones: null }
      };
      setImages(prev => [...prev, newImg]);

      const uploadRes = await api.uploadImage(file);
      const realId = uploadRes.image_id;

      setImages(prev => prev.map(img => img.id === tempId ? { ...img, id: realId } : img));

      await api.preprocessImage(realId);

      const meta = await api.getImageMetadata(realId);
      const previewUrl = api.getPreviewUrl(realId);

      setImages(prev => prev.map(img => img.id === realId ? {
        ...img,
        metadata: meta,
        previewUrl,
        status: 'COMPLETED'
      } : img));

    } catch (err) {
      console.error('Upload failed:', err);
      setImages(prev => prev.map(img => img.id === tempId ? { ...img, status: 'FAILED' } : img));
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      Array.from(e.target.files).forEach(file => processFile(file));
    }
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      Array.from(e.dataTransfer.files).forEach(file => processFile(file));
    }
  }, []);

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => e.preventDefault();

  const removeImage = (id: string) => {
    setImages(prev => prev.filter(img => img.id !== id));
  };

  const xrays    = images.filter(img => img.metadata?.modality === 'X-RAY');
  const mris     = images.filter(img => img.metadata?.modality === 'MRI');
  const unknowns = images.filter(img => img.metadata?.modality !== 'X-RAY' && img.metadata?.modality !== 'MRI');

  const isValid = images.length > 0 && images.every(img => img.status === 'COMPLETED');

  const renderImageCard = (img: CaseImage) => (
    <div key={img.id} className="is-image-card">
      <div className="is-image-thumb">
        {img.previewUrl
          ? <img src={img.previewUrl} alt="Preview" />
          : <div className="is-thumb-placeholder"><FileImage size={20} /></div>
        }
      </div>
      <div className="is-image-info">
        <h4 className="is-filename" title={img.file?.name || 'Uploaded File'}>
          {img.file?.name || 'Uploaded File'}
        </h4>
        <div className="is-meta-list">
          <span>{img.metadata?.modality || (img.status === 'PROCESSING' ? 'Detecting...' : '—')}</span>
          {img.metadata?.dimensions && (
            <span>{img.metadata.dimensions.width}&times;{img.metadata.dimensions.height}</span>
          )}
        </div>
        <div className={`is-status ${img.status.toLowerCase()}`}>
          {img.status === 'COMPLETED'  && <><CheckCircle2 size={13} /> Ready</>}
          {img.status === 'PROCESSING' && <>⏳ Processing...</>}
          {img.status === 'FAILED'     && <><AlertCircle size={13} /> Failed</>}
          {img.status === 'PENDING'    && <>Pending</>}
        </div>
      </div>
      <button className="is-remove-btn" onClick={() => removeImage(img.id)} title="Remove">
        <X size={16} />
      </button>
    </div>
  );

  return (
    <div className="is-container fade-in">
      <div className="is-header">
        <h2 className="is-title">Add Imaging Studies</h2>
        <p className="is-subtitle">Upload X-Ray and MRI images associated with this case.</p>
      </div>

      <div
        className="is-dropzone"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={() => fileInputRef.current?.click()}
      >
        <div className="is-dropzone-content">
          <div className="is-icon-group">
            <div className="is-icon-circle"><FileStack size={26} /></div>
          </div>
          <h3>Drag and drop studies here</h3>
          <p>Supports DICOM, PNG, and JPEG files. Multiple files allowed.</p>
          <div className="is-upload-actions">
            <Button variant="secondary" onClick={(e) => { e.stopPropagation(); fileInputRef.current?.click(); }}>
              Browse Files
            </Button>
          </div>
        </div>
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: 'none' }}
          multiple
          accept=".dcm,.png,.jpg,.jpeg,image/png,image/jpeg,application/dicom"
          onChange={handleFileChange}
        />
      </div>

      {images.length > 0 && (
        <div className="is-studies">
          {xrays.length > 0 && (
            <div className="is-study-group">
              <h3 className="is-group-title">X-RAY <span>{xrays.length} {xrays.length === 1 ? 'Image' : 'Images'}</span></h3>
              <div className="is-grid">{xrays.map(renderImageCard)}</div>
            </div>
          )}
          {mris.length > 0 && (
            <div className="is-study-group">
              <h3 className="is-group-title">MRI <span>{mris.length} {mris.length === 1 ? 'Image' : 'Images'}</span></h3>
              <div className="is-grid">{mris.map(renderImageCard)}</div>
            </div>
          )}
          {unknowns.length > 0 && (
            <div className="is-study-group">
              <h3 className="is-group-title">PROCESSING / UNKNOWN <span>{unknowns.length} {unknowns.length === 1 ? 'Image' : 'Images'}</span></h3>
              <div className="is-grid">{unknowns.map(renderImageCard)}</div>
            </div>
          )}
        </div>
      )}

      <div className="is-actions">
        <Button variant="ghost" onClick={onBack}>&larr; Back to Patient</Button>
        <Button variant="primary" onClick={onNext} disabled={!isValid}>
          Continue to Anatomy &rarr;
        </Button>
      </div>
    </div>
  );
};
