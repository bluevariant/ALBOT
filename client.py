import cv2
import base64

cap = cv2.VideoCapture(0)
retval, image = cap.read()
retval, buffer = cv2.imencode(".jpg", image)
jpg_as_text = base64.b64encode(buffer).decode()
print(jpg_as_text)
cap.release()
