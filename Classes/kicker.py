from motor import motor
import time

class Kicker:
    def __init__(self, forward):
        self.solenoid = Motor(False, forward, False)

    def kick(self, power):
        self.solenoid.on()
        time.sleep(power * 10)