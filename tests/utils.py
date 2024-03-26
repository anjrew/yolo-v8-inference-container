import cv2


def draw_detections_on_frame(frame, detections):
    """
    Draw bounding boxes and labels on the frame.
    """
    for detection in detections:
        box = detection["box"]
        class_name = detection["class_name"]
        confidence = detection["confidence"]

        # Draw the bounding box
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 0, 0), 2)

        # Put the label near the bounding box
        label = f"{class_name}: {confidence:.2f}"
        cv2.putText(
            frame,
            label,
            (box[0], box[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 0, 0),
            2,
        )
