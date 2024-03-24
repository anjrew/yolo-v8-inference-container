import socket
import struct
import cv2
import numpy as np
import logging
from typing import List, Tuple

from services.i_object_detector import ObjectDetector


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
        self.logger = self.setup_logging(log_level)

    def setup_logging(self, log_level: str) -> logging.Logger:
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(log_level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def process_image(
        self, image_data: cv2.typing.MatLike
    ) -> List[Tuple[int, int, int, int, str]]:
        """Process the image to get bounding boxes and labels
        as a tuple of (x, y, w, h, label)

        """

        if self.show_image:
            cv2.imshow("Image", image_data)

            while True:
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

            cv2.destroyAllWindows()

        return self.object_detector.detect(image_data)  # type: ignore

    def run(self) -> None:
        """
        Run the image processing server.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            self.logger.info(f"Server listening on {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                with conn:
                    self.logger.info(f"Connected by {addr}")

                    # Receiving image data
                    image_size = struct.unpack(">L", conn.recv(4))[
                        0
                    ]  # Assuming the first 4 bytes indicate the image size
                    self.logger.debug(f"Received image size: {image_size} bytes")

                    image_data = b""
                    while len(image_data) < image_size:
                        data = conn.recv(4096)
                        if not data:
                            break
                        image_data += data

                    # Decode image
                    nparr = np.frombuffer(image_data, np.uint8)  # type: ignore
                    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                    self.logger.info("Processing image...")

                    # Process the image to get bounding boxes and labels
                    bounding_boxes = self.process_image(image)

                    self.logger.info("Image processing completed")

                    # Send back the bounding boxes and labels if requested
                    if self.return_coordinates:
                        response = str(bounding_boxes).encode()
                        conn.sendall(response)
                        self.logger.info("Bounding box coordinates sent to the client")
