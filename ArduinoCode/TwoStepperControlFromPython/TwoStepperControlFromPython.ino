/*
TwoStepperControlFromPython.ino

Listens for commands from the Raspberry Pi over USB.  This code assumes a motor shield is
connected and two stepper motors can be controlled by the Arduino.

Currently for use with the Python code: draw_from_Gcode.py

Requires the Adafruit motor shield library (https://....    )
and AccelStepper with AFMotor support (https://github.com/adafruit/AccelStepper )
uses the Adafruit Motor Shield vs http://www.adafruit.com/products/1438

*/


#include <AccelStepper.h>
#include <Adafruit_MotorShield.h>
#include <Wire.h>
//include "utility/Adafruit_PWMServoDriver.h"

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
int count = 2;
int distance_to_go = 0;

// message is the data sent over the USB, my diy communication protocol
// message: [count, 'n', L steps, 'n', R steps, 'n', end]
int message[3]={0,0,0};





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
    stepper_left.setMaxSpeed(200.0);        // originally 200, from example
    stepper_left.setAcceleration(100.0);    // originally 100,
    
    stepper_right.setMaxSpeed(200.0);       // originally 200, from example
    stepper_right.setAcceleration(100.0);   // originally 100
    
}    // end of setup()



void loop()
{
  
  if (Serial.available() > 0 && distance_to_go == 0)
  {

    getSerial2(message);
    // Output to serial "point, left motor steps, right
    Serial.print(message[0]);
    Serial.print(" ");
    Serial.print(message[1]);
    Serial.print(" ");
    Serial.println(message[2]);
    
       
    // Specify the next motor command
    stepper_left.move(message[1]);
    stepper_right.move(message[2]);
    
    // Reset the message
    for (int i=0; i<3; i++){
      message[i] = 0;
    }

  } // end of Serial read
  
  
  // Move the motors
  stepper_left.run();
  stepper_right.run();
  
  distance_to_go = stepper_left.distanceToGo() + stepper_right.distanceToGo();

  
  delay(20);
  
  
//  // Check to see motor position
//  if (stepper_left.speed()>0 || stepper_right.speed()>0)
//  { 
//      //int temp = 5;
//      //delay(100);
//    Serial.print("x ");
//    Serial.print(stepper_left.currentPosition());
//    Serial.print("   ");
//    Serial.println(stepper_right.currentPosition());
//  }
    
   
}    // end of loop()



//////////////////////////////
// FUNCTION DEFINITIONS
//////////////////////////////


void getSerial2(int m[]){
  int in_byte = 0;
  int index = 0;
  int pos_neg_x = 1;
  
  // Read through the whole message (not 109 = 'm')
  while (in_byte != 109){
    in_byte = Serial.read();
    if (in_byte > 0 && in_byte != 109 && in_byte != 110 && in_byte != 114){
      
      m[index] = m[index]*10 + in_byte - '0';
      
      // Swap the pos/neg multiplier if the last in_byte was neg
      if (m[index] == -3){
        pos_neg_x = -1;
        m[index] = 0;
      }
      
    }
    // When the current read is done, account for negatives
    if (in_byte == 110){
      m[index] = m[index] * pos_neg_x;
      pos_neg_x = 1;
      index++;
    }
    // Release the motors
    if (in_byte == 114){
      motor_left->release();
      motor_right->release();
      Serial.println("release() sent");
    }
      
  } // end of "message"
  
  
  
}


