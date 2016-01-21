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



print('running: make_square_path.py')


import math
import numpy as np
import serial
import time

# define points of the square
xy = np.array([[0, 0],[0,-20],[20,-20],[20,0]])    # desired movement
offset = np.array([203, -260])                     # offset to center of drawing
xy = xy + offset



# define system parameters
r  = 11.5 / 2                   # [mm] radius of 3d printed pully
dm = 406.4                      # [mm] distance between motor shafts
motor_steps = 200               # number of steps per revolution (1.8 degrees)

# setup the arduino interface
arduino = serial.Serial('/dev/ttyACM0', 9600)
time.sleep(2)   # let the connection settle

print()
print(str(xy[0])+'(1)       <----        '+str(xy[3])+'(4)')
print('   |                             ^')
print('   |                             |')
print('   v                             |')
print(str(xy[1])+'(2)      ---->       '+str(xy[2])+'(3)')
print()

def changeInLength(xy1,xy2,dm):
    # Given two points, find the change in length of the two strings
    print(xy1)
    # Find the initial length
    length_left_1  = math.sqrt(xy1[0]**2 + xy1[1]**2)
    length_right_1 = math.sqrt((dm-xy1[0])**2 + xy1[1]**2)
    print(str(length_left_1)+' initial length of left string')
    print(str(length_right_1)+' initial length of right string')

    print(xy2)
    # Find the final length
    length_left_2  = math.sqrt(xy2[0]**2 + xy2[1]**2)
    length_right_2 = math.sqrt((dm-xy2[0])**2 + xy2[1]**2)
    print(str(length_left_2)+' final length of left string')
    print(str(length_right_2)+' final length of right string')

    # Return the change in lengths
    return length_left_2 - length_left_1, length_right_2 - length_right_1


def length2Steps(del_left,del_right,r,steps):
    print('change in strings = '+str(del_left)+',   '+str(del_right))
    mm2step = steps / (2 * 3.14 * r)
    steps_left  = del_left * mm2step
    steps_right = del_right * mm2step
    print(str(steps_left)+' left motor rotation')
    print(str(steps_right)+' right motor rotation')
    return round(steps_left), round(steps_right)

def sendSteps2Arduino(steps_left,steps_right):
    print('sending '+str(steps_left)+' steps to left motor')
    print('sending '+str(steps_right)+' steps to right motor')

    if steps_left > 0:
        direction_left = 'FORWARD'
    elif steps_left < 0:
        direction_left = 'BACKWARD'

    if steps_right > 0:
        direction_right = 'FORWARD'
    elif steps_right < 0:
        direction_right = 'BACKWARD'

    


    arduino.write(bytes(str(steps_left).encode('ascii')))
    return




# iterate through the xy and calculate the change in lengths
for point in range(1,2):
    print('moving to point ' + str(xy[point]))
    
    # find the change in the string length for left and right
    [del_left,del_right] = changeInLength(xy[point-1],xy[point],dm)
    # find the number of steps for each motor
    [steps_left,steps_right] = length2Steps(del_left,del_right,r,motor_steps)
    print()
    # send the steps to the arduino
    sendSteps2Arduino(steps_left,steps_right)

    
    print()

print('moving to point ' + str(xy[0]))

arduino.close()








