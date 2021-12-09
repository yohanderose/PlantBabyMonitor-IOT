import sys
import time
from motor import Motor
from temphumid import TempHumidSensor
from moisture import MoistureSensor
import RPi.GPIO as GPIO
import signal
import board
from concurrent.futures import ThreadPoolExecutor

MOTOR_PIN = 21
TEMPHUMID_PIN = board.D26
temp = 0
humid = 0
moist = 0

def signal_handler(sig, frame):
    """Deallocate active GPIO pin on sudden exit.

    :param sig: Receive signal code when user hits ctrl+c
    :type sig: int
    :param frame: Current program state.
    :type frame: dict
    """

    print("Exiting...")
    GPIO.cleanup()
    sys.exit(0)

def handler(cmd):
    global temp, humid, moist

    if cmd == "temphumid":
        temphumid_sensor = TempHumidSensor(TEMPHUMID_PIN)
        while True:
            time.sleep(1)
            t, h = temphumid_sensor.read()
            if t != None and h != None:
                temp, humid = t, h

    elif cmd == "moisture":
        moisture_sensor = MoistureSensor()
        while True:
            time.sleep(1)
            moist = moisture_sensor.read()

    elif cmd == "pump":
        pump = Motor(MOTOR_PIN)
        while True:
            time.sleep(2)
            if moist < 6:
                print("{}C\t{}% humidity\t{} soil moisture".format(temp, humid, moist))
    else:
        sys.exit("Command not found")

def main():
    signal.signal(signal.SIGINT, signal_handler)

    cmds = "temphumid moisture pump".split()
    with ThreadPoolExecutor(max_workers=3) as exe:
        exe.map(handler, cmds)

if __name__ == "__main__":
    main()

