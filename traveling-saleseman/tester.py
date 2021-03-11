"""
This module is currently a sandbox for trying out different solvers

"""

import os
import time
from solvers import *
from copy import deepcopy
from math import sin, cos, pi
from collections import namedtuple
from random import randint, seed, uniform
from utils import *

TestSet = namedtuple("TestSet", ['points', 'n', 'm'])
TestPackage = namedtuple("TestPackage", ['test_set_funs', 'algos'])

###############################################################################
###### Test Sets ##############################################################
###############################################################################
def testSetRandomUniform1():
    # small enough for BruteForce to work (30s)
    n = m = 20
    n_points = 10
    seed(0)
    points = list(set([(randint(0, m-1), randint(0, n-1)) for ex in range(n_points)])) 
    return TestSet(points, n, m) 


def testSetRandomUniform2():
    # larger, last one a python Branch and Bound solver can do (120s)
    n = m = 50
    n_points = 12
    seed(0)
    points = list(set([(randint(0, m-1), randint(0, n-1)) for ex in range(n_points)])) 
    return TestSet(points, n, m) 


def testSetRandomUniform3():
    n = m = 100
    n_points = 35
    seed(0)
    points = list(set([(randint(0, m-1), randint(0, n-1)) for ex in range(n_points)])) 
    return TestSet(points, n, m) 


def testSetRandomUniform4():
    n = 1000
    m = 1000
    n_points = 300
    seed(0)
    points = list(set([(randint(0, m-1), randint(0, n-1)) for ex in range(n_points)])) 
    return TestSet(points, n, m) 


def testSetRandomUniform5():
    n = 10000
    m = 10000
    n_points = 1000
    seed(0)
    points = list(set([(randint(0, m-1), randint(0, n-1)) for ex in range(n_points)])) 
    return TestSet(points, n, m) 


def testSetCircle1():
    n = 100
    m = 100
    n_points = 100
    center = [n // 2, m  // 2]
    r = n // 4
    seed(0)
    
    points = []
    for sample in range(n_points):
        sample_theta = uniform(0., 2 * pi)
        x_shift = cos(sample_theta) * r
        y_shift = sin(sample_theta) * r
        points.append((center[0] + x_shift, center[1] + y_shift))
    
    return TestSet(points, n, m) 


def testSetTwoDisjointCities1():
    # deliveries occur within two separable cities
    n = 1000
    m = 1000
    n_points = 300
    seed(0)
    
    # define cities as rectangles, defined by upper right and lower left vertex
    city1 = [(10, 10), (200, 800)]
    city2 = [(500, 10), (700, 800)]

    points = []
    for sample in range(n_points // 2):

        points.append((uniform(city1[0][0], city1[1][0]), 
                       uniform(city1[0][1], city1[1][1])))
        
        points.append((uniform(city2[0][0], city2[1][0]), 
                       uniform(city2[0][1], city2[1][1])))

    return TestSet(points, n, m)    



###############################################################################
###### End Test Sets ##########################################################
###############################################################################

if __name__ == "__main__":

    # define the tests you want to try
    test1 = TestPackage(
                        [testSetRandomUniform4], 
                        [GenticAlgorithmSolver]
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
            printDistanceAndPlot(points, solver.name, test_set_fun.__name__, total_time, 
                    os.path.join('./figures', test_set_fun.__name__ + '_' + class_name.__name__ + '.png'))



