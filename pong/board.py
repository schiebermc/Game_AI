import time
import pygame
from players import *
from constants import *
from random import randint


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


class Player():

    BLOCK_LENGTH = 100
    BLOCK_HEIGHT = 30

    DIRECTIONS = {
                    "LEFT"  : -1, 
                    "RIGHT" : 1,
                    "NONE" : 0
                 }
    
    OUTER_BORDER_SIZE = 10

    def __init__(self, y_plane, left_bound, right_bound, player_num, max_velocity=8):

        self.y_plane = y_plane
        self.x_coord = WIDTH // 2
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.velocity = 0
        self.player_num = player_num
        self.max_velocity = max_velocity

    def lossRect(self, window):
            
        if self.player_num == 0:
            return pygame.draw.rect(window, WHITE, (0,\
                HEIGHT - (self.OUTER_BORDER_SIZE // 2), WIDTH, self.OUTER_BORDER_SIZE)) 
        elif self.player_num == 1:
            return pygame.draw.rect(window, WHITE, (0, 0, WIDTH, self.OUTER_BORDER_SIZE // 2)) 
        else:
            raise Exception()

    def draw(self, window):
        return pygame.draw.rect(window, GREY, (self.x_coord, \
            self.y_plane, self.BLOCK_LENGTH, self.BLOCK_HEIGHT))

    def propagate(self, move, fraction_of_max_velocity):
        x_shift = self.DIRECTIONS[move] * self.max_velocity * fraction_of_max_velocity
        self.x_coord += x_shift
        self.x_coord = max(self.x_coord, self.left_bound)
        self.x_coord = min(self.x_coord, self.right_bound - self.BLOCK_LENGTH)
        self.velocity = x_shift


class OnePlayerBoard:

    OUTER_BORDER_SIZE = 10
        
    def __init__(self, board_prints=True, human_player=True, num_computers=0):
       
        self.board_prints = board_prints
        
        self.bottom_plane = HEIGHT - Player.BLOCK_HEIGHT

        self.human_player = human_player

        self.players = []
        if self.human_player:
            self.players.append(Player(self.bottom_plane,\
            self.OUTER_BORDER_SIZE, WIDTH - self.OUTER_BORDER_SIZE, len(self.players)))

        self.computers = []
        max_computer_velocity = 20
        for computer_player in range(num_computers):

            if computer_player == 0:
                self.players.append(Player(self.bottom_plane,\
                    self.OUTER_BORDER_SIZE, WIDTH - self.OUTER_BORDER_SIZE, 
                    len(self.players), max_velocity=max_computer_velocity))
                self.computers.append(ComputerPlayerReverser(max_computer_velocity, self.OUTER_BORDER_SIZE))
            

            elif computer_player == 1:
                self.computers.append(ComputerPlayerReverser(max_computer_velocity, self.OUTER_BORDER_SIZE))
                self.players.append(Player(self.OUTER_BORDER_SIZE, 
                                        self.OUTER_BORDER_SIZE, 
                                        WIDTH - self.OUTER_BORDER_SIZE,
                                        len(self.players),
                                        max_velocity=max_computer_velocity))        

        if len(self.players) > 2:
            raise Exception("NOT EQUIPED FOR THIS")

        self.restart()

    
    def restart(self):

        self.ball = Ball(WIDTH // 2, HEIGHT // 2, 0, -4)
        self.score = 0
        self.game_over = False


    def allTurns(self, keys):
        
        if self.human_player:
            self.humanTurn(0, keys)
       
        for ind, computer in enumerate(self.computers):
            player_num = int(self.human_player) + ind
            fraction, move = computer.makeMove(self.ball, self.players[player_num])
            self.forecast_move(player_num, move, fraction)
 

    def humanTurn(self, player_number, keys):
        
        if keys[pygame.K_LEFT]:
            self.forecast_move(player_number, "LEFT")
            
        elif keys[pygame.K_RIGHT]:
            self.forecast_move(player_number, "RIGHT")
        


    def draw(self, window):
        window.fill(WHITE)
       
        while(True): 
        
 
            # draw the player first
            for player in self.players:
                player.draw(window)
            
            # propagate ball
            self.ball.propagate()
            ball_rect = self.ball.draw(window)
            
            # horizontal outer borders
            walls = []
            if len(self.players) <= 1:
                walls.append(pygame.draw.rect(window, BLACK, (0, 0, WIDTH, self.OUTER_BORDER_SIZE))) 

            # vertical outer borders
            walls.append(pygame.draw.rect(window, BLACK, (0, 0, self.OUTER_BORDER_SIZE, HEIGHT)))
            walls.append(pygame.draw.rect(window, BLACK, (WIDTH - self.OUTER_BORDER_SIZE, 0,  \
                             self.OUTER_BORDER_SIZE, HEIGHT)))
            
            loss_rects = []
            player_rects = []
            for player in self.players:
                loss_rects.append(player.lossRect(window))
                player_rects.append(player.draw(window))            

            # loss rects
            collision_list = ball_rect.collidelistall(loss_rects)
            if len(collision_list) != 0:
                self.game_over = True
                continue

            # walls
            collision_occurred = False
            collision_list = ball_rect.collidelistall(walls)
            if len(collision_list) == 0:
                pass
            else:
                collision_occurred = True
                
                player_bump = len(self.players) - 1
                if len(self.players) == 1:
                    if 0 in collision_list:
                        self.ball.yv *= -1

                    if 1 in collision_list or 2 in collision_list:
                        self.ball.xv *= -1

                elif len(self.players) == 2:
                    self.ball.xv *= -1
                
                else:
                    raise Exception()

            # players
            collision_list = ball_rect.collidelistall(player_rects)
            if len(collision_list) != 0: 
                collision_occurred = True
                player_velocity = self.players[collision_list[0]].velocity
                self.ball.yv *= -1
                self.ball.xv += player_velocity + randint(-1, 1)
                self.score += 1
                
            # no collision occurred, so we can exit        
            if not collision_occurred:
                break

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

    
    def forecast_move(self, player_number, move="NONE", fraction_of_max_velocity=1.0):
       
        if move in ["LEFT", "RIGHT", "NONE"]:
            self.players[player_number].propagate(move, fraction_of_max_velocity)
        else:
            print("No action performed on players")
















