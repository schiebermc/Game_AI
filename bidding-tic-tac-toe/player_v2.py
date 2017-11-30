#!/bin/python
# Bidding Tic-Tac-Toe Player, by Matthew Schieber
# Total revamp over vanilly player. 
# Bidding strategy was wholey changed after noticing
# logic for whinning strategies.  Essentially, if player
# possesses the amount of chips to end the game, bid out.
# If not, check if player could lose the game in one turn,
# if so, bid out.  Otherwise bid the minimum amount.  
# The objective is to accrue enough chips to end the game.
# Also, the game player is separated into two different players,
# so minimax is never actually used in this game.  The objective
# is to see how fast either player can win the game, and to
# bid and take actions accorodingly.
# This player attains the 'solved' status on Hackerrank,
# achieving 54.76 points and landing at #22 out of 283.
# One final mode of improvement would be to weight moves
# more heavily if they result in wins in moroe than one way.
# Template for use on hackerrank


class Game_Player:
    
    def __init__(self, player):
        self.player = player

    def nextMove(self, board):
        # see how fast I can finish the game
        if(self.player == 'X'):
            move, val, depth = self.nextMove_recurse(board, self.player, 'O', 0)
        else:
            move, val, depth = self.nextMove_recurse(board, self.player, 'X', 0)
        return move, val, depth
        
    
    def nextMove_recurse(self, playing_board, player, not_player, depth):
        # There is no minimix here. This checks how fast a game can be won!

        # get moves and use evaulation function
        moves = playing_board.get_legal_moves()   
        score = self.eval_fn(playing_board, player, not_player)

        # returns if I won the game
        if(score != 0):
            return None, score, depth
        
        # returns when there are no moves left
        elif(len(moves) == 0):
            return None, score, depth
    
        # setup ~
        best_move = False
        best_depth = float('inf')
        best_val = float('-inf')
        
        # recurse
        for move in moves: 
            
            # forecast move, get minimax value from child
            child_board = playing_board.forecast_move(move, player)
            
            # big difference is here, where I do not switch the polarity of maximizing_player!
            thing, val, end_depth = self.nextMove_recurse(child_board, player, not_player, depth + 1)
            
            # is this a faster when then other moves (subgraphs)?
            if (val >= best_val and end_depth < best_depth):
                best_move, best_val, best_depth = move, val, end_depth  
        
        return best_move, best_val, best_depth

        
    def eval_fn(self, playing_board, player, not_player):    
        end = playing_board.end_game()
        if(end):
            if(end == player):
                return 1
            else:
                return -1
        else:
            return 0
    
    def bid(self, win_depth1, win_depth2, chips1, chips2, tiebreaker):
        # priorities ~
        # 1. win if possible
        # 2. do not lose
        # 3. bid low if the situation is not dire
        # 4. flail
        
        if(tiebreaker): 
            summ = 0
            tmp_chips = chips2
            for i in range(win_depth1):
                if(not (i % 2)):
                    summ += tmp_chips
                    tmp_chips += tmp_chips
                else:
                    summ += (tmp_chips + 1)
                    tmp_chips += (tmp_chips + 1)                    
            if(chips1 >= summ):
                if(chips2):
                    possible = chips2
                else:
                    possible = 1
            else:
                possible = False
        else:
            summ = 0
            tmp_chips = chips2
            for i in range(win_depth1):
                if(not (i % 2)):
                    summ += (tmp_chips + 1)
                    tmp_chips += (tmp_chips + 1)
                else:
                    summ += tmp_chips
                    tmp_chips += tmp_chips
            if(chips1 >= summ):
                possible = chips2 + 1
            else:
                possible = False
        
        if(possible):            
            return possible, False
        elif(win_depth2 == 1):
            if(tiebreaker):
                if(chips1 >= chips2):
                    return chips2, True
                else:
                    return chips1, True
            else:
                if(chips1 >= chips2 + 1):
                    return chips2 + 1, True
                else:
                    return chips1, True
        else:
            if(chips1):
                return 1, False
            else:
                return 0, False
    def get_tiebreaker_sieve(self, first_player_bids, second_player_bids):
        sieve = []
        polar = 1
        for i in range(len(first_player_bids)):
            sieve.append(polar)
            if(first_player_bids[i] == second_player_bids[i]):
                polar = (1 - polar)
        sieve.append(polar)
        return sieve

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
        # if the game is won, returns the winning player, otherwise returns false
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
    
    # set up playing board, game players
    playing_board = Board(board)   
    game_player1 = Game_Player('X')
    game_player2 = Game_Player('O')

    # see how fast either player can win    
    best_move1, val1, best_depth1 = game_player1.nextMove(playing_board)
    best_move2, val2, best_depth2 = game_player2.nextMove(playing_board)    
    
    # who gets the draw advantage..?
    tiebreaker_sieve = game_player1.get_tiebreaker_sieve(first_player_bids, second_player_bids)
    draw_advantage = 'X' if tiebreaker_sieve[-1] else 'O'
    tiebreaker = True if player == draw_advantage else False

    # how many chips do both players have left
    X_chips = 4
    O_chips = 4
    for i in range(len(first_player_bids)):
        if(tiebreaker_sieve[i]):
            if(first_player_bids[i] >= second_player_bids[i]):
                X_chips -= first_player_bids[i]
            else:
                X_chips += second_player_bids[i]
            if(second_player_bids[i] > first_player_bids[i]):
                O_chips -= second_player_bids[i]
            else:
                O_chips += first_player_bids[i]        
        else:
            if(first_player_bids[i] > second_player_bids[i]):
                X_chips -= first_player_bids[i]
            else:
                X_chips += second_player_bids[i]
            if(second_player_bids[i] >= first_player_bids[i]):
                O_chips -= second_player_bids[i]
            else:
                O_chips += first_player_bids[i]        

    # checks with unit tests
    #print(tiebreaker_sieve)
    #print(X_chips)
    #print(O_chips)
    #print(best_depth1)
    #print(best_depth2)
    #print(best_move1)
    #print(best_move2)
    
    if(player == 'X'):
        bid, dire = game_player1.bid(best_depth1, best_depth2, X_chips, O_chips, tiebreaker)
    else:
        bid, dire = game_player1.bid(best_depth2, best_depth1, O_chips, X_chips, tiebreaker)

    # make the move! 
    if(move == "BID"):
        print(bid)
    else:
        if(board[1][1] == '_' and (not dire)):
            print 1, 1
        elif(player == 'X'):
            if(dire):
                print best_move2[0], best_move2[1]
            else:
                print best_move1[0], best_move1[1]
        else:
            if(dire):
                print best_move1[0], best_move1[1]
            else:
                print best_move2[0], best_move2[1]

            
#gets the id of the player
player = raw_input()

move = raw_input()         #current position of the scotch

first_player_bids = [int(i) for i in raw_input().split()]
second_player_bids = [int(i) for i in raw_input().split()]
board = []

for i in xrange(0, 3):
    board.append(raw_input())

#next_move('X', [1, 1, 1], [1, 1, 2], [['X','O','_'],['_','O','_'],['_','_','_']], "PLAY")
next_move(player, first_player_bids, second_player_bids, board, move)

