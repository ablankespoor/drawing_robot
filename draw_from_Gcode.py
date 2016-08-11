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

# file_name = 'PelotonLogoXY.csv'
file_name = 'Star-Wars-Yoda.csv'
# file_name = 'circleXY.csv'
# file_name = 'nested_square.csv'

xy = np.genfromtxt(file_path+file_name, delimiter=',')
xy_relative = xy

offset = np.array([203,-260])   # offset the pen to the center of drawing
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


def changeInXY(xy1,xy2):
    # Given two points, find the change in relative position
    # used in the output for the user
    #[del_x,del_y] = changeInXY(start_point,end_point)
    del_x = xy2[0] - xy1[0]
    del_y = xy2[1] - xy1[1]

    return del_x,del_y


def changeInLength(xy1,xy2,dm):
    # Given two points, find the change in length of the two strings
    # [left,right] = changeInLength(start_point,end_point,motor_distance)
    
    # Find the initial length
    length_left_1  = math.sqrt(xy1[0]**2 + xy1[1]**2)
    length_right_1 = math.sqrt((dm-xy1[0])**2 + xy1[1]**2)

    # Find the final length
    length_left_2  = math.sqrt(xy2[0]**2 + xy2[1]**2)
    length_right_2 = math.sqrt((dm-xy2[0])**2 + xy2[1]**2)

    # Return the change in lengths
    return length_left_2 - length_left_1, length_right_2 - length_right_1


def length2Steps(del_left,del_right,r,steps):

    # [left,right] = length2Steps(distance_left,distance_right,radius,motor_steps)
    mm2step = steps / (2 * 3.14 * r)
    steps_left  = del_left * mm2step
    steps_right = del_right * mm2step
    return round(steps_left), round(steps_right)

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





# Iterate through the xy array, calculate the change in lengths, and send
# the commands to the Arduino
for point in range(1,len(xy)):

    # Find the relative change in xy to the next point
    [del_x,del_y] = changeInXY(xy[point-1],xy[point])
    print('moving to point ' + str(point+1) + '/' + str(xy.shape[0]) + '    ['+str(del_x)+', '+str(del_y)+']')
    
    # Find the change in the string length for left and right
    [del_left,del_right] = changeInLength(xy[point-1],xy[point],dm)

    # Find the number of steps for each motor
    [steps_left,steps_right] = length2Steps(del_left,del_right,r,motor_steps)

    # Send the steps to the arduino
    sendMessage2Arduino(point,steps_left,steps_right)
    ##  remove the line below when using arduino
    #print('PI -> ARDUINO: '+str(point+1)+' '+str(steps_left)+' '+str(steps_right))


    # Pause for user input
    #input("Press Enter to continue")    

    
    print()

# Test for sending messages
#sendMessage2Arduino(3,-10,10)

# Tell the Arduino to release the motors
#print('PI -> ARDUINO: release')
arduino.write('r'.encode('ascii'))
arduino.write('m'.encode('ascii'))
print(arduino.readline())


arduino.close()
