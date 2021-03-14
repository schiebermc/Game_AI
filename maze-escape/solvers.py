import abc
import pygame
from constants import *
from copy import deepcopy
from collections import deque
from heapq import heappush, heappop
    
class BaseMazeSolver(abc.ABC):
    
    MOVE_DIRS = { 
                  "RIGHT" : (0, 1),
                  "LEFT"  : (0, -1),
                  "DOWN"  : (1, 0),
                  "UP"    : (-1, 0)
                }

    def __init__(self, maze, end_val):
        self.n = maze.n
        self.m = maze.m
        self.maze = deepcopy(maze.maze)
        self.pos = maze.current_pos
        self.end_val = end_val

    def getLegalMoves(self, i, j):
        moves = []
        for move, val in self.MOVE_DIRS.items():
            x, y = val
            i2, j2 = i + x, j + y
            if i2 < 0 or j2 < 0 or i2 >= self.n or j2 >= self.m or self.maze[i2][j2] == 1:
                continue
            moves.append(((i2, j2), move))
        return moves

    @abc.abstractmethod
    def solve(self):
        pass


class DFSSolver(BaseMazeSolver):
        
    def __init__(self, maze, end_val):
        BaseMazeSolver.__init__(self, maze, end_val)

    def solve(self):
        print("Automatically solving...")
        
        def dfs(pos, visited=None):

            if visited == None:
                visited = set([])

            if self.maze[pos[0]][pos[1]] == self.end_val:
                return True, []

            for vals, move in self.getLegalMoves(pos[0], pos[1]):     
                if vals in visited:
                    continue
                    
                visited.add(vals)
                solved, path = dfs(vals, visited)
                if solved:
                    return True, [move] + path
                visited.remove(vals)

            return False, []

        solved, path = dfs(self.pos)
        
        print(path)
        return path


class BFSSolver(BaseMazeSolver):
        
    def __init__(self, maze, end_val):
        BaseMazeSolver.__init__(self, maze, end_val)

    def solve(self):
        print("Automatically solving...")
        
        visited = set([])
        f = deque([(self.pos, [])])
        while(len(f) > 0):
            
            node, path = f.pop()

            if node in visited:
                continue

            visited.add(node)

            i, j = node
            if self.maze[i][j] == self.end_val:
                return path
            
            for vals, move in self.getLegalMoves(i, j):     
                if vals in visited:
                    continue
                           
                f.appendleft((vals, path + [move]))
        

        return []
























