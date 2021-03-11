"""
    This module invokes pygame to play the N-puzzle game!

    Basic Usage:
        python play_game.py -n 3
        python play_game.py -n 4
        python play_game.py -n 5
        
    Note: graphics are not well equipped to handle anythign past 5

    N-Puzzle game driver and solutions by Matthew Schieber
    All implementations were concieved and iterated by me.
    Please make any suggestions at https://github.com/schiebermc/Game_AI
"""

import time
import pygame 
import argparse
from constants import *  
from board import *
from solvers import UnidirectionalSolver

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT + INSTRUCTIONS_HEIGHT))

pygame.display.set_caption(GAME_NAME)


def parse_cli():
    parser = argparse.ArgumentParser(
            description="Argument Parser for N-Puzzle Game")
    parser.add_argument("-n", "-n_size", type=int, default=3)
    return parser.parse_args()


def instructions(window, automatic_solve_invoked=False):
            
    pygame.draw.rect(window, WHITE, (0, HEIGHT, WIDTH, INSTRUCTIONS_HEIGHT))
    
    if automatic_solve_invoked:
        text1 = FONT1.render(\
            "AUTOMATIC SOLVE INVOKED, THINKING OF SOLUTION . . .",\
            1, (0, 0, 0)) 
        window.blit(text1, (10, HEIGHT + 10))         
    else: 
        text1 = FONT1.render("USE THE ARROW KEYS TO SLIDE THE GREY BLOCK",\
            1, (0, 0, 0)) 
        text2 = FONT1.render("PRESS 'a' TO INVOKE AN AUTOMATIC SOLVE",\
            1, (0, 0, 0)) 
        window.blit(text1, (10, HEIGHT + 10))         
        window.blit(text2, (10, HEIGHT + 50))         


def solved_instructions(window, step, total, total_visited):
    pygame.draw.rect(window, WHITE, (0, HEIGHT, WIDTH, INSTRUCTIONS_HEIGHT))
    
    text1 = FONT1.render("AUTOMATIC SOLVE INVOKED, THINKING OF SOLUTION . . .",\
        1, (0, 0, 0)) 

    text2 = FONT1.render("DONE! FOUND SOLUTION AFTER VISITING {} NODES"\
        .format(total_visited), 1, (0, 0, 0)) 

    text3 = FONT1.render("PERFORMING MOVE {} OF {}"\
        .format(step, total),\
        1, (0, 0, 0)) 

    window.blit(text1, (10, HEIGHT + 10))         
    window.blit(text2, (10, HEIGHT + 40))         
    window.blit(text3, (10, HEIGHT + 70))         


def main():

    run = True
    clock = pygame.time.Clock()

    args = parse_cli()
    board = Board(args.n)
    
    while run:
        
        clock.tick(FPS)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
       
            elif event.type == pygame.KEYDOWN: 
            
                if event.key == pygame.K_DOWN:
                    board.forecast_move("DOWN")
            
                elif event.key == pygame.K_UP:
                    board.forecast_move("UP")
        
                elif event.key == pygame.K_LEFT:
                    board.forecast_move("LEFT")
            
                elif event.key == pygame.K_RIGHT:
                    board.forecast_move("RIGHT")
           
                elif event.key == pygame.K_a:
                    
                    # first, update display to reflect current course of action
                    instructions(WINDOW, automatic_solve_invoked=True)
                    pygame.display.update()
                   
                    # get solution 
                    solver = UnidirectionalSolver(board)
                    num_visited, moves = solver.get_solution()
                    print("Solution found after visiting {} nodes".format(\
                        num_visited))                   
 
                    # play back the solution, printing each step
                    for ind, move in enumerate(moves):
                        print("Move {} of {}".format(ind, len(moves)))
                        board.forecast_move(move)
                        board.draw(WINDOW)
                        solved_instructions(WINDOW, ind, len(moves), num_visited)
                        pygame.display.update()
                        time.sleep(0.25)
                    time.sleep(5)
                else:
                    print("I don't care about that key ;)")
            else:
                pass
        
        board.draw(WINDOW)
        instructions(WINDOW)
        pygame.display.update()

    pygame.quit()
        

if __name__ == "__main__":
    main()

 
