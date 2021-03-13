import pygame

# board parameters
WIDTH = 600
HEIGHT = 600 
INSTRUCTIONS_HEIGHT = 100
INSTRUCTIONS_BORDER_HEIGHT = 10
FPS = 60
GAME_NAME = "MAZE ESCAPE"
BASE_WIDTH = 20
BASE_HEIGHT = 20
LEVEL_BUMP = 5
MAZE_END_VAL = 3

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (128, 0, 0)
BLUE = (0, 0, 128)

# fonts
pygame.init() # to avoid font error
FONT1 = pygame.font.SysFont("comicsans", 30)


