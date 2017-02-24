#!/usr/bin/python3
#
# Make some geometric trajectories and output the x-y coordinates
#
# TODO:
#     the __main__ portion needs work
#        - fix the file names for the nested circles
#        - can I pass arguments (type of geo-shape?) to plot)  ... sort of manual right now
#
#   On 2/6/2017 I started making a subfunction to divide lines into smaller
#   segments.  I dicided it was more than I wanted to do for the task of
#   testing the offset problem



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
  

def test_rectangle(x_length,y_length):
    path = list()

    path.append([0,0])
    path.append([x_length,0])
    ####
    # add subpoints here
    path.append([0,-y_length])
    number_divisions = 50      # this should actually be some sort of max length...
    del_x = (path[2][0] - path[1][0]) / number_divisions
    slope = (path[2][1] - path[1][1]) / (path[2][0] - path[1][0])
    print(path)
    for ii in range(number_divisions):
        y = slope * (del_x*(ii+1)) + path[1][1]
        print(y,ii,del_x*(ii+1))
        path.append([path[1][0]+del_x*(ii+1),y])

    path.remove([0, -50])
    ####    path.append([0,-y_length])
    # subsegments = get_path_subsegments(path[-2],path[-1],3)
    path.append([0,0])
    path.append([x_length,-y_length])
    path.append([x_length,0])
    path.append([0,0])

    path = np.array(path)


    print(path)

    return path
        
##def get_path_subsegments(point_1, point_2,max_length):
##
##
##    subsegments = list()
##
##    # Find the delta x, segment length in the x direction
##    delta_x = (point_2[0]-point_1[0]) / max_length
##    direction = abs(point_2[0]-point_1[0]) / (point_2[0]-point_1[0])
##    # Find the slope
##    slope = (point_2[1] - point_1[1]) / (point_2[0] - point_1[0])
##    # Iteratively find the new segments between point1 and point2
##    x = np.arange(point_1[0],point_2[0],direction*max_length)
##    for ii in x:
##        print(ii)
##
##    
##    print(delta_x,slope)
##    print(point_1,point_2)  
##
##    return subsegments


def plotter(path):
    # Plot the xy points
    plt.plot(path[:,0],path[:,1],'.-',path[0][0],path[0][1],'o')
    plt.plot([0,0],[-10, 10],'k',[-10,10],[0,0],'k',lw=2)
    plt.title('X-Y Coordinates from Gcode')
    plt.xlabel('x [mm]')
    plt.ylabel('y [mm]')
    plt.grid(True)
    #plt.xlim([min(path[:,0]*1.1),max(path[:,0]*1.1)])
    #plt.ylim([min(path[:,1]*1.1),max(path[:,1]*1.1)])
    #plt.xlim([-180,180])   # approx size of board
    #plt.ylim([-180,180])
    plt.xlim([-10,30])
    plt.ylim([-60,10])
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
        path = test_rectangle(20,50)

    # Save the path data and export to Raspberry Pi for plotting
    file_name   = shape
    file_path   = 'DrawingInputFiles/'
    output_file = file_name+'.csv'
    np.savetxt(file_path+output_file,path,delimiter=",")
    

    # Plot the path
    plotter(path)

    
