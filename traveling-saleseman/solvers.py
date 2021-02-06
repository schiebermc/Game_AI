"""
    Solvers for TSP by Matthew Schieber
    All implementations by me, with motivation from: 
        https://en.wikipedia.org/wiki/Travelling_salesman_problem
    
    Please make any suggestions at https://github.com/schiebermc/Game_AI

    Current Status:
        Exact Solvers:
            - BruteForceSolver (all permuations)
            - HeldKarpSolver (all perm. + dynamic programming)
            - BBSolver (branch and bounds / dfs + pruning)

        Basic (highly approximate) Solvers:
            - HorizontalSortSolver
            - VerticalSortSolver
            - OriginSortSolver
            - RandomSampleSolver

        Greedy Solvers:
            - NearestNeighborSolver
            - NearestNeighborSolverParallel


"""
import abc
import concurrent.futures
from copy import deepcopy
import multiprocessing as mp
from random import shuffle, seed, randint
from collections import defaultdict
from utils import distance, totalDistance
from itertools import permutations, combinations

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
    
    # *very* approximate
    # TC: O(nlogn)

    def __init__(self, n, m, points):
        BaseSolver.__init__(self, n, m, points)

    def computePath(self):
        self.points.sort(key=lambda x:x[0])
        return self.points


class VerticalSortSolver(BaseSolver):

    name = "VerticalSort"

    # *very* approximate
    # TC: O(nlogn)

    def __init__(self, n, m, points):
        BaseSolver.__init__(self, n, m, points)

    def computePath(self):
        self.points.sort(key=lambda x:x[1])
        return self.points


class OriginSortSolver(BaseSolver):

    name = "OriginSort"

    # *very* approximate (last one i promise xD)
    # TC: O(nlogn)

    def __init__(self, n, m, points):
        BaseSolver.__init__(self, n, m, points)

    def computePath(self):
        self.points.sort(key=lambda x:(x[0]**2 + x[1]**2))
        return self.points


class BruteForceSolver(BaseSolver):

    name = "BruteForce"
    
    # exact 
    # TC: O(n!)

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


class RandomSampleSolver(BaseSolver):

    name = "RandomSampler"
    
    # *very* approximate
    # TC: O(N) 

    def __init__(self, n, m, points, samples=1000):
        BaseSolver.__init__(self, n, m, points)
        self.samples = samples

    def computePath(self):
        best = [float('inf'), None]
        for i in range(self.samples):
            shuffle(self.points)            
            dist = totalDistance(self.points)
            if dist < best[0]:
                best = [dist, deepcopy(self.points)]
        return best[1]


class BBSolver(BaseSolver):

    name = "BranchAndBound"
    
    # exact 
    # TC: O(N!) (but prunes a lot. do not use past ~30 points)

    def __init__(self, n, m, points):
        BaseSolver.__init__(self, n, m, points)

    def computePath(self):
        
        self.best = [float('inf'), None]
        self.curr = []

        def dfs(last, todo, dist=0):

            # prune if this branch cannot beat an already logged optima            
            if dist >= self.best[0]:
                return

            if len(todo) == 0:
                self.best = [dist, deepcopy(self.curr)]
                # every time we get here, we have something better :)
                print(self.best)

            # try all remaining points
            vals = list(todo)
            for i in vals:
                todo.remove(i)
                self.curr.append(i)
                dfs(i, todo, dist + distance(self.points[last], self. points[i]))
                todo.add(i)
                self.curr.pop()

        # iterate over all starting points
        for i in range(len(self.points)):
            todo = set([j for j in range(len(self.points))])
            todo.remove(i)
            self.curr = [i]
            dfs(i, todo)            

        return [self.points[i] for i in self.best[1]]


