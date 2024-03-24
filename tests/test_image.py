import argparse
import os

import cv2

from client import YoloV8ImageProcessingClient


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

    parser.add_argument(
        "--show-image", action="store_true", help="Show the image during processing"
    )

    args = parser.parse_args()

    image_path = os.path.abspath(args.image_path)

    show_image = args.show_image

    client = YoloV8ImageProcessingClient(args.host, args.port, args.log_level)

    image = cv2.imread(image_path)

    if show_image:
        cv2.imshow("Image", image)

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

    cv2.destroyAllWindows()

    client.send_image(image)
