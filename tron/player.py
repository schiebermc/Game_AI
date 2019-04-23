#!/bin/python
# Tron game player
# By Matthew Schieber

# game player here uses minimax decision making with alpha
# beta pruning. The evaluation function 


# imports
from copy import deepcopy

# size of Tron Board
N = 15
M = 15

# player icons
player1 = 'r'
player2 = 'g'


class Evaluator:

    # class to handle move evaluations and scoring
    
    def __init__(self):
        pass
    
    
    def score(self, game, maximizing_player):
        
        # check for partitions
        PC = PartitionChecker(deepcopy(game.get_board()), game.get_pos1(), game.get_pos2())
        PC.partition_check(1)
        PC.partition_check(2)
        partition1 = PC.get_partition(1)
        partition2 = PC.get_partition(2)
        partition = True if (not game.get_pos1() in partition2) and (not game.get_pos2() in partition1) else False
        l1 = len(partition1)        
        l2 = len(partition2)        

        # get move counts
        counts = game.get_move_counts()
        player = game.get_current_player_number()

        # decision making
        if(maximizing_player): 
            if(counts[0] == 0):
                return -1000
            elif(counts[1] == 0):
                return 1000
            else:
                if(player == 1):
                    return 1000 if l1 > l2 else -1000
                else:
                    return 1000 if l2 > l1 else -1000
        else:
            if(counts[1] == 0):
                return -1000
            elif(counts[0] == 0):
                return 1000
            else:
                if(player == 1):
                    return 1000 if l1 < l2 else -1000
                else:
                    return 1000 if l2 < l1 else -1000

class TronBoard:

    # class to handle board maintenence and game playing
    
    def __init__(self, board, N, M, player1, player2, pos1, pos2, current_player):

        self.N = N
        self.M = M
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.pos1 = pos1
        self.pos2 = pos2
        self.current_player = current_player
        
    def get_board(self):
        return self.board

    def get_pos1(self):
        return tuple(self.pos1)

    def get_pos2(self):
        return tuple(self.pos2)
        
    def get_legal_moves(self):
        # returns a list of legal moves (tuples: row, col)    
        moves = []
        row, col = self.pos1 if self.current_player == self.player1 else self.pos2
        for new_row, new_col in self.generate_moves(row, col):
            if(self.board[new_row][new_col] == '-'):
                moves.append((new_row, new_col))
        return moves    

    def get_move_counts(self):
        # returns the number of moves that player one and player two have
        # returns a tuple [moves current player has, moves next player has]
        counts = [0, 0]
        if(self.current_player == 'r'):
            counts[0] = self.get_moves_from_here(self.pos1[0], self.pos1[1])        
            counts[1] = self.get_moves_from_here(self.pos2[0], self.pos2[1])
        else:
            counts[1] = self.get_moves_from_here(self.pos1[0], self.pos1[1])        
            counts[0] = self.get_moves_from_here(self.pos2[0], self.pos2[1])
        return counts        
   
    def get_current_player_number(self):
        return 1 if self.current_player == 'r' else 2
 
    def get_moves_from_here(self, row, col):
        # returns moves from certain position
        count = 0
        for new_row, new_col in self.generate_moves(row, col):
            if(self.board[new_row][new_col] == '-'):
                count += 1
        return count 
     
    def generate_moves(self, row, col):        
        # generator for all legal moves, outputs row, col of legal move.
        for row_bump, col_bump in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            new_row = row + row_bump 
            new_col = col + col_bump 
            # could do try-accept here, but actually checking is much faster in recurse
            if(new_row >= 0 and new_row < self.N and new_col >= 0 and new_col < self.M):
                yield new_row, new_col

    def forecast_move(self, move):
        # returns a new class instance with forecasted move        

        # copy board, make move
        new_board = deepcopy(self.board)
        new_board[move[0]][move[1]] = self.current_player

        # return new TronBoard
        if(self.current_player == self.player1):
            return TronBoard(new_board, self.N, self.M, self.player1, self.player2, move, self.pos2,
                             self.player1 if self.player2 == self.current_player else self.player2)
        else:
            return TronBoard(new_board, self.N, self.M, self.player1, self.player2, self.pos1, move,
                             self.player1 if self.player2 == self.current_player else self.player2)


