import board
import busio
import adafruit_lsm303
from math import atan2, sqrt, cos, degrees


class Compass:
    """
    A class for reading heading from LSM303

    Methods
    -------
    heading()
        :returns: heading of board
    heading2()
        :returns: heading of board
    offset()
        :returns: offset from forward direction
    """

    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_lsm303.LSM303(i2c)
        self.FORWARD = self.heading()

        self.theta = atan2(self.sensor.acceleration[0],
                                sqrt(self.sensor.acceleration[1]**2 + self.sensor.acceleration[2]**2))
        self.psi = atan2(self.sensor.acceleration[1],
                              sqrt(self.sensor.acceleration[0]**2 + self.sensor.acceleration[2]**2))

    def heading(self):
        """
        Calculate the heading of the robot with magnetic components.

        :return: heading in degrees
        """

        return degrees(atan2(self.sensor.magnetic[1], self.sensor.magnetic[0]))

    def heading2(self):
        """
        Calculate the heading of the robot adjusted by board tilt.

        :return: heading in degrees
        """

        y = self.sensor.magnetic[1] * cos(self.psi)
        x = self.sensor.magnetic[0] * cos(self.theta)
        return degrees(atan2(x, y))

    def offset(self):
        self.FORWARD - self.heading()
