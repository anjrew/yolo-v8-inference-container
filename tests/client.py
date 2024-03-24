import socket
import struct
import logging
import cv2
import numpy


class YoloV8ImageProcessingClient:
    def __init__(self, host: str, port: int, log_level: str):
        self.host = host
        self.port = port
        self.logger = self.setup_logging(log_level)

    def setup_logging(self, log_level: str) -> logging.Logger:
        logger = logging.getLogger("ImageProcessingClient")
        logger.setLevel(log_level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def send_image(self, image_data: numpy.ndarray):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            self.logger.info(f"Connected to server: {self.host}:{self.port}")

            # Encode the image data as JPEG
            _, encoded_image = cv2.imencode(".jpg", image_data)
            image_bytes = encoded_image.tobytes()

            # Send the size of the image first
            image_size = len(image_bytes)
            s.sendall(struct.pack(">L", image_size))
            self.logger.info("Sent image size to the server")

            # Send the image data
            s.sendall(image_bytes)
            self.logger.info("Sent image data to the server")

            # Receive and print the response (bounding boxes and labels)
            response = s.recv(4096)
            self.logger.info(f"Received response from the server: {response.decode()}")
