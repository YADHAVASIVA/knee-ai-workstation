from enum import IntEnum

class SegmentationClass(IntEnum):
    BACKGROUND = 0
    FEMUR = 1
    TIBIA = 2
    MEDIAL_MENISCUS = 3

class ModelStatus(str):
    REAL = "real"
    DEMO = "demo"
    NOT_AVAILABLE = "not_available"
    ERROR = "error"
