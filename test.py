import glob
import cv2
from hand_tracking import get_hands, handle_hands

hands = get_hands()

for file in glob.glob("images1/*.jpg"):
    image = cv2.imread(file)

    def on_event(action):
        print(f"action: {action}")

    handle_hands(hands, image, debug=False, on_event=on_event)
