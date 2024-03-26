import abc
from typing import List, Union
import cv2
import numpy as np

from models.detection import Detection


class ObjectDetector(metaclass=abc.ABCMeta):
    """
    Abstract base class for object detection algorithms.

    This class defines the interface for performing object detection using various algorithms.
    Subclasses must implement the `get_color_for_class_name` and `detect` methods.

    Attributes:
        None
    """

    @abc.abstractmethod
    def get_color_for_class_name(self, class_name: str):
        """
        Get the color associated with a specific class name.

        Args:
            class_name: A string representing the name of the object class.

        Returns:
            The color associated with the specified class name.
        """

    @abc.abstractmethod
    def detect(
        self,
        source: Union[str, int, np.ndarray, cv2.typing.MatLike],
        confidence: float = 0.7,
        save=False,
        save_txt=False,
    ) -> List[Detection]:
        """
        Performs object detection on an image or video frame.

        Args:
            source: The source of the image or video frame to be segmented.
                Can be a file path (str), camera ID (int), or a NumPy array containing the image data.
            confidence: The minimum confidence level required for a detection to be included in the results.
            save: Whether to save the results to an image file (default=False).
            save_txt: Whether to save the results to a text file (default=False).

        Returns:
            A list of dictionaries containing the detection results.
            Each dictionary contains the following keys:
                - 'box': A list of four integers
                    [left, top, right, bottom] representing the bounding box coordinates.
                - 'mask': A NumPy array containing the segmentation mask for the detected object.
                - 'class_name': A string representing the name of the detected object class.
                - 'confidence': A float representing the confidence level of the detection.
        """
