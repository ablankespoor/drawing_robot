#!/usr/bin/python3
#
# Read g-code file and generate the number of motor steps.
# The input is a .gcode file generated with Unicorn in Inkscape
# The output is a .csv file with the number of steps to send
#   the Arduino

def extract_xy_from_Gcode(file):
    with open(file) as f:
        Gcode = f.read().splitlines()
    f.close()

    # Iterate through the gcode and fine the trajectory (lines with "G1")
    path   = list()

    for line in Gcode:
        if line == '(end of print job)':
            break

        # Save the lines with X-Y movement instructions
        if line.find('G1') == 0:
            # Save the x-y coordinates
            index_x1 = line.find('X')
            index_x2 = line.find(' ',index_x1)
            index_y1 = line.find('Y')
            index_y2 = line.find(' ',index_y1)

            x = float(line[index_x1+1:index_x2])
            y = float(line[index_y1+1:index_y2])

            path.append([x,y])

    path = np.array(path)

    # Remove any initial displacements (start at 0,0)
    to_zero = path[0,:]
    path = path - to_zero

    return path

def convert_length_to_steps(del_left,del_right):
    # [left,right] = length2Steps(distance_left,distance_right)

    r     = robot['pully_radius']
    steps = robot['motor_steps']
    
    mm2step = steps / (2 * 3.14 * r)
    steps_left  = del_left * mm2step
    steps_right = del_right * mm2step
    return round(steps_left), round(steps_right)



def find_change_in_length(xy1,xy2):
    # Given two points, find the change in length of the two strings
    # [left,right] = changeInLength(start_point,end_point)

    dm = robot['motor_to_motor_dist']
    
    # Find the initial length
    length_left_1  = math.sqrt(xy1[0]**2 + xy1[1]**2)
    length_right_1 = math.sqrt((dm-xy1[0])**2 + xy1[1]**2)

    # Find the final length
    length_left_2  = math.sqrt(xy2[0]**2 + xy2[1]**2)
    length_right_2 = math.sqrt((dm-xy2[0])**2 + xy2[1]**2)

    # Return the change in lengths
    return length_left_2 - length_left_1, length_right_2 - length_right_1



def find_change_in_xy(xy1,xy2):
    # Given two points, find the change in relative position
    # used in the output for the user
    #[del_x,del_y] = changeInXY(start_point,end_point)
    del_x = xy2[0] - xy1[0]
    del_y = xy2[1] - xy1[1]

    return del_x,del_y



def find_motor_steps(path):
    steps = np.zeros([len(path),6])
    
    for point in range(1,len(path)):
        # Find the relative change in xy to the next point
        [del_x,del_y] = find_change_in_xy(path[point-1],path[point])
        #print('moving to point ' + str(point+1) + '/' + str(path.shape[0]) + '    ['+str(del_x)+', '+str(del_y)+']')
        steps[point,2:] = [del_x, del_y, path[point,0], path[point,1] ]

        # Find the change in the string length for left and right
        [del_left,del_right] = find_change_in_length(path[point-1],path[point])

        # Find the number of steps for each motor
        [steps_left,steps_right] = convert_length_to_steps(del_left,del_right)
        steps[point,0:2] = [steps_left, steps_right]

    return steps



def plotter(path):
    # Plot the xy points
    plt.plot(path[:,0],path[:,1],'.-',path[0][0],path[0][1],'o')
    plt.title('X-Y Coordinates')
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.grid(True)
    plt.show()
    







if __name__ == '__main__':
    print('Running: generate_motor_steps.py')

    import matplotlib.pyplot as plt
    import math
    import numpy as np

    # Import my file names and the robot parameters
    import load_my_file
    import robot_parameters

    global robot
    robot = robot_parameters.bench_robot

    
    # Call my script to open a file from a list
    file_name = load_my_file.file_namer()
    file_path = load_my_file.file_path_os('win')
    output_file = file_name[:file_name.find('.')]+'.csv'

    


    # Open Gcode file and extract the X,Y trajectory points
    path = extract_xy_from_Gcode(file_path+file_name)
    # Plot the trajectory
    #plotter(path)

    # Run through the array and calculate the number of motor steps
    # [steps_left, steps_right, relative_x, relative_y, x, y]
    step_data = find_motor_steps(path)
    print()
    print('step_left, step_right,   rel_x, rel_y,   x, y')
    print(step_data[0:10])



    # Save the path data and export to Raspberry Pi for plotting
    np.savetxt(file_path+output_file,step_data,delimiter=",")




     







