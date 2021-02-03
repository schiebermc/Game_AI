"""
This module is currently a sandbox for trying out different solvers

"""
import numpy as np
from solvers import *
from copy import deepcopy
from collections import namedtuple
import matplotlib.pyplot as plt
from random import randint, seed
from utils import totalDistance

TestSet = namedtuple("TestSet", ['points', 'n', 'm'])

def generateTestSet1():
    # static test set for testing
    n = m = 20
    n_points = 10
    seed(0)
    points = list(set([(randint(0, m-1), randint(0, n-1)) for ex in range(n_points)])) 
    return TestSet(points, n, m) 


def printDistanceAndPlot(points, name):

    print("Path: {}".format(points))
    total_distance = totalDistance(points)
    
    plt.plot(*np.asarray(points).T, marker='s')
    plt.title("Path Traveled Using Algorithm: {}\nTotal Distance: {}".\
        format(name, round(totalDistance(points), 2)))
    plt.show()


test_these = [HorizontalSortSolver, VerticalSortSolver, BruteForceSolver]


for class_name in test_these: 
    
    # use test set of choice    
    test_set = generateTestSet1()
    points, n, m = test_set.points, test_set.n, test_set.m    

    # create solver
    solver = class_name(n, m, points)
   
    # solve and evaluate 
    points = solver.computePath()
    printDistanceAndPlot(points, solver.name)


