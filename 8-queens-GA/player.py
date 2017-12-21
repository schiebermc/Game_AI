# 8-queens solver with genetic algorithm implementation
# creature class, population class

from random import randint # for initialization, breeding, and mutations
from numpy.random import choice


class creature(object):
    
    def __init__(self, n, pos=None):
        self.n = n
        
        if(pos):
            # init queens to pos
            self.pos = pos
        else:    
            # initialize queens to random positions
            self.pos = []
            for i in range(self.n):
                self.pos.append(randint(0, self.n-1))
            
        self.board = [['_' for i in range(self.n)] for j in range(self.n)]
        for i in range(self.n):
            self.board[i][self.pos[i]] = 'Q'

    def fitness(self):
        count = 0
        for i in range(self.n):
            for j in range(self.n):
                if(self.board[i][j] == 'Q'):
                    for move_type in range(1, 9):
                        count += self.move(move_type, i, j)
        return int(28 - count)


    def move(self, move_type, row, col):
        if(move_type == 1):
            col += 1
        elif(move_type == 2):
            col += 1
            row += 1
        elif(move_type == 3):
            row += 1
        elif(move_type == 4):
            col -= 1
            row += 1
        elif(move_type == 5):
            col -= 1
        elif(move_type == 6):
            col -= 1
            row -= 1
        elif(move_type == 7):
            row -= 1
        else:
            col += 1
            row -= 1
            
        # check if this move goes off the board
        if(col == self.n or row == self.n or col < 0 or row < 0):
            return 0
       
        # does it hit another queen?
        val = 0.0
        if(self.board[row][col] == 'Q'):
            val += 0.5
        
        return val + self.move(move_type, row, col)

    def visualize_board(self):
        for i in self.board:
            print (i)

    def get_pos(self):
        return self.pos

class population(object):

    def __init__(self, n, board_size, mutation_rate, creatures=None):
        self.pop = []
        self.n = n
        self.mutation_rate = mutation_rate
        self.nsurvivors = n // 2
        self.board_size = board_size
        self.fitness = []

        if(creatures):
            for i in range(self.n):
                self.pop.append(creature(self.board_size, creatures[i]))
        else:
            for i in range(self.n):
                self.pop.append(creature(self.board_size))

    def rank_fitness(self):
        self.fitness = []
        for i in range(self.n):
            val = self.pop[i].fitness()
            self.fitness.append((val, i)) 
        self.fitness.sort(key=lambda x: x[0])        
 
    def choose_survivors(self):
            
        # get relative fitnesses
        self.rank_fitness()
        fitness_net = [0] * self.n
        for i in range(self.n):
            fitness_net[self.fitness[i][1]] = self.fitness[i][0]
        sum_fitnesses = float(sum(fitness_net))
        
        # get sampling distro
        survival_distro = [0.0] * self.n
        for i in range(self.n):
            survival_distro[i] = fitness_net[i] / sum_fitnesses
        
        return survival_distro   
 
    def breed(self, survival_distro):

        new_pop = []
        for i in range(self.n):
            parents = choice(self.n, 2, replace=False, p=survival_distro)
            self.breed_child(new_pop, self.pop[parents[0]].get_pos(), self.pop[parents[1]].get_pos())    
        self.pop = new_pop

    def breed_child(self, pop, a, b):
        
        # cross
        trait_split = randint(2,6)
        pos1 = [0] * self.board_size
        pos2 = [0] * self.board_size
        for i in range(self.board_size):
            if(i < trait_split):
                pos1[i] = a[i]
                pos2[i] = b[i]
            else:
                pos1[i] = b[i]
                pos2[i] = a[i] 

        # mutate
        self.mutate(pos1) 
        self.mutate(pos2) 
        
        # add children to population
        pop.append(creature(self.board_size, pos1))
        pop.append(creature(self.board_size, pos2)) 
        
        return
    
    def mutate(self, pos):
        mutate = choice(2, 1, p=[1.0-self.mutation_rate, self.mutation_rate])[0]
        if(mutate):
            ind = randint(0,7)
            val = randint(0,7)
            pos[ind] = val

    def solve(self, niters):
        
        # setup ~ 
        niter = 0
        worst = []
        median = []
        best = []        

        while(niter < niters):
            
            # kill off the weak
            survival_distro = self.choose_survivors()
            self.visualize_boards()

            # record fitness
            worst.append(self.get_worst()[0])
            median.append(self.get_median()[0])
            best.append(self.get_best()[0])
                
            # breed
            self.breed(survival_distro)

            print(niter, worst[-1])
            niter += 1
   
        return worst, median, best
 
    def get_worst(self):
        return self.fitness[0]

    def get_median(self):
        return self.fitness[self.nsurvivors]

    def get_best(self):
        return self.fitness[-1]

    def visualize_boards(self):
        pass
        # visualize worst, median, best
        #print("worst ~ ", self.fitness[0])
        #self.pop[self.worst].visualize_board() 
        #print("")
        #print("median ~ ", self.fitness[self.nsurvivors])
        #self.pop[self.median].visualize_board() 
        #print("")
        #print("best ~ ", self.fitness[-1])
        #self.pop[self.best].visualize_board() 
        #print("")


