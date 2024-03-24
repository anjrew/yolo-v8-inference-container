import argparse
import cv2
from tests.client import YoloV8ImageProcessingClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image Processing Client")
    parser.add_argument(
        "--host", default="localhost", help="Server host (default: localhost)"
    )
    parser.add_argument(
        "--port", type=int, default=5000, help="Server port (default: 5000)"
    )
    parser.add_argument(
        "--camera-id", type=int, default=0, help="Camera ID (default: 0)"
    )
    parser.add_argument("--log-level", default="INFO", help="Log level (default: INFO)")

    args = parser.parse_args()

    cap = cv2.VideoCapture(args.camera_id)

    if not cap.isOpened():
        print("Failed to open camera.")
        exit()

    client = YoloV8ImageProcessingClient(args.host, args.port, args.log_level)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from camera.")
            break

        client.send_image(frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
