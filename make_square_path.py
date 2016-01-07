#! python
#
# in linux use #! /usr/bin/python

# Generate a square trajectory and plot in x-y


print('running: make_square_path.py')

import matplotlib.pyplot as plt
import math
import numpy as np

# define points of the square
xy = np.array([[5, 0],[5,-5],[10,-5],[10,0]])

print(xy[1])
# TODO iterate through the xy array and plot the points


# TODO iterate through the xy and calculate the change in lengths

plt.plot([0,2,2,0],[0,0,2,2],'o')
plt.plot([0,2],[2,2])
plt.axis([-1,3,-1,3])
plt.grid(True)
plt.show()
