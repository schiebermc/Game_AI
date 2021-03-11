
import abc
from copy import deepcopy
from heapq import heappush, heappop

class AStarBaseHeuristicComputer():
    
    def __init__(self):
        pass

    @abc.abstractmethod
    def compute_heuristic(self, tiles):
        pass


class AStarManhattanHeuristic():

    def __init__(self):
        pass

    def compute_heuristic(self, tiles):
        # returns sum of manhattan distances to the correct locations
        d = {}
        n = len(tiles)
        for i in range(n):
            for j in range(n):
                val = tiles[i][j].val
                d[val] = (i, j)

        summ = 0
        for val in range(n * n):
            row_diff = abs(val // n - d[val][0]) #* (val // n)
            col_diff = abs(val %  n - d[val][1]) #* (val % n)
            summ += row_diff + col_diff
        return summ


class AStarManhattanHeuristicOuterEmphasis():

    def __init__(self):
        pass

    def compute_heuristic(self, tiles):
        # returns sum of manhattan distances to the correct locations
        d = {}
        n = len(tiles)
        for i in range(n):
            for j in range(n):
                val = tiles[i][j].val
                d[val] = (i, j)

        summ = 0
        for val in range(n * n):
            row_diff = abs(val // n - d[val][0]) * (val // n)
            col_diff = abs(val %  n - d[val][1]) * (val % n)
            summ += row_diff + col_diff
        return summ


class UnidirectionalSolver:
    
    def __init__(self, board, heuristic=AStarManhattanHeuristic):
        self.board = board
        self.heuristic_computer = heuristic()
        print("Using solver: {}".format(self.name()))
 
    def get_tile_tup(self, board):
        tup = []
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                tup.append(board.tiles[row][col].val)
        tup = tuple(tup)
        return tup    

    
    def get_solution(self):
        
        visited = set([])
        f = [((self.heuristic_computer.compute_heuristic(self.board.tiles),\
             [], deepcopy(self.board)))]
        
        while(len(f) > 0):

            h, path, board = heappop(f)

            if h == 0:
                return len(visited), path

            tup = self.get_tile_tup(board)
            if tup in visited:
                continue
            visited.add(tup)
 
            for move in ["RIGHT", "LEFT", "UP", "DOWN"]:
                new_board = deepcopy(board)
                if new_board.forecast_move(move) and \
                                not self.get_tile_tup(new_board) in visited:
                    new_h = self.heuristic_computer.compute_heuristic(\
                                                new_board.tiles)
                    heappush(f, (new_h, path + [move], new_board))

    
    def name(self):
        return type(self).__name__ + '_' \
            + type(self.heuristic_computer).__name__
     






