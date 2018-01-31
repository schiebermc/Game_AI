#!/usr/bin/env python
class OpenMoveEvalFn:

    def score(self, game, maximizing_player_turn=True):
        """Score the current game state
        
        Evaluation function that outputs a score equal to how many 
        moves are open for AI player on the board.
            
        Args
            param1 (Board): The board and game state.
            param2 (bool): True if maximizing player is active.

        Returns:
            float: The current state's score. Number of your agent's moves.
            
        """

        return len(game.get_legal_moves())


class CustomEvalFn2:

    def __init__(self):
        pass

    def score(self, game, maximizing_player_turn):
        """Score the current game state
        
        Custom evaluation function that acts however you think it should. This 
        is not required but highly encouraged if you want to build the best 
        AI possible.
        
        Args
            game (Board): The board and game state.
            maximizing_player_turn (bool): True if maximizing player is active.
        Returns:
            float: The current state's score, based on your own heuristic.
            
        """
        tots = len(game.get_legal_moves())        

        # endgame?
        if(not tots):
            if(maximizing_player_turn):
                return float("inf")
            else:
                return float("-inf")
        else:
            if(maximizing_player_turn):
                return tots
            else:
                return -tots

class CustomEvalFn:

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
        """Score the current game state
        
        Custom evaluation function that acts however you think it should. This 
        is not required but highly encouraged if you want to build the best 
        AI possible.
        
        Args
            game (Board): The board and game state.
            maximizing_player_turn (bool): True if maximizing player is active.

        Returns:
            float: The current state's score, based on your own heuristic.
            
        """

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

class CustomPlayer:
    """Player that chooses a move using 
    your evaluation function and 
    a minimax algorithm 
    with alpha-beta pruning.
    You must finish and test this player
    to make sure it properly uses minimax
    and alpha-beta to return a good move."""

    def __init__(self, search_depth=2, eval_fn=CustomEvalFn()):
        """Initializes your player.
        
        if you find yourself with a superior eval function, update the default 
        value of `eval_fn` to `CustomEvalFn()`
        
        Args:
            search_depth (int): The depth to which your agent will search
            eval_fn (function): Utility function used by your agent
        """
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
    
        # my lame attempt at an opening book..
        elif(game.move_count == 1):
            last_move = game.__last_queen_move__
            
            # | Q |   |   |   |    
            #     |   |   |   |    
            #         |   |   |    
            #             |   |
            #if(last_move == (0, 0) or last_move == (0, 6)):# here
            #    best_move = (6, 0) 
            if(last_move == (6, 0) or last_move == (6, 6)):
                best_move = (6, 4) 
            # -----------------------------------------------------
            
            # |   | Q |   |   |    
            #     |   |   |   |    
            #         |   |   |    
            #             |   |
            elif(last_move == (0, 1) or last_move == (1, 0)):# here
                best_move = (0, 0) 
            elif(last_move == (0, 5) or last_move == (1, 6)):
                best_move = (0, 6) 
            elif(last_move == (5, 0) or last_move == (6, 1)):
                best_move = (6, 0) 
            elif(last_move == (5, 6)): 
                best_move = (4, 5)
            elif(last_move == (6, 5)):
                best_move = (5, 4) 
            # -----------------------------------------------------
            
            # |   |   | Q |   |    
            #     |   |   |   |    
            #         |   |   |    
            #             |   |
            elif(last_move == (0, 2) or last_move == (0, 4)):# here
                best_move = (0, 3) 
            elif(last_move == (2, 0) or last_move == (4, 0)):
                best_move = (3, 0) 
            elif(last_move == (6, 2) or last_move == (6, 4)):
                best_move = (6, 3) 
            elif(last_move == (2, 6) or last_move == (4, 6)):
                best_move = (3, 6) 
            # -----------------------------------------------------
            
            # |   |   |   | Q |    
            #     |   |   |   |    
            #         |   |   |    
            #             |   |
            elif(last_move == (0, 3) or last_move == (3, 0) or last_move == (3, 6) or last_move == (6, 3)): #test this!
                best_move = (3, 3)
            # -----------------------------------------------------
            
            # |   |   |   |   |    
            #     | Q |   |   |    
            #         |   |   |    
            #             |   |
            elif(last_move == (1, 1)): #here
                best_move = (0, 2) 
            elif(last_move == (1, 5)):
                best_move = (0, 4) 
            elif(last_move == (5, 1)):
                best_move = (4, 0) 
            elif(last_move == (5, 5)):
                best_move = (6, 4)

            # -----------------------------------------------------
            
            # |   |   |   |   |    
            #     |   | Q |   |    
            #         |   |   |    
            #             |   |

            elif(last_move == (1, 2)):
                best_move = (6, 2) 
            elif(last_move == (2, 1)):
                best_move = (2, 6) 
            
            elif(last_move == (4, 1)):
                best_move = (1, 4) 
            elif(last_move == (1, 4)):
                best_move = (4, 1) 
    
            elif(last_move == (2, 5)):
                best_move = (5, 2) 
            #elif(last_move == (5, 2)):
            #    best_move = (2, 5) 
            
            elif(last_move == (4, 5)):
                best_move = (1, 2) 
            elif(last_move == (5, 4)):
                best_move = (2, 1) 
            
            # -----------------------------------------------------
            
            # |   |   |   |   |    
            #     |   |   | Q |    
            #         |   |   |    
            #             |   |
        

            # -----------------------------------------------------
            
            # |   |   |   |   |    
            #     |   |   |   |    
            #         | Q |   |    
            #             |   |
            
            elif(last_move == (2, 4)): #here
                best_move = (1, 3) 
            elif(last_move == (2, 2)): 
                best_move = (1, 3) 
            elif(last_move == (4, 2)): 
                best_move = (5, 3) 
            elif(last_move == (4, 4)): 
                best_move = (5, 3) 
            
            # -----------------------------------------------------
            
            # |   |   |   |   |    
            #     |   |   |   |    
            #         |   |   |    
            #             | Q |
            
            elif(last_move == (3, 3)):
                best_move = (1, 3)
            else:
                best_move = moves[randint(0, len(moves) - 1)
    

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

    def utility(self, game):
        """Can be updated if desired"""
        return self.eval_fn.score(game)

    def minimax(self, game, time_left, depth=0, maximizing_player=True):
        """Implementation of the minimax algorithm
        
        Args:
            game (Board): A board and game state.
            time_left (function): Used to determine time left before timeout
            depth: Used to track how deep you are in the search tree
            maximizing_player (bool): True if maximizing player is active.

        Returns:
            (tuple, int): best_move, best_val
        """
        
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
        """Implementation of the alphabeta algorithm
        
        Args:
            game (Board): A board and game state.
            time_left (function): Used to determine time left before timeout
            depth: Used to track how deep you are in the search tree
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning
            maximizing_player (bool): True if maximizing player is active.

        Returns:
            (tuple, int): best_move, best_val
        """
        
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

