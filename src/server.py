import socket
import struct
import cv2
import numpy as np
from typing import List, Tuple


def process_image(image_data: cv2.imread) -> List[Tuple[int, int, int, int, str]]:
    # Placeholder for image processing logic
    # Return a list of bounding boxes and labels
    # For example: [(x, y, w, h, "label"), ...]

    cv2.imshow("Image", image_data)

    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cv2.destroyAllWindows()

    return [(50, 60, 100, 200, "Example")]


def server(host="0.0.0.0", port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on {host}:{port}")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")

            # Receiving image data
            image_size = struct.unpack(">L", conn.recv(4))[
                0
            ]  # Assuming the first 4 bytes indicate the image size
            image_data = b""
            while len(image_data) < image_size:
                data = conn.recv(4096)
                if not data:
                    break
                image_data += data

            # Decode image
            nparr = np.frombuffer(image_data, np.uint8)  # type: ignore
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Process the image to get bounding boxes and labels
            bounding_boxes = process_image(image)

            # Send back the bounding boxes and labels
            response = str(bounding_boxes).encode()
            conn.sendall(response)


if __name__ == "__main__":
    server()
