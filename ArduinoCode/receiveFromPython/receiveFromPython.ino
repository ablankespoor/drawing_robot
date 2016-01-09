/*
Quick code to read information over serial from Python and turn on LED
The LED blinks n times, which is passed to the Arduino from Python code.

The python code is python2arduino_blink.py

*/

const int ledPin = 13;

void setup() {
  pinMode(ledPin,OUTPUT);
  Serial.begin(9600);
  
}

void loop() {
  if (Serial.available())  {
    light(Serial.read() - '0');
  }
  delay(5000);
  
}


void light(int n) {
  for (int i = 0; i<n; i++) {
    digitalWrite(ledPin, HIGH);
    delay(1000);
    digitalWrite(ledPin, LOW);
    delay(1000);
  }
}
