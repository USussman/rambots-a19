from direction import Compass
from driver import Driver
from finder import Camera
from ir_sensors import IRSensor


class Director:
    def __init__():
        self.eyes = Camera()
        self.legs = Driver()
        self.ir = IRSensor()
        self.navigator = Compass()
    
    def direct(self):
        while True:
            ...

if __name__ == '__main__':
    the_director = Director()
    the_director.direct()
