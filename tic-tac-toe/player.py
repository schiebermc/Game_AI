#!/bin/python
# Tic-Tac-Toe Player, by Matthew Schieber
# Incldues an opening book and minimax decision making
# alpha-beta is uneccessary, we can always search to endgame.

import random

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
        
        # otherwise employ minimax algorithm
        else:
            if(player == 'X'):
                not_player = 'O'
            else:
                not_player = 'X'
            move, val = self.nextMove_recurse(board, player, not_player, True)
        
        return move
        
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
        
        return best_move, best_val

    def eval_fn(self, playing_board, player, not_player):    
        board = playing_board.board
        n = 3
        # check rows:
        for i in range(n):
            if(board[i][0] == player and board[i][1] == player and board[i][2] == player):
                return 10
            elif(board[i][0] == not_player and board[i][1] == not_player and board[i][2] == not_player):
                return -10
            
        # check cols
        for i in range(n):
            if(board[0][i] == player and board[1][i] == player and board[2][i] == player):
                return 10
            elif(board[0][i] == not_player and board[1][i] == not_player and board[2][i] == not_player):
                return -10
            
        # check diags
        winner = True
        for i in range(n):
            if(board[i][i] != player):
                winner = False
        if(winner):
            return 10
        
        winner = False
        for i in range(n):
            if(board[i][i] != not_player):
                winner = True
        if(not winner):
            return -10
        
        winner = True
        for i in range(n):
            if(board[n - 1 - i][n - 1 - i] != player):
                winner = False
        if(winner):
            return 10
        
        winner = False
        for i in range(n):
            if(board[n - 1 - i][n - 1 - i] != not_player):
                winner = True
        if(not winner):
            return -10
        
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
    
    
#If player is X, I'm the first player.
#If player is O, I'm the second player.
player = raw_input()

#Read the board now. The board is a 3x3 array filled with X, O or _.
board = []
for i in xrange(0, 3):
    board.append(raw_input())

playing_board = Board(board)
game_player = Game_Player(player)
move = game_player.nextMove(playing_board)
print move[0], move[1]

