from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
import datetime
import uuid

from app.db.session import Base

class ImplantComponent(Base):
    __tablename__ = "implant_components"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    component_type = Column(String, index=True, nullable=False) # "femoral" or "tibial"
    size = Column(String, index=True, nullable=False)
    
    width = Column(Float, nullable=False)
    ap_dimension = Column(Float, nullable=False)
    
    manufacturer = Column(String, default="Demonstration")
    model_name = Column(String, default="Synthetic Demo Component")
    
    source_type = Column(String, default="synthetic_demo")
    dataset_version = Column(String, default="demo-v1")
    is_demo = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
