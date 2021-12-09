import pickle
import time


# Script to read the internal state of the plant and print this information
# to the IoT device standard out.
while True:
    time.sleep(5)

    try:
        with open('local-plantstate.pickle', 'rb') as handle:
            data = pickle.load(handle)
            print(data)
    except Exception as e:
        pass
