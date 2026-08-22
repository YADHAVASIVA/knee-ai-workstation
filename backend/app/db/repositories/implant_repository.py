from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.models.implant import ImplantComponent
from app.db.schemas import ImplantComponentCreate

class ImplantRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, component_type: Optional[str] = None, size: Optional[str] = None) -> List[ImplantComponent]:
        query = self.db.query(ImplantComponent)
        if component_type:
            query = query.filter(ImplantComponent.component_type == component_type)
        if size:
            query = query.filter(ImplantComponent.size == size)
        return query.all()

    def get_by_id(self, implant_id: str) -> Optional[ImplantComponent]:
        return self.db.query(ImplantComponent).filter(ImplantComponent.id == implant_id).first()

    def create(self, component_in: ImplantComponentCreate) -> ImplantComponent:
        db_obj = ImplantComponent(**component_in.dict())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete_demo_data(self):
        self.db.query(ImplantComponent).filter(ImplantComponent.is_demo == True).delete()
        self.db.commit()

    def count_by_type(self, component_type: str) -> int:
        return self.db.query(ImplantComponent).filter(ImplantComponent.component_type == component_type).count()
