import os
import uuid
import json
from typing import Dict, Any
from PIL import Image, UnidentifiedImageError
from fastapi import UploadFile, HTTPException

from app.core.config import settings
from app.services.dicom_service import DicomService

class ImagePreprocessingService:
    SUPPORTED_MIME_TYPES = {"image/jpeg", "image/png", "application/dicom", "application/octet-stream"}
    SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".dcm"}

    @staticmethod
    def validate_upload(file: UploadFile) -> None:
        if file.content_type not in ImagePreprocessingService.SUPPORTED_MIME_TYPES:
            # Maybe it's a DICOM without content type
            ext = os.path.splitext(file.filename)[1].lower() if file.filename else ""
            if ext not in ImagePreprocessingService.SUPPORTED_EXTENSIONS and not file.filename.endswith(".dcm"):
                raise HTTPException(status_code=400, detail="Unsupported image format. Please use PNG, JPG/JPEG, or DICOM.")
            
    @staticmethod
    async def save_uploaded_file(file: UploadFile) -> Dict[str, Any]:
        ImagePreprocessingService.validate_upload(file)
        
        content = await file.read()
        file_size = len(content)
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="Empty file.")
        
        if file_size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(status_code=400, detail="Image file is too large.")

        image_id = str(uuid.uuid4())
        ext = os.path.splitext(file.filename)[1].lower() if file.filename else ".jpg"
        
        is_dicom = DicomService.is_dicom(content)
        if is_dicom:
            ext = ".dcm"
            
        internal_filename = f"{image_id}{ext}"
        
        if is_dicom:
            upload_path = os.path.join(settings.UPLOAD_DIR, "dicom", internal_filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        else:
            upload_path = os.path.join(settings.UPLOAD_DIR, "images", internal_filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            
        try:
            with open(upload_path, "wb") as buffer:
                buffer.write(content)
        except Exception as e:
            raise HTTPException(status_code=500, detail="Upload failure.")

        metadata_dict = {
            "image_id": image_id,
            "filename": file.filename,
            "internal_filename": internal_filename,
            "content_type": file.content_type,
            "file_size": file_size,
            "format": "DICOM" if is_dicom else "IMAGE",
            "status": "uploaded",
            "spatial_calibration_available": False,
            "orientation_available": False
        }

        if is_dicom:
            try:
                dicom_res = DicomService.parse_dicom(content)
                d_meta = dicom_res["metadata"]
                metadata_dict.update(d_meta)
                # Save metadata
                meta_path = os.path.join(settings.UPLOAD_DIR, f"{image_id}_meta.json")
                with open(meta_path, "w") as f:
                    json.dump(metadata_dict, f)
            except Exception as e:
                os.remove(upload_path)
                raise HTTPException(status_code=400, detail=f"Invalid DICOM file: {str(e)}")
        else:
            try:
                with Image.open(upload_path) as img:
                    img.verify()
                with Image.open(upload_path) as img:
                    metadata_dict["width"] = img.size[0]
                    metadata_dict["height"] = img.size[1]
                meta_path = os.path.join(settings.UPLOAD_DIR, f"{image_id}_meta.json")
                with open(meta_path, "w") as f:
                    json.dump(metadata_dict, f)
            except Exception as e:
                os.remove(upload_path)
                raise HTTPException(status_code=400, detail="Invalid medical image or corrupted file.")

        return metadata_dict

    @staticmethod
    def preprocess_image(image_id: str) -> Dict[str, Any]:
        meta_path = os.path.join(settings.UPLOAD_DIR, f"{image_id}_meta.json")
        if not os.path.exists(meta_path):
            raise HTTPException(status_code=404, detail="Image metadata not found.")
            
        with open(meta_path, "r") as f:
            metadata = json.load(f)
            
        internal_filename = metadata.get("internal_filename")
        is_dicom = metadata.get("format") == "DICOM"
        
        if is_dicom:
            upload_path = os.path.join(settings.UPLOAD_DIR, "dicom", internal_filename)
        else:
            upload_path = os.path.join(settings.UPLOAD_DIR, "images", internal_filename)
            
        if not os.path.exists(upload_path):
            raise HTTPException(status_code=404, detail="Original image not found.")

        try:
            if is_dicom:
                with open(upload_path, "rb") as f:
                    dicom_res = DicomService.parse_dicom(f.read())
                img = DicomService.extract_image_array(dicom_res["dataset"])
            else:
                img = Image.open(upload_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                    
            original_width, original_height = img.size
            
            processed_filename = f"{image_id}.png"
            processed_path = os.path.join(settings.PROCESSED_DIR, processed_filename)
            img.save(processed_path, format="PNG")
            
            preview_filename = f"{image_id}_preview.jpg"
            preview_path = os.path.join(settings.PREVIEWS_DIR, preview_filename)
            
            img.thumbnail((800, 800))
            img.save(preview_path, format="JPEG", quality=85)
            
            processed_width, processed_height = original_width, original_height

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Preprocessing failure: {str(e)}")

        metadata["status"] = "processed"
        metadata["original_dimensions"] = {"width": original_width, "height": original_height}
        metadata["processed_dimensions"] = {"width": processed_width, "height": processed_height}
        
        with open(meta_path, "w") as f:
            json.dump(metadata, f)
            
        return metadata

    @staticmethod
    def get_preview_path(image_id: str) -> str:
        preview_filename = f"{image_id}_preview.jpg"
        preview_path = os.path.join(settings.PREVIEWS_DIR, preview_filename)
        
        if not os.path.exists(preview_path):
            raise HTTPException(status_code=404, detail="Preview unavailable.")
        
        return preview_path
