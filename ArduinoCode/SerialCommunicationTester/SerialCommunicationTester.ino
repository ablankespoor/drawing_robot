/*
SerialCommunicationTester.ino

Listens for commands from the Raspberry Pi over USB. 

Currently for use with the Python code: draw_from_Gcode.py

*/


#include <Wire.h>


// Variables
int count = 2;


// message is the data sent over the USB, my diy communication protocol
// message: [count, 'n', L steps, 'n', R steps, 'n', end]
int message[3]={0,0,0};



void setup()
{   
    Serial.begin(9600);           // set up Serial library at 9600 bps
    delay(100);
}    // end of setup()



void loop()
{
  
  if (Serial.available() > 0 )
  {

    getSerial2(message);
    //Serial.println("return from getSerial2()");

    Serial.print(message[0]);
    Serial.print(" ");
    Serial.print(message[1]);
    Serial.print(" ");
    Serial.println(message[2]);
    
    // Reset the message
    for (int i=0; i<3; i++){
      message[i] = 0;
    }
    
  }
  
  
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
      Serial.println("release() sent");
    }    
          
  } // end of "message"
  
  
  
}


