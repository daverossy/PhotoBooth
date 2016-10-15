# Pulse Thread - Used to pulse the LED without slowing down the rest
def pulse(threadName, *args):
    # gpio.setmode(gpio.BCM)
    global gpio
    gpio.setup(17, gpio.OUT)

    # print timepulse
    while closeme:
        global LEDon

        # print LEDon

        if timepulse == 999:
            gpio.output(17, False)
            LEDon = True
        else:
            if LEDon:
                gpio.output(17, True)
                time.sleep(timepulse)
                LEDon = False
            else:
                gpio.output(17, False)
                time.sleep(timepulse)
                LEDon = True
