#include "Arduino.h"
#include "Motor.h"

Motor::Motor(int power, int forward, int backward) {
  // Set class variables
  _speed = power;
  _forward = forward;
  _backward = backward;

  // configure pins
  if (_forward) {
    pinMode(_forward, OUTPUT);
    digitalWrite(_forward, LOW);
  }

  if (_backward) {
    pinMode(_backward, OUTPUT);
    digitalWrite(_backward, LOW);
  }
  
  if (_speed) {
    pinMode(_speed, OUTPUT);
    analogWrite(_speed, 0);
  }
}

void Motor::runMotor(int power) {
  // drive forward
  if (power > 0) {
    digitalWrite(_backward, LOW);
    digitalWrite(_forward, HIGH);
  }
  // drive backward
  else if (power < 0) {
    digitalWrite(_backward, HIGH);
    digitalWrite(_forward, LOW);
  }
  // stop
  else {
    digitalWrite(_backward, LOW);
    digitalWrite(_forward, LOW);
  }
  analogWrite(_speed, abs(power));
}

void Motor::on() {
  digitalWrite(_forward, HIGH);
}

void Motor::off() {
  digitalWrite(_forward, LOW);
}
