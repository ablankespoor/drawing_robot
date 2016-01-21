/* 
StepperControlFromPython.ino

Listens for motor commands from the Raspberry Pi over USB.  This
code assumes a motor shield is connected and two stepper motors 
can be controlled by the Arduino.  

Currently for use with Python code: make_square_path.py

For use with the Adafruit Motor Shield v2 
---->	http://www.adafruit.com/products/1438
*/


#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Connect a stepper motors with 200 steps per revolution (1.8 degree)
// Left motor is connected to M1
// Right motor is connected to M2
Adafruit_StepperMotor *motor_left = AFMS.getStepper(200, 1);
Adafruit_StepperMotor *motor_right = AFMS.getStepper(200, 2);


const int led_pin = 13;

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  //Serial.println("Stepper test!");

  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  
  motor_left->setSpeed(10);  // 10 rpm  
  
  pinMode(led_pin,OUTPUT); 
}

void loop() {
  
    if (Serial.available())  {
      motorCommand(Serial.read() - '0');
      light(Serial.read() - '0');
    }
    delay(5000);
    // Serial.println("Single coil steps");
    //motor1->step(numSteps, FORWARD, SINGLE); 

}


void motorCommand(int n) {
  motor_left->step(n*100,FORWARD, SINGLE);
}

void light(int n) {
  for (int i = 0; i<n; i++) {
    digitalWrite(led_pin,HIGH);
    delay(1000);
    digitalWrite(led_pin,LOW);
    delay(1000);
  }
}
