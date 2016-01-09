# drawing_robot

Project to design and build a wall-hanging drawing robot.

Along with the end results (drawings), this project is a way to learn more about programming and interfacing a Linux computer with motors (and maybe sensors).  A Raspberry Pi will be used as the Linux computer for the computations.   The Pi will communicate with an Arduino, which will control two motors for positioning the pen in X-Y.  A lot of work has already been done on drawing robots, and may be incorporated into this project (with proper citations).

##Hardware:
* NEMA 17 motors ([Adafruit motor](www.adafruit.com/products/324)
* [Adafruit motor shield for the Arduino](www.adafruit.com/products/1438)

##Software:
* [Adafruit motor shield library](https://github.com/adafruit/Adafruit_Motor_Shield_V2_Library) to control motor with Arduino
* 

###ArduinoCode:
* StepperTest - from Adafruit
* receiveFromPython - listens over USB to input from python2arduino_blink.py
* StepperControlFromPython - listens over USB for motor commands

####Python Code:
* python2arduino_blink.py - code to send Arduino the number of times to blink LED
* python2arduino_motor.py - code to send Arduino motor commands



Adam Blankespoor

