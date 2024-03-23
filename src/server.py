import socket
import struct
import cv2
import numpy as np
import argparse
import logging
from typing import List, Tuple


class ImageProcessingServer:
    def __init__(
        self,
        host: str,
        port: int,
        show_image: bool,
        return_coordinates: bool,
        log_level: str,
    ):
        self.host = host
        self.port = port
        self.show_image = show_image
        self.return_coordinates = return_coordinates
        self.logger = self.setup_logging(log_level)

    def setup_logging(self, log_level: str) -> logging.Logger:
        logger = logging.getLogger("ImageProcessingServer")
        logger.setLevel(log_level)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def process_image(
        self, image_data: cv2.imread
    ) -> List[Tuple[int, int, int, int, str]]:
        # Placeholder for image processing logic
        # Return a list of bounding boxes and labels
        # For example: [(x, y, w, h, "label"), ...]

        if self.show_image:
            cv2.imshow("Image", image_data)

            while True:
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

            cv2.destroyAllWindows()

        return [(50, 60, 100, 200, "Example")]

    def run_server(self):
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Processing Server")
    parser.add_argument(
        "--host", default="0.0.0.0", help="Server host (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=5000, help="Server port (default: 5000)"
    )
    parser.add_argument(
        "--show-image", action="store_true", help="Show the image during processing"
    )
    parser.add_argument(
        "--return-coordinates",
        action="store_true",
        help="Return the bounding box coordinates",
        default=True,
    )
    parser.add_argument("--log-level", default="INFO", help="Log level (default: INFO)")

    args = parser.parse_args()

    server = ImageProcessingServer(
        args.host, args.port, args.show_image, args.return_coordinates, args.log_level
    )
    server.run_server()
