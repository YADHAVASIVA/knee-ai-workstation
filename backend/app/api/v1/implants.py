from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.session import get_db
from app.db.schemas import ImplantComponentResponse
from app.db.repositories.implant_repository import ImplantRepository

router = APIRouter()

@router.get("/", response_model=List[ImplantComponentResponse])
def get_implants(
    component_type: Optional[str] = Query(None, description="Filter by component type (femoral or tibial)"),
    size: Optional[str] = Query(None, description="Filter by size"),
    db: Session = Depends(get_db)
):
    repo = ImplantRepository(db)
    if component_type and component_type not in ["femoral", "tibial"]:
        raise HTTPException(status_code=400, detail="Invalid component type")
    
    return repo.get_all(component_type=component_type, size=size)

@router.get("/femoral", response_model=List[ImplantComponentResponse])
def get_femoral_implants(db: Session = Depends(get_db)):
    repo = ImplantRepository(db)
    return repo.get_all(component_type="femoral")

@router.get("/tibial", response_model=List[ImplantComponentResponse])
def get_tibial_implants(db: Session = Depends(get_db)):
    repo = ImplantRepository(db)
    return repo.get_all(component_type="tibial")

@router.get("/{implant_id}", response_model=ImplantComponentResponse)
def get_implant_by_id(implant_id: str, db: Session = Depends(get_db)):
    repo = ImplantRepository(db)
    implant = repo.get_by_id(implant_id)
    if not implant:
        raise HTTPException(status_code=404, detail="Implant not found")
    return implant
