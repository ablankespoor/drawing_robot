#! bin/python3
#
# python2arduino_motor.py
#
# Initial Python program to interface with the Arduino over USB.
# Sends a command from Raspberry Pi, with Python, to the Arduino for
# motor control over the serial connection (USB)
#
# The Arduino is on /dev/ttyACM0  or AMC1
# and has to be flashed with StepperControlFromPython.ino


import serial
import time

print('running python2arduino_motor.py')

arduino = serial.Serial('/dev/ttyACM1', 9600)
time.sleep(1)
num = '2'
arduino.write(bytes(num.encode('ascii')))

