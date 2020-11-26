from flask_restful import Resource, Api, request
from flask import Flask, jsonify
import sys
import time
import pickle

# Hardware interaction packages
import RPi.GPIO as GPIO
import signal


# Overlook common GPIO errors
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


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


def needs_water():
    """Check the plant's current state from the local pickle and verify if the plant requires water.

    :return: True if plant moisture is less than 6.5 (optimal), False if already optimal or above.
    :rtype: bool
    """
    try:
        with open('local-plantstate.pickle', 'rb') as handle:
            data = pickle.load(handle)

            if data['moist'] > 6.5:
                return False
            return True
    except Exception as e:
        # Handle read when monitor is writing currently
        pass

    return False


# Set up singal handler and motor pin
signal.signal(signal.SIGINT, signal_handler)
GPIO.setmode(GPIO.BCM)
motor = 21
GPIO.setup(motor, GPIO.OUT)
activ = False


# Instantiate the API
app = Flask(__name__)
api = Api(app)


class Waterer(Resource):
    """API resource that handles incoming requests to turn the motor on.

    :param Resource: Inherit from the flask API object.
    :type Resource: flask_restful.Resource
    """

    def __init__(self):
        # Make sure motor is off on initialisation
        GPIO.output(motor, 0)

    def get(self):
        # global activ
        # activ = not activ

        response = {}

        # If soil moisture is below optimal, trigger the pump for three seconds.
        # Return the valid or fail response to the client.
        if needs_water():
            # print("PUMP TRIGGERED")
            GPIO.output(motor, 1)
            time.sleep(3)
            GPIO.output(motor, 0)
            # print("PUMP OFF")
            response = {'pump_water': ['done']}
        else:
            response = {'pump_water': ['not needed']}

        return jsonify(response)


# Create routes to interface with the application
api.add_resource(Waterer, '/')

# Run the application
if __name__ == '__main__':
    app.run()
