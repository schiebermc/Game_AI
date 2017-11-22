#!/bin/python
# Maze Escape Player, by Matthew Schieber
# complete player, which employs the "keep right hand on wall" strategy
# template for use on hackerrank.com/challenges/maze-escape


def move_me(board):
    
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
                    
        #:    
        #:    b -
        #:    #  
        elif(board[1][2] == '-'):
            print ("RIGHT")
        
        elif(board[1][0] == '-'):
            print ("LEFT")
                
           
           
# Tail starts here
if __name__ == "__main__":
    pos = [int(i) for i in input().strip().split()]
    board = [[j for j in input().strip()] for i in range(3)]
    move_me(board)
