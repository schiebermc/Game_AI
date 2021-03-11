
from board import *
from solvers import *
from collections import namedtuple

TestSet = namedtuple("TestSet", ["n", "board"])

###############################################################################
###### Test Sets ##############################################################
###############################################################################

# n = 3
test_set1 = TestSet(3, [7, 1, 2, 4, 5, 8, 3, 6, 0]) 
test_set2 = TestSet(3, [7, 0, 2, 1, 4, 8, 5, 3, 6])
test_set3 = TestSet(3, [6, 0, 5, 8, 2, 1, 3, 7, 4])
test_set4 = TestSet(3, [0, 3, 4, 5, 6, 2, 7, 1, 8])

# n = 4
test_set5 = TestSet(4, [1, 9, 2, 10, 11, 7, 4, 6, 13, 5, 3, 15, 0, 8, 14, 12])
test_set6 = TestSet(4, [5, 1, 11, 15, 4, 3, 10, 14, 13, 9, 2, 6, 7, 12, 8, 0])

test_sets_to_use = [test_set5, test_set6]
solvers_to_use = [
                    (UnidirectionalSolver, AStarManhattanHeuristic),
                    (UnidirectionalSolver, AStarManhattanHeuristicOuterEmphasis)
                 ]

names = {}
stats = [[0, 0] for i in range(len(solvers_to_use))]
for test_set in test_sets_to_use:
    
    board = Board(test_set.n, test_set.board, random_shifts=0, board_prints=False)
    
    for ind, solver_and_heuristic in enumerate(solvers_to_use):
        
        solver = solver_and_heuristic[0](board, solver_and_heuristic[1])
        names[ind] = solver.name()

        num_visited, moves = solver.get_solution()
        num_moves = len(moves)
        
        stats[ind][0] += num_moves
        stats[ind][1] += num_visited

total_tests = len(test_sets_to_use)

print("\n\nFinal Testing Results:")
for i in range(len(solvers_to_use)):
    print("Solver Name: {}".format(names[i]))
    print("Average path size: {}, Average nodes visited: {}\n", \
            stats[i][0] / total_tests, stats[i][1] / total_tests)

         



