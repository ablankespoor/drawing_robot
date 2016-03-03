#!bin/python3
#
# make_square_path.py
#
# Defines an array of x,y coordinates for a square and sends
# the neccessary commands to the Arduino to move the pen to
# each point.
#
# The Arduino can be on /dev/ttyACM0 or /dev/ttyACM1
#
# This code currently communicates to the Arduino that is flashed
# with: StepperControlFromPython.ino



print('Running: make_square_path.py')
print()


import math
import numpy as np
import serial
import time

# Define points of the square
xy = np.array([[0, 0],[0,-20],[20,-20],[20,0],[0,0]])    # desired movement
offset = np.array([203, -260])                     # offset to center of drawing
xy = xy + offset



# Define system parameters
r  = 11.5 / 2                   # [mm] radius of 3d printed pully
dm = 406.4                      # [mm] distance between motor shafts
motor_steps = 200               # number of steps per revolution (1.8 degrees)

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

print()
print(str(xy[0])+'(1)    <----        '+str(xy[3])+'(4)')
print('   |                             ^')
print('   |                             |')
print('   v                             |')
print(str(xy[1])+'(2)      ---->       '+str(xy[2])+'(3)')
print()

def changeInLength(xy1,xy2,dm):
    # Given two points, find the change in length of the two strings

    # Find the initial length
    length_left_1  = math.sqrt(xy1[0]**2 + xy1[1]**2)
    length_right_1 = math.sqrt((dm-xy1[0])**2 + xy1[1]**2)
    #print(str(length_left_1)+' initial length of left string')
    #print(str(length_right_1)+' initial length of right string')


    # Find the final length
    length_left_2  = math.sqrt(xy2[0]**2 + xy2[1]**2)
    length_right_2 = math.sqrt((dm-xy2[0])**2 + xy2[1]**2)
    #print(str(length_left_2)+' final length of left string')
    #print(str(length_right_2)+' final length of right string')

    # Return the change in lengths
    return length_left_2 - length_left_1, length_right_2 - length_right_1


def length2Steps(del_left,del_right,r,steps):
    #print('change in strings = '+str(del_left)+',   '+str(del_right))
    mm2step = steps / (2 * 3.14 * r)
    steps_left  = del_left * mm2step
    steps_right = del_right * mm2step
    #print(str(steps_left)+' left motor steps')
    #print(str(steps_right)+' right motor steps')
    return round(steps_left), round(steps_right)

def sendSteps2Arduino(steps_left,steps_right):

    if steps_left > 0:
        direction_left = 'F'
    elif steps_left < 0:
        direction_left = 'B'

    if steps_right > 0:
        direction_right = 'F'
    elif steps_right < 0:
        direction_right = 'B'

    # Send left motor steps and direction
    arduino.write(str(steps_left).encode('ascii'))
    arduino.write('n'.encode('ascii'))
    print('PI -> ARDUINO: '+str(steps_left)+' left')
    
    # Send right motor steps and direction
    arduino.write(str(steps_right).encode('ascii'))
    arduino.write('n'.encode('ascii'))
    print('PI -> ARDUINO: '+str(steps_right)+' right')
    

    # wait for acknowledge from Arduino
    #print(arduino.readline())
    
    return




# Iterate through the xy and calculate the change in lengths
for point in range(1,4):
    print('moving to point (' + str(point+1) + ') ' + str(xy[point]))
    
    # Find the change in the string length for left and right
    [del_left,del_right] = changeInLength(xy[point-1],xy[point],dm)
    # Find the number of steps for each motor
    [steps_left,steps_right] = length2Steps(del_left,del_right,r,motor_steps)
    # Send the steps to the arduino
    sendSteps2Arduino(steps_left,steps_right)
    
    print()

# Return to the starting point
print('moving to point (1)' + str(xy[0]))
[del_left,del_right] = changeInLength(xy[point],xy[0],dm)
[steps_left,steps_right] = length2Steps(del_left,del_right,r,motor_steps)
sendSteps2Arduino(steps_left,steps_right)
print()

# Tell the Arduino to release the motors
#arduino.write('r'.encode('ascii'))


arduino.close()








