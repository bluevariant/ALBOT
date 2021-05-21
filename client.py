import cv2
import base64

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()

    if not success:
        print("Ignoring empty camera frame.")
        continue

    success, buffer = cv2.imencode(".jpg", image)

    if success:
        jpg_as_text = base64.b64encode(buffer).decode()
        print(jpg_as_text)

cap.release()
