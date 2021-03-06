/*
Quick code to read information over serial from Python and turn on LED
Use python2arduino_blink.py to control the LED
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
