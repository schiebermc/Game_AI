
import abc
import pygame
from math import ceil
from constants import *
from random import randint

class Tile:

    def __init__(self, x, y, w, l, val):
        self.x = x
        self.y = y
        self.w = w
        self.l = l
        self.val = val    

    def getVal(self):
        return self.val

    def setVal(self, val):
        self.val = val

    def draw(self, window):
        if self.val == 0:
            color = WHITE
        elif self.val == 1:
            color = BLACK
        elif self.val == 2: # start
            color = GREY
        elif self.val == MAZE_END_VAL: # end
            color = RED
        elif self.val == 4:
            color = BLUE
        else:
            raise Exception()

        pygame.draw.rect(window, color, (self.x, self.y, self.w, self.l))


class DisjointSet:

    def __init__(self, n):
        self.n = n
        self.parent = [i for i in range(self.n)]
        self.size = [1] * self.n
    
    def find(self, n):
        p = self.parent[n]
        if p != n:
            self.parent[n] = self.find(p)
        return self.parent[n]
        
    def union(self, n1, n2):
        p1 = self.find(n1)
        p2 = self.find(n2)
        if p1 != p2:
            s1 = self.size[p1]
            s2 = self.size[p2]
            if s1 > s2:
                self.parent[p2] = p1
                self.size[p1] += self.size[p2]
            else:
                self.parent[p1] = p2
                self.size[p2] += self.size[p1]
        

class BaseMazeGenerator(abc.ABC):
    
    def __init__(self, n, m):
        self.n = n
        self.m = m

    def isCorner(self, i, j):
        return (i == 0 and j == 0) or (i == 0 and j == self.m - 1) or\
               (i == self.n - 1 and j == 0) or (i == self.n - 1 and j == self.m - 1)
 
    def randomPerimeter(self):
        i = j = 0
        while(self.isCorner(i, j)):
            i = 0 if randint(0, 1) else self.n - 1
            j = randint(0, self.m-1)
        return (i, j)    
   
    def sameSide(self, start, end):
        return start[0] == end[0] or start[1] == end[1]

    def getEndsDifferentSides(self):
        # pick a start and end for the maze
        start = self.randomPerimeter()
        end = self.randomPerimeter()
        while(self.sameSide(start, end)):
            end = self.randomPerimeter()
        return start, end
 
    def unionNeighbors(self, i, j, dj):
        for x in range(-1, 2):
            for y in range(-1, 2):
                if abs(x) + abs(y) != 1:
                    continue
                i2, j2 = i + x, j + y
                if i2 < 0 or j2 < 0 or i2 >= self.n or j2 >= self.m:
                    continue
                
                if self.maze[i2][j2] == 0:
                    dj.union(i * self.m + j, i2 * self.m + j2)

    def closeBorder(self):
        # close up the border
        for i in range(self.n):
            self.maze[i][0] = self.maze[i][self.m-1] = 1
        for j in range(self.m):
            self.maze[0][j] = self.maze[self.n-1][j] = 1
        
    def randomMaze(self):
        # randomly initialize maze
        self.maze = [[0] * self.m for row in range(self.n)]
        for i in range(self.n):
            for j in range(self.m):
                self.maze[i][j] = randint(0, 1)
       
        self.closeBorder() 
        return self.maze

    def emptyMaze(self):
        # randomly initialize maze
        self.maze = [[0] * self.m for row in range(self.n)]
        self.closeBorder() 
        
        return self.maze

    def initializeDJ(self):
        dj = DisjointSet(self.n * self.m)
        for i in range(self.n):
            for j in range(self.m):
                if self.maze[i][j] == 0:
                    self.unionNeighbors(i, j, dj)
                # the symmetry-based unions botched the maze gen 2 algo,
                # i'm not sure why? TODO
                #elif i < self.n - 1 and self.maze[i+1][j] == 0:
                #    dj.union(i * self.m + j, (i+1) * self.m + j)
                #elif j < self.m - 1 and self.maze[i][j+1] == 0:
                #    dj.union(i * self.m + j, i * self.m + j + 1)
        return dj 

    def numOpenComponents(self):
        # calculates the number of open space components. 
        # this can be really useful in maze generation, since we
        # generally do not want a disjoint set of open spaces that 
        # our agent cannot access..
        dj = self.initializeDJ()
        s = set([])
        for i in range(self.n):
            for j in range(self.m):
                if self.maze[i][j] == 0:
                    s.add(dj.find(i * self.m + j))
        return len(s)
    

    @abc.abstractmethod
    def generate(self):
        pass


