from direction import Compass
from driver import Driver
from finder import Camera
from ir_sensors import LineSensor


class Director:
    def __init__(self):
        self.eyes = Camera()
        self.legs = Driver()
        self.lookout = LineSensor()
        self.navigator = Compass()
    
    def direct(self):
        while True:
            ...

if __name__ == '__main__':
    the_director = Director()
    the_director.direct()
