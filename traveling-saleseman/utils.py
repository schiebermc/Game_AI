from math import sqrt
from typing import Tuple, List # necessary before 3.9

Point = Tuple[int, int]
Path = List[Point]

def distance(u: Point, v: Point) -> float:
    """ Computes the distance between two points """
    return sqrt((u[0] - v[0]) ** 2 + (u[1] - v[1]) ** 2)

def totalDistance(path: Path) -> float:
    """ Computes total distance traveled by this point-to-point path
        
        Args:
            path: point-to-point path a salesman will travel

        Returns:
            float: sum of distance travelled by the salesman on this route
    """
    return sum([distance(path[i], path[i+1]) for i in range(len(path)-1)])


