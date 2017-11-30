#!/bin/python
# Bidding Tic-Tac-Toe Player, by Matthew Schieber
# Incldues an opening book and minimax decision making
# alpha-beta is uneccessary, we can always search to endgame.
# vanilla version with respect to the bidding strategy
# scores 26.4 on hackerrank. strategy involves bidding maximum if a killer
# move is available.  if a killer move is unavailable, max bid
# if there is chips.
# template if for use at hackerrank.com/challenges/biddingtictactoe/

class Game_Player:
    
    def __init__(self, player):
        self.player = player

    def nextMove(self, board):
        # count the number of spaces left
        moves = board.get_legal_moves()
        count = len(moves)
                
        # opening book
        if(count >= 8):
            move = self.openingBook(board, count)
            val = 1
        
        # otherwise employ minimax algorithm
        else:
            if(player == 'X'):
                move, val = self.nextMove_recurse(board, player, 'O', True)
            else:
                move, val = self.nextMove_recurse(board, player, 'X', True)
        return move, val
        
    def openingBook(self, playing_board, count):
        if(count == 9):
            move = (1, 1)
        elif(count == 8):
            if(playing_board.board[1][1] == '_'):
                move = (1, 1)
            else:
                move = (0, 0)
        return move
    
    def nextMove_recurse(self, playing_board, player, not_player, maximizing_player):
        # Minimax algorithm for picking optimal move
        # this game is so small, we don't even need alpha-beta
        moves = playing_board.get_legal_moves()   
       
        # check if game is over
        score = self.eval_fn(playing_board, player, not_player)
        if(score != 0 or not len(moves)):
            return None, score
    
        # recurse
        best_move = False
        best_val = float('-inf') if maximizing_player else float('inf') 
        for move in moves: 
     
            # forecast move, get minimax value from child
            if(maximizing_player):
                child_board = playing_board.forecast_move(move, player)
            else:
                child_board = playing_board.forecast_move(move, not_player)
            
            thing, val = self.nextMove_recurse(child_board, player, not_player, not maximizing_player)
            
            # apply minimax rules
            if(maximizing_player):
                if val > best_val:
                    best_move, best_val = move, val
            else:
                if val < best_val:
                    best_move, best_val = move, val
        
        if(best_move):
            return best_move, best_val
        else:
            return moves[0], best_val
        
    def eval_fn(self, playing_board, player, not_player):    
        end = playing_board.end_game()
        if(end):
            if(end == player):
                return float('inf')
            else:
                return float('-inf')
        else:
            return 0

    
class Board:
    
    def __init__(self, board):
        self.board = board
        self.n = 3
    
    def get_legal_moves(self):
        """
        Takes current game state and returns all
        available moves.
        
        return:
        moves = list(tuples(int, int))
        """
        moves = []
        for i in range(self.n):
            for j in range(self.n):
                if (self.board[i][j] == '_'):
                    moves.append((i, j))
        return moves
         
    def forecast_move(self, pos, player):
        """
        Takes current game state and creates a forecasted
        board accordign to player and pos. 
        
        params:
        pos = tuple(int, int)
        player = string

        return:
        new_board = class Board
        """
        new_board = []
        for i in range(self.n):
            new_board.append([])
            for j in range(self.n):
                if(i == pos[0] and j == pos[1]):
                    new_board[i].append(player)
                else:
                    new_board[i].append(self.board[i][j])
        new_playing_board = Board(new_board)
        return new_playing_board
    
    def end_game(self):
        # check rows/cols:
        board = self.board
        for i in range(self.n):
            if(board[i][0] != '_' and board[i][0] == board[i][1] and board[i][1] == board[i][2]):
                return board[i][0]
            elif(board[0][i] != '_' and board[0][i] == board[1][i] and board[1][i] == board[2][i]):
                return board[0][i]
        # check diags
        if(board[0][0] != '_' and board[0][0] == board[1][1] and board[1][1] == board[2][2]):
            return board[1][1]
        elif(board[0][2] != '_' and board[0][2] == board[1][1] and board[1][1] == board[2][0]):
            return board[1][1]
        else:
            return False
   
def next_move(player, first_player_bids, second_player_bids, board, move):
    playing_board = Board(board)
    game_player = Game_Player(player)
    best_move, val = game_player.nextMove(playing_board)

    first_player = True if player == 'X' else False        
    leftover = 4
    for i in range(len(first_player_bids)):        
        if(first_player):
            if(first_player_bids[i] >= second_player_bids[i]):
                leftover -= first_player_bids[i]
            else:
                leftover += second_player_bids[i]
        else:
            if(second_player_bids[i] >= first_player_bids[i]):
                leftover -= second_player_bids[i]
            else:
                leftover += first_player_bids[i]    
    
    if(move == "BID"):
        if(val >=1):
            print(leftover) 
        else:
            if(leftover):
                print(leftover)
            else:
                print(0)
    else:
        print best_move[0], best_move[1]
   
#gets the id of the player
player = raw_input()

move = raw_input()         #current position of the scotch

first_player_bids = [int(i) for i in raw_input().split()]
second_player_bids = [int(i) for i in raw_input().split()]
board = []

for i in xrange(0, 3):
    board.append(raw_input())

next_move(player, first_player_bids, second_player_bids, board, move)
