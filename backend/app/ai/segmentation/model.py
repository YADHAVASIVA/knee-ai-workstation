from abc import ABC, abstractmethod
import numpy as np

class SegmentationModel(ABC):
    @abstractmethod
    def load(self) -> None:
        pass

    @abstractmethod
    def predict(self, image_array: np.ndarray) -> np.ndarray:
        """
        Takes an image array and returns a segmentation mask of the same width/height
        with class values defined in SegmentationClass.
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass

    @abstractmethod
    def get_model_info(self) -> dict:
        pass
