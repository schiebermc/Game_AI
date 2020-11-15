
N = 8
EMPTY_CHAR = '-'

class Board:

    def __init__(self, player1, player2):
        
        self.player1 = player1
        self.player2 = player2
        self.board = [[EMPTY_CHAR for j in range(N)] for i in range(N)]


    def print_board(self):
        
        print("Current board: ")
        print("    0    1    2    3    4    5    6    7")
        for ind, row in enumerate(self.board):
            print(ind, row)
        print()

    def get_legal_moves(self):
        
        legal_moves = []
        for col in range(N):
            row = -1
            for this_row in range(N-1, -1, -1):
                if(self.board[this_row][col] == EMPTY_CHAR):
                    legal_moves.append(col)
                    break 
    
        return legal_moves

        
    def perform_move(self, player, col, print_info=False):
  
        if(print_info):
            print("Player color {} chose column {}".format(player, col))
 
        assert(col >= 0 and col < N) 
        assert(player == self.player1 or player == self.player2)

        row = -1
        for this_row in range(N-1, -1, -1):
            if(self.board[this_row][col] == EMPTY_CHAR):
                row = this_row
                break 
        
        assert(row >= 0)
        self.board[this_row][col] = player


    def four_contiguous_from_here(self, x, y, x_shift, y_shift):
        
        return [self.board[x+mult*x_shift][y+mult*y_shift] 
                for mult in range(4)]
            

    def check_this_direction(self, x, y, x_shift, y_shift):
        check  = self.four_contiguous_from_here(x, y, x_shift, y_shift)
        if(len(set(check)) == 1 and check[0] != EMPTY_CHAR):
            return True


    def game_over(self):
       
        # the baked-in numbers assume this is a traditional connect-4 board 
        for x in range(8):
            for y in range(8):

                # check rows
                if(y <= 4 and self.check_this_direction(x, y, 0, 1)):
                    return True, (x, y, 'row')
                
                # check cols
                if(x <= 4 and self.check_this_direction(x, y, 1, 0)):
                    return True, (x, y, 'col')
                
                # check diagonals
                if(x <= 4 and y <= 4 and self.check_this_direction(x, y, 1, 1)):
                    return True, (x, y, 'diag')
        
        return False, None


    def is_draw(self):
        
        game_over, how = self.game_over()
        if(game_over):
            return False
        
        else:
            return len(self.get_legal_moves()) == 0 
        




