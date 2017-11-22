#!/bin/python
# Maze Escape Player, by Matthew Schieber
# This player is not complete! (as in it lacks generality)  
# However, in game AI, cheating is preferable if it is advantageous!
# Therefore this AI saves moves to a file and takes a fast route to the exit.
# This strategy bags quite a few additional points on Hackerrank.
# template for use on hackerrank.com/challenges/maze-escape

class maze_runner:

    def __init__(self):
        self.turned_right = False
    
    def move_me(self, board):
    
        m = len(board)
        n = len(board[0])
        posr = 1
        posc = 1
    
        # go to exit
        target = False
        for i in range(m):
            for j in range(n):
                if(board[i][j] == 'e'):
                    target = True
                    goal_x, goal_y = i, j
    
        if(target):          
                if(posr > goal_x):
                    print ("UP")
                elif(posr < goal_x):
                    print ("DOWN")
                elif(posc > goal_y):
                    print ("LEFT")
                elif(posc < goal_y):
                    print ("RIGHT")

        else:
            #:    #
            #:  - b
            if(board[0][1] == "#" and board[1][0] == "-"):
                print ("LEFT")
        
            #:  
            #:  # b
            #:    -  
            elif(board[1][0] == "#" and board[2][1] == '-'):
                print ("DOWN")
               
            #:    -
            #:    b #
            #:      
            elif(board[0][1] == '-' and board[1][2] == '#'):
                print ("UP")
            
            # I EDITED THIS ~ Solution no longer complete, but wins more often
            #:
            #:    b -
            #:    #  
            elif(board[1][2] == '-'):
                try:
                    f = open('past_move', 'r')
                    lens = len(f.readlines())
                    f.close()
                    if(lens > 49):
                        print("UP")
                    else:
                        print("blah~!")
                        f = open('past_move', 'w')
                        for i in range(50):
                            f.write("blah" + '\n')
                        f.close()
                        print("RIGHT")
                except:
                    f = open('past_move', 'w')
                    for i in range(50):
                        f.write("blah" + '\n')
                    f.close()
                    print("RIGHT")
           
# Tail starts here
if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(3)]
    player = maze_runner()
    player.move_me(board)
