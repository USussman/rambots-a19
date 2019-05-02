from direction import Compass
from driver import Driver
from kicker import Kicker
from dribbler import Dribbler
from finder import Camera
from ir_sensors import LineSensor
import pins


CAPTURING_TOLERANCE = 30 # degrees
APPROACH_BUFFER = 25 # centimeters


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
            rho = self.eyes.distance
            theta = self.eyes.direction
            comp_offset = 180 - theta
            if theta > 180:
                theta -= 360
            if (180 - abs(180 - theta)) < CAPTURING_TOLERANCE:
                self.legs.drive_angle(theta, 100, 0)
            elif rho < APPROACH_BUFFER:
                # Circumnavigate ball
                if theta > 0:
                    self.legs.drive_angle(theta + 90)
            else:
                ...


if __name__ == '__main__':
    the_director = Director()
    the_director.direct()
