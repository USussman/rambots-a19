from .motor import Motor

# TODO : set default speed
# TODO : determine how many pins needed
SPEED = 0


class Dribbler:
    """
    A class for a single directional motor using L298N.

    Methods
    -------
    dribble()
        sets motor to run at a predetermined speed.
    stop()
        stops dribbling
    """

    def __init__(self, speed, forward, backward):
        """
        Initialize a Motor object for dribbler.

        :param speed: speed pin number
        :param forward: forward pin number
        :param backward: backward pin number
        """

        self.motor = Motor(speed, forward, backward)

    def dribble(self):
        self.motor.run(SPEED)

    def stop(self):
        self.motor.run(0)
