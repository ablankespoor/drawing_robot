#! bin/python3
#
# Initial Python program to interface with the Arduino over USB
#
# The Arduino is on /dev/ttyACM0


import serial

print('running python2arduino_blink.py')

arduino = serial.Serial('/dev/ttyACM0', 9600)
num = '3'
arduino.write(bytes(num.encode('ascii')))
