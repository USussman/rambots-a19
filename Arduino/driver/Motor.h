/*
  Motor.h - Library for analog PWM motor control.
  Created by Uriel M. Sussman, February 15, 2020.
*/
#ifndef Motor_h
#define Motor_h

#include "Arduino.h"

class Motor {
  public:
    Motor(int power, int forward, int backward);
    void runMotor(int power);
    void on();
    void off();
  private:
    int _speed;
    int _forward;
    int _backward;
};

#endif
