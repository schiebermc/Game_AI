#!/usr/bin/env python

class Evaluator:

    def __init__(self):

        self.good_partition = False
        self.current_game = None

    
    def partition_check(self, game):
        
        self.current_game = game.__board_state__
        move = game.__last_queen_move__ 

        return self.partition_check_recurse(move[0], move[1], True)
    
    
    def partition_check_recurse(self, i, j, start):

        # implements 8-way flood fill algorithm
        tots = 0
        if(i >= 0 and j >= 0 and i <= 6 and j <= 6):
            
            val = self.current_game[i][j]
            if(start or (val != -1 and val != 'Q')):
                
                # mark it
                if(val == 0):
                    tots += 1
                self.current_game[i][j] = -1
        
                # recurse
                tots += self.partition_check_recurse(i + 1, j, False)     # down 
                tots += self.partition_check_recurse(i - 1, j, False)     # up
                tots += self.partition_check_recurse(i, j + 1, False)     # right
                tots += self.partition_check_recurse(i, j - 1, False)     # left
                tots += self.partition_check_recurse(i + 1, j + 1, False) # down, right
                tots += self.partition_check_recurse(i - 1, j + 1, False) # up, right
                tots += self.partition_check_recurse(i - 1, j - 1, False) # up, left
                tots += self.partition_check_recurse(i + 1, j - 1, False) # down, left

        return tots
    

    def score(self, game, maximizing_player_turn):

        # how many moves are around me?
        tots = self.partition_check(game)
        if(maximizing_player_turn):
            if(not tots):
                return float("inf")
            elif(tots % 2):
                return tots - 50
            else:
                return 50 - tots
        else:
            if(not tots):
                return float("-inf")
            elif(tots % 2):
                return 50 - tots
            else:
                return tots - 50

class Player:

    def __init__(self, search_depth=2, eval_fn=Evaluator()):

        self.eval_fn = eval_fn
        self.search_depth = search_depth

    def move(self, game, legal_moves, time_left):
        """Called to determine one move by your agent
        
        Args:
            game (Board): The board and game state.
            legal_moves (dict): Dictionary of legal moves and their outcomes
            time_left (function): Used to determine time left before timeout
            
        Returns:
            (tuple): best_move
        """
        from random import randint
 
        moves = game.get_legal_moves()
 
        # this is pretty dominant
        if(game.move_count == 0):
            best_move = (0, 0)
    
        # otherwise do the usual
        else:
        
            # iterative deepening best goes here
            total_time = time_left()
            self.iterative_depth = self.search_depth
       
            # quiesence utilities
            previous_move = None
            quiesence_count = 0
            decent_move = None 
            previous_utility = None
            best_prev = None

            # print game.get_legal_moves()
            
            while(quiesence_count < 15): 
                
                # get best move from minmax
                best_move, utility = self.alphabeta(game, time_left)

                # get out if time is out
                if(best_move == None and utility == None):
                    utility = prev_utility
                    if(previous_move == None and len(game.get_legal_moves())):
                        best_move = game.get_legal_moves()[0]
                        break
                    else:
                        best_move = previous_move
                        break            

                # save a decent move for later
                prev_utility = utility
                if(utility > 0):
                    if(best_prev == None or utility > best_prev):
                        best_prev = utility
                        decent_move = best_move
                
    
                print self.iterative_depth, "move: ", best_move, "utility ", utility

                # catch error
                if(best_move == None and len(game.get_legal_moves())):
                    best_move = game.get_legal_moves()[0]

                # test for quiesence
                if(previous_move == best_move):
                    quiesence_count += 1
                else:
                    quiesence_count = 0
                    previous_move = best_move
               
                # go deeper
                self.iterative_depth += 1
            
            if(utility < -48):
                if(decent_move != None):
                    best_move = decent_move
                elif(len(game.get_legal_moves())):
                    best_move = game.get_legal_moves()[randint(0, len(game.get_legal_moves()) -1)]
        

        print "Time: ", time_left(), "move: ", best_move
        print "````````````````````````"
        # change minimax to alphabeta after completing alphabeta part of assignment
        
        return best_move

    def minimax(self, game, time_left, depth=0, maximizing_player=True):
        
        # update
        depth += 1
        
        # check
        if(not len(game.get_legal_moves()) or depth > self.iterative_depth):
            return None, self.eval_fn.score(game, not maximizing_player)
        
        # recurse
        best_val = None
        for move in game.get_legal_moves(): 
        
            # forecast move, get minimax value from child
            child_game = game.forecast_move(move)
            thing, val = self.minimax(child_game, time_left, depth, not maximizing_player)
            
            # exit if time is running out
            if(time_left() < 5):
                return None, None     
            if(thing == None and val == None):
                return None, None
            
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

    def alphabeta(self, game, time_left, depth=0, alpha=float("-inf"), beta=float("inf"),
                  maximizing_player=True):
        
        # update
        depth += 1
        
        # check
        if(not len(game.get_legal_moves()) or depth >= self.iterative_depth):
            return None, self.eval_fn.score(game, not maximizing_player)
        
        # recurse
        best_val = None
        for move in game.get_legal_moves(): 
        
            # forecast move, get minimax value from child
            child_game = game.forecast_move(move)
            thing, val = self.alphabeta(child_game, time_left, depth, alpha, beta, not maximizing_player)
       
            # exit if time is running out
            if(time_left() < 100):
                return None, None     
            if(thing == None and val == None):
                return None, None
           
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

