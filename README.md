# Yolo V8 Inference Container

A project with code enabling inference on video feed from within a docker container

# Getting Started

1. [Setup your development environment](./docs/setting_up_the_environment.md).

# Running the Server

## Docker 

### Build the docker image
```bash
docker build -t yolo-v8-inference -f docker/Dockerfile.Tcp .
```

### Run the docker container
```bash
docker run -it --rm --name yolo-v8-inference -p 5000:5000 yolo-v8-inference
```

# Use the example client

To see how to interact with the server, you can use the example client in the [`test`](./tests/) directory.

## Test an image

```bash
python tests/test_image.py
```

## Test a video

```bash
python tests/test_camera.py
```