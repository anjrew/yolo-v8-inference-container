import socket
import struct
import os
import argparse
import logging


class ImageProcessingClient:
    def __init__(self, host: str, port: int, image_path: str, log_level: str):
        self.host = host
        self.port = port
        self.image_path = image_path
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

    def send_image(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            self.logger.info(f"Connected to server: {self.host}:{self.port}")

            # Read image data
            with open(self.image_path, "rb") as image_file:
                image_data = image_file.read()
                self.logger.debug(f"Image size: {len(image_data)} bytes")

            # Send the size of the image first
            s.sendall(struct.pack(">L", len(image_data)))
            self.logger.info("Sent image size to the server")

            # Send the image data
            s.sendall(image_data)
            self.logger.info("Sent image data to the server")

            # Receive and print the response (bounding boxes and labels)
            response = s.recv(4096)
            self.logger.info(f"Received response from the server: {response.decode()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Processing Client")
    parser.add_argument(
        "--host", default="localhost", help="Server host (default: localhost)"
    )
    parser.add_argument(
        "--port", type=int, default=5000, help="Server port (default: 5000)"
    )
    parser.add_argument(
        "--image-path",
        default=os.path.abspath("./tests/images/bus.jpg"),
        help="Path to the image file",
    )
    parser.add_argument("--log-level", default="INFO", help="Log level (default: INFO)")

    args = parser.parse_args()

    image_path = os.path.abspath(args.image_path)

    client = ImageProcessingClient(args.host, args.port, image_path, args.log_level)
    client.send_image()
