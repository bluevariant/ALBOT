import cv2
import base64
import requests
from gpiozero import Device, LED
from gpiozero.pins.mock import MockFactory
from util import is_raspberrypi
import websocket
import json
import uuid

# mock pin to test on pc
if not is_raspberrypi():
    Device.pin_factory = MockFactory()
else:
    print("raspberry pi is ready")

# https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering
GO_LED = LED(17)
DANCE_LED = LED(18)

API_END_POINT = "http://192.168.137.1:8080/call"

try:
    import thread
except ImportError:
    import _thread as thread
import time

CLIENT_ID = str(uuid.uuid4())


def on_message(ws, message):
    data = json.loads(message)

    print(f'action: {data["content"]}')


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            success, image = cap.read()

            if not success:
                print("Ignoring empty camera frame.")
                continue

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (320, 240))
            success, buffer = cv2.imencode(".jpg", image)

            if success:
                jpg_as_text = base64.b64encode(buffer).decode()

                ws.send(
                    json.dumps(
                        {
                            "to": "hand_tracker",
                            "from": CLIENT_ID,
                            "content": jpg_as_text,
                        }
                    )
                )

        cap.release()

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
