#    Bidding Game Game AI by Matthew Schieber
#    All implementations were concieved and iterated by me.
#    Please make any suggestions at https://github.com/schiebermc/Game_AI

from math import ceil

STARTING_CHIPS = 100

class Player:

    def __init__(self):
        self.player   = int(input())
        self.pos = int(input())
        if(self.player == 1):
            self.my_moves = self.read_moves()
            self.enemy_moves = self.read_moves()
        else:    
            self.enemy_moves = self.read_moves()
            self.my_moves = self.read_moves()
        
        self.get_chips()

    def get_chips(self):
        self.my_chips = STARTING_CHIPS
        self.enemy_chips = STARTING_CHIPS
        self.tiebreaker = True if self.player == 1 else False
        for ind, val in enumerate(self.my_moves):
            if(val > self.enemy_moves[ind]):
                self.my_chips -= val
            elif(val < self.enemy_moves[ind]):
                self.enemy_chips -= self.enemy_moves[ind]
            else:
                if(self.tiebreaker):
                    self.my_chips -= val
                else:
                    self.enemy_chips -= self.enemy_moves[ind]
                self.tiebreaker = not self.tiebreaker


    def read_moves(self):
        moves = [int(val) for val in input().split()]
        return moves

    def print_all(self):
        print("player: ", self.player)
        print("position of scotch: ", self.pos)
        print("my moves: ", self.my_moves)
        print("enemy moves: ", self.enemy_moves)
        print("current chips: ", self.my_chips, self.enemy_chips, self.tiebreaker)

    def move(self):

        # with most bidding games, the idea is to intentionally lose some
        # bids with the objective of having the enemy waste their resources
        # eventually, with enough lost bids, the difference in chips will 
        # allow for a winning strategy to arise.

        # below, the idea is to have some rubber band effect
        # pull harder the closer the item gets to the enemy
        # hopefully, they waste their chips faster.
        
        # I chose a fairly simple funcitonal form: min(least, coef*rate^dist_to_me)
        # where dist_to_me \in {1...9} increases the power function exponent
        # special considerations for killer moves

        rate = 2
        least = 2
        coef = 0.05
        frac_of_mine = 0.5

        dist = self.pos if self.player == 1 else 10 - self.pos 
        if(dist == 1):
            chips = self.my_chips
        elif(dist == 9):
            chips = self.enemy_chips if self.tiebreaker else self.enemy_chips + 1
        else:
            chips = ceil(min(frac_of_mine*self.my_chips, coef * (rate ** dist)))
            
        # an observation is that many people floor at 1, so oubidding them 
        # with 2 is nice.
        print(max(chips, least))


if __name__ == "__main__":

    mastermind = Player()
    mastermind.print_all()
    mastermind.move()

 

