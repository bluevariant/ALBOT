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
import websocket
import json

hands = get_hands()

try:
    import thread
except ImportError:
    import _thread as thread
import time

CLIENT_ID = "hand_tracker"


def on_message(ws, message):
    print(f"message: {message}")


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        print("ready")

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)

    ws = websocket.WebSocketApp(
        "wss://ws.dongnv.dev/",
        header={
            "identification": CLIENT_ID,
            "Origin": "dongnv.dev",
        },
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever()

# class HandAction(BaseModel):
#     image_file: FileContent = Field(..., mime_type="image/jpg", title="Image")
#
#
# class HandActionOutput(BaseModel):
#     action: str = Field(..., title="Action")
#
#
# def hand_action(
#     input: HandAction,
# ) -> HandActionOutput:
#     hand_image = Image.fromarray(
#         np.array(Image.open(io.BytesIO(input.image_file.as_bytes())))
#     )
#     hand_image = cv2.cvtColor(np.array(hand_image), cv2.COLOR_RGB2BGR)
#     hand_image = cv2.flip(hand_image, 1)
#     action = ""
#
#     cv2.imwrite(f"images/{uuid.uuid4().hex}.jpg", hand_image)
#
#     def on_event(action0):
#         action = action0
#
#         print(f"action: {action0}")
#
#     handle_hands(hands, hand_image, debug=True, on_event=on_event)
#
#     return HandActionOutput(action=action)
