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

    delta_t = numpy.array(delta_t)
    return delta_t


def extract_steps(lines):

    steps  = list()

    for line in lines[3:]:
        index_steps = line.find('steps')+7
        left_steps  = line[index_steps:line.find(' ',index_steps)]
        right_steps = line[line.find(' ',index_steps)+1:]
        #print(left_steps, right_steps)
        steps.append([float(left_steps), float(right_steps)])

    steps = numpy.array(steps)
    return steps
        


def plot_delta_t(delta_t):
    # Plot the difference in time
    plt.figure(1)
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

def plot_steps_vs_time(t,steps):
    plt.figure(2)
    plt.plot(t[2:],abs(steps[:,0]),'b.',t[2:],abs(steps[:,1]),'r.')
    plt.title('Steps vs Travel Time')
    plt.xlabel('time [s]')
    plt.ylabel('steps')
    plt.grid(True)

    

if __name__ == '__main__':

    import math
    import numpy
    import time
    from datetime import datetime
    import matplotlib.pyplot as plt

    print('Running: examine_logs.py')
    print()

    with open('LogFiles/logfile_2017_04_07_08_16.log', 'r') as f:
        lines = f.readlines()
    
    # Extract the differences in time samples
    delta_t = extract_delta_time(lines)

    # Extract the number of steps
    steps = extract_steps(lines)

    # Output mean and median
    print('mean   ',numpy.mean(delta_t))
    print('median ',numpy.median(delta_t))
    
    # Plot the data
    plot_delta_t(delta_t)
    plot_steps_vs_time(delta_t,steps)
    plt.show()



    
    

    
