""" Tests the object detection container on a camera feed"""

import argparse
import logging
import time
import cv2
from client import YoloV8ImageProcessingClient
from utils import draw_detections_on_frame

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Real-time Image Processing Client")

    parser.add_argument(
        "--host", default="localhost", help="Server host (default: localhost)"
    )
    parser.add_argument(
        "--port", type=int, default=5000, help="Server port (default: 5000)"
    )
    parser.add_argument(
        "--show-image", action="store_true", help="Show the image during processing"
    )
    parser.add_argument(
        "--log-level",
        default="DEBUG",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Log level (default: DEBUG)",
    )

    args = parser.parse_args()

    LOGGER = logging.getLogger(__name__)
    log_level = args.log_level.upper()
    LOGGER.setLevel(getattr(logging, log_level))

    # Add a StreamHandler to print logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    LOGGER.addHandler(console_handler)

    show_image = args.show_image
    client = YoloV8ImageProcessingClient(args.host, args.port, args.log_level)

    # Start capturing from the camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        LOGGER.error("Could not open video device")
        exit()

    try:
        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                LOGGER.error("Failed to capture frame")
                break

            start_time = time.time()
            detections = client.get_image_detections(frame)
            total_request_time = time.time() - start_time
            LOGGER.debug("Total request time: %.6f seconds", total_request_time)

            draw_detections_on_frame(frame, detections)

            # Display the resulting frame
            cv2.imshow("Frame", frame)

            # Press Q on keyboard to exit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
