import sys
import time
import pickle
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn


class MoistureSensor():
    def __init__(self) -> None:
        # CLK = 11
        # MISO = 9
        # MOSI = 10
        # CS = 25
        # INPUT_PIN = 0
        
        # create the spi bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        
        # create the cs (chip select)
        cs = digitalio.DigitalInOut(board.D25)
        
        # create the mcp object
        mcp = MCP.MCP3008(spi, cs)
        
        # create an analog input channel on pin 0
        self.chan = AnalogIn(mcp, MCP.P0)
        self.read()

    def read(self):
        """Reads from the soil moisture sensor via the MCP3008 analogue to digital converter,
        maps raw value to the sensoterra index and updates the multiprocessing global.
        """
        moisture_reading = self.chan.value
        self.adjusted_reading = self.linear_sensoterra_map(moisture_reading)
        return self.adjusted_reading


    def linear_sensoterra_map(self, value):
        """Takes the bit data returned by the analogue to digital converter connected to the analogue soil 
        moisture sensor and maps the value to within the sensoterra index range (0-10) as a standard
        measure of soil moisture.

        :param value: Raw bits in the range of 0 to 1024 indicating soil moisture level.
        :type value: int
        :return: Remapped soil moisture reading.
        :rtype: float
        """
        old_min = 0
        old_max = 65472
        new_min = 0
        new_max = 10
        sensoterra_value = (value - old_min)/(old_max -
                                              old_min) * (new_max - new_min) + new_min
        return sensoterra_value

    def loop(self):
        while True:
            time.sleep(.5)
            print(self.read())



