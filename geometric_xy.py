#!/usr/bin/python3
#
# Make some geometric trajectories and output the x-y coordinates
#
# TODO:
#     the __main__ portion needs work
#        - fix the file names for the nested circles
#        - can I pass arguments (type of geo-shape?) to plot)  ... sort of manual right now 



def nested_squares(side_length,delta,number_of):

    path   = list()

    for ii in range(0,number_of):
        print('square number ' + str(ii+1) + ' side = ' +
              str(side_length-ii*delta))

        # Make the 4 corners for a given ii'th square
        current_side = side_length - ii*delta

        # Upper Left
        x = -0.5 * current_side
        y = 0.5 * current_side
        path.append([x,y])

        # Upper Right
        x = 0.5 * current_side
        y = 0.5 * current_side
        path.append([x,y])

        # Lower Right
        x = 0.5 * current_side
        y = -0.5 * current_side
        path.append([x,y])

        # Lower Left
        x = -0.5 * current_side
        y = -0.5 * current_side
        path.append([x,y])


    print()
    path = np.array(path)

    return path




def nested_circles(start_radius,delta,number_of):
    
    path = list()
    
    # Iterate for a single circle
    for ii in range(0,number_of):

        current_radius = start_radius - ii*delta
        if current_radius <=0:
            print('current_radius must be greater than 0, stopping...')
            break

        # Calculate the curret circle resolution
        tuning = 5         # lower number is more points in circles
        delta_theta = int(tuning * (start_radius/current_radius))
        print(str(current_radius)+' radius   '+str(delta_theta)+' del theta')

        # Iterate for the points in a given circle
        for theta in range(0,360,delta_theta):
            x = current_radius * math.cos(theta*3.14/180)
            y = current_radius * math.sin(theta*3.14/180)

            path.append([x,y])
            
        
    path = np.array(path)
    
    return path
  

def five_move_rectangle(x_length,y_length):
    path = list()

    path.append([0,0])
    path.append([x_length,0])
    path.append([0,-y_length])
    path.append([0,0])
    path.append([x_length,-y_length])
    path.append([x_length,0])
    path.append([0,0])

    path = np.array(path)

    return path
        



def plotter(path):
    # Plot the xy points
    plt.plot(path[:,0],path[:,1],'.-',path[0][0],path[0][1],'o')
    plt.plot([0,0],[-10, 10],'k',[-10,10],[0,0],'k',lw=2)
    plt.title('X-Y Coordinates from Gcode')
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.grid(True)
    plt.show()





if __name__ == '__main__':

    #shape = 'nested_squares'
    #shape = 'nested_circles'
    shape = 'rectangle'

    import matplotlib.pyplot as plt
    import math
    import numpy as np

    print('Running: geometric_xy.py for --->  '+shape)

    if shape == 'nested_squares':
        path = nested_squares(50,5,3)
    if shape == 'nested_circles':
        path = nested_circles(40,1,30)
    if shape == 'rectangle':
        path = five_move_rectangle(20,50)

    # Save the path data and export to Raspberry Pi for plotting
    file_name   = shape
    file_path   = 'DrawingInputFiles/'
    output_file = file_name+'.csv'
    np.savetxt(file_path+output_file,path,delimiter=",")
    

    # Plot the path
    plotter(path)

    
