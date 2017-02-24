#!/usr/bin/python3
#
# examine_logs.py
#
# Code to load and examine the log file data




def extract_delta_time(lines):

    times   = list()
    delta_t = list()

    for line in lines:
        t = line[0:line.find(',')]
        times.append(t)

    fmt = '%Y-%m-%d  %H:%M:%S.%f'
    for ii in range(1,len(times)):
        # Find the decimal point of the seconds
        point_index = times[ii].find('.')
        # Convert the time-stamp strings to floats
        t2=(time.mktime(time.strptime(times[ii],fmt)))+float(times[ii][point_index:])
        t1=(time.mktime(time.strptime(times[ii-1],fmt)))+float(times[ii-1][point_index:])

        delta_t.append(t2-t1)

    return delta_t



def plot_delta_t(delta_t):
    # Plot the difference in time
    plt.subplot(211)
    plt.plot(delta_t,'.',)
    plt.title('Delta T from Log Files')
    plt.xlabel('sample number')
    plt.ylabel('delta T [s]')
    plt.grid(True)

    # Plot histogram of time samples
    plt.subplot(212)
    plt.hist(delta_t,100)
    plt.xlabel('delta T [s]')
    plt.ylabel('count')
    plt.grid(True)
    plt.show()

    

if __name__ == '__main__':

    import math
    import numpy
    import serial
    import time
    import logging
    from datetime import datetime
    import matplotlib.pyplot as plt

    print('Running: examine_logs.py')
    print()

    with open('LogFiles/logfile_2017_02_10_19_45.log', 'r') as f:
        lines = f.readlines()
    
    # Extract the differences in time samples
    delta_t = extract_delta_time(lines)

    # Output mean and median
    print('mean   ',numpy.mean(delta_t))
    print('median ',numpy.median(delta_t))
    
    # Plot the data
    plot_delta_t(delta_t)



    
    

    
