import RPi.GPIO as GPIO

class Motor:
    def __init__(self, speed, forward, backward):
        #GPIO.setmode()
        self.forward = forward
        self.backward = backward
        if not forward:
            GPIO.setup(forward, GPIO.OUT)
            GPIO.output(forward, GPIO.LOW)
        if not backward:
            GPIO.setup(backward, GPIO.OUT)
            GPIO.output(backward, GPIO.LOW)
        if not speed:
            self.motor = GPIO.PWM(speed, 1000)
            self.motor.start(0)

    def run(self, speed):
        if speed > 0:
            GPIO.output(self.backward, GPIO.LOW)
            GPIO.output(self.forward, GPIO.HIGH)
        elif speed < 0:
            GPIO.output(self.forward, GPIO.LOW)
            GPIO.output(self.backward, GPIO.HIGH)
        else:
            GPIO.output(self.forward, GPIO.LOW)
            GPIO.output(self.backward, GPIO.LOW)
        self.motor.ChangeDutyCycle(abs(speed))

    def on(self):
        GPIO.output(self.forward, GPIO.HIGH)

    def off(self):
        GPIO.output(self.forward, GPIO.LOW)
