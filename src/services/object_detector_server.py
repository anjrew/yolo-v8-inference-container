import json
import socket
import struct
import cv2
import numpy as np
import logging
from typing import List

from models.detection import Detection
from services.i_object_detector import ObjectDetector

LOGGER = logging.getLogger(__name__)


class ObjectDetectionServer:
    def __init__(
        self,
        object_detector: ObjectDetector,
        host: str,
        port: int,
        show_image: bool,
        return_coordinates: bool,
        log_level: str,
    ):
        self.object_detector = object_detector
        self.host = host
        self.port = port
        self.show_image = show_image
        self.return_coordinates = return_coordinates

    def process_image(self, image_data: cv2.typing.MatLike) -> List[Detection]:
        """Process the image to get bounding boxes and labels
        as a tuple of (top, right, bottom, left, label)

        """

        if self.show_image:
            cv2.imshow("Image", image_data)

            while True:
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

            cv2.destroyAllWindows()

        return self.object_detector.detect(image_data)

    def run(self) -> None:
        """
        Run the image processing server.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            LOGGER.info(f"Server listening on {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                with conn:
                    LOGGER.info(f"Connected by {addr}")

                    # Receiving image data
                    image_size = struct.unpack(">L", conn.recv(4))[
                        0
                    ]  # Assuming the first 4 bytes indicate the image size
                    LOGGER.debug(f"Received image size: {image_size} bytes")

                    image_data = b""
                    while len(image_data) < image_size:
                        data = conn.recv(4096)
                        if not data:
                            break
                        image_data += data

                    # Decode image
                    nparr = np.frombuffer(image_data, np.uint8)  # type: ignore
                    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                    LOGGER.debug("Processing image...")

                    # Process the image to get bounding boxes and labels
                    detections = self.process_image(image)

                    LOGGER.debug("Image processing completed")

                    # Send back the bounding boxes and labels if requested
                    if self.return_coordinates:
                        response = json.dumps(
                            [detection.to_dict() for detection in detections]
                        ).encode()
                        conn.sendall(response)
                        LOGGER.debug("Bounding box coordinates sent to the client")
