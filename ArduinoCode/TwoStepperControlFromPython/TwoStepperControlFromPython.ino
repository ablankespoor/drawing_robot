/*
TwoStepperControlFromPython.ino

Combine the StepperControlFromPython.ino, which only runs 1 stepper at a time, and 
AF_MultiStepperTest.ino.

Listens for commands from the Raspberry Pi over USB.  This code assumes a motor shield is
connected and two stepper motors can be controlled by the Arduino.

Currently for use with the Python code: make_square_path.py

Requires the Adafruit motor shield library (https://....    )
and AccelStepper with AFMotor support (https://github.com/adafruit/AccelStepper )
uses the Adafruit Motor Shield vs http://www.adafruit.com/products/1438

*/


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

// Variables
int n_steps_left = 0;
int n_steps_right = 0;
int serial_data = 0;
int in_byte = 0;
int left_done = 1;
int right_done = 1;


// AccelStepper wrappers for the motors
// Can change these to DOUBLE or INTERLEAVE or MICROSTEP!
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

// Define the AccelStepper objects for motor control
AccelStepper stepper_left(forwardstep1, backwardstep1);
AccelStepper stepper_right(forwardstep2, backwardstep2);


void setup()
{   
    Serial.begin(9600);           // set up Serial library at 9600 bps
    delay(100);
  
    AFMS.begin();
    
    // Set some motor parameters
    stepper_left.setMaxSpeed(200.0);
    stepper_left.setAcceleration(100.0);
    //stepper_left.moveTo(-500);
    
    stepper_right.setMaxSpeed(200.0);
    stepper_right.setAcceleration(100.0);
    //stepper_right.moveTo(-500);
    
}    // end of setup()



void loop()
{
  // If data is in the USB buffer
  if (Serial.available() > 0 && left_done == 1 && right_done == 1)
  {
    n_steps_left  = getSerial();
    n_steps_right = getSerial();
    
    Serial.print("left   ");
    Serial.print(n_steps_left);
    Serial.print("      right   ");
    Serial.println(n_steps_right);
    delay(100);
    
    stepper_left.move(n_steps_left);
    stepper_right.move(n_steps_right);
    
    // Reset the "done" variables
    left_done  = 0;
    right_done = 0;
  }

  
  stepper_left.run();
  stepper_right.run();
  
  // Check if the current movement is complete
  if (stepper_left.distanceToGo() == 0)
    {
      left_done = 1;
      motor_left->release();
    }
  if (stepper_right.distanceToGo() == 0)
    {
      right_done = 1;
      motor_right->release();
    }
  
//  if (stepper_left.distanceToGo() != 0 && stepper_right.distanceToGo() != 0)
//  {
//    Serial.print("left distance =  ");
//    Serial.print(stepper_left.distanceToGo());
//    Serial.print("      right distance =  ");
//    Serial.println(stepper_right.distanceToGo());
//  }

  
  
}    // end of loop()



//////////////////////////////
// FUNCTION DEFINITIONS
//////////////////////////////

// Read the bytes from the USB, one at a time
// Accumulate the result in serial_data and return 
int getSerial() {
     serial_data = 0;
     int pos_neg_flag = 1;
     // while not the end of number:  'n'
     // 'n' --> ascii = 110 
     while (in_byte != 110) 
     { 
        in_byte = Serial.read();   // if Serial.read() is empty, it returns -1
        if (in_byte > 0 && in_byte != 110 && in_byte != 114) 
        {
           // data = previous_byte*10 + new_byte - '0'
           serial_data = serial_data * 10 + in_byte - '0';
           
           // deal with negative steps
           if (serial_data == -3) {
              pos_neg_flag = -1; 
              serial_data = 0;             
           }  
        } 
//       else if (in_byte == 114){
//           motor_left->release();
//           motor_right->release();
//           Serial.println("release() sent");
//       }
     }
     
     in_byte = 0;

     return serial_data * pos_neg_flag;  
}


