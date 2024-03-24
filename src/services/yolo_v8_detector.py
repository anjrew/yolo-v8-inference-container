"""
This module contains the implementation of the YoloObjectDetector class,
which is used to detect objects of multiple types using YOLOv8.

The YoloObjectDetector class inherits from the ObjectDetector class
and provides methods for detecting objects in images or video frames using the YOLOv8 model.

Example usage:
    detector = YoloObjectDetector(model_name="yolov8n.pt")
    results = detector.detect(source="image.jpg", confidence=0.7, save=True, save_txt=True)
    for result in results:
        print(result)

Note: This module requires the ultralytics and OpenCV libraries to be installed.

"""

import logging
import time
from typing import Dict, List, Tuple, Union, cast
import numpy as np
from numpy.typing import NDArray
from ultralytics import YOLO
from services.i_object_detector import ObjectDetector

LOGGER = logging.getLogger(__name__)


class YoloObjectDetector(ObjectDetector):
    """Detect objects of multiple types Using YOLOv8"""

    def __init__(self, model_name: str = "yolov8n.pt") -> None:
        self.model = YOLO(model_name)  # load an official model
        self.class_names = cast(Dict[str, str], self.model.names or {})
        LOGGER.debug("Detecting from : %s", self.class_names)
        self.colors: NDArray[np.float64] = np.random.uniform(
            0, 255, size=(len(self.class_names), 3)
        )
        self._class_name_id = {v: k for k, v in self.class_names.items()}

    def get_color_for_class_name(self, class_name: str) -> Tuple[int, int, int]:
        return self.colors[self._class_name_id[class_name]]  # type: ignore

    def detect(
        self,
        source: Union[str, int, np.ndarray],
        confidence: float = 0.7,
        save=False,
        save_txt=False,
    ) -> List[dict]:
        start_detect_time = time.time()
        res: List[dict] = []

        detections = self.model.predict(
            source, save=save, save_txt=save_txt, conf=confidence
        )

        for detection in detections:
            if hasattr(detection, "boxes") and detection.boxes:
                #   boxes (torch.Tensor) or (numpy.ndarray): A tensor or numpy array containing the detection boxes,
                bxs = detection.boxes
                for i, box in enumerate(bxs):  # type: ignore
                    #   with shape (num_boxes, 6). The last two columns should contain confidence and class values.
                    box = box.data.tolist()[0]
                    # Extract the height, width, top, bottom, left, and right values
                    lft = box[0]
                    tp = box[1]
                    rt = box[2]
                    btm = box[3]
                    confidence = box[4]

                    rlt = {
                        "box": [int(lft), int(tp), int(rt), int(btm)],
                        "class_name": self.class_names[int(box[5])],  # type: ignore
                        "confidence": box[4],
                    }
                    if detection.masks:
                        rlt["mask"] = detection.masks[i].numpy().data

                    res.append(rlt)
        LOGGER.debug(
            "Image detection time: %s seconds", lambda: time.time() - start_detect_time
        )
        return res
