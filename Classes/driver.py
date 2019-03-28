#!/usr/bin/env python3
from Adafruit_MotorHAT import Adafruit_MotorHAT
import time
import atexit
import math

class Driver:
    def __init__(self):
        mh = Adafruit_MotorHAT(addr=0x60)

        self.motors = tuple(mh.getMotor(n) for n in (1, 2, 3, 4))

    def drive(self, x, y, r):

        mpowers = [0, 0, 0, 0]

        x = min(max(x, -100), 100)
        y = min(max(y, -100), 100)
        
        mpowers[0] = y + x + r
        mpowers[1] = -y + x + r
        mpowers[2] = -y - x + r
        mpowers[3] = y - x + r
        
        max_power = max(abs(m) for m in mpowers)
        
        if max_power > 0:
            scale = 255 / max_power
        else:
            scale = 0
            
        mpowers = tuple(m * scale for m in mpowers)
        
        mmode = tuple(Adafruit_MotorHAT.RELEASE if m == 0 else (Adafruit_MotorHAT.FORWARD if m > 0 else Adafruit_MotorHAT.BACKWARD) for m in mpowers)
        
        for i in range(4):
            self.motors[i].setSpeed(abs(int(mpowers[i])))
            self.motors[i].run(mmode[i])

    # rDrive(a, v, r)
    # a: angle relative to robot's front, 0-360 degrees
    # v: velocity, 0-100% of full speed
    # r: clockwise rotation, 0-100% of full speed

    def rDrive(self, a, v, r):
        rad  = (a - 90) * math.pi / 180
        x = v * math.cos(rad)
        y = v * math.sin(rad) * -1
        self.drive(int(x), int(y), r)

    # spin(r):
    # r: clockwise rotation, 0-100% of full speed
    def spin(self, r):
        self.drive(0, 0, r)

    def halt(self):
        self.drive(0, 0, 0)

