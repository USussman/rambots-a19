import board
import busio
import adafruit_lsm303
import math


class Compass:
    """
    A class for reading heading from LSM303

    Methods
    -------
    heading()
        :returns: heading of board
    """
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_lsm303.LSM303(i2c)
    
    def heading(self):
        return math.atan2(self.sensor.magnetic[1], self.sensor.magnetic[0])