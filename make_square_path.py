#! python
#
# in linux use #! /usr/bin/python

# Generate a square trajectory and plot in x-y


print('running make_square_path.py')

import matplotlib.pyplot as plt

plt.plot([0,2,2,0],[0,0,2,2],'o')
plt.axis([-1,3,-1,3])
plt.grid(True)
plt.show()
