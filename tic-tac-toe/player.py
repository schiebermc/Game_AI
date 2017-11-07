#!/bin/python
import random

# Complete the function below to print 2 integers separated by a single space which will be your next move 
def nextMove(player,board):
    
    n = 3
    count = 0
    for i in range(3):
        for j in range(3):
            if(board[i][j] == '_'):
                count += 1
                
    # opening book
    if(count == 9):
        move = (1, 1)
    elif(count == 9):
        if(board[1][1] != '_'):
            move = (1, 1)
        else:
            move = (0, 0)
    else:
        if(player == 'X'):
            not_player = 'O'
        else:
            not_player = 'X'
        move, val = nextMove_recurse(board, player, not_player, True)
    
    print ('%d %d' % (move[0], move[1]))

def nextMove_recurse(board, player, not_player, maximizing_player):

    # Minimax algorithm for picking optimal move
    # this game is so small, we don't even need alpha-beta
    moves = get_legal_moves(board)   
   
    # check if game is over
    score = eval_fn(board, player, not_player)
    if(score != 0 or not len(moves)):
        return None, score

    # recurse
    best_val = None
    for move in moves: 
 
        # forecast move, get minimax value from child
        if(maximizing_player):
            child_board = forecast_move(board, move, player)
        else:
            child_board = forecast_move(board, move, not_player)
        
        thing, val = nextMove_recurse(child_board, player, not_player, not maximizing_player)
        
        # apply minimax rules
        if(best_val == None):
            best_move, best_val = move, val
        elif(maximizing_player):
            if val > best_val:
                best_move, best_val = move, val
        else:
            if val < best_val:
                best_move, best_val = move, val
    
    return best_move, best_val

def get_legal_moves(board):
    n = 3
    moves = []
    for i in range(n):
        for j in range(n):
            if (board[i][j] == '_'):
                moves.append((i, j))
    return moves

def eval_fn(board, player, not_player):
    
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
     
def forecast_move(board, loc, player):
    import copy
    new_board = []
    n = 3
    for i in range(n):
        new_board.append([])
        for j in range(n):
            if(loc == (i, j)):
                new_board[i].append(player)
            else:
                new_board[i].append(board[i][j])
    return new_board
    
#If player is X, I'm the first player.
#If player is O, I'm the second player.
player = raw_input()

#Read the board now. The board is a 3x3 array filled with X, O or _.
board = []
for i in xrange(0, 3):
    board.append(raw_input())

nextMove(player,board); 


