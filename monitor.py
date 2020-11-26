import sys
import time
import pickle
from datetime import datetime
from multiprocessing import Pool, Value

# Accessing the Firebase realtime database
import pyrebase
from config import apiKey, authDomain, databaseUrl, storageBucket

# Hardware interaction packages
import Adafruit_DHT
import Adafruit_MCP3008

# Set up temperature and humidity hardware model and pin number
temphumid_sensor = 11
temphumid_pin = 20

# Set up analogue moisture sensing hardware and digital converter
CLK = 18
MISO = 23
MOSI = 24
CS = 25
INPUT = 0
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Variables to be shared between all the processes - reading physical data and
# pushing to firebase independent processes
temp = Value('f', -1)
humid = Value('f', -1)
moist = Value('f', -1)


def update_temphumid():
    """Reads from the temperature and humidity sensor and updates the multiprocessing globals on a 
        successful read. Attempts are in batches of 10, does nothing if unsuccessful.
    """
    humidity, temperature = Adafruit_DHT.read_retry(
        temphumid_sensor, temphumid_pin)

    # Only lock and update multiprocessing globals on a successful sensor read`
    if humidity is not None and temperature is not None:
        temp.acquire()
        humid.acquire()
        temp.value = temperature
        humid.value = humidity
        # print('Temp: {0:0.1f} C  Humidity: {1:0.1f}'.format(temp.value, humid.value))
        temp.release()
        humid.release()
    else:
        print("error: UNABLE TO READ DATA")


def linear_sensoterra_map(value):
    """Takes the bit data returned by the analogue to digital converter connected to the analogue soil 
    moisture sensor and maps the value to within the sensoterra index range (0-10) as a standard
    measure of soil moisture.

    :param value: Raw bits in the range of 0 to 1024 indicating soil moisture level.
    :type value: int
    :return: Remapped soil moisture reading.
    :rtype: float
    """
    old_min = 0
    old_max = 1024
    new_min = 0
    new_max = 10
    sensoterra_value = (value - old_min)/(old_max -
                                          old_min) * (new_max - new_min) + new_min
    return sensoterra_value


def update_moisture():
    """Reads from the soil moisture sensor via the MCP3008 analogue to digital converter,
    maps raw value to the sensoterra index and updates the multiprocessing global.
    """
    moisture_reading = mcp.read_adc(INPUT)
    adjusted_reading = linear_sensoterra_map(moisture_reading)

    moist.acquire()
    moist.value = adjusted_reading
    # print("Moisture: {0:.3f}".format(moist.value))
    moist.release()


def handle_process(cmd):
    """Multiprocessing controller that coordinates the temperature and humidity reading,
    the soil moisture reading and pushing the most current plant state to firebase and
    a local binary file. Gives the time interval each process should execute within.

    :param cmd: Process to run of 'temphumid', 'moisture' or 'database'.
    :type cmd: string
    :return: Returns an error string if the cmd parameter is unrecognised.
    :rtype: string
    """

    if cmd == "temphumid":
        while True:
            update_temphumid()
            time.sleep(1)
    elif cmd == "moisture":
        while True:
            update_moisture()
            time.sleep(1)
    elif cmd == "database":
        while True:
            time.sleep(10)

            temp.acquire()
            humid.acquire()
            moist.acquire()
            if humid.value != -1 and temp.value != -1 and moist.value != -1:
                # If global state vars are not the defaults (meaning unsucessful reads),
                # create a dictionary object containing the vars and a timestamp.

                now = datetime.now()
                timestamp = datetime.timestamp(now)

                data = {
                    "temp": float(temp.value),
                    "humid": float(humid.value),
                    "moist": float(moist.value),
                    "timestamp": float(timestamp)
                }

                # Push the data point to this plant's realtime database entry
                db.child('7MBL5Bbt48NnpWcZappr').child().push(data)
                # print("Plant state saved => [ temp: {0}C\thumid: {1}% \tmoisture: {2:.3f} ]".format(temp.value, humid.value, moist.value))

                # Write this most recent state to a local file to give the motor software provisions
                # to block the watering operation if the soil is already sufficiently saturated
                try:
                    with open('local-plantstate.pickle', 'wb') as handle:
                        pickle.dump(
                            data, handle, protocol=pickle.HIGHEST_PROTOCOL)
                except Exception as e:
                    # Avoid writing plant state if motor is currently reading
                    pass

            temp.release()
            humid.release()
            moist.release()
    else:
        return "ERROR: Unrecognised command"


def fetch_data(db):
    """Helper function to pull the Firebase realtime database and parse the data
    to be suitable for graphing.

    :param db: Firebase database object.
    :type db: firebase.database
    """
    rows = db.get()

    temps = []
    humids = []
    times = []
    for row in rows.each():
        # print(row.key(), row.val())
        temps.append(row.val()['temp'])
        humids.append(row.val()['humid'])
        times.append(row.val()['timestamp'])

    print(temps)
    print(humids)
    print(times)


if __name__ == "__main__":

    # Define the certificates and database credentials of your firebase project
    # defined in config.py
    config = {
        "apiKey": apiKey,
        "authDomain": authDomain,
        "databaseURL": databaseUrl,
        "storageBucket": storageBucket
    }

    # Initialise connection and database connection
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    # Initialize multiple processes to handle sensor reading and database writing
    p = Pool(5)
    p.map(handle_process, ["temphumid", "moisture", "database"])
