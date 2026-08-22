# Knee AI Analysis

AI-Assisted Assessment of Medial Meniscus Thickness and Patient-Specific Knee Implant Sizing.

## Development Commands (Windows)

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

## Image Pipeline & Limitations

### Supported Formats
- PNG
- JPG / JPEG
*(DICOM processing is planned and the current MVP uses standard image input for development/demo purposes)*

### Upload Limitations
- Max file size: 10 MB
- Valid medical image file required

### APIs Created
- **Upload API**: `POST /api/v1/images/upload` - Accepts multipart/form-data. Returns generated `image_id`.
- **Preprocessing API**: `POST /api/v1/images/preprocess/{image_id}` - Converts to standard representation, extracts metadata, sets spatial calibration status.
- **Image Preview API**: `GET /api/v1/images/{image_id}/preview` - Returns the optimized generated preview.

**Note:** This is a hackathon prototype. Do not use for real clinical diagnosis. No real patient data should be uploaded.
