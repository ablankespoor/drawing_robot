// MultiStepper
// -*- mode: C++ -*-
//
// Control both Stepper motors at the same time with different speeds
// and accelerations. 
// Requires the AFMotor library (https://github.com/adafruit/Adafruit-Motor-Shield-library)
// And AccelStepper with AFMotor support (https://github.com/adafruit/AccelStepper)
// Public domain!

// Modified by Adam to test motors for drawing robot

#include <AccelStepper.h>
#include <Adafruit_MotorShield.h>
#include <Wire.h>
#include "utility/Adafruit_PWMServoDriver.h"


// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Connect a stepper motors with 200 steps per revolution (1.8 degree)
// Left motor is connected to M1
// Right motor is connected to M2
Adafruit_StepperMotor *motor_left  = AFMS.getStepper(200, 1);
Adafruit_StepperMotor *motor_right = AFMS.getStepper(200, 2);

// you can change these to DOUBLE or INTERLEAVE or MICROSTEP!
// wrappers for the first motor!
void forwardstep1() {  
  motor_left->onestep(FORWARD, SINGLE);
}
void backwardstep1() {  
  motor_left->onestep(BACKWARD, SINGLE);
}
// wrappers for the second motor!
void forwardstep2() {  
  motor_right->onestep(FORWARD, SINGLE);
}
void backwardstep2() {  
  motor_right->onestep(BACKWARD, SINGLE);
}

// Motor shield has two motor ports, now we'll wrap them in an AccelStepper object
AccelStepper stepper_left(forwardstep1, backwardstep1);
AccelStepper stepper_right(forwardstep2, backwardstep2);

void setup()
{  
    AFMS.begin();
    
    stepper_left.setMaxSpeed(200.0);
    stepper_left.setAcceleration(100.0);
    stepper_left.moveTo(100);
    
    stepper_right.setMaxSpeed(200.0);
    stepper_right.setAcceleration(100.0);
    stepper_right.moveTo(100);
    
}

void loop()
{
    

  
    // Change direction at the limits - it goes back and forth
//    if (stepper_left.distanceToGo() == 0)
//	stepper_left.moveTo(-stepper_left.currentPosition());
//
//    if (stepper_right.distanceToGo() == 0)
//        stepper_right.moveTo(-stepper_right.currentPosition());
        
    stepper_left.run();
    stepper_right.run();
    
    if (stepper_left.distanceToGo() == 0)
    {
        stepper_left.disableOutputs();
        stepper_right.disableOutputs();
    }
    

}
