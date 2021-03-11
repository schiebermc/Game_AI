import pygame
from constants import *
from random import shuffle, seed, sample

class Tile:
    
    """
        Representation of tiles in the N-puzzle game
        These tiles are actively altered throughout the game,
        so they must be responsible for drawing themselves.
    """

    def __init__(self, val, x, y, w, l):
        self.val = val
        self.x = x
        self.y = y
        self.w = w
        self.l = l

    def draw_tile(self, window):
        if self.val == 0:
            pygame.draw.rect(window, GREY, (self.x, self.y, self.w, self.l))
        else:
            val = self.val
            font = pygame.font.SysFont('arial', 100)
            text = font.render(str(val), True, BLACK)
            
            
            if int(val) >= 10:
                draw_x = self.x + self.w // 7 
                draw_y = self.y + self.l // 4
            else:
                draw_x = self.x + self.w // 3 
                draw_y = self.y + self.l // 4
 
            window.blit(text, (draw_x, draw_y))
                    
    def __repr__(self):
        return str(self.val)


class Board:

    OUTER_BORDER_SIZE = 10
    INNER_BORDER_SIZE = 5
        
    MOVE_DIRS = { 
                  "RIGHT" : (0, 1),
                  "LEFT"  : (0, -1),
                  "DOWN"  : (1, 0),
                  "UP"    : (-1, 0)
                }

    def __init__(self, n, board=None, random_shifts=100):
       
        self.board_prints = True
 
        self.board = board if board != None else [i for i in range(n*n)]
        self.rows = n
        self.cols = n
        
        # inner borders
        self.inner_width  = WIDTH - 2 * self.OUTER_BORDER_SIZE - \
                                (self.cols - 1) * self.INNER_BORDER_SIZE
        self.inner_height = HEIGHT - 2 * self.OUTER_BORDER_SIZE - \
                                (self.rows - 1) * self.INNER_BORDER_SIZE
        self.tile_width = self.inner_width / self.cols
        self.tile_height = self.inner_height / self.rows
       
        # after some trial and error, I found it was best to designate the 
        # disjoint components of the board into "tiles", which are each 
        # responsible for drawing themselves 
        self.tiles = []
        for row in range(self.rows):
            self.tiles.append([])
            for col in range(self.cols):
                
                # basic idea: each tile knows its value, its upper left x-y
                # coordinate, and its width and height
                self.tiles[row].append(Tile(self.board[row*self.cols + col], 
                    self.OUTER_BORDER_SIZE + \
                        col * (self.tile_width + self.INNER_BORDER_SIZE),
                    self.OUTER_BORDER_SIZE + \
                        row * (self.tile_height + self.INNER_BORDER_SIZE), 
                        self.tile_width, self.tile_height))

        # to ensure our board has a solution, we start with the solved state
        # and randomize it according to legal moves. This is important, since
        # not all permuations of N-puzzles have solutions, but if we only 
        # progress our board using legal moves, our board will have a solution
        all_pos = list(self.MOVE_DIRS.keys())
        for shift in range(random_shifts):
            move = sample(all_pos, 1)[0]
            self.forecast_move(move)


    def draw(self, window):
        window.fill(WHITE)
        
        # horizontal outer borders
        pygame.draw.rect(window, BLACK, (0, 0, WIDTH, self.OUTER_BORDER_SIZE)) 
        pygame.draw.rect(window, BLACK, (0, HEIGHT - self.OUTER_BORDER_SIZE, \
                         WIDTH, self.OUTER_BORDER_SIZE)) 
        
        # vertical outer borders
        pygame.draw.rect(window, BLACK, (0, 0, self.OUTER_BORDER_SIZE, HEIGHT))
        pygame.draw.rect(window, BLACK, (WIDTH - self.OUTER_BORDER_SIZE, 0,  \
                         self.OUTER_BORDER_SIZE, HEIGHT))
 
        for col in range(1, self.cols):
            pygame.draw.rect(window, BLACK, (self.OUTER_BORDER_SIZE + col * \
                self.tile_width + (col-1) * self.INNER_BORDER_SIZE, 0, \
                self.INNER_BORDER_SIZE, HEIGHT)) 
            
        for row in range(1, self.rows):
            pygame.draw.rect(window, BLACK, (0, self.OUTER_BORDER_SIZE + row  *\
                self.tile_height + (row-1) * self.INNER_BORDER_SIZE, WIDTH, \
                self.INNER_BORDER_SIZE)) 

        for row in range(self.rows):
            for col in range(self.cols):
                self.tiles[row][col].draw_tile(window) 


    def forecast_move(self, move):
        """ Alters the current board according to the 'move'. If the move 
            passed is impossible to perform due to board constraints, this 
            function will do nothing and return False.      
    
            Args:
                move (str): Direction in whcih to slide the empty tile
            
            Returns:
                bool : whether the move was successful or not
                - if move was successful, this instance was altered

        """
        if self.board_prints:
            print(move)
 
        # find the empty tile location
        zero_pos = None
        for row in range(self.rows):
            for col in range(self.cols):
                if self.tiles[row][col].val == 0:
                    zero_pos = (row, col)
                    break   
            if zero_pos != None:
                break

        assert zero_pos != None

        if not move in self.MOVE_DIRS:
            raise Exception ("Illegal move name passed to forecast_move: {}".format(move))
       
        # compute new locations
        x, y = self.MOVE_DIRS[move]
        row, col = zero_pos
        row2, col2 = row + x, col + y
        
        if row2 < 0 or col2 < 0 or row2 >= self.rows or col2 >= self.cols:
            print("Impossible move passed") 
            return False
        else:
            self.tiles[row][col].val = self.tiles[row2][col2].val
            self.tiles[row2][col2].val = 0
            return True


