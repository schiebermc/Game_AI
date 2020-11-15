
import os
from player import *
from board import Board


if __name__ == "__main__":

    print("Starting a game..")

    turn = 0
    game_over = False
        
    player1_char = 'R'
    player2_char = 'B'

    board = Board(player1_char, player2_char)

    player1 = RandomPlayer('R', 'B')
    player2 = RandomPlayer('B', 'R')
    
    while(not game_over):
        
        #os.system("./a.out")
 
        if(turn % 2):
            # Player 1's turn
            move = player1.make_move(board)
            board.perform_move(player1_char, move)           
            game_over, how = board.game_over()

        else:
            # Player 2's turn
            move = player2.make_move(board)
            board.perform_move(player2_char, move)            
            game_over, how = board.game_over()
        
        print("Turn {}".format(turn))
        board.print_board()               

        if(game_over):
            print("Game over! Player {} wins!".format(player1_char if turn % 2 else player2_char))
            print(how)

        turn += 1





    




