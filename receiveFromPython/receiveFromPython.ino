/*
Quick code to read information over serial from Python

*/

void setup() {
  pinMode(ledPin,OUTPUT);
  Serial.begin(9600);
  
}

void loop() {
  if (Serial.available())  {
    light(Serial.read() - '0');
  }
  delay(500);
  
}
