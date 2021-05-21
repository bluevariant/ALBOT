import cv2
import base64
import requests
from gpiozero import Device, LED
from gpiozero.pins.mock import MockFactory
from util import is_raspberrypi

# mock pin to test on pc
if not is_raspberrypi():
    Device.pin_factory = MockFactory()
else:
    print("raspberry pi is ready")

# https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering
GO_LED = LED(17)
DANCE_LED = LED(18)

API_END_POINT = "http://192.168.137.1:8080/call"

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            continue

        success, buffer = cv2.imencode(".jpg", image)

        if success:
            jpg_as_text = base64.b64encode(buffer).decode()
            r = requests.post(API_END_POINT, json={"image_file": jpg_as_text})

            print(f'action: {r.json()["action"]}')

    cap.release()
