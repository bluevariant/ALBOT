from hand_tracking import start as start_hand_tracking


def on_hand_action(action):
    print(f"action: {action}")


if __name__ == "__main__":
    start_hand_tracking(debug=False, on_event=on_hand_action)
