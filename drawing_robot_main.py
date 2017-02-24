#!/usr/bin/python3
#
# drawing_robot_main.py
#
# Code to load a drawing file and run the motors to make a drawing
#
# The Arduino can be on /dev/ttyACM0 or /dev/ttyACM1
#
# This code currently communicates to the Arduino that is flashed
# with: TwoStepperControlFromPython.ino








if __name__ == '__main__':

    import math
    import numpy
    import serial
    import time
    import logging
    from datetime import datetime

    print('Running: drawing_robot_main.py')
    print()

    # Setup the logfile (this should maybe be in a config file to minimize
    # the details here...
    log_file = datetime.now().strftime('logfile_%Y_%m_%d_%H_%M.log')
    log_file = 'LogFiles/'+log_file

    #fmt='%(asctime)s.%(msecs)03d',datefmt='%Y-%m-%d,%H:%M:%S'
    logging.basicConfig(filename=log_file,
                        format='%(asctime)s%(msecs)03d,  %(message)s',
                        datefmt='%Y-%m-%d  %H:%M:%S.',
                        filemode='a',   #append to file
                        level=logging.DEBUG)
    logging.debug('Generating log file')

    # Load the trajectory from the .csv file
    file_path = 'DrawingInputFiles/'
    file_name = 'cat_outline_11_9_16_tsp.csv'
    logging.debug('loading data from: %s', file_name)

    xy = numpy.genfromtxt(file_path+file_name, delimiter=',')
    xy_relative = xy
    # Offset the pen to the center of the drawing surface
    offset = numpy.array([203,-260])
    xy = xy + offset

    # Define system parameters
    r  = 11.5 / 2                   # [mm] radius of 3d printed pully
    dm = 406.4                      # [mm] distance between motor shafts
    motor_steps = 200               # number of steps per revolution (1.8 degrees)

    # Iterate through the xy array, calculate the change in lengths, and send
    # the commands to the Arduino
    for point in range(1,len(xy)):

        print('moving to point ' + str(point+1) + '/' + str(xy.shape[0]))
        logging.debug('%s / %s', str(point+1), str(xy.shape[0]))

    
