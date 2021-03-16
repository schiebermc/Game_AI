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

    
def game_over(window):
    pygame.draw.rect(window, WHITE, (100, 100, WIDTH - 200, 250))

    draw_x, draw_y = 150, 150
    font1 = pygame.font.SysFont("arial", 32)
    font2 = pygame.font.SysFont("arial", 22)
    text1 = font1.render("GAME OVER", True, BLACK)
    text2 = font2.render("PRESS 'r' TO RESTART THE GAME", True, BLACK)
    window.blit(text1, (40 + draw_x, draw_y))
    window.blit(text2, (20 + draw_x, draw_y + 100))


def main():

    run = True
    clock = pygame.time.Clock()

    board = OnePlayerBoard(human_player=False, num_computers=4)
 
    while run:
            
        clock.tick(FPS)
        
        if board.game_over:
            game_over(WINDOW)

        keys = pygame.key.get_pressed()

        if board.game_over and keys[pygame.K_r]:
            board.restart()
        
        board.allTurns(keys)
 
        if not board.game_over:
            board.draw(WINDOW)
        instructions(WINDOW)
        pygame.display.update()
 
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
 
    

    pygame.quit()
        

if __name__ == "__main__":
    main()

 
