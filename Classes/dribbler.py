import RPi.GPIO as GPIO
from motor import Motor

SPEED = 0

class Dribbler:
    def __init__(self, speed, forward, backward):
        self.motor = Motor(speed, forward, backward)

    def dribble(self):
        self.motor.run(SPEED)

    def stop(self):
        self.motor.run(0)