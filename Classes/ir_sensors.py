#!/usr/bin/env python
import RPi.GPIO as GPIO

class IRSensor:
    def __init__(self, channel):

        self.channel = channel

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(channel, GPIO.RISING, callback=on_callback)
        GPIO.add_event_detect(channel, GPIO.FALLING, callback=off_callback)

    def on_callback(self, channel):
        self.on_line = True
    
    def off_callback(self, channel):
        self.on_line = False

    def __del__(self):
        GPIO.remove_event_detect(self.channel)
        GPIO.output(self.out_led_pin, GPIO.HIGH)
        GPIO.cleanup()

class LineSensor:
    
    def __init__(self):
        self.left = IRSensor(0)
        self.right = IRSensor(0)
        self.front = IRSensor(0)
        self.back = IRSensor(0)