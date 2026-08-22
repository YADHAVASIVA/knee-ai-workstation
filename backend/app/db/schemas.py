from pydantic import BaseModel
from typing import Optional
import datetime

class ImplantComponentBase(BaseModel):
    component_type: str
    size: str
    width: float
    ap_dimension: float

class ImplantComponentCreate(ImplantComponentBase):
    manufacturer: str = "Demonstration"
    model_name: str = "Synthetic Demo Component"
    source_type: str = "synthetic_demo"
    dataset_version: str = "demo-v1"
    is_demo: bool = True

class ImplantComponentResponse(ImplantComponentBase):
    id: str
    manufacturer: str
    model_name: str
    source_type: str
    dataset_version: str
    is_demo: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True
