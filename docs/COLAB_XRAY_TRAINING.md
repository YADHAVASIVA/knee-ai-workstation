# Phase 12.9: Google Colab GPU Training Guide

This document explains how to securely port the complete PyTorch training package for the X-Ray KL grading model to Google Colab to leverage a CUDA GPU (e.g. T4) for the 50-epoch training schedule. 

### 1. Preparing the Package
You will need to run training over the verified dataset. Since uploading 15,000+ files to Colab directly takes too long, we use Google Drive.
Zip the local `backend/data/xray` and `backend/ai/training` directories into an archive `xray_training_pkg.zip` and upload it to your Google Drive. 

### 2. Colab Setup
1. Create a new notebook in Google Colab.
2. Go to **Runtime > Change runtime type** and select **T4 GPU**.
3. Mount your Google Drive:

```python
from google.colab import drive
drive.mount('/content/drive')
```

### 3. Extract and Verify Environment
```bash
# Copy and extract the package
!cp "/content/drive/MyDrive/xray_training_pkg.zip" /content/
!unzip -q xray_training_pkg.zip -d /content/pkg/

# Install exact dependencies
!pip install torch torchvision pandas numpy scikit-learn matplotlib seaborn
```

### 4. CUDA and Hardware Verification
```python
import torch
print("PyTorch Version:", torch.__version__)
print("CUDA Available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print("VRAM:", torch.cuda.get_device_properties(0).total_memory / 1e9, "GB")
```
*Note: If `CUDA Available` is `False`, do not proceed. The training scripts are hard-coded to halt if CUDA is missing.*

### 5. Training
Run the exact training script natively inside the Colab environment. The script is configured to use environment variables for path routing, so we supply them below:

```bash
!export PROJECT_ROOT=/content/pkg && \
 export DATA_ROOT=/content/pkg/backend/data/xray/raw && \
 export SPLITS_DIR=/content/pkg/backend/data/xray/splits && \
 export MODEL_OUTPUT_DIR=/content/pkg/backend/models/xray && \
 export BATCH_SIZE=16 && \
 python /content/pkg/backend/ai/training/train.py
```
This process will take time. It strictly evaluates on the Validation set (Macro-F1) every epoch.

### 6. Held-out Evaluation
Only execute this after `train.py` completes. It evaluates on the strictly held-out `test.csv` (1,473 images) and extracts all per-class metrics.

```bash
!export PROJECT_ROOT=/content/pkg && \
 export DATA_ROOT=/content/pkg/backend/data/xray/raw && \
 export SPLITS_DIR=/content/pkg/backend/data/xray/splits && \
 export MODEL_OUTPUT_DIR=/content/pkg/backend/models/xray && \
 export BATCH_SIZE=16 && \
 python /content/pkg/backend/ai/training/evaluate.py
```

### 7. Porting Checkpoints Back
Finally, you must compress the trained weights and artifacts to migrate back to the local Omen machine.

```bash
!zip -r /content/trained_models.zip /content/pkg/backend/models/xray/
!cp /content/trained_models.zip "/content/drive/MyDrive/"
```
Download `trained_models.zip` from your Google Drive, extract it locally, and the existing API Gateway will automatically route it to the front-end UI.
