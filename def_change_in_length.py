#! python
#
# in linux use #! /usr/bin/python

# Begining of code for a function to determine
# the change in length of the two strings

# [del_left, del_right] = change_in_length(x1,y1,x2,y2,dm)


print('running def_change_in_length.py')
print()

import matplotlib.pyplot as plt
import math

x1 = 5
y1 = -5
x2 = 7
y2 = -10

dm = 16         # distance between motors

# Find the beginning length of strings
l_left_1  = math.sqrt(x1**2 + y1**2)
l_right_1 = math.sqrt((dm-x1)**2 + y1**2)

# Find the ending length of strings
l_left_2  = math.sqrt(x2**2 + y2**2)
l_right_2 = math.sqrt((dm-x2)**2 + y2**2)

# Find delta length
del_left  = l_left_2 - l_left_1
del_right = l_right_2 - l_right_1

print(del_left)
print(del_right)


plt.plot([0,16],[0,0],'o')
plt.plot([x1,x2],[y1,y2],'bo')
plt.axis([-1,20,-20,1])
plt.grid(True)
plt.show()
