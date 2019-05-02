#!/usr/bin/env python3
"""
Driver class module

Classes
-------
Driver
    interface with wheels for holonomic drive
"""

from motor import Motor
import math


class Driver:
    """
    A class for driving the robot.

    Methods
    -------
    drive(x, y, r)
        drive with directional components and rotation.
    rDrive(a, v, r)
        wrapper on drive for angle, velocity, rotation
    spin(r)
        wrapper to rotate at given speed
    halt()
        drive wrapper to stop robot
    """

    def __init__(self, *pins):
        """
        Creates motor object attributes.
        """

        self.motors = tuple(Motor(*pin_set) for pin_set in pins)

    def drive(self, x, y, r):
        """
        Drive the robot with direction components.

        :param x: x velocity
        :param y: y velocity
        :param r: rotation
        """

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

        for i in range(4):
            self.motors[i].run(mpowers[i])

    def drive_angle(self, a, v, r):
        """
        Wrapper for driving in direction at speed.

        :param a: angle relative to robot's front, 0-360 degrees
        :param v: velocity, 0-100% of full speed
        :param r: clockwise rotation, 0-100% of full speed
        """

        rad  = (a - 90) * math.pi / 180
        x = v * math.cos(rad)
        y = v * math.sin(rad) * -1
        self.drive(int(x), int(y), r)

    def spin(self, r):
        """
        Spin the robot on spot

        :param r: clockwise rotation, 0-100% of full speed
        """

        self.drive(0, 0, r)

    def halt(self):
        """
        Stops all wheels.
        """

        self.drive(0, 0, 0)

    def drive_angle2(self, a, v, r, offset):
        """
        Wrapper for rotating while driving in a straight line

        :param a: angle relative to forward direction, 0-360 degrees
        :param v: velocity, 0-100% of full speed
        :param r: clockwise rotation, 0-100% of full speed
        :param offset: offset from forward from compass
        """

        self.drive_angle((a + offset) % 360, v, r)
