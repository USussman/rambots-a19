from .direction import Compass
from .driver import Driver
from .kicker import Kicker
from .dribbler import Dribbler
from .finder import Camera
from .ir_sensors import LineSensor
from . import pins


CAPTURING_TOLERANCE = 30 # degrees
APPROACH_BUFFER = 25 # centimeters

GOTCHA_TOLERANCE = 10 # degrees
GOTCHA_BUFFER = 1 # in centimeters


class Director:
    def __init__(self):
        self.eyes = Camera()
        self.legs = Driver()
        self.navigator = Compass()
        self.lookout = LineSensor(*pins.line_sensors)
        self.kicker = Kicker(pins.kicker)
        self.dribbler = Dribbler(*pins.dribbler)

    def direct(self):
        while True:
            self.striker()

    def striker(self):
        rho = self.eyes.distance
        theta = self.eyes.direction
        comp_offset = (180 - abs(180 - theta))

        # control dribbler
        if comp_offset < CAPTURING_TOLERANCE:
            self.dribbler.dribble()
        else:
            self.dribbler.stop()

        if rho < GOTCHA_BUFFER and comp_offset < GOTCHA_TOLERANCE:
            # we have the ball
            self.legs.drive_angle(0, 100)
        elif rho < APPROACH_BUFFER and comp_offset > CAPTURING_TOLERANCE:
            # Circumnavigate ball
            self.legs.drive_angle(theta + 90 if theta < 180 else theta - 90)
        else:
            self.legs.drive_angle(theta, 100)

    def goalie(self):



if __name__ == '__main__':
    the_director = Director()
    the_director.direct()
