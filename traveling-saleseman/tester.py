"""
This module is currently a sandbox for trying out different solvers

"""
import time
from solvers import *
from copy import deepcopy
from collections import namedtuple
from random import randint, seed
from utils import *

TestSet = namedtuple("TestSet", ['points', 'n', 'm'])
TestPackage = namedtuple("TestPackage", ['test_set_funs', 'algos'])

###############################################################################
###### Test Sets ##############################################################
###############################################################################
def testSet1():
    # small enough for BruteForce to work (30s)
    n = m = 20
    n_points = 10
    seed(0)
    points = list(set([(randint(0, m-1), randint(0, n-1)) for ex in range(n_points)])) 
    return TestSet(points, n, m) 


def testSet2():
    # larger, last one a python Branch and Bound solver can do (120s)
    n = m = 50
    n_points = 12
    seed(0)
    points = list(set([(randint(0, m-1), randint(0, n-1)) for ex in range(n_points)])) 
    return TestSet(points, n, m) 


def testSet3():
    n = m = 100
    n_points = 35
    seed(0)
    points = list(set([(randint(0, m-1), randint(0, n-1)) for ex in range(n_points)])) 
    return TestSet(points, n, m) 


def testSet4():
    n = 1000
    m = 1000
    n_points = 300
    seed(0)
    points = list(set([(randint(0, m-1), randint(0, n-1)) for ex in range(n_points)])) 
    return TestSet(points, n, m) 


def testSet5():
    n = 10000
    m = 10000
    n_points = 1000
    seed(0)
    points = list(set([(randint(0, m-1), randint(0, n-1)) for ex in range(n_points)])) 
    return TestSet(points, n, m) 

###############################################################################
###### End Test Sets ##########################################################
###############################################################################

if __name__ == "__main__":

    # define the tests you want to try
    test1 = TestPackage(
                        [testSet3, testSet4, testSet5],
                        [OriginSortSolver, NearestNeighborSolver, ChristofidesAlgorithmSolver]
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
            printDistanceAndPlot(points, solver.name, total_time, 
                    test_set_fun.__name__ + '_' + class_name.__name__ + '.jpeg')