class Player:

    # game playing class
    # employes minimax tree-based decision making with alpha-beta pruning

    def __init__(self, search_depth=6, eval_fn=Evaluator()):

        self.eval_fn = eval_fn
        self.search_depth = search_depth

    def move(self, game):
 
        # iterative deepening best goes here
        # need timing mechanics before adding ID      

        # first check if we are in a good partition (reduces search space for ideal moves)
        PC = PartitionChecker(deepcopy(game.get_board()), game.get_pos1(), game.get_pos2())
        PC.partition_check(1)
        PC.partition_check(2)
        partition1 = PC.get_partition(1)
        partition2 = PC.get_partition(2)
        partition = True if (not game.get_pos1() in partition2) and (not game.get_pos2() in partition1) else False
        l1 = len(partition1)        
        l2 = len(partition2)        
        
        #print(partition)
        if(partition):
            best_move, utility = self.partition_move(game) 
        else:
            # get best move from alpha-beta pruning search
            best_move, utility = self.alphabeta(game)
    
        #print("move made: ", best_move, "utility ", utility)

        return best_move


    def partition_move(self, game):

        # here we are in a partition, we just need to last as long as possible.
        player = game.get_current_player_number()
        if(player == 1):
            pos = game.get_pos1()
        else:
            pos = game.get_pos2()

        moves = game.get_legal_moves()
        for row_bump, col_bump in [1, 0], [-1, 0], [-1, 0], [0, 1]: 
            move = (pos[0] + row_bump, pos[1] + col_bump)
            if(move in moves):
                return move, 10
        raise Exception("what happend?")
    
    def alphabeta(self, game, depth=0, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        
        # return the score of this move if it is end-game or as far in as we can go.
        if(not len(game.get_legal_moves()) or depth >= self.search_depth):
            return None, self.eval_fn.score(game, maximizing_player)

        # recurse
        best_val = None
        for move in game.get_legal_moves(): 
        
            # forecast move, get minimax value from child
            child_game = game.forecast_move(move)
            thing, val = self.alphabeta(child_game, depth+1, alpha, beta, not maximizing_player)
       
            # apply minimax rules
            if(best_val == None):
                best_move, best_val = move, val
            elif(maximizing_player):
                if val > best_val:
                    best_move, best_val = move, val 
            else:
                if val < best_val: 
                    best_move, best_val = move, val 

            # apply alpha beta rules
            if(maximizing_player):
                # highest maximizing value
                alpha = max(alpha, val)
            else:
                # lowest minimizing value
                beta = min(beta, val)
            if beta <= alpha:
                break
        
        return best_move, best_val

class PartitionChecker:

    def __init__(self, game, pos1, pos2):
        
        self.game1 = deepcopy(game)
        self.game2 = deepcopy(game)
        self.pos1 = pos1
        self.pos2 = pos2
        self.partition1 = set([])
        self.partition2 = set([])

    def get_partition(self, player):
        if(player == 1):
            return self.partition1
        elif(player == 2):
            return self.partition2
        else:
            raise Exception("get_partition: incorrect player specified!")

    def partition_check(self, player):
    
        # checks if the two players are within
        # different partiions of the tron board.
        # player is either 1 or 2
        
        if(player == 1):
            self.flood_fill(self.pos1[0], self.pos1[1], player)   
        elif(player == 2):
            self.flood_fill(self.pos2[0], self.pos2[1], player)   
        else:
            raise Exception("partition_check: incorrect player specified!")
        
        return 
        
    def flood_fill(self, i, j, player, start=True):
        
        # implements 4-way flood fill algorithm
        
        if(i >= 0 and j >= 0 and i < N and j < M):
           
            # hit other players 
            # to account for decision points
            if(player == 1):
                if((i, j) == self.pos2):
                    self.partition1.add((i, j))
                    return
            else: 
                if((i, j) == self.pos1):
                    self.partition2.add((i, j))
                    return
            
            val = self.game1[i][j] if player == 1 else self.game2[i][j]
            
            if(start or (val == '-')):
                
                # add it
                if(player == 1):
                    self.partition1.add((i, j)) 
                if(player == 2):
                    self.partition2.add((i, j))
                
                # mark it
                if(player == 1):
                    self.game1[i][j] = 'X'
                else:
                    self.game2[i][j] = 'X' 
        
                # recurse
                self.flood_fill(i + 1, j, player, False)     # down 
                self.flood_fill(i - 1, j, player, False)     # up
                self.flood_fill(i, j + 1, player, False)     # right
                self.flood_fill(i, j - 1, player, False)     # left
        
 
def move(current_player, player1, player2, pos1, pos2, board):
    
    # outer interface to player class.  creates a player class then calls move function. 
    player = Player()
    row, col = pos1 if current_player == player1 else pos2
    move = player.move(TronBoard(board, N, M, player1, player2, pos1, pos2, current_player))
    return map_move_to_string(board, row, col, move[0], move[1])


def map_move_to_string(board, cr, cc, nr, nc):
    
    # maps the given move in row, col format to a direction.    

    if(cr == nr):
        if(cc == nc - 1):
            return "RIGHT"
        elif(cc == nc + 1):
            return "LEFT"
        else:
            raise Exception("Illegal move")
    elif(cc == nc):
        if(cr == nr - 1):
            return "DOWN"
        elif(cr == nr + 1):
            return "UP"
        else:
            raise Exception("Illegal move")
    else:        
        raise Exception("Illegal move")
    
def get_pos(positions):
    pos1 = [positions[0], positions[1]]
    pos2 = [positions[2], positions[3]]
    return pos1, pos2 

    
if __name__ == "__main__":
  
    current_player = input().strip().split()[0]
    pos1, pos2 = get_pos([int(val) for val in input().strip().split()])
    board = [list(input()) for echo in range(N)]
    move = move(current_player, player1, player2, pos1, pos2, board)
    print(move)
       
