from typing import Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel

class ModelStatus(str, Enum):
    DEMO = "DEMO"
    EXPERIMENTAL = "EXPERIMENTAL"
    VALIDATED_RESEARCH = "VALIDATED_RESEARCH"

class ModelMetadata(BaseModel):
    model_id: str
    model_name: str
    task: str
    modality: str
    version: str
    dataset: str
    dataset_version: str
    input_size: list[int]
    preprocessing_version: str
    metrics: Dict[str, float]
    license: str
    status: ModelStatus
    weights_path: Optional[str] = None
    training_configuration: Optional[Dict[str, Any]] = None
    validation_configuration: Optional[Dict[str, Any]] = None

class ModelRegistry:
    _registry: Dict[str, ModelMetadata] = {}

    @classmethod
    def register(cls, metadata: ModelMetadata):
        cls._registry[metadata.model_id] = metadata

    @classmethod
    def get_model(cls, model_id: str) -> Optional[ModelMetadata]:
        return cls._registry.get(model_id)

    @classmethod
    def get_models_by_task(cls, task: str) -> list[ModelMetadata]:
        return [m for m in cls._registry.values() if m.task == task]

# NO DEMO MODELS REGISTERED HERE ANYMORE.
# The system requires a real model to be present in models/xray/...
