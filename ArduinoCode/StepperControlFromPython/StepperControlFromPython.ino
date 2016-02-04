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
    // if data is in the USB buffer 
    if (Serial.available() > 0)  
    {
      // Collect the data for the left and right motor commands
      n_steps_left = getSerial();
      Serial.print("Arduino received: ");
      Serial.print(n_steps_left);
      Serial.println(" left");
      n_steps_right = getSerial();
      Serial.print("Arduino received: ");
      Serial.print(n_steps_right);
      Serial.println(" right");
      Serial.println(" ");  
      //delay(10);
      //Serial.println("Adruino: message received");
      
      // After pulling motor commands from USB, send to motor sheild
      motorCommand(n_steps_left, n_steps_right);
    }

}



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
        if (in_byte > 0 && in_byte != 110) 
        {
           // data = previous_byte*10 + new_byte - '0'
           serial_data = serial_data * 10 + in_byte - '0';
           
           // deal with negative steps
             if (serial_data == -3) {
                pos_neg_flag = -1; 
                serial_data = 0;             
             }  
        }  
     }
     
     in_byte = 0;

     return serial_data * pos_neg_flag;  
}


void motorCommand(int steps_left, int steps_right) 
{ 
  if (steps_left < 0){
    motor_left->step(steps_left, BACKWARD, SINGLE);
  }
  else {
    motor_left->step(steps_left, FORWARD, SINGLE);
  }
  
  if (steps_right < 0) {
    motor_right->step(steps_right, BACKWARD, SINGLE);
  }
  else {
    motor_right->step(steps_right, FORWARD, SINGLE);
  }
}