class MazeGenerator1(BaseMazeGenerator):

    # algorithm: 
    # 1) randomize maze
    # 2) smash non-perimeter walls until start and end are in the 
    #    same disjoint set

    def __init__(self, n, m):
        BaseMazeGenerator.__init__(self, n, m)
        
    def generate(self):
    
        # start with a randomized maze
        self.randomMaze()        
        
        # pick a start and end for the maze
        start, end = self.getEndsDifferentSides()

        self.maze[start[0]][start[1]] = 0 
        self.maze[end[0]][end[1]]     = 0
        
        # create disjoint set to track maze openings
        dj = self.initializeDJ()

        lin_start = start[0] * self.m + start[1]
        lin_end   = end[0]  * self.m + end[1]
        while(dj.find(lin_start) != dj.find(lin_end)):
            
            # note: want to keep border of maze as closed, so do not
            # sample the perimeter
            i = randint(1, self.n-2)
            j = randint(1, self.m-2)

            self.maze[i][j] = 0
            self.unionNeighbors(i, j, dj)

        self.maze[start[0]][start[1]] = 2 
        self.maze[end[0]][end[1]]     = MAZE_END_VAL

        return start, end, self.maze


class MazeGenerator2(BaseMazeGenerator):

    # algorithm: 
    # 1) start with a completely empty maze
    # 2) add as many walls as possible, without creating another disjoint set
    
    def __init__(self, n, m):
        BaseMazeGenerator.__init__(self, n, m)
        
    def generate(self):
   
        print("I'm thinking of a good maze for you..")
 
        # start with a randomized maze
        self.emptyMaze()        
        
        # pick a start and end for the maze
        start, end = self.getEndsDifferentSides()
            
        self.maze[start[0]][start[1]] = 0 
        self.maze[end[0]][end[1]]     = 0
        
        lin_start = start[0] * self.m + start[1]
        lin_end   = end[0]  * self.m + end[1]
        
        # create disjoint set to track maze openings
        to_print = [0.0, 25.0, 50.0, 75.0, 100.0]
        printed = set([])
        for attempt in range(self.n * self.m):
            
            percent = (attempt+1) / (self.n * self.m) * 100
            for threshold in to_print:
                if percent >= threshold and not threshold in printed:
                    print("{}%".format(threshold))
                    printed.add(threshold)
            
            i = randint(1, self.n-2)
            j = randint(1, self.m-2)
            if self.maze[i][j] == 1:
                continue
            else:
                self.maze[i][j] = 1
                num_components = self.numOpenComponents()
                if num_components > 1:
                    # revert this wall, we don't want it
                    self.maze[i][j] = 0

        self.maze[start[0]][start[1]] = 2 
        self.maze[end[0]][end[1]]     = MAZE_END_VAL
        
        print("Done! Good luck!\n")

        return start, end, self.maze


class Maze:
        
    MOVE_DIRS = { 
                  "RIGHT" : (0, 1),
                  "LEFT"  : (0, -1),
                  "DOWN"  : (1, 0),
                  "UP"    : (-1, 0)
                }

    def __init__(self, n, m, w, h):
        self.n = n  
        self.m = m
        self.w = w
        self.h = h
        self.tile_w = self.w / self.m
        self.tile_h = self.h / self.n
    
        maze_generator = MazeGenerator2(n, m)
        self.start, self.end, self.maze = maze_generator.generate()

        self.current_pos = self.start

        self.tiles = []
        for i in range(self.n):
            self.tiles.append([])
            for j in range(self.m):
                self.tiles[i].append(Tile(j * self.tile_w, i * self.tile_h, 
                                    self.tile_w, self.tile_h, self.maze[i][j]))

        self.board_prints = True
        
        self.explored = set([self.current_pos])


    def game_over(self):
        val = self.current_pos == self.end                
        return val

    def get(self):
        return self.maze

    def forecast_move(self, move):
        if self.board_prints:
            print(move)
 
        if not move in self.MOVE_DIRS:
            raise Exception ("Illegal move name passed to forecast_move: {}".format(move))
       
        # compute new locations
        x, y = self.MOVE_DIRS[move]
        row, col = self.current_pos
        row2, col2 = row + x, col + y
       
        if row2 < 0 or col2 < 0 or row2 >= self.n or col2 >= self.m or\
            self.tiles[row2][col2].val == 1:
            
            if self.board_prints:
                print("Impossible move passed") 
            return False
        else:
            self.tiles[row][col].val = 2
            self.tiles[row2][col2].val = 4
            self.current_pos = (row2, col2)
            self.explored.add((row2, col2))
            return True
        
    
    def draw(self,  window):
        window.fill(WHITE)

        for i in range(self.n):
            for j in range(self.m):
                self.tiles[i][j].draw(window) 



 
