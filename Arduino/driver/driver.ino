/*
  driver.ino - A sketch for arduino based I2C motor controller.
  Created by Uriel M. Sussman, February 16, 2020.
  Property of Rambam Rambots 2020.
*/

// Built-in libraries
#include <Arduino.h>
#include <Wire.h>

// 3rd party libraries
#include <PID_v1.h>
#include <Adafruit_LSM303DLH_Mag.h>

// in-house libraries
#include "Driver.h"

//// Magnetometer setup
// Assign a unique ID to this sensor at the same time
Adafruit_LSM303DLH_Mag_Unified mag = Adafruit_LSM303DLH_Mag_Unified(12345);

// create event variable
sensors_event_t event;

// create axis variables
double x, y;

//// PID setup
// declare PID variables
double Setpoint, Input, Output;

// Specify the links and initial tuning parameters
// and create PID object
PID myPID(&Input, &Output, &Setpoint, 2, 5, 1, DIRECT);

//// Driver setup
// set pin numbers
// TODO: get pin numbers
int pins[4][3] = {{0,0,0},{0,0,0},{0,0,0},{0,0,0}};

// initialize driver object
Driver driver(pins);

// declare drive variables
double angle, velocity, desiredOrientation;

//// I2C handling variables
byte ireg = 0;


// Calculate heading from magnetometer reading.
double getHeading() {
  // get magnetometer reading/new sensor event
  mag.getEvent(&event);
  x = event.magnetic.x;
  y = event.magnetic.y;

  // calculate heading
  if (x == 0) {
    if (y < 0) {
      return 90;
    } else {
      return 0;
    }
  } else {
    return atan2(y, x) * RAD_TO_DEG;
  }
}

// I2C handler
void handleI2C(int numberBytes) {
  for (int i = 0; 1 < Wire.available(); i++) {
    if (ireg == 0x10) {
      angle = Wire.read();
    }
    else if (ireg == 0x11) {
      velocity = Wire.read();
    }
    else if (ireg == 0x12) {
      desiredOrientation = Wire.read();
    }
    if (ireg == 0 && i == 1) {
      ireg = Wire.read();
    }
  }
}

// setup code to run once
void setup(void) {
  //// Magnetometer init
  // Enable auto-gain
  mag.enableAutoRange(true);

  // Initialise the sensor
  if (!mag.begin()) {
    /* There was a problem detecting the LSM303 ... check your connections */
    // TODO: show an error using LED
    while (1)
      ;
  }

  //// PID init
  // initialize linking variables
  Input = getHeading();
  Setpoint = 0;

  // turn the PID on
  myPID.SetMode(AUTOMATIC);

  //// I2C init
  // Join I2C bus with address 0x20
  Wire.begin(0x20);
  Wire.onReceive(handleI2C);
}

// main code to run repeatedly:
void loop() {
  //// PID implementation
  Input = getHeading() + desiredOrientation;
  myPID.Compute();
  driver.angleDrive(angle, velocity, Output);
}
