import time
import pygame
from constants import *
from random import randint

class Player():

    BLOCK_LENGTH = 100
    BLOCK_HEIGHT = 30

    DIRECTIONS = {
                    "LEFT"  : -8, 
                    "RIGHT" : 8,
                    "NONE" : 0
                 }

    def __init__(self, y_plane, left_bound, right_bound):
        self.y_plane = y_plane - self.BLOCK_HEIGHT
        self.x_coord = WIDTH // 2
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.velocity = 0

    def draw(self, window):
        return pygame.draw.rect(window, GREY, (self.x_coord, \
            self.y_plane, self.BLOCK_LENGTH, self.BLOCK_HEIGHT))

    def propagate(self, move):
        x_shift = self.DIRECTIONS[move]
        self.x_coord += x_shift
        self.x_coord = max(self.x_coord, self.left_bound)
        self.x_coord = min(self.x_coord, self.right_bound - self.BLOCK_LENGTH)
        self.velocity = x_shift


class Ball():

    RADIUS = 30

    def __init__(self, x, y, xv, yv):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv
        
    def draw(self, window):
        return pygame.draw.circle(window, RED, (self.x, self.y), self.RADIUS)

    def propagate(self):
        self.x += self.xv
        self.y += self.yv


class OnePlayerBoard:

    OUTER_BORDER_SIZE = 10
        
    def __init__(self, board_prints=True):
       
        self.board_prints = board_prints
        
        self.bottom_plane = HEIGHT

        self.player1 = Player(self.bottom_plane,\
            self.OUTER_BORDER_SIZE, WIDTH - self.OUTER_BORDER_SIZE)

        self.ball = Ball(WIDTH // 2, HEIGHT // 2, 0, -15)
        self.score = 0
        self.game_over = False


    def draw(self, window):
        window.fill(WHITE)
       
        while(True): 
        
            # horizontal outer borders
            top_border_rect = pygame.draw.rect(window, BLACK, (0, 0, WIDTH, self.OUTER_BORDER_SIZE)) 
            bottom_border_rect = pygame.draw.rect(window, WHITE, (0,\
                HEIGHT - (self.OUTER_BORDER_SIZE // 2), WIDTH, self.OUTER_BORDER_SIZE)) 
            
            # vertical outer borders
            left_border_rect  = pygame.draw.rect(window, BLACK, (0, 0, self.OUTER_BORDER_SIZE, HEIGHT))
            right_border_rect = pygame.draw.rect(window, BLACK, (WIDTH - self.OUTER_BORDER_SIZE, 0,  \
                             self.OUTER_BORDER_SIZE, HEIGHT))
 
            # draw the player first
            player1_rect = self.player1.draw(window)
            
            # propagate ball
            self.ball.propagate()
            ball_rect = self.ball.draw(window)
            
            collision_list = ball_rect.collidelistall([top_border_rect, bottom_border_rect,
                    left_border_rect, right_border_rect, player1_rect])
            
            if len(collision_list) == 0:
                break
            else:
                print(collision_list)
                if 0 in collision_list:
                    self.ball.yv *= -1

                if 1 in collision_list:
                    self.game_over = True
 
                if 2 in collision_list or 3 in collision_list:
                    self.ball.xv *= -1

                elif 4 in collision_list:
                    self.ball.yv *= -1
                    self.ball.xv += self.player1.velocity + randint(-1, 1)
                    self.score += 1
                
                
        draw_x = draw_y = 2 * self.OUTER_BORDER_SIZE
        font = pygame.font.SysFont('arial', 60)
        text = font.render(str(self.score), True, BLACK)
        window.blit(text, (draw_x, draw_y))

        if self.game_over:
            self.draw_endgame(window)
        
        return not self.game_over 

    def draw_endgame(self, window):
        
        draw_x, draw_y = 100, 100
        font = pygame.font.SysFont("arial", 60)
        text = font.render("GAME OVER", True, BLACK)
        window.blit(text, (draw_x, draw_y))

    
    def forecast_move(self, move="NONE"):
        
        if move in ["LEFT", "RIGHT", "NONE"]:
            self.player1_rect = self.player1.propagate(move)
        else:
            print("No action performed on players")


