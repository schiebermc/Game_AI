
N = 7
from board import Board
from random import randint


class Player:


    def __init__(self, player_char, enemy_char):
        self.player_char = player_char
        self.enemy_char = enemy_char

    def generate_move(self, board):
        raise NotImplementederror() # pure virtual

    def make_move(self, board):
        return self.generate_move(board)

    def get_player_char(self):
        return self.player_char
    
    def get_enemy_char(self):
        return self.enemy_char


class RandomPlayer(Player):
    

    def __init__(self, player_char, enemy_char):
        Player.__init__(self, player_char, enemy_char)

    def generate_move(self, board):
        moves = board.get_legal_moves()
        move = moves[randint(0, len(moves)-1)]
        return move
  
 
class BoardEvaluatorBasic(Board):

    def __init__(self, player1_char, player2_char):
        Board.__init__(self, player1_char, player2_char)

    
    def compute_winning_metric(self, player):
       
        # nothing fancy right now, just see if game is over
        won, how = self.game_over()
        if(won):
            winner = how[0]
            if winner == player:
                return 100
            else:
                return -100
        else:
            return 0
    
    def get_utility(self, player):
        # get the utility of this board, relative to designated player
        return self.compute_winning_metric(player)

    
class BoardEvaluatorFavorMiddle(BoardEvaluatorBasic):

    def __init__(self, player1_char, player2_char):
        BoardEvaluatorBasic.__init__(self, player1_char, player2_char)


    def compute_centroid(self, player):
        
        ys = 0.
        tots = 0.
        for i in range(N):
            for j in range(N):
                if(self.board[i][j] == player):
                    tots += 1
                    ys += j
        return ys / tots            


    def get_utility(self, player):
        winning_metric = self.compute_winning_metric(player)
        centroid = self.compute_centroid(player)

        return winning_metric - abs(3.0 - centroid) + randint(-2, 2)



class MaxPlayer(Player):


    def __init__(self, player_char, enemy_char):
        Player.__init__(self, player_char, enemy_char)


    def generate_move(self, board):
        
        best_utility, best_move = float('-inf'), None

        other_player = self.enemy_char
        active_player = self.player_char

        for col in board.get_legal_moves():
            
            # forecase this move
            new_board = board.forecast_move(active_player, col)
            
            # get the utility of forecasted board
            evaluator = BoardEvaluator(active_player, other_player)
            evaluator.set_board(new_board)
            this_utility = evaluator.get_utility(active_player)
             
            # compare
            if(this_utility > best_utility):
                best_utility, best_move = this_utility, col


        return best_move

    
class MiniMaxPlayer(Player):


    def __init__(self, player_char, enemy_char, max_depth=3):
        Player.__init__(self, player_char, enemy_char)
        self.max_depth = max_depth
        self.evaluator = BoardEvaluatorFavorMiddle

    def generate_move(self, board):
        
        utility, move = self.minimax_recursive(board, 1)
        
        print(utility, move)
        return move


    def minimax_recursive(self, board, depth, maximizing=True):
       
        if(maximizing):     
            best_utility, best_move = float('-inf'), None
        else:
            best_utility, best_move = float('inf'), None
            
       
        if(maximizing): 
            other_player = self.enemy_char
            active_player = self.player_char
        else:
            other_player = self.enemy_char
            active_player = self.player_char
            #other_player = self.player_char
            #active_player = self.enemy_char
            
        # base case, game is already over
        won, how = board.game_over()
        if(won or board.is_draw()):
            evaluator = self.evaluator(active_player, other_player)
            evaluator.set_board(board.get_board())
            best_utility = evaluator.get_utility(active_player)
        
        else:

            for col in board.get_legal_moves():
                    
                # forecast this move
                new_board, new_board_instance = board.forecast_move(active_player, col)

                this_utility, this_move = float('-inf'), None

                if(depth == self.max_depth):            
                    
                    # get the utility of forecasted board
                    evaluator = self.evaluator(active_player, other_player)
                    evaluator.set_board(new_board)
                    this_utility = evaluator.get_utility(active_player)

                else:
                
                    # recurse further down game tree
                    this_utility, this_move = self.minimax_recursive(new_board_instance, 
                                        depth + 1, not maximizing)
 
                # compare
                if(maximizing):
                    if(this_utility > best_utility):
                        best_utility, best_move = this_utility, col
                else:
                    if(this_utility < best_utility):
                        best_utility, best_move = this_utility, col
                    

        return best_utility, best_move
        
        

        

   





 
