
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
        



    
