
import os
from player import *
from board import Board


def play_connect_4(player1, player2, print_info=True):

    if(print_info):
        print("Starting a game..")

    turn = 0
    winner = None        
    game_over = False
    winning_move = None
    
    board = Board(player1_char, player2_char)

    while(not game_over):
        
        turn += 1
 
        if(turn % 2):
            # Player 1's turn
            move = player1.make_move(board)
            board.perform_move(player1_char, move, print_info=print_info)           
            game_over, how = board.game_over()

        else:
            # Player 2's turn
            move = player2.make_move(board)
            board.perform_move(player2_char, move, print_info=print_info)            
            game_over, how = board.game_over()
        
        if(print_info):
            print("Turn {}".format(turn))
            board.print_board()               

        if(game_over):
            winner = player1_char if turn % 2 else player2_char
            winning_move = how

        if(board.is_draw()):
            return None, board, None

    return winner, board, how

   
def simulate_games(player1, player2, N_games):
    # simulation driver to determine how good an AI is

    draws = 0
    player1_wins = 0
    player2_wins = 0
    
    player1_char = player1.get_player_char()    
    player2_char = player2.get_player_char()    
    
    for game in range(N_games):
        
        winner, board, how = play_connect_4(player1, player2)
        
        if(winner == None):
            draws += 1
            continue

        if(winner == player1_char):
            player1_wins += 1
        elif(winner == player2_char):
            player2_wins += 1       
        else:
            raise Exception() 

    draws_percentage = draws / float(N_games) * 100.
    player1_win_percentage = player1_wins / float(N_games) * 100.
    player2_win_percentage = player2_wins / float(N_games) * 100.

    print("After {} games - results: ({}, {}, {}), percentages: ({}, {}, {})".format(N_games,
                player1_wins, player2_wins, draws, player1_win_percentage, 
                player2_win_percentage, draws_percentage))


if __name__ == "__main__":

    player1_char = 'R'
    player2_char = 'B'

    #player1 = RandomPlayer('R', 'B')
    player1 = MiniMaxPlayer('R', 'B', max_depth=1)
    player2 = MiniMaxPlayer('B', 'R', max_depth=5)
   
    simulate_games(player1, player2, 1)

#    winner, board, how = play_connect_4(player1, player2, print_info=True)
#    board.print_board()
#    print(how)
#    print("Game over! Player {} wins!".format(winner))





 
