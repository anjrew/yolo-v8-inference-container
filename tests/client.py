import socket
import struct
import os


def send_image(abs_image_path: str, host="localhost", port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Read image data
        with open(abs_image_path, "rb") as image_file:
            image_data = image_file.read()

        # Send the size of the image first
        s.sendall(struct.pack(">L", len(image_data)))

        # Send the image data
        s.sendall(image_data)

        # Receive and print the response (bounding boxes and labels)
        response = s.recv(4096)
        print("Received:", response.decode())


if __name__ == "__main__":
    image_path = "./tests/images/bus.jpg"  # Relative to the project root
    image_path = os.path.abspath(image_path)
    send_image(image_path)
