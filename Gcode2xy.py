#!/usr/bin/python3
#
# Read some g-code files and extract the x-y coordinates

print('Running: Gcode2xy.py')

import matplotlib.pyplot as plt
#import math
import numpy as np

# load the Gcode file
file_path = 'Data/'
file_name = 'PelotonLinkLogo.gcode'
output_file = 'PelotonLinkLogoXY.txt'

with open(file_path+file_name) as f:
    gcode = f.read().splitlines()
f.close()
    
# Iterate through the gcode and fine the trajectory (lines with "G1")
path_x = list()
path_y = list()
path   = list()

for line in gcode[0:1300]:
    # Save the lines that start with G1
    if line.find('G1') == 0:
        # Save the x-y coordinates
        index_x1 = line.find('X')
        index_x2 = line.find(' ',index_x1)
        index_y1 = line.find('Y')
        index_y2 = line.find(' ',index_y1)
        # Exlude the "Peloton" text (couldn't crop in Inkscape...)
        x = float(line[index_x1+1:index_x2])
        y = float(line[index_y1+1:index_y2])
        if y > -30:
            path_x.append(x)
            path_y.append(y)
            path.append([x,y])


path = np.array(path)

##print(path[0:5][:])
### Move the initial point to the origin
##for index in range(1,path.shape[0]):
###for index in range(1,5):
##    print(str(index) + '  ' + str(path[index,0]) + '  ' + str(path[index, 1]))
##    path[index][0] = path[index][0] - path[0][0]
##    path[index,1] = path[index,1] - path[0][1]
##path[0][:] = [0, 0]
##
##print()
##print(path[0:5][:])

offset = path[0,:]
path = path - offset


# Plot the xy points
plt.plot(path[:,0],path[:,1],'.-',path[0][0],path[0][1],'o')
plt.title('X-Y Coordinates from Gcode')
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')
plt.grid(True)
plt.show()

# Save the path data and export to Raspberry Pi for plotting
np.savetxt('Data/PelotonLogoXY.csv',path,delimiter=",")
 







