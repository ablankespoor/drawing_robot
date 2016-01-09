/* 
StepperControlFromPython.ino

Based on the StepperTest.ino code from the Adafruit Motor Shield library.

It accepts commands from a Python code run on the 
Raspberry Pi - python2arduino_motor.py

For use with the Adafruit Motor Shield v2 
---->	http://www.adafruit.com/products/1438
*/


#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #1 (M1 and M2)
Adafruit_StepperMotor *motor1 = AFMS.getStepper(200, 1);


void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  //Serial.println("Stepper test!");

  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  
  motor1->setSpeed(10);  // 10 rpm   
}

void loop() {
  
    if (Serial.available())  {
      motorCommand(Serial.read() - '0');
    }
     
    // Serial.println("Single coil steps");
    //motor1->step(numSteps, FORWARD, SINGLE); 

}


void motorCommand(int n) {
  motor1->step(n*100,FORWARD, SINGLE);
}
