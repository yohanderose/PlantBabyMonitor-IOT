import time
import RPi.GPIO as GPIO

class Motor():
    def __init__(self, pin) -> None:
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.off()

    def on(self):
        self.active = True
        GPIO.output(self.pin, 1)

    def off(self):
        self.active = False
        GPIO.output(self.pin, 0)

    def loop(self):
        while True:
            time.sleep(1)
            self.on()
            time.sleep(1)
            self.off()

