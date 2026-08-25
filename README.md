# Knee AI Clinical Workstation

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![React](https://img.shields.io/badge/frontend-React%20%7C%20TypeScript-61DAFB)
![FastAPI](https://img.shields.io/badge/backend-FastAPI%20%7C%20Python-009688)
![Status](https://img.shields.io/badge/status-Research%20Prototype-orange)

An advanced, AI-assisted clinical workstation prototype for the assessment of osteoarthritis (OA), meniscus thickness, and patient-specific knee implant sizing. Built with a modern tech stack and designed for high-integrity medical data processing.

> **⚠️ IMPORTANT DISCLAIMER:** This application is a research and demonstration prototype. The measurements, potential anatomical matches, AI-associated analysis, and surgical planning presented here have **not been clinically validated** and must **not** be used for diagnosis, surgical planning, or direct patient care. Final clinical interpretation is the sole responsibility of the attending physician.

---

## 🌟 Key Features

### 1. Case Management & Intake
- Patient demographic tracking and secure case generation.
- Modern, distraction-free interface tailored for clinical workflows.

### 2. Multi-Modality Imaging Pipeline
- Upload and manage clinical imaging (Radiographs/X-Ray).
- Standardized image representation and spatial calibration.

### 3. AI-Assisted Radiographic Findings
- Integration with DenseNet121 for automated Kellgren-Lawrence (KL) grading of knee osteoarthritis.
- Transparent reporting of model confidence, probability distributions, and interpretative findings.

### 4. Surgical Pre-Operative Planning (Data-Driven)
- **Traceable Measurements:** Anatomical landmarks mapped to physical space via DICOM pixel spacing or manual calibration.
- **Biomechanical Alignment:** Calculation of the Hip-Knee-Ankle (HKA) mechanical axis.
- **Implant Sizing:** Data-driven matching of patient geometry against digitized implant catalogs (Femoral/Tibial).
- **Strict Data Integrity:** The system actively refuses to synthesize fake data. If required validation (e.g., view metadata, calibration) is missing, the plan is securely locked into an `INCOMPLETE` state.

### 5. Automated Clinical Reporting
- Printable, high-fidelity clinical diagnostic document summarizing all validated findings.
- Explicit provenance tagging (e.g., `[AI]`, `[DICOM]`, `[CALCULATED]`, `[USER]`).

---

## 🏗️ Architecture

The workstation is built using a decoupled client-server architecture:

- **Frontend:** React, TypeScript, Vite. Features a custom CSS design system emphasizing medical-grade clarity, 8px grid spacing, and robust state management.
- **Backend:** FastAPI, Python. Handles image processing, inference orchestration, and REST API routing.
- **AI Models:** PyTorch-based models for classification and segmentation.

---

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- `git`

### Backend Setup (Windows)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
The backend API will run on `http://localhost:8000`. API documentation is available at `http://localhost:8000/docs`.

### Frontend Setup

Open a new terminal window:
```powershell
cd frontend
npm install
npm run dev
```
The frontend application will run on `http://localhost:5173`.

---

## 📂 Project Structure

```
knee-ai-workstation/
├── backend/                  # FastAPI backend
│   ├── app/                  # Application code (API, AI logic, schemas)
│   ├── data/                 # Local data storage (uploads, catalogs)
│   └── tests/                # Backend unit and integration tests
├── frontend/                 # React frontend
│   ├── public/               # Static assets
│   └── src/                  # React components, pages, services, and styles
├── docs/                     # Technical documentation and audits
└── README.md
```

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
