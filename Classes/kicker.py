from .motor import Motor
import time


class Kicker:
    """
    A class for controlling solenoid using L298N object.

    Methods
    -------
    kick(power)
        Activates the solenoid.
    """
    def __init__(self, output):
        """
        :param output: pin number for connecting to motor (BCM/BOARD)
        """
        self.solenoid = Motor(False, output, False)

    def kick(self, power):
        """
        Engages solenoid.
        :param power: controls kick strength by power time
        """

        # TODO : set default power
        self.solenoid.on()
        time.sleep(power * 10)
