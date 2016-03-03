#!bin/python3
#
# draw_from_Gcode.py
#
# Load a file with XY coordinates generated with Inkscape and
# a Gcode extension (Unicorn).  Send the neccessary commands to
# the Arduino to move the pen to each point.
#
# The Arduino can be on /dev/ttyACM0 or /dev/ttyACM1
#
# This code currently communicates to the Arduino that is flashed
# with: TwoStepperControlFromPython.ino



print('Running: draw_from_Gcode.py')
print()


import math
import numpy as np
import serial
import time

# Load the trajectory from the .csv file (gcode derived)
file_path = 'DrawingInputFiles/'
file_name = 'PelotonLogoXY.csv'
xy = np.genfromtxt(file_path+file_name, delimiter=',')

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



def changeInLength(xy1,xy2,dm):
    # Given two points, find the change in length of the two strings

    # Find the initial length
    length_left_1  = math.sqrt(xy1[0]**2 + xy1[1]**2)
    length_right_1 = math.sqrt((dm-xy1[0])**2 + xy1[1]**2)

    # Find the final length
    length_left_2  = math.sqrt(xy2[0]**2 + xy2[1]**2)
    length_right_2 = math.sqrt((dm-xy2[0])**2 + xy2[1]**2)

    # Return the change in lengths
    return length_left_2 - length_left_1, length_right_2 - length_right_1


def length2Steps(del_left,del_right,r,steps):
    mm2step = steps / (2 * 3.14 * r)
    steps_left  = del_left * mm2step
    steps_right = del_right * mm2step
    return round(steps_left), round(steps_right)


def sendSteps2Arduino(steps_left,steps_right):
    # Send left motor steps and direction
    arduino.write(str(steps_left).encode('ascii'))
    arduino.write('n'.encode('ascii'))
    print('PI -> ARDUINO: '+str(steps_left)+' left')
    
    # Send right motor steps and direction
    arduino.write(str(steps_right).encode('ascii'))
    arduino.write('n'.encode('ascii'))
    print('PI -> ARDUINO: '+str(steps_right)+' right')
    return




# Iterate through the xy array, calculate the change in lengths, and send
# the commands to the Arduino
for point in range(1,xy.shape[0]):
    print('moving to point ' + str(point+1) + '/' + str(xy.shape[0]) + '   ' + str(xy[point]))
    
##    # Find the change in the string length for left and right
##    [del_left,del_right] = changeInLength(xy[point-1],xy[point],dm)
##    # Find the number of steps for each motor
##    [steps_left,steps_right] = length2Steps(del_left,del_right,r,motor_steps)
##    # Send the steps to the arduino
##    sendSteps2Arduino(steps_left,steps_right)
    
    print()



# Tell the Arduino to release the motors
#arduino.write('r'.encode('ascii'))


arduino.close()
