import io
from pydantic import BaseModel, Field
from PIL import Image
import numpy as np
from opyrator.components.types import FileContent
import uuid
import cv2
import numpy as np


class HandAction(BaseModel):
    image_file: FileContent = Field(..., mime_type="image/jpg", title="Image")


class HandActionOutput(BaseModel):
    action: str = Field(..., title="Action")


def hand_action(
    input: HandAction,
) -> HandActionOutput:
    hand_image = Image.fromarray(
        np.array(Image.open(io.BytesIO(input.image_file.as_bytes())))
    )
    hand_image = cv2.cvtColor(np.array(hand_image), cv2.COLOR_RGB2BGR)
    action = ""

    return HandActionOutput(action=action)
