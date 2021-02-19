import itertools
from math import sqrt
import numpy as np
from typing import Tuple, List # necessary before 3.9
import matplotlib.pyplot as plt

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


def printDistanceAndPlot(path: Path, solver_name: str, 
        test_name: str, total_time: float, figname: str=None) -> None:
    """ computes distance and produces a plot of a path
        
        Args:
            path: point-to-point path a salesman will travel
            solver_name: name of algorithm used to produce this path
            test_name: name of test set
            total_time: total time for computing path 
            figname: filename used to save plot, if any

    """

    # total distance
    total_distance = totalDistance(path)

    # plot and show
    plt.plot(*np.asarray(path).T, marker='s')
    plt.title("Path Traveled Using Algorithm: {}\nTest Set Name: {}\nTotal Distance: {} - Time: {:0.3e}".\
        format(solver_name, test_name, round(total_distance, 2), total_time))
    
    plt.tight_layout()
    if figname:
        plt.savefig(figname)
   
     
    plt.show()



def generate_groups(lst, n=2):
    if not lst:
        yield []
    else:
        for group in (((lst[0],) + xs) for xs in itertools.combinations(lst[1:], n-1)):
            for groups in generate_groups([x for x in lst if x not in group], n):
                yield [group] + groups



