"""

"""

import time
import pygame 
import argparse
from constants import *  
from board import *

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT + INSTRUCTIONS_HEIGHT))

pygame.display.set_caption(GAME_NAME)

def instructions(window, automatic_solve_invoked=False):
            
    pygame.draw.rect(window, WHITE, (0, HEIGHT, WIDTH, INSTRUCTIONS_HEIGHT))
    text1 = FONT1.render("USE THE ARROW KEYS TO NAVIGATE BOARD",\
        1, (0, 0, 0)) 
    window.blit(text1, (10, HEIGHT + 10))         
    

def main():

    run = True
    clock = pygame.time.Clock()

    board = OnePlayerBoard()
   
 
    while run:
            
        clock.tick(FPS)
        
        if board.game_over:
            pass
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                board.forecast_move("LEFT")
                
            elif keys[pygame.K_RIGHT]:
                board.forecast_move("RIGHT")
            
            else:
                board.forecast_move()
        
            board.draw(WINDOW)
            instructions(WINDOW)
            pygame.display.update()
 
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
 
    

    pygame.quit()
        

if __name__ == "__main__":
    main()

 
