from direction import Compass
from driver import Driver
from kicker import Kicker
from dribbler import Dribbler
from finder import Camera
from ir_sensors import LineSensor
import pins


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
            ...


if __name__ == '__main__':
    the_director = Director()
    the_director.direct()
