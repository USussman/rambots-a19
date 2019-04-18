#!/usr/bin/env python
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
        GPIO.output(self.out_led_pin, GPIO.HIGH)
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

    def __init__(self):
        """
        Initializes one sensor object for each direction.
        """

        # TODO : add pin numbers
        self.left = IRSensor(0)
        self.right = IRSensor(0)
        self.front = IRSensor(0)
        self.back = IRSensor(0)