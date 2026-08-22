from sqlalchemy.orm import Session
from app.db.schemas import ImplantComponentCreate
from app.db.repositories.implant_repository import ImplantRepository

def seed_demo_implants(db: Session):
    repo = ImplantRepository(db)
    
    # Check if data already exists to avoid duplicates
    if repo.count_by_type("femoral") > 0 or repo.count_by_type("tibial") > 0:
        return

    femoral_demo_data = [
        {"size": "1", "width": 55.0, "ap_dimension": 50.0},
        {"size": "2", "width": 60.0, "ap_dimension": 54.0},
        {"size": "3", "width": 64.0, "ap_dimension": 58.0},
        {"size": "4", "width": 68.0, "ap_dimension": 62.0},
        {"size": "5", "width": 72.0, "ap_dimension": 66.0},
    ]

    tibial_demo_data = [
        {"size": "1", "width": 60.0, "ap_dimension": 42.0},
        {"size": "2", "width": 64.0, "ap_dimension": 45.0},
        {"size": "3", "width": 68.0, "ap_dimension": 48.0},
        {"size": "4", "width": 72.0, "ap_dimension": 51.0},
        {"size": "5", "width": 76.0, "ap_dimension": 54.0},
    ]

    for data in femoral_demo_data:
        repo.create(ImplantComponentCreate(
            component_type="femoral",
            size=data["size"],
            width=data["width"],
            ap_dimension=data["ap_dimension"],
            manufacturer="Demonstration",
            model_name="Synthetic Demo Femoral Component",
            source_type="synthetic_demo",
            dataset_version="demo-v1",
            is_demo=True
        ))

    for data in tibial_demo_data:
        repo.create(ImplantComponentCreate(
            component_type="tibial",
            size=data["size"],
            width=data["width"],
            ap_dimension=data["ap_dimension"],
            manufacturer="Demonstration",
            model_name="Synthetic Demo Tibial Component",
            source_type="synthetic_demo",
            dataset_version="demo-v1",
            is_demo=True
        ))
