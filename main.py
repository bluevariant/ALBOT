from hand_tracking import start as start_hand_tracking
from gpiozero import Device, LED
from gpiozero.pins.mock import MockFactory
from util import is_raspberrypi

# mock pin to test on pc
if not is_raspberrypi():
    Device.pin_factory = MockFactory()

# https://gpiozero.readthedocs.io/en/stable/recipes.html#pin-numbering
go_led = LED(17)
dance_led = LED(18)


def on_hand_action(action):
    # actions: FIVE, FOUR, THREE, TWO, ONE, ROCK, SPIDERMAN, LIKE, OK, FUCK, GO
    # print(f"action: {action}")

    if action == "GO":
        dance_led.off()
        go_led.on()

    if action == "ROCK" or action == "SPIDERMAN":
        go_led.off()
        dance_led.on()

    if action == "OK" or action == "FIVE":
        go_led.off()
        dance_led.off()

    print(f"is dancing: {dance_led.is_active}")
    print(f"is walking: {go_led.is_active}")


if __name__ == "__main__":
    start_hand_tracking(debug=True, on_event=on_hand_action)
