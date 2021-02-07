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
            - ChristofidesAlgorithmSolver (WIP)

"""
import abc
import concurrent.futures
from copy import deepcopy
import multiprocessing as mp
from heapq import heappush, heappop
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

        # TODO not working, circle back to this
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


class Graph():

    # graph class to help some solvers
    # uses adjacency list

    def __init__(self, n):
        self.n = n
        self.edges = {i : {} for i in range(self.n)}

    def addVertex(self, ident):
        self.edges[ident] = {}
        self.n += 1

    def addUndirectedEdge(self, i, j, c):
        self.addDirectedEdge(i, j, c)
        self.addDirectedEdge(j, i, c)

    def addDirectedEdge(self, i, j, c):
        self.edges[i][j] = min(self.edges[i].get(j, float('inf')), c)

    def PrimsMST(self):
        # return the MST using Prim's algorithm
        
        # initialize unconnected graph
        mst = Graph(self.n)

        # special heappush for efficiency
        def push(h, node1, active_set):
            if node1 in active_set:
                return
            for node2 in self.edges[node1]:
                if node2 in active_set:
                    continue
                heappush(h, (self.edges[node1][node2], node1, node2))            

        # all candidate edges, sorted    
        h = []
        
        # start with a random active vertex        
        start = randint(0, self.n-1)
        push(h, start, {})
        active = set([start])

        while(len(active) != self.n):
    
            # get the smallest edge from active vertices
            while(h[0][1] in active and h[0][2] in active):
                heappop(h) # this edge no longer relevant        
    
            dist, node1, node2 = heappop(h)
           
            # push edges to candidate queue
            push(h, node1, active)
            push(h, node2, active)

            # add edges to active set
            active.add(node1)
            active.add(node2)
            
            # add edge to mst
            mst.addUndirectedEdge(node1, node2, dist)
                
        return mst
        

class ChristofidesAlgorithmSolver(BaseSolver):
    
    name = "ChristofidesAlgorithm"
    
    # exact 
    # TC: O(2^nsqrt(n))
    
    def __init__(self, n, m, points):
        BaseSolver.__init__(self, n, m, points)

    def computePath(self):
        
        k = len(self.points)
        
        # 1) construct complete graph
        g = Graph(k)
        for i in range(k):
            for j in range(i+1, k):
                g.addUndirectedEdge(i, j, distance(self.points[i], self.points[j]))

        # 2) find MSP 
        mst = g.PrimsMST()
       
        # 3) find set of verticies, O, with odd degree in mst
        odds = set([])
        for node in range(k):
            if len(mst.edges[node]) % 2 == 1:
                odds.add(node)

        # 4) form complete subgraph using nodes in odds
        mapper = {ind, val for ind, val in enumerate(odds)}
        odds_subgraph = Graph()

        # 5) contruct minimum-weight perfect matching of this subgraph 
        #  - this is where things start to get tricky!
        #  - remember: the operations leading up to 5) have gauranteed
        #   that 






























