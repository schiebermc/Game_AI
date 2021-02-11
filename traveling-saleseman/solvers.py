"""
    Solvers for TSP by Matthew Schieber
    All implementations by me, with motivation from: 
        https://en.wikipedia.org/wiki/Travelling_salesman_problem
      ( and other online resources )
    
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
from collections import defaultdict, deque
from utils import *
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


    def lowCostPerfectMatching(self):
               
        # Implementing what I am currently comfortable with, so it
        # is not quite "minCost", but "lowCost". The outline is similar
        # to Prim's above, in that we search edges based on the lowest
        # cost. In this context, the greedy search is definitely an
        # approximation. I will look into more advanced stuff later (Hungarian algo)
        # This is a shortcut to achieve a working version of Christofides. 
        # I underestimated how involved Christofides algo is in general xD 
 
        # initialize unconnected graph
        lcpm = Graph(self.n)

        h = []
        for node1 in self.edges:
            for node2 in self.edges[node1]:
                heappush(h, (self.edges[node1][node2], node1, node2))

        active = set([])             
        while(h and len(active) != self.n):
            
            # get the smallest edge from active vertices
            while(h[0][1] in active or h[0][2] in active):
                heappop(h)

            dist, node1, node2 = heappop(h)
           
            # add edges to active set
            active.add(node1)
            active.add(node2)
            
            # add edge to mst
            lcpm.addUndirectedEdge(node1, node2, dist)
            
        
        assert len(active) == len(lcpm.edges)
        return lcpm

    def minCostPerfectMatching(self):
        # here I implement the exact soluion using combinatorics. 
        # i need proof of concept before I rush and tacke the 
        # Hungarian algorithm.
        
        def costOfMatching(matching):
            summ = 0
            for i, j in matching:
                summ += self.edges[i][j]
            return summ        
    
        best = [float('inf'), None]
        for matching in generate_groups([i for i in range(self.n)]):
            cost = costOfMatching(matching)
            if cost < best[0]:
                best = [cost, matching]
 
        mcpm = Graph(self.n)
        for i, j in best[1]:
            mcpm.addUndirectedEdge(i, j, self.edges[i][j])
        
        return mcpm


    def getOddVertices(self):
        odds = set([])
        for node in self.edges:
            if len(self.edges[node]) % 2 == 1:
                odds.add(node)
        return odds


class MultiGraph():

    # needed to make a multigraph class too!
    # turns out, after trial and error, that the Euler tour calculation
    # requires that step 6 in Christofides requires union of the mst
    # and perfect matching to be a multigraph! To quickly move around
    # this issue, I partitioned the graph functions to what can be
    # done by a Graph and MultiGraph, respectively. I will try 
    # to comb through and organize better latter, but no promises!

    def __init__(self, n, graph=None):
        
        self.n = n
        self.edges = {i : defaultdict(list) for i in range(self.n)}

        if graph:
            for node1 in graph.edges:
                for node2 in graph.edges[node1]:
                    self.addUndirectedEdge(node1, 
                        node2, graph.edges[node1][node2])

    def addVertex(self, ident):
        self.edges[ident] = {}
        self.n += 1

    def addUndirectedEdge(self, i, j, c):
        self.addDirectedEdge(i, j, c)
        self.addDirectedEdge(j, i, c)
    
    def addDirectedEdge(self, i, j, c):
        self.edges[i][j].append(c)

    def removeAnEdge(self, i, j):
        # remove one of the edges between i and j. since
        # I am implementing this multigraph on the fly, i   
        # am not adding edge ids. The needed applications
        # do not require such features
       
        # since cost doesn't matter, just remove one
        # in theory, the adds were not interleaved, so pops
        # should at least target the same edge for both nodes
        val1 = self.edges[i][j].pop() 
        val2 = self.edges[j][i].pop()
        
        # if that was the last one, delete this key (breaking condition)
        if len(self.edges[i][j]) == 0:
            del self.edges[i][j]
        if len(self.edges[j][i]) == 0:
            del self.edges[j][i]
        
        assert val1 == val2
        return val1

    def reachableFromHere(self, src):
        
        # simple BFS for counting number of nodes in this component
        visited = set([])
        f = deque([src])
        
        while(f):

            node = f.pop()
            if node in visited:
                continue
            visited.add(node)
            
            for neighbor in self.edges[node]:
                if neighbor in visited:
                    continue
                f.appendleft(neighbor)
    
        return len(visited)
            

    def isBridge(self, node1, node2):

        # i wonder if disjoint sets are applicabable here? I am thinking no..
        # since they do `union` and not `divorce` xD

        c1 = self.reachableFromHere(node1)

        # remove edge, count again, and put it back
        tmp = self.removeAnEdge(node1, node2)            
        c2 = self.reachableFromHere(node1)
        self.addUndirectedEdge(node1, node2, tmp) 

        # if the count changes, an additional component was formed.
        return c1 != c2


    def getOddVertices(self):
        odds = set([])
        for node in self.edges:
            summ = 0
            for node2 in self.edges[node]:
                summ += len(self.edges[node][node2])
            if summ % 2 == 1:
                odds.add(node)
        return odds

 
    def EulerTour(self):
        
        # Fleury's Algorithm ~~
        
        # pick our starting point wisely
        odds = self.getOddVertices()
        assert len(odds) == 0 or len(odds) == 2
        start = randint(0, len(self.edges)-1) if len(odds) == 0 else odds.pop()      

        tour = []
        while(self.edges[start]):
        
            next_edge = None
            for node2 in self.edges[start]:

                # if this edge forms a bridge, we must not use it
                if self.isBridge(start, node2):
                    continue

                # great! no bridge, let's add it, and remove this edge
                next_edge = (start, node2)    
                break

            if next_edge == None:
                # there were no non-bridges, let's use the first bridge
                for node2 in self.edges[start]:
                    next_edge = (start, node2)    
                    break

            # add this edge to our tour
            tour.append((start, node2))
            
            # remove this edge (could be one of many, we are a MultiGraph now)
            self.removeAnEdge(start, node2)            
            
            # restart from destination
            start = node2

        return tour 


def shortcutEulerTour(tour):
    shorted_tour = []   
    visited = set([])
    for node1, node2 in tour:
        if not node1 in visited:
            shorted_tour.append(node1)
        if not node2 in visited:
            shorted_tour.append(node2)
        visited.add(node1)
        visited.add(node2)
    return shorted_tour 
 

class ChristofidesAlgorithmSolver(BaseSolver):
    
    name = "ChristofidesAlgorithm"
    
    # approximate
    
    def __init__(self, n, m, points):
        BaseSolver.__init__(self, n, m, points)
        
        # needed this for sanity. testing to follow
        self.debug = False

    def computePath(self):
        
        k = len(self.points)
       
        if self.debug:
            print("\nPrinting points")
            for i in range(k):
                print(i, self.points[i])
 
        # 1) construct complete graph
        g = Graph(k)
        for i in range(k):
            for j in range(i+1, k):
                g.addUndirectedEdge(i, j, distance(self.points[i], self.points[j]))

        # 2) find MSP 
        mst = g.PrimsMST()
       
        # 3) find set of verticies, O, with odd degree in mst
        odds = mst.getOddVertices()

        # 4) form complete subgraph using nodes in odds
        if self.debug:
            print("\nPrinting mst of completely connected graph")
            for edge in mst.edges:
                print(edge, mst.edges[edge])
            
            print("\nOdd vertices:")
            print(odds)

        # need some indexing to convert back and form from reduced form to full
        odds = list(odds)
        mapper = {ind : val for ind, val in enumerate(odds)}
        
        odds_subgraph = Graph(len(mapper))
        for i in range(len(odds)):
            for j in range(i+1, len(odds)):
                odds_subgraph.addUndirectedEdge(i, j, 
                    distance(self.points[mapper[i]], self.points[mapper[j]])) 

        # 5) contruct minimum-weight perfect matching of this subgraph 
        M = odds_subgraph.minCostPerfectMatching()

        if self.debug:
            print("\nMapping from full to subgraph:")
            print(mapper)

            print("\nPrinting perfect matching:")
            for edge in M.edges:
                print(edge, M.edges[edge])

        # 6) Unite matching and spanning trees (mst U M)
        united_multigraph = MultiGraph(k, mst)
        for node1 in mapper:
            for node2 in M.edges[node1]:
                united_multigraph.addUndirectedEdge(mapper[node1], 
                        mapper[node2], M.edges[node1][node2])
        
        if self.debug:
            print("\nPrinting united graph of MST and perfect matching")
            for edge in mst.edges:
                print(edge, united_multigraph.edges[edge])
 
        # 7) Calculate the Euler tour    
        Etour = united_multigraph.EulerTour()

        # 8) take out duplicates, shortcut
        return [self.points[ind] for ind in shortcutEulerTour(Etour)]





