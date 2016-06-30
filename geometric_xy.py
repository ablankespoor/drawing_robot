#!/usr/bin/python3
#
# Make some geometric trajectories and output the x-y coordinates

print('Running: geometric_xy.py')

import matplotlib.pyplot as plt
import math
import numpy as np

file_name = 'nested_squares'
file_path = 'DrawingInputFiles/'
output_file = file_name[:file_name.find('.')]+'.csv'


    
# Iterate through the gcode and fine the trajectory (lines with "G1")
path_x = list()
path_y = list()
path   = list()

# Define parameters of initial square
side   = 100
delta  = 5
number = 10

path   = list()

for ii in range(0,number):
    print('square number ' + str(ii+1) + ' sides = ' + str(side-ii*delta))

    # Make the 4 corners for a given ii'th square
    current_side = side - ii*delta

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
print(path)
        

    
    






#offset = path[0,:]
#path = path - offset

# Save the path data and export to Raspberry Pi for plotting
np.savetxt(file_path+output_file,path,delimiter=",")

# Plot the xy points
plt.plot(path[:,0],path[:,1],'.-',path[0][0],path[0][1],'o')
plt.title('X-Y Coordinates from Gcode')
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')
plt.grid(True)
plt.show()
