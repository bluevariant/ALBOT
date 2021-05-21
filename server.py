import io
from pydantic import BaseModel, Field
from PIL import Image
import numpy as np
from opyrator.components.types import FileContent
import cv2
from hand_tracking import get_hands, handle_hands
import uuid
import websocket
import json
from io import StringIO
import base64

try:
    import thread
except ImportError:
    import _thread as thread
import time

hands = get_hands()

CLIENT_ID = "hand_tracker"


def on_message(ws, message):
    data = json.loads(message)
    imgdata = base64.b64decode(data["content"])
    image = Image.fromarray(np.array(Image.open(io.BytesIO(imgdata))))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    def on_event(action):
        print(f"action: {action}")

        ws.send(
            json.dumps(
                {
                    "to": data["from"],
                    "from": CLIENT_ID,
                    "content": action,
                }
            )
        )

    handle_hands(hands, image, debug=False, on_event=on_event)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        print("ready")

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(False)

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
