#!/usr/bin/python3
#
# Read some g-code files and extract the x-y coordinates

print('Running: Gcode2xy.py')

import matplotlib.pyplot as plt
#import math
import numpy as np

# load the Gcode file
file_path = 'Data/'
file_name = 'PelotonLinkLogoFromUnicorn.gcode'

with open(file_path+file_name) as f:
    gcode = f.read().splitlines()
f.close()
    
# Iterate through the gcode and fine the trajectory (lines with "G1")
path_x = list()
path_y = list()

for line in gcode[0:1320]:
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
        if y > -100:
            path_x.append(x)
            path_y.append(y)



# Plot the xy points
plt.plot(path_x,path_y,'.')
plt.title('X-Y Coordinates from Gcode')
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')
plt.grid(True)
plt.show()








