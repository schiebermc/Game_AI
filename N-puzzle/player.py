#!/bin/python
#!/bin/python
# N-puzzle solver, by Matthew Schieber
# An N-puzzle solver that employs A* search to reach the goal state
# The heapq class was used as a priority queue for my search algo.
# Various heuristic functions were tested, but I ultimately used
# the sum of Manhattan distances. 
# This is a unidirectinal search, I wonder how bidirectional
# searches would fare?
# I would love to get this visualized on arbitrary NxN boards
# template if for use at hackerrank.com/challenges/n-puzzle

import heapq
class PriorityQueue(object):

    def __init__(self):
        self.queue = []

    def pop(self):
        return heapq.heappop(self.queue)

    def replace_if_cheaper(self, candidate):

        replace = False
        not_in = True
        state = candidate[2]

        # is this the cheapest option?
        for i in self.queue:
            if(i[2] == state):
                not_in = False
                if(i[1] > candidate[1]):
                    replace = True
                    break

        # replace if it is
        # no simple way to replace an item, so I reconstruct it :(
        if(not_in):
            heapq.heappush(self.queue, candidate)
        elif(replace):
            data = []
            for i in self.queue:
                if(i[2] != state):
                    heapq.heappush(data, i)
            self.queue = data
            heapq.heappush(self.queue, candidate)


    def append(self, node):
        heapq.heappush(self.queue, node)

class BoardHelper:
    def __init__(self, k):
        self.k = k
    
    def GetMoves(self, state):
        # determine context (all moves with respect to 0)
        k = self.k
        for i in range(k):
            for j in range(k):
                if(state[i][j] == 0):
                    loc = (i, j)
                    break
        
        # determine moves available
        moves = []
        if(loc[0] == 0 and loc[1] == 0): # upper left corner
            moves.append("RIGHT")
            moves.append("DOWN")
        elif(loc[0] == 0 and loc[1] == k - 1): # upper right corner
            moves.append("LEFT")
            moves.append("DOWN")
        elif(loc[0] == k - 1 and loc[1] == 0): # lower left corner
            moves.append("RIGHT")
            moves.append("UP")
        elif(loc[0] == k - 1 and loc[1] == k - 1): # lower riight corner
            moves.append("LEFT")
            moves.append("UP")
        elif(loc[1] == 0):        # left column
            moves.append("RIGHT")
            moves.append("DOWN")
            moves.append("UP")
        elif(loc[0] == 0):        # top row
            moves.append("RIGHT")
            moves.append("LEFT")
            moves.append("DOWN")
        elif(loc[0] == k - 1):    # lower row
            moves.append("RIGHT")
            moves.append("LEFT")
            moves.append("UP")
        elif(loc[1] == k - 1):    # right column
            moves.append("LEFT")
            moves.append("UP")
            moves.append("DOWN")
        else:                     # center
            moves.append("RIGHT")
            moves.append("LEFT")
            moves.append("DOWN")
            moves.append("UP")
            
        return (loc, moves)
            
    def ForecastMove(self, state, move, loc):
        import copy
        new_board = copy.deepcopy(state)
        i = loc[0]
        j = loc[1]
        
        if(move == "RIGHT"):
            if(j == k - 1):
                raise Exception("incorrect moving right")
            tmp = new_board[i][j + 1]
            new_board[i][j + 1] = new_board[i][j]
            new_board[i][j] = tmp
        elif(move == "LEFT"):
            if(j == 0):
                raise Exception("incorrect moving left")
            tmp = new_board[i][j - 1]
            new_board[i][j - 1] = new_board[i][j]
            new_board[i][j] = tmp
        elif(move == "UP"):
            if(i == 0):
                raise Exception("incorrect moving up")
            tmp = new_board[i - 1][j]
            new_board[i - 1][j] = new_board[i][j]
            new_board[i][j] = tmp
        elif(move == "DOWN"):
            if(i == k - 1):
                raise Exception("incorrect moving down")
            tmp = new_board[i + 1][j]
            new_board[i + 1][j] = new_board[i][j]
            new_board[i][j] = tmp
            
        return new_board
    
    def PrintBoard(self, board):
        for i in range(self.k):
            print (board[i])
    
class Scorer:
    def __init__(self, k):
        self.k = k
        self.pos_map = {}
        count = 0
        for i in range(k):
            for j in range(k):
                self.pos_map[count] = (i, j)
                count += 1
        #del self.pos_map[k * k]
        #self.pos_map[0] = (k - 1, k - 1)
        
    def GetScore(self, board):
        # sum of Manhattan distances for each piece
        k = self.k
        score = 0
        for i in range(k):
            for j in range(k):
                val = board[i][j]
                wanted = self.pos_map[val]
                score += (abs(i - wanted[0]) + abs(j - wanted[1]))
        
        return score
          
    def GetScoreN(self, board, row_num, row=True):
        # sum of row/col manhattan distances, allowing to weight the rows/cols
        # this can be used to solve fringe problems!
        k = self.k
        score = 0
        if(row):
            count = 1 + row_num * k
            for i in range(k):
                val = count
                wanted = self.pos_map[val]
                for j in range(k):
                    for z in range(k):
                        if (board[j][z] == val):
                            loc = (j, z)
                score += (abs(loc[0] - wanted[0]) + abs(loc[1] - wanted[1]))
                count += 1
        else:     
            count = 1 + row_num
            for i in range(k):
                val = count
                wanted = self.pos_map[val]
                for j in range(k):
                    for z in range(k):
                        if (board[j][z] == val):
                            loc = (j, z)
                score += (abs(loc[0] - wanted[0]) + abs(loc[1] - wanted[1]))
                count += k
        
        return score
    
def SolveGame(board, k):
    
    # setup~ frontier: tuple(f, g, path)
    scorer = Scorer(k)
    frontier = PriorityQueue()
    board_helper = BoardHelper(k)
    
    # each state has a score, cost, and path associated with it
    frontier.append([scorer.GetScore(board), 0, board, []])
    explored = []
        
    while(True):

        # explore cheapest option
        node = frontier.pop()
        score = node[0]
        cost  = node[1]
        state = node[2]
        path = node[3]
        
        explored.append(state)
            #print (state)
            #print (cost)
        if(score == 0):
            return path
            break
        else:
            stuff = board_helper.GetMoves(state)
            loc = stuff[0]
            moves = stuff[1]
            for j in moves:
                new_state = board_helper.ForecastMove(state, j, loc)
                if(not (new_state in explored)):
                    new_path = path + [j]
                    h = scorer.GetScore(new_state)
                    #h = scorer.GetScoreN(new_state, row_num, row_round)
                    frontier.replace_if_cheaper([h, len(new_path), new_state, new_path])
    


if __name__ == "__main__": 
    
    k = [int(i) for i in input().strip().split()][0]     
    board = []
    for i in range(k):
        board.append([])
        for j in range(k):
            board[i].append([int(i) for i in input().strip().split()][0])
    
    # simple unit test
    #k = 3
    #board = [[0, 3, 8], [4, 1, 7], [2, 6, 5]]
    #board = [[0, 2, 8], [4, 6, 7], [3, 1, 5]]
    
    path = SolveGame(board, k)
    count = 0
    for i in path:
        count += 1
    print (count)
    for i in path:
        print (i)


