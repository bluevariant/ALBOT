import io
from pydantic import BaseModel, Field
from PIL import Image
import numpy as np
from opyrator.components.types import FileContent
import uuid
import cv2
import numpy as np
from hand_tracking import get_hands, handle_hands
import uuid

hands = get_hands()


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
    hand_image = cv2.flip(hand_image, 1)
    action = ""

    cv2.imwrite(f"images/{uuid.uuid4().hex}.jpg", hand_image)

    def on_event(action0):
        action = action0

        print(f"action: {action0}")

    handle_hands(hands, hand_image, debug=True, on_event=on_event)

    return HandActionOutput(action=action)
