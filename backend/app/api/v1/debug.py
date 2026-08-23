from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/debug")
def debug_paths():
    file_dir = os.path.dirname(__file__)
    models_dir = os.path.abspath(os.path.join(file_dir, '../../../models/xray/'))
    return {
        "file_dir": file_dir,
        "models_dir": models_dir,
        "json_exists": os.path.exists(os.path.join(models_dir, 'classification_report.json')),
        "pth_exists": os.path.exists(os.path.join(models_dir, 'best_model.pth')),
        "cwd": os.getcwd()
    }
