# import pygame library 
import pygame 
import time
from random import shuffle, seed, sample
  
WIDTH = 600
HEIGHT = 600 

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 60

pygame.display.set_caption("N-Puzzle")

# to avoid font error
pygame.init()

class Tile:

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

    def __init__(self, n):
        
        self.board = [i for i in range(n*n)]
        shuffle(self.board)
        self.rows = n
        self.cols = n
        
        # inner borders
        self.inner_width  = WIDTH - 2 * self.OUTER_BORDER_SIZE -  (self.cols - 1) * self.INNER_BORDER_SIZE
        self.inner_height = HEIGHT - 2 * self.OUTER_BORDER_SIZE - (self.rows - 1) * self.INNER_BORDER_SIZE
        self.tile_width = self.inner_width / self.cols
        self.tile_height = self.inner_height / self.rows
        
        self.tiles = []
        for row in range(self.rows):
            self.tiles.append([])
            for col in range(self.cols):
                self.tiles[row].append(Tile(self.board[row*self.cols + col], 
                    self.OUTER_BORDER_SIZE + col * (self.tile_width + self.INNER_BORDER_SIZE),
                    self.OUTER_BORDER_SIZE + row * (self.tile_height + self.INNER_BORDER_SIZE), self.tile_width, self.tile_height))


    def draw(self, window):
        window.fill(WHITE)
        
        # horizontal outer borders
        pygame.draw.rect(window, BLACK, (0, 0, WIDTH, self.OUTER_BORDER_SIZE)) 
        pygame.draw.rect(window, BLACK, (0, HEIGHT - self.OUTER_BORDER_SIZE, WIDTH, self.OUTER_BORDER_SIZE)) 
        
        # vertical outer borders
        pygame.draw.rect(window, BLACK, (0, 0, self.OUTER_BORDER_SIZE, HEIGHT))
        pygame.draw.rect(window, BLACK, (WIDTH - self.OUTER_BORDER_SIZE, 0, self.OUTER_BORDER_SIZE, HEIGHT))
 
        for col in range(1, self.cols):
            pygame.draw.rect(window, BLACK, (self.OUTER_BORDER_SIZE + col * self.tile_width + (col-1) * self.INNER_BORDER_SIZE, 0, self.INNER_BORDER_SIZE, HEIGHT)) 
            
        for row in range(1, self.rows):
            pygame.draw.rect(window, BLACK, (0, self.OUTER_BORDER_SIZE + row * self.tile_height + (row-1) * self.INNER_BORDER_SIZE, WIDTH, self.INNER_BORDER_SIZE)) 

        for row in range(self.rows):
            for col in range(self.cols):
                self.tiles[row][col].draw_tile(window) 


    def forecast_move(self, move):
        
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

def AStarHeuristic(tiles):
    # returns sum of manhattan distances to the correct locations
    d = {}
    n = len(tiles)
    for i in range(n):
        for j in range(n):
            val = tiles[i][j].val
            d[val] = (i, j)

    summ = 0
    for val in range(n * n):
        row_diff = abs(val // n - d[val][0]) * (val // n)
        col_diff = abs(val %  n - d[val][1]) * (val % n)
        summ += row_diff + col_diff
    return summ


from functools import reduce
from copy import deepcopy
from heapq import heappush, heappop
class Solver:
    
    def __init__(self, board):
        self.board = board
        
    def get_tile_tup(self, board):
        tup = []
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                tup.append(board.tiles[row][col].val)
        tup = tuple(tup)
        return tup    
    
    def get_solution(self):
        
        f = [((AStarHeuristic(self.board.tiles), [], deepcopy(self.board)))]
        visited = set([])
        while(len(f) > 0):

            h, path, board = heappop(f)

            print(h)
            if h == 0:
                return path

            tup = self.get_tile_tup(board)
            if tup in visited:
                continue
            visited.add(tup)
 
            for move in ["RIGHT", "LEFT", "UP", "DOWN"]:
                new_board = deepcopy(board)
                if new_board.forecast_move(move) and not self.get_tile_tup(new_board) in visited:
                    new_h = AStarHeuristic(new_board.tiles)
                    heappush(f, (new_h, path + [move], new_board))


def main():

    run = True
    clock = pygame.time.Clock()
    board = Board(4)
    
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
                    print("Automatic solve invoked..")
                    solver = Solver(board)
                    moves = solver.get_solution()
                    for ind, move in enumerate(moves):
                        print("Move {} of {}".format(ind, len(moves)))
                        board.forecast_move(move)
                        board.draw(WIN)
                        pygame.display.update()
                        time.sleep(0.5)
                else:
                    print(event.type)
            else:
                pass
        
        board.draw(WIN)
        pygame.display.update()


    pygame.quit()

        

if __name__ == "__main__":
    main()

 
