"""
This module is currently a sandbox for trying out different solvers

"""
import time
import numpy as np
from solvers import *
from copy import deepcopy
from collections import namedtuple
import matplotlib.pyplot as plt
from random import randint, seed
from utils import totalDistance

TestSet = namedtuple("TestSet", ['points', 'n', 'm'])
TestPackage = namedtuple("TestPackage", ['test_set_funs', 'algos'])

def generateTestSet1():
    # small enough for BruteForce to work (30s)
    n = m = 20
    n_points = 10
    seed(0)
    points = list(set([(randint(0, m-1), randint(0, n-1)) for ex in range(n_points)])) 
    return TestSet(points, n, m) 


def generateTestSet2():
    # larger, last one a python Branch and Bound solver can do (120s)
    n = m = 50
    n_points = 12
    seed(0)
    points = list(set([(randint(0, m-1), randint(0, n-1)) for ex in range(n_points)])) 
    return TestSet(points, n, m) 


def generateTestSet3():
    # larger, last one a python Branch and Bound solver can do (120s)
    n = m = 200
    n_points = 500
    seed(0)
    points = list(set([(randint(0, m-1), randint(0, n-1)) for ex in range(n_points)])) 
    return TestSet(points, n, m) 


def generateTestSet4():
    # larger, last one a python Branch and Bound solver can do (120s)
    n = 50
    m = 1000
    n_points = 500
    seed(0)
    points = list(set([(randint(0, m-1), randint(0, n-1)) for ex in range(n_points)])) 
    return TestSet(points, n, m) 


def printDistanceAndPlot(points, name, total_time):
    # plot the path, total distance, and time
    total_distance = totalDistance(points)
    plt.plot(*np.asarray(points).T, marker='s')
    plt.title("Path Traveled Using Algorithm: {}\nTotal Distance: {} - Time: {:0.3e}".\
        format(name, round(totalDistance(points), 2), total_time))
    plt.show()


if __name__ == "__main__":

    # define the tests you want to try
    test1 = TestPackage(
                        [generateTestSet3, generateTestSet4],
                        [HorizontalSortSolver, VerticalSortSolver, OriginSortSolver, NearestNeighborSolver]
                        )
    
    for test_set_fun in test1.test_set_funs:
        
        for class_name in test1.algos: 
            
            # retrieve test set
            test_set = test_set_fun()
            points, n, m = test_set.points, test_set.n, test_set.m    
        
            # create solver
            solver = class_name(n, m, points)
           
            # solve 
            t0 = time.time()
            points = solver.computePath()
            total_time = time.time() - t0        

            # evaluate
            printDistanceAndPlot(points, solver.name, total_time)






