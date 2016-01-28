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



int n_steps_left = 0;
int n_steps_right = 0;
int serial_data = 0;
int in_byte = 0;

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  delay(100);
  //Serial.println("Stepper test!");

  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz
  
  motor_left->setSpeed(10);  // 10 rpm  This is a power input...
  motor_right->setSpeed(10);
  

}

void loop() {
  
    if (Serial.available() > 0)  {
      // read one byte (ascii) and subtracts 48 to get 0-9 integer   (the Serial.read() - '0' part)
      // desired = previous*10 + current
      //n_steps_left = n_steps_left*10 + Serial.read() - '0';  
      //Serial.print("Arduino received: ");
      //Serial.println(n_steps_left);
      n_steps_left = getSerial();
      Serial.print("Arduino received: ");
      Serial.print(n_steps_left);
      Serial.println(" left");
      n_steps_right = getSerial();
      Serial.print("Arduino received: ");
      Serial.print(n_steps_right);
      Serial.println(" right");
      
      
      Serial.println(" ");     
    }

}



// Read the bytes from the over the USB, one at a time
// Accumulate the result in serial_data and return 
int getSerial() {
     serial_data = 0;
     // while not the end of number:  'n'
     // 'n' --> ascii = 110 
     while (in_byte != 110) 
     { 
        in_byte = Serial.read();   // if Serial.read() is empty, it returns -1
        if (in_byte > 0 && in_byte != 110) 
          {
           // data = previous_byte*10 + new_byte - '0'
           serial_data = serial_data * 10 + in_byte - '0';
          }  
     }
     
     in_byte = 0;
     return serial_data;  
}


void motorCommand(int n) {
  motor_left->step(n*100,FORWARD, SINGLE);
}

