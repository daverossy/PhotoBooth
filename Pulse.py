import time
import RPi.GPIO as gpio

# Pulse Thread - Used to pulse the LED without slowing down the rest
def pulse(threadName, *args):
    gpio.setup(17, gpio.OUT)

    while closeme:
        global LEDon
        # Print LED on
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