class NearestNeighborSolver(BaseSolver):

    name = "NearestNeighbor"
    
    # approximate
    # TC: O(N^3) 

    def __init__(self, n, m, points):
        BaseSolver.__init__(self, n, m, points)

    def computePath(self):
        
        seed(0)
        
        c = []
        k = len(self.points)
        for i in range(k):
            c.append([])
            for j in range(k):
                # note: randint here is just used as a tiebreaker in the event that two cities
                # are equidistant from curr. Without seeding, this would be nondeterministic
                c[i].append((distance(self.points[i], self.points[j]), randint(1, 100), j)) 

        for i in range(k):
            c[i].sort()

        seed(0)
        best = [float('inf'), None]
        for start in range(k):

            dist = 0      
            used = set([start])
            curr = start
            res = [start]

            while(len(used) != k):

                for this_dist, tiebreaker, j in c[curr]:
                    if not j in used:
                        dist += this_dist
                        curr = j
                        break

                used.add(curr)
                res.append(curr)
                
            if dist < best[0]:
                best = [dist, res]

        return [self.points[i] for i in best[1]]


class NearestNeighborSolverParallel(BaseSolver):

    name = "NearestNeighborParallel"
    
    # approximate
    # TC: O(N^3 / p)
    # This algorithm is pleasantly parallel 

    def __init__(self, n, m, points):
        BaseSolver.__init__(self, n, m, points)

    def computeNNPathFromHere(self, start, k, c):
        
        dist = 0      
        used = set([start])
        curr = start
        res = [start]
        while(len(used) != k):

            for this_dist, tiebreaker, j in c[curr]:
                if not j in used:
                    dist += this_dist
                    curr = j
                    break

            used.add(curr)
            res.append(curr)
    
        return (dist, res)


    def computePath(self, n_threads=4):
        
        seed(0)
        
        c = []
        k = len(self.points)
        for i in range(k):
            c.append([])
            for j in range(k):
                # note: randint here is just used as a tiebreaker in the event that two cities
                # are equidistant from curr. Without seeding, this would be nondeterministic
                c[i].append((distance(self.points[i], self.points[j]), randint(1, 100), j)) 

        for i in range(k):
            c[i].sort()

        items = [(start, k, c) for start in range(k)]
        executor = concurrent.futures.ProcessPoolExecutor(n_threads, mp_context=mp.get_context('fork'))
        futures = [executor.submit(self.computeNNPathFromHere, *item) for item in items]
        concurrent.futures.wait(futures) 

        # get best result
        best = [float('inf'), None]
        for future in futures:
            dist, res = future.result()
            if dist < best[0]:
                best = [dist, res]

        return [self.points[i] for i in best[1]]


class HeldKarpSolver(BaseSolver):

    name = "Held-Karp"
    
    # exact 
    # TC: O(2^nsqrt(n))

    def __init__(self, n, m, points):
        BaseSolver.__init__(self, n, m, points)

    def computePath(self):

        # NOTE: this algorithm is assuming first postion is starting point
        # A workaround is required: 
        # 1) iterate over all points or
        # 2) add this assumption to other algorithms.
        for i in range(len(self.points)):
            points = self.points[i:] + self.points[:i]
            self.hk(points)


    def hk(self, points):

        # .. it's not quite right, and currently does not return path. 
        # so needs worked up.

        # init the distance matrix
        k = len(points)
        c = [[0] * k for i in range(k)]
        for i in range(k):
            for j in range(k):
                c[i][j] = distance(points[i], points[j])

        g = defaultdict(dict)
        for i in range(1, k):
            g[tuple([i])][i] = c[i][0]

        inds = [i for i in range(1, k)]
        for s in range(2, k):
            for combo in combinations(inds, s):
                for k in combo:
                    best = float('inf')
                    for m in combo:
                        if m == k:
                            continue
                        
                        # here I take the set difference, keeping
                        # in mind that the tuple must be lexographically
                        # sorted in order for the DP to work correctly
                        diff = list(set(combo) - set([k]))
                        diff.sort()
                        diff = tuple(diff)
                        
                        best = min(best, g[diff][m] + c[m][k])
                    
                    g[combo][k] = best
        
        best = float('inf')
        for i in range(1, k):
            best = min(best, g[tuple(inds)][i] + c[i][0])

        # whoops, need to return the path associated with best, 
        # but that info was lost along the way. need to circle back to this
        return points


