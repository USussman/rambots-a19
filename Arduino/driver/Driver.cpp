#include "Arduino.h"
#include "Driver.h"
#include "Motor.h"

Driver::Driver(int pins[4][3]) {
  Motor _frontLeft(pins[0][0], pins[0][1], pins[0][2]);
  Motor _backLeft(pins[1][0], pins[1][1], pins[1][2]);
  Motor _backRight(pins[2][0], pins[2][1], pins[2][2]);
  Motor _frontRight(pins[3][0], pins[3][1], pins[3][2]);
}

void Driver::drive(double xPower, double yPower, double rotationPower) {
  double scale = sqrt(pow(1 - abs(rotationPower), 2) / 2);
  xPower *= scale;
  yPower *= scale;
  
  double theta = atan2(yPower, xPower) - HALF_PI;
  double magnitude = sqrt(pow(xPower, 2) + pow(yPower, 2));
  xPower = magnitude * sin(theta + M_PI_4);
  yPower = magnitude * sin(theta - M_PI_4);

  (*_frontLeft).runMotor(yPower - rotationPower);
  (*_backLeft).runMotor(xPower - rotationPower);
  (*_backRight).runMotor(yPower + rotationPower);
  (*_frontRight).runMotor(xPower + rotationPower);
}

void Driver::angleDrive(int angle, int velocity, int rotationPower) {
  angle = (angle - 90) * DEG_TO_RAD;
  double xPower = velocity * cos(angle);
  double yPower = velocity * sin(angle) * -1;
  drive(xPower, yPower, rotationPower);
}

void Driver::spin(double rotationPower) {
  drive(0, 0, rotationPower);
}

void Driver::halt() {
  drive(0, 0, 0);
}
