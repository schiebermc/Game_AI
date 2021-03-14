"""

"""

import time
import pygame 
import argparse
from solvers import *
from constants import *  
from maze_generators import *

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT + INSTRUCTIONS_HEIGHT))

pygame.display.set_caption(GAME_NAME)

def instructions(window, num_explored, current_level):
            
    pygame.draw.rect(window, WHITE, (0, HEIGHT, WIDTH, INSTRUCTIONS_HEIGHT))
    pygame.draw.rect(window, BLACK, (0, HEIGHT, WIDTH, INSTRUCTIONS_BORDER_HEIGHT))
    
    text1 = FONT1.render("USE THE ARROW KEYS TO NAVIGATE",\
            1, (0, 0, 0)) 
    text2 = FONT1.render("TOTAL TILES EXPLORED: {}".format(num_explored),\
            1, (0, 0, 0)) 
    text3 = FONT1.render("MAZE DIFFICULTY LEVEL: {}".format(current_level),\
            1, (0, 0, 0)) 
    window.blit(text1, (10, HEIGHT + INSTRUCTIONS_BORDER_HEIGHT + 10))         
    window.blit(text2, (10, HEIGHT + INSTRUCTIONS_BORDER_HEIGHT + 40))         
    window.blit(text3, (10, HEIGHT + INSTRUCTIONS_BORDER_HEIGHT + 70))         


def game_over(window):
    pygame.draw.rect(window, WHITE, (100, 100, WIDTH - 200, 250))

    draw_x, draw_y = 150, 150
    font1 = pygame.font.SysFont("arial", 32)
    font2 = pygame.font.SysFont("arial", 22)
    text1 = font1.render("LEVEL PASSED", True, BLACK)
    text2 = font2.render("PRESS 'r' FOR NEXT LEVEL", True, BLACK)
    window.blit(text1, (40 + draw_x, draw_y))
    window.blit(text2, (20 + draw_x, draw_y + 100))

    
def main():


    run = True
    clock = pygame.time.Clock()
    
    maze = Maze(BASE_WIDTH, BASE_HEIGHT, WIDTH, HEIGHT)
    current_level = 1
    level_bump = LEVEL_BUMP
 
    solved = False
 
    while run:
            
        clock.tick(FPS)
        
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                run = False
        
            elif solved:
                game_over(WINDOW)
                if event.type == pygame.KEYDOWN and\
                        event.key == pygame.K_r:
                    
                    shift = level_bump * current_level
                    maze = Maze(BASE_WIDTH + shift, \
                            BASE_HEIGHT + shift, WIDTH, HEIGHT)
                    solved = False
                    current_level += 1

            elif event.type == pygame.KEYDOWN: 
           
                if event.key == pygame.K_a:

                    solver = BFSSolver(maze, MAZE_END_VAL)
                    solution = solver.solve()
                    for move in solution:
                        maze.forecast_move(move)
                        maze.draw(WINDOW)
                        instructions(WINDOW, len(maze.explored), current_level)
                        pygame.display.update()
                        time.sleep(0.25)
         
                elif event.key == pygame.K_DOWN:
                    maze.forecast_move("DOWN")
            
                elif event.key == pygame.K_UP:
                    maze.forecast_move("UP")
        
                elif event.key == pygame.K_LEFT:
                    maze.forecast_move("LEFT")
            
                elif event.key == pygame.K_RIGHT:
                    maze.forecast_move("RIGHT")
                
                else:
                    print("I'm good")       
 
        if not solved:
            maze.draw(WINDOW)
        solved = maze.game_over()
        instructions(WINDOW, len(maze.explored), current_level)
        pygame.display.update()
            

    pygame.quit()
        

if __name__ == "__main__":
    main()

 
