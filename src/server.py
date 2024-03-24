import argparse

from services.object_detector_server import ObjectDetectionServer
from services.yolo_v8_detector import YoloObjectDetector


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

    obj_detector = YoloObjectDetector()

    server = ObjectDetectionServer(
        obj_detector,
        args.host,
        args.port,
        args.show_image,
        args.return_coordinates,
        args.log_level,
    )
    server.run()
