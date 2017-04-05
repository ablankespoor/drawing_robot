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

def load_data():
    # Returns:
    #    [point, steps_left, steps_right, relative_x, relative_y, x, y]
    import load_my_file
    file_name = load_my_file.file_namer('.csv')
    file_path = load_my_file.file_path_os('pi')
    logging.debug('loading data from: %s', file_name)
    return np.genfromtxt(file_path+file_name, delimiter=',')

    
def get_arduino_response():
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


def send_message_2_arduino(point,steps_L,steps_R):
    # send the point number
    steps_L = int(steps_L)
    steps_R = int(steps_R)
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
    [pnt,l,r] = get_arduino_response()


def set_up_arduino():
    usb_locations = ['/dev/ttyACM0','/dev/ttyACM1']
    for device in usb_locations:
        try:
            arduino = serial.Serial(device, 9600)
            print("Connected to Arduino on "+device)
            logging.debug("Connected to Arduino on "+device)
            break
        except:
            arduino = ""
            print("Failed to connect on "+device)
                
    time.sleep(2)   # let the connection settle
    if arduino == "":
        print('   No Arduino connected')
        logging.debug('no adruino connected')
    else:
        arduino.flushInput()
    return arduino
        

def set_up_logging():
    
    # Setup the logfile
    log_file = datetime.now().strftime('logfile_%Y_%m_%d_%H_%M.log')
    log_file = 'LogFiles/'+log_file
    #fmt='%(asctime)s.%(msecs)03d',datefmt='%Y-%m-%d,%H:%M:%S'
    logging.basicConfig(filename=log_file,
                        format='%(asctime)s%(msecs)03d,  %(message)s',
                        datefmt='%Y-%m-%d  %H:%M:%S.',
                        filemode='a',   #append to file
                        level=logging.DEBUG)
    logging.debug('Generating log file')
    print('Saving log file to: '+log_file)


def release_motors():
    if arduino != "":    
        print('PI -> ARDUINO: release')
        arduino.write('r'.encode('ascii'))
        arduino.write('m'.encode('ascii'))
        print(arduino.readline())
        arduino.close()





if __name__ == '__main__':

    print('Running: drawing_robot_main.py')
    
    import math
    import numpy as np
    import serial
    import time
    import logging
    from datetime import datetime

    # Call function to initialize Logging
    set_up_logging()

    # Load the path data from the .csv file
    # path: [point, steps_left, steps_right, relative_x, relative_y, x, y]
    path = load_data()

    
    # Setup the arduino interface
    arduino = set_up_arduino()

    
    # Iterate through the steps array, and send the commands to the Arduino
    for point in range(1,5):  #len(path)):

        # Send the steps to the arduino
        if arduino != "":
            send_message_2_arduino(point,path[point,1],path[point,2])

        # Print the current movement 
        print('moving to point ' + str(point+1) + '/' + str(path.shape[0]))
        print()

        # Log the current movement
        logging.debug('%s / %s,   %s %s', str(point+1), str(path.shape[0]),
                      str(path[point,1]), str(path[point,2]) )



    # Once the trajectory is completed, tell the Arduino to release the motors
    release_motors()




    
