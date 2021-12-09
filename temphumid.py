import adafruit_dht
import board
import time

class TempHumidSensor():
    def __init__(self, ada_pin) -> None:
        self.pin = ada_pin
        self.sensor = adafruit_dht.DHT11(self.pin, use_pulseio=False)

    def read(self) -> tuple:
        try:
            # Print the values to the serial port
            temp = self.sensor.temperature
            humidity = self.sensor.humidity
            return temp, humidity

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
        except Exception as error:
            self.sensor.exit()
            raise error

        return None, None

    def loop(self):
        while True:
            time.sleep(1)
            print(self.read())
            

