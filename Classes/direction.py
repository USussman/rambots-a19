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

        self.theta = math.atan2(self.sensor.acceleration[0],
                                math.sqrt(self.sensor.acceleration[1]**2 + self.sensor.acceleration[2]**2))
        self.psi = math.atan2(self.sensor.acceleration[1],
                              math.sqrt(self.sensor.acceleration[0]**2 + self.sensor.acceleration[2]**2))
    def heading(self):
        """
        Calculate the heading of the robot with magnetic components.

        :return: heading in radians
        """

        return math.atan2(self.sensor.magnetic[1], self.sensor.magnetic[0])

    def heading2(self):
        """
        Calculate the heading of the robot adjusted by board tilt.

        :return: heading in radians
        """

        y = self.sensor.magnetic[1] * math.cos(self.psi)
        x = self.sensor.magnetic[0] * math.cos(self.theta)
        return math.atan2(x, y)
