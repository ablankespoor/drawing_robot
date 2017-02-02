#!bin/python3
#
# serial_communication_tester.py
#
# Send and receive commands to the Arduino.  
#
# The Arduino can be on /dev/ttyACM0 or /dev/ttyACM1
#
# This code currently communicates to the Arduino that is flashed
# with: SerialCommunicationTester.ino



print('Running: serial_communication_tester.py')
print()


#import math
#import numpy as np
import serial
import time



# Setup the arduino interface
a_locations = ['/dev/ttyACM0','/dev/ttyACM1']
for device in a_locations:
    try:
        arduino = serial.Serial(device, 9600)
        print("Connected to Arduino on "+device)
        break
    except:
        print("Failed to connect on "+device)
            
time.sleep(2)   # let the connection settle

arduino.flushInput()



def getArduinoResponse():
    # [point,left,right] = getArduinoResponse()
    r = str(arduino.readline())
    #print(r)
    space1 = r.find(' ')
    space2 = r.find(' ',space1+1)
    dash1  = r.find('\r')
    pnt = r[2:space1]
    l = r[space1+1:space2]
    r = r[space2+1:-5]
    print('ARDUINO -> PI: '+pnt+' '+l+' '+r)
    # Wait here for motors to finish moving
##    motor_done = "no"
##    while (motor_done == "no"):
##        motor_done = str(arduino.readline())[2:5]
##        print(motor_done)
    #r2 = str(arduino.readline())
    #print(r2)
    
    return pnt,l,r


def sendMessage2Arduino(point,steps_L,steps_R):
    # send the point number
    arduino.write(str(point+1).encode('ascii'))
    arduino.write('n'.encode('ascii'))              # end of write
    # send the number of steps for left motor
    arduino.write(str(steps_L).encode('ascii'))
    arduino.write('n'.encode('ascii'))              # end of write
    # send the number of steps for right motor
    arduino.write(str(steps_R).encode('ascii'))
    arduino.write('n'.encode('ascii'))              # end of write
    # send the "end of message" command
    arduino.write('m'.encode('ascii'))              # end of message

    print('PI -> ARDUINO: '+str(point+1)+' '+str(steps_L)+' '+str(steps_R))

    # Wait for a response from arduino, with correct data...
    [pnt,l,r] = getArduinoResponse()
    #print('ARDUINO -> PI: '+pnt+' '+l+' '+r)

##    if int(pnt)==point+1:
##        print('matching response')



##
### Iterate through the xy array, calculate the change in lengths, and send
### the commands to the Arduino
##for point in range(1,len(xy)):
##    
##    # Send the steps to the arduino
##    sendMessage2Arduino(point,steps_left,steps_right)
##
##    # Pause for user input
##    #input("Press Enter to continue")    

    
    print()

# Test for sending messages
sendMessage2Arduino(3,-10,10)
sendMessage2Arduino(4,5,5)

# Tell the Arduino to release the motors
#print('PI -> ARDUINO: release')
arduino.write('r'.encode('ascii'))
arduino.write('m'.encode('ascii'))
print(arduino.readline())


#arduino.close()
