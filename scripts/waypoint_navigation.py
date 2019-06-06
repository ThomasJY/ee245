#!/usr/bin/env python

import math
from math import cos, sin, pi
import numpy as np
from crazyflieParser import CrazyflieParser

def circle2D():
    loop = 3
    waypoints = [[0.5*cos(t), 0.5*sin(t) - 1.5, 1] for t in np.linspace(0, 2*pi*loop, 60*loop)]
    return waypoints

def figure8_2D():
    waypoints1 = [[-0.5*cos(t) + 1, 0.5*sin(t) - 1.5, 1] for t in np.linspace(0, 2*pi, 60)]
    waypoints2 = [[0.5*cos(t), 0.5*sin(t) - 1.5, 1] for t in np.linspace(0, 2*pi, 60)]
    waypoints = waypoints1 + waypoints2
    return waypoints

def figure8_3D():
    a = -pi/12
    R = np.array([  [cos(a), 0, -sin(a)],
                    [0,      1,       0],
                    [sin(a), 0, cos(a)]])

    waypoints1 = [[-0.5*cos(t) + 1, 0.5*sin(t) - 1.5, 1] for t in np.linspace(0, 2*pi, 60*2)]
    waypoints2 = [[0.5*cos(t), 0.5*sin(t) - 1.5, 1] for t in np.linspace(0, 2*pi, 60*2)]
    waypoints = np.array(waypoints1 + waypoints2)
    waypoints = R.dot(waypoints.T).T
        
    return list(waypoints)


if __name__ == '__main__':

    index = 3   # for cf1
    initialPosition = [0,-1.5,0] # x,y,z coordinate for this crazyflie
    cfs = CrazyflieParser(index, initialPosition)
    cf = cfs.crazyflies[0]
    time = cfs.timeHelper

    cf.setParam("commander/enHighLevel", 1)
    cf.setParam("stabilizer/estimator", 2) # Use EKF
    cf.setParam("stabilizer/controller", 2) # Use mellinger controller
    #cf.setParam("ring/effect", 7)

    cf.takeoff(targetHeight = 0.5, duration = 3.0)
    time.sleep(3.0)

    # FILL IN YOUR CODE HERE
    # Please try both goTo and cmdPosition

    # 2D multi-segment straight line trajectory
    # print(cf.position())  
    # cf.goTo([1.5, 0, 0.5], 0, 3, relative=True)
    # time.sleep(12.0)
    # print(cf.position())
    # cf.goTo([-1.5, 0, 0], 0, 3, relative=True)
    # time.sleep(12.0)
    # print(cf.position())  
    # print("2D line")

    # # 2D circular trajectory
    # cf.goTo([0.5, 0, 0], 0, 3, relative=True)
    # time.sleep(3.0)
    # waypoints = circle2D()
    # for t in range(len(waypoints)):
    #     cf.cmdPosition(waypoints[t], 0)
    #     time.sleep(0.1)

    # time.sleep(15.0)
    # print(cf.position())
    # print("circle")

    # # 2D figure-8 trajecduitory
    # waypoints = figure8_2D()
    # # print(waypoints)
    # for t in range(len(waypoints)):
    #     cf.cmdPosition(waypoints[t], 0)
    #     time.sleep(0.1)
    # time.sleep(3.0)
    # print(cf.position())
    # print("8")

    # 3D figure-8 trajectory
    waypoints = figure8_3D()
    cf.goTo(waypoints[0], 0, 5, relative=True)  
    time.sleep(10.0)
    for t in range(len(waypoints)):
        if t < 20:
            print(waypoints[t])
        cf.cmdPosition(waypoints[t], 0)
        time.sleep(0.1)
    time.sleep(3.0)      

    cf.land(targetHeight = 0.0, duration = 5.0)
    time.sleep(5.0)
