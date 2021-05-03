from hand_tracking import start as start_hand_tracking
from gpiozero import LED


def on_hand_action(action):
    # actions: FIVE, FOUR, THREE, TWO, ONE, ROCK, SPIDERMAN, LIKE, OK, FUCK, GO
    print(f"action: {action}")


if __name__ == "__main__":
    start_hand_tracking(debug=False, on_event=on_hand_action)
