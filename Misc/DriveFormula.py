#!/usr/bin/env python3

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
 
import time
import atexit
import math

mh = Adafruit_MotorHAT(addr=0x60)

motor1 = mh.getMotor(1)
motor2 = mh.getMotor(2)
motor3 = mh.getMotor(3)
motor4 = mh.getMotor(4)

def drive(x, y, r):
    if x > 100:
        x = 100
    elif x < -100:
        x = -100
    
    if y > 100:
        y = 100
    elif y < -100:
        y = -100
    
    m1 = y + x + r
    m2 = (-1 * y) + x + r
    m3 = (-1 * y) + (-1 * x) + r
    m4 = y + (-1 * x) + r
    
    max = 0
    if abs(m1) > max:
        max = abs(m1)
    if abs(m2) > max:
        max = abs(m2)
    if abs(m3) > max:
        max = abs(m3)
    if abs(m4) > max:
        max = abs(m4)
    
    if max > 0:
        scale = 1
        if max > 100:
            scale = 1 / (max / 100.0)
        
        scale *= 2.55
        m1 *= scale
        m2 *= scale
        m3 *= scale
        m4 *= scale
    
    d1 = Adafruit_MotorHAT.RELEASE if m1 == 0 else (Adafruit_MotorHAT.FORWARD if m1 > 0 else Adafruit_MotorHAT.BACKWARD)
    d2 = Adafruit_MotorHAT.RELEASE if m2 == 0 else (Adafruit_MotorHAT.FORWARD if m2 > 0 else Adafruit_MotorHAT.BACKWARD)
    d3 = Adafruit_MotorHAT.RELEASE if m3 == 0 else (Adafruit_MotorHAT.FORWARD if m3 > 0 else Adafruit_MotorHAT.BACKWARD)
    d4 = Adafruit_MotorHAT.RELEASE if m4 == 0 else (Adafruit_MotorHAT.FORWARD if m4 > 0 else Adafruit_MotorHAT.BACKWARD)
    
    motor1.setSpeed(abs(int(m1)))
    motor2.setSpeed(abs(int(m2)))
    motor3.setSpeed(abs(int(m3)))
    motor4.setSpeed(abs(int(m4)))
    
    motor1.run(d1)
    motor2.run(d2)
    motor3.run(d3)
    motor4.run(d4)

# rDrive(a, v, r)
# a: angle relative to robot's front, 0-360 degrees
# v: velocity, 0-100% of full speed
# r: clockwise rotation, 0-100% of full speed

def rDrive( a, v, r):
    rad  = (a - 90) * math.pi / 180
    x = v * math.cos(rad)
    y = v * math.sin(rad) * -1
    drive(int(x), int(y), r)

# spin(r):
# r: clockwise rotation, 0-100% of full speed
def spin(r):
    drive(0, 0, r)

def halt():
    drive(0, 0, 0)

