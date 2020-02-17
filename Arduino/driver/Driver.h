/*
  Driver.h - Library for holomic drive with omniwheels.
  Created by Uriel M. Sussman, February 15, 2020.
*/
#ifndef Driver_h
#define Driver_h

#include "Arduino.h"
#include "Motor.h"

class Driver {
  public:
    Driver(int pins[4][3]);
    void drive(double xPower, double yPower, double rotationPower);
    void angleDrive(int angle, int velocity, int rotationPower);
    void spin(double rotationPower);
    void halt();
  private:
    double getHeading();
    
    Motor* _frontLeft;
    Motor* _backLeft;
    Motor* _backRight;
    Motor* _frontRight;
};

#endif
