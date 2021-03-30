import abc
from constants import *
from board import *

class BaseComputer(abc.ABC):
    
    def __init__(self, max_velocity, border_size):
        self.max_velocity = max_velocity
        self.border_size  = border_size

    @abc.abstractmethod
    def makeMove(self, ball, player):
        pass


class ComputerPlayerHorizontalFollower(BaseComputer):

    def __init__(self, max_velocity, border_size):
        BaseComputer.__init__(self, max_velocity, border_size)

    def makeMove(self, ball, player):
        center = player.x_coord + player.BLOCK_LENGTH // 2
        
        if ball.x > center + 10:
            move ="RIGHT"
        elif ball.x < center - 10:
            move = "LEFT"
        else:
            return 1.0, None
        
        fraction = (((abs(center - ball.x) / (WIDTH / 2)) * 100 ) ** 1.3 ) / 100
        fraction = max(.10, fraction)
        fraction = min(1.0, fraction)

        return fraction, move


class ComputerPlayerHorizontalReverser(BaseComputer):

    def __init__(self, max_velocity, border_size):
        BaseComputer.__init__(self, max_velocity, border_size)

    def getX(self, x, y, vx, vy):
        pass
    
    def isNearHit(self, x, y, vx, vy, radius, block_height):
        if vy > 0:
            return y  + radius  + block_height> HEIGHT- 2 * self.border_size
        else:
            return y  - radius  - block_height < 2 * self.border_size


    def makeMove(self, ball, player):
        center = player.x_coord + player.BLOCK_LENGTH // 2

        near_hit = self.isNearHit(ball.x, ball.y, ball.xv, ball.yv, ball.RADIUS, player.BLOCK_HEIGHT)
        
        if near_hit:
            
            # reverse the ball to slow it down
            return 0.1, "LEFT" if ball.xv > 1 else "RIGHT"
        
        else:
            # Try to get in front of the ball        
            if ball.x > center + 10:
                move ="RIGHT"
            elif ball.x < center - 10:
                move = "LEFT"
            else:
                return 1.0, None
        
            return 1.0, move


class ComputerPlayerVerticalReverser(BaseComputer):

    def __init__(self, max_velocity, border_size):
        BaseComputer.__init__(self, max_velocity, border_size)

    def getX(self, x, y, vx, vy):
        pass
    
    def isNearHit(self, x, y, vx, vy, radius, block_height):
        if vx > 0:
            return x  + radius  + block_height > WIDTH - 2 * self.border_size
        else:
            return x  - radius  - block_height < 2 * self.border_size


    def makeMove(self, ball, player):
        center = player.y_coord + player.BLOCK_LENGTH // 2

        near_hit = self.isNearHit(ball.x, ball.y, ball.xv, ball.yv, ball.RADIUS, player.BLOCK_HEIGHT)
        
        if near_hit:
            
            # reverse the ball to slow it down
            return 0.1, "UP" if ball.yv > 1 else "DOWN"
        
        else:
            # Try to get in front of the ball        
            if ball.y > center + 10:
                move ="DOWN"
            elif ball.y < center - 10:
                move = "UP"
            else:
                return 1.0, None
        
            return 1.0, move




















