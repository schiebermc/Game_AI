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


class HorizontalPlayer():

    BLOCK_LENGTH = 100
    BLOCK_HEIGHT = 30

    DIRECTIONS = {
                    "LEFT"  : -1, 
                    "RIGHT" : 1,
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
        
        assert player_num <= 1

    def lossRect(self, window):
            
        if self.player_num == 0:
            return pygame.draw.rect(window, WHITE, (0, 0, WIDTH, self.OUTER_BORDER_SIZE // 2)) 
        elif self.player_num == 1:
            return pygame.draw.rect(window, WHITE, (0,\
                HEIGHT - (self.OUTER_BORDER_SIZE // 2), WIDTH, self.OUTER_BORDER_SIZE // 2)) 
        else:
            raise Exception()

    def draw(self, window):
        return pygame.draw.rect(window, GREY, (self.x_coord, \
            self.y_plane, self.BLOCK_LENGTH, self.BLOCK_HEIGHT))

    def propagate(self, move, fraction_of_max_velocity):

        if not move in self.DIRECTIONS:
            raise Exception("Illegal move: ({}, {})".format(move, self.player_num))

        x_shift = self.DIRECTIONS[move] * self.max_velocity * fraction_of_max_velocity
        self.x_coord += x_shift
        self.x_coord = max(self.x_coord, self.left_bound)
        self.x_coord = min(self.x_coord, self.right_bound - self.BLOCK_LENGTH)
        self.velocity = x_shift


class VerticalPlayer():

    BLOCK_LENGTH = 100
    BLOCK_HEIGHT = 30

    DIRECTIONS = {
                    "UP"  : -1, 
                    "DOWN" : 1,
                 }
    
    OUTER_BORDER_SIZE = 10

    def __init__(self, x_plane, up_bound, down_bound, player_num, max_velocity=8):

        self.x_plane = x_plane
        self.y_coord = HEIGHT // 2
        self.up_bound = up_bound
        self.down_bound = down_bound
        self.velocity = 0
        self.player_num = player_num
        self.max_velocity = max_velocity
    
        assert player_num >= 2

    def lossRect(self, window):
            
        if self.player_num == 2:
            return pygame.draw.rect(window, WHITE, (0, 0, self.OUTER_BORDER_SIZE // 2, HEIGHT)) 
        elif self.player_num == 3:
            return pygame.draw.rect(window, WHITE, (WIDTH - (self.OUTER_BORDER_SIZE // 2), 0, 
                                self.OUTER_BORDER_SIZE // 2, HEIGHT)) 


    def draw(self, window):
        return pygame.draw.rect(window, GREY, (self.x_plane, \
            self.y_coord, self.BLOCK_HEIGHT, self.BLOCK_LENGTH))

    def propagate(self, move, fraction_of_max_velocity):

        if not move in self.DIRECTIONS:
            raise Exception("Illegal move: ({}, {})".format(move, self.player_num))

        y_shift = self.DIRECTIONS[move] * self.max_velocity * fraction_of_max_velocity
        self.y_coord += y_shift
        self.y_coord = max(self.y_coord, self.up_bound)
        self.y_coord = min(self.y_coord, self.down_bound - self.BLOCK_LENGTH)
        self.velocity = y_shift


class OnePlayerBoard:

    OUTER_BORDER_SIZE = 10
        
    def __init__(self, board_prints=True, human_player=True, num_computers=0):
        
        total_players = int(human_player) + num_computers
        if total_players < 0 or total_players > 4:
            raise Exception("Illegal number of players passed: {}".format(total_players))

        self.board_prints = board_prints
        
        self.human_player = human_player

        self.players = []
        if self.human_player:
            self.players.append(Player(self.bottom_plane,\
            self.OUTER_BORDER_SIZE, WIDTH - self.OUTER_BORDER_SIZE, len(self.players)))

        self.computers = []
        max_computer_velocity = 20
        for computer_player in range(num_computers):

            player_num = len(self.players)
            if player_num == 0:
                self.players.append(HorizontalPlayer(HEIGHT - HorizontalPlayer.BLOCK_HEIGHT - self.OUTER_BORDER_SIZE,\
                    self.OUTER_BORDER_SIZE, WIDTH - self.OUTER_BORDER_SIZE, 
                    len(self.players), max_velocity=max_computer_velocity))
                self.computers.append(ComputerPlayerHorizontalReverser(max_computer_velocity, self.OUTER_BORDER_SIZE))
            

            elif player_num == 1:
                self.computers.append(ComputerPlayerHorizontalReverser(max_computer_velocity, self.OUTER_BORDER_SIZE))
                self.players.append(HorizontalPlayer(self.OUTER_BORDER_SIZE, 
                                        self.OUTER_BORDER_SIZE, 
                                        WIDTH - self.OUTER_BORDER_SIZE,
                                        len(self.players),
                                        max_velocity=max_computer_velocity))        
            
            elif player_num == 2:
                self.computers.append(ComputerPlayerVerticalReverser(max_computer_velocity, self.OUTER_BORDER_SIZE))
                self.players.append(VerticalPlayer(self.OUTER_BORDER_SIZE, 
                                        self.OUTER_BORDER_SIZE, 
                                        HEIGHT - self.OUTER_BORDER_SIZE,
                                        len(self.players),
                                        max_velocity=max_computer_velocity))        

            elif player_num == 3:
                self.computers.append(ComputerPlayerVerticalReverser(max_computer_velocity, self.OUTER_BORDER_SIZE))
                self.players.append(VerticalPlayer(WIDTH - VerticalPlayer.BLOCK_HEIGHT - self.OUTER_BORDER_SIZE, 
                                        self.OUTER_BORDER_SIZE, 
                                        HEIGHT - self.OUTER_BORDER_SIZE,
                                        len(self.players),
                                        max_velocity=max_computer_velocity))        

            else:
                raise Exception()


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
            if len(self.players) <= 2:
                walls.append(pygame.draw.rect(window, BLACK, (0, 0, self.OUTER_BORDER_SIZE, HEIGHT)))
            
            if len(self.players) <= 3:
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

                else:
                    self.ball.xv *= -1
                
                
            # players
            collision_list = ball_rect.collidelistall(player_rects)
            if len(collision_list) != 0: 
                
                val = collision_list.pop()
                collision_occurred = True
                player_velocity = self.players[val].velocity
                self.score += 1
                
                if val <= 1:
                    self.ball.yv *= -1
                    self.ball.xv += player_velocity + randint(-2, 2)
                else:
                    self.ball.xv *= -1
                    self.ball.yv += player_velocity + randint(-2, 2)
                                    


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
         
        if move == "NONE" or move == None:
            return
   
        legal_moves = ["LEFT", "RIGHT"] if player_number <= 1 else ["UP", "DOWN"]
       
        if move in legal_moves:
            self.players[player_number].propagate(move, fraction_of_max_velocity)
        else:
            raise Exception("Illegal move passed: ({}, {})".format(player_number, move))
    






