import io


def is_raspberrypi():
    try:
        with io.open("/sys/firmware/devicetree/base/model", "r") as m:
            print(m.read().lower())

            if "raspberry pi" in m.read().lower():
                return True
    except Exception as e:
        print(e)
        pass
    return False
