#!/usr/bin/python3
#
# Read some g-code files and extract the x-y coordinates

print('Running: Gcode2xy.py')

import matplotlib.pyplot as plt
#import math
import numpy as np

# load the Gcode file
#file_name = 'PelotonLinkLogo.gcode'
#file_name = 'cat_outline_from_unicorn.gcode'
#file_name = 'circle_from_unicorn.gcode'
#file_name = 'Star-Wars-Yoda.gcode'
#file_name = 'yoda_from_plotterize.gcode'
#file_name = 'sitting_cat_outline.gcode'
#file_name = 'tiger_10_4_16_with_unicorn.gcode'
file_name = 'cat_outline_11_9_16_tsp.gcode'

#file_path = 'DrawingInputFiles/'
#file_path = '/home/pi/Documents/image_gcode_developmen/gcode_files/'
file_path = '/home/pi/Documents/drawing_robot/DrawingInputFiles/'
output_file = file_name[:file_name.find('.')]+'_original.csv'


with open(file_path+file_name) as f:
    gcode = f.read().splitlines()
f.close()
    
# Iterate through the gcode and fine the trajectory (lines with "G1")
path_x = list()
path_y = list()
path   = list()

for line in gcode:
    
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
print(offset)
path = path - offset

# Save the path data and export to Raspberry Pi for plotting
np.savetxt(file_path+output_file,path,fmt='%.2f',delimiter=",")

# Plot the xy points
plt.plot(path[:,0],path[:,1],'.-',path[0][0],path[0][1],'o')
plt.title('X-Y Coordinates from Gcode')
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')
plt.grid(True)
plt.show()


 







