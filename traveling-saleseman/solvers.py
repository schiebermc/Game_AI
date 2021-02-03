"""
This module implements the solver classes

"""
import abc
from utils import totalDistance
from itertools import permutations


class BaseSolver(abc.ABC):

    def __init__(self, n, m, points):
        self.n = n
        self.m = m
        self.points = points

    @abc.abstractmethod
    def computePath(self):
        pass


class HorizontalSortSolver(BaseSolver):

    name = "HorizontalSort"

    def __init__(self, n, m, points):
        BaseSolver.__init__(self, n, m, points)

    def computePath(self):
        self.points.sort(key=lambda x:x[0])
        return self.points


class VerticalSortSolver(BaseSolver):

    name = "VerticalSort"

    def __init__(self, n, m, points):
        BaseSolver.__init__(self, n, m, points)

    def computePath(self):
        self.points.sort(key=lambda x:x[1])
        return self.points


class BruteForceSolver(BaseSolver):

    name = "BruteForce"

    def __init__(self, n, m, points):
        BaseSolver.__init__(self, n, m, points)

    def computePath(self):
        
        best = [float('inf'), None]
        for perm in permutations(self.points):
            perm = list(perm)
            dist = totalDistance(perm)
            if dist < best[0]:
                best = [dist, perm]
        return best[1]

    


