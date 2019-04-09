#!/usr/bin/env python
"""
A module for interfacing with line sensors.

Classes
-------
IRSensor
    individual sensor class
LineSensor
    all sensor class
"""

import RPi.GPIO as GPIO


class IRSensor:
    """
    A class for interfacing with a single TCRT5000 IR Tracking Sensor.

    Attributes
    ----------
    on_line : bool
        whether the sensor is over the out of bounds line.
    """

    def __init__(self, channel):
        """
        Initializes pins and creates callbacks to change on_line attribute.
        :param channel: pin for input
        """
        self.channel = channel

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(channel, GPIO.RISING, callback=self._on_callback)
        GPIO.add_event_detect(channel, GPIO.FALLING, callback=self._off_callback)

    def _on_callback(self, channel):
        self.on_line = True
    
    def _off_callback(self, channel):
        self.on_line = False

    def __del__(self):
        GPIO.remove_event_detect(self.channel)
        GPIO.cleanup()


class LineSensor:
    """
    A class for interfacing with all four IR Sensors.

    Attributes
    ----------
    left : IRSensor
        left IRSensor object
    right : IRSensor
        right IRSensor object
    front : IRSensor
        front IRSensor object
    back : IRSensor
        back IRSensor object
    """

    def __init__(self, left, right, front, back):
        """
        Initializes one sensor object for each direction.

        :param left: left sensor output pin number
        :param right: right sensor output pin number
        :param front: front sensor output pin number
        :param back: back sensor output pin number
        """

        # TODO : add pin numbers
        self.left = IRSensor(left)
        self.right = IRSensor(right)
        self.front = IRSensor(front)
        self.back = IRSensor(back)
