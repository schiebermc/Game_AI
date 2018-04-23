#!/bin/python
# Tron! :D
from copy import deepcopy

N = 15
M = 15
player1 = 'r'
player2 = 'g'


def get_pos(positions):
    pos1 = [positions[0], positions[1]]
    pos2 = [positions[2], positions[3]]
    return pos1, pos2 


class Evaluator:

    # class to handle move evaluations and scoring
    
    def __init__(self):
        pass
    

    def score(self, game, maximizing_player_turn):
        # evaluation function, this is everything!

        return 0


class TronBoard:

    def __init__(self, board, N, M, player1, player2, pos1, pos2, current_player):

        self.N = N
        self.M = M
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.pos1 = pos1
        self.pos2 = pos2
        self.current_player = current_player
        
        
    def get_legal_moves(self):
        # returns a list of legal moves (tuples: row, col)    
        
        moves = []
        row, col = self.pos1 if self.current_player == self.player1 else self.pos2
        for row_bump in [-1, 0, 1]:
            for col_bump in [-1, 0, 1]:
                if(row_bump != 0 and col_bump != 0):
                    continue
                new_row = row + row_bump 
                new_col = col + col_bump 
                # could do try-accept here, but actually checking is much faster in recurse
                if(new_row >= 0 and new_row < self.N and new_col >= 0 and new_col < self.M):
                    if(self.board[new_row][new_col] == '-'):
                        moves.append((new_row, new_col))
        return moves    

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

    def __init__(self, search_depth=4, eval_fn=Evaluator()):

        self.eval_fn = eval_fn
        self.search_depth = search_depth

    def move(self, game):
 
        # iterative deepening best goes here
        # need timing mechanics before adding ID      
 
        # quiesence utilities
        previous_move = None
        quiesence_count = 0

        moves = game.get_legal_moves()
        
        while(quiesence_count < 5): 
            
            # get best move from alpha-beta pruning search
            best_move, utility = self.alphabeta(game)
    
            #print("move: ", best_move, "utility ", utility)

            # test for quiesence
            if(previous_move == best_move):
                quiesence_count += 1
            else:
                quiesence_count = 1
                previous_move = best_move
           
        return best_move


    def alphabeta(self, game, depth=0, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        
        # return the score of this move if it is end-game or as far in as we can go.
        if(not len(game.get_legal_moves()) or depth >= self.search_depth):
            return None, self.eval_fn.score(game, not maximizing_player)
        
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

    
def move(current_player, player1, player2, pos1, pos2, board):
    
    row, col = pos1 if current_player == player1 else pos2
   
    player = Player()
    move = player.move(TronBoard(board, N, M, player1, player2, pos1, pos2, current_player))
    return map_move_to_string(board, row, col, move[0], move[1])

def map_move_to_string(board, cr, cc, nr, nc):
    
    if(cr == nr):
        if(cc == nc - 1):
            return "LEFT"
        elif(cc == nc + 1):
            return "RIGHT"
        else:
            raise Exception("Illegal move")
    elif(cc == nc):
        if(cr == nr - 1):
            return "UP"
        elif(cr == nr + 1):
            return "DOWN"
        else:
            raise Exception("Illegal move")
    else:        
        raise Exception("Illegal move")
    
    
if __name__ == "__main__":
  
    current_player = input().strip().split()[0]
    pos1, pos2 = get_pos([int(val) for val in input().strip().split()])
    board = [list(input()) for echo in range(N)]
    move = move(current_player, player1, player2, pos1, pos2, board)
    print(move)
        
