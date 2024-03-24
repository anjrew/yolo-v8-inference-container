from dataclasses import dataclass
import json
from typing import Dict, Tuple, Union, cast


@dataclass
class Detection:
    """A class to represent a detection of an object in an image."""

    box: Tuple[int, int, int, int]
    """Top right bottom left coordinates of the bounding box."""

    class_name: str
    """The name of the class of the detected object."""

    confidence: int
    """The confidence of the classification."""

    def to_dict(
        self,
    ) -> Dict[str, Union[Tuple[int, int, int, int], str, int]]:
        return {
            "box": self.box,
            "class_name": self.class_name,
            "confidence": self.confidence,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_vector(
        self,
    ) -> Tuple[int, int, int, int, float, str]:
        return (*self.box, self.confidence, self.class_name)

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Union[Tuple[int, int, int, int], str, int]],
    ) -> "Detection":
        # Asserting the type of `box`
        if not isinstance(data.get("box"), tuple) or not all(
            isinstance(item, int) for item in cast(Tuple, data["box"])
        ):
            raise ValueError(
                f"The 'box' field must be a tuple of ints, got {type(data.get('box'))} with values {data.get('box')}"
            )

        # Asserting the type of `class_name`
        if not isinstance(data.get("class_name"), str):
            raise ValueError(
                f"The 'class_name' field must be a string, got {type(data.get('class_name'))}"
            )

        # Asserting the type of `confidence`
        if not isinstance(data.get("confidence"), int):
            raise ValueError(
                f"The 'confidence' field must be a int, got {type(data.get('confidence'))}"
            )

        return cls(
            box=cast(Tuple[int, int, int, int], data["box"]),
            class_name=cast(str, data["class_name"]),
            confidence=cast(int, data["confidence"]),
        )

    @classmethod
    def from_vector(cls, vector: Tuple[int, int, int, int, int, str]) -> "Detection":
        if len(vector) != 6:
            raise ValueError(
                "Vector must be a tuple of 6 elements (top, right, bottom, left, confidence, class_name)"
            )
        box = vector[:4]  # Extract the box coordinates
        confidence = vector[4]  # Extract the confidence
        class_name = vector[5]  # Extract the class name
        return cls(box=box, class_name=class_name, confidence=confidence)
