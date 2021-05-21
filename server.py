from face_aligner2 import save_align_face
import io
from pydantic import BaseModel, Field
from PIL import Image
import numpy as np
from opyrator.components.types import FileContent
import uuid


class HandAction(BaseModel):
    image_file: FileContent = Field(..., mime_type="image/jpg", title="Hand Image")


class HandActionOutput(BaseModel):
    action: str = Field(..., title="Action")


def hand_action(
    input: HandAction,
) -> HandActionOutput:
    hand_image = Image.fromarray(
        np.array(Image.open(io.BytesIO(input.image_file.as_bytes())))
    )
    return HandActionOutput(action=action)
