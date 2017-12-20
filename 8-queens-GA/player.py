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
        if(self.board[row][col] == 'Q'):
            return 0.5
        else:
            return self.move(move_type, row, col)

    def visualize_board(self):
        for i in self.board:
            print (i)

    def get_pos(self):
        return self.pos

class population(object):

    def __init__(self, n, board_size, mutation_rate):
        self.pop = []
        self.n = n
        self.mutation_rate = mutation_rate
        self.nsurvivors = n // 2
        self.board_size = board_size

        for i in range(self.n):
            self.pop.append(creature(self.board_size))
        self.fitness = []

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
            new_pop.append(self.breed_child(self.pop[parents[0]].get_pos(), self.pop[parents[1]].get_pos()))    
        self.pop = new_pop

    def breed_child(self, a, b):
        
        # determine crossover traits
        from_a = choice(self.board_size, self.board_size // 2, replace=False)
        from_b = range(8)
        for i in from_a:
            from_b.remove(i)
        ind = [0] * self.board_size
        for i in range(self.board_size):
            ind[i] = 1 if (i in from_a) else 0
        
        # cross
        pos = [0] * self.board_size
        for i in range(self.board_size):
            pos[i] = a[i] if ind[i] else b[i]

        # mutate
        for i in range(self.board_size):
            mutate = choice(2, 1, replace=False, p=[self.mutation_rate, 1.0-self.mutation_rate])[0]
            if(mutate):
                val = randint(0, 7)
                pos[i] = val
        
        self.pop.append(creature(self.board_size))
        return creature(self.board_size, pos=pos)

    def solve(self):
        
        m = 1000
        niter = 0
        while(niter < m):
            # kill off the weak
            survival_distro = self.choose_survivors()

            # breed
            self.breed(survival_distro)

            niter += 1
            self.visualize_boards()
            print("niter: ", niter, " ~~~~~~~~~~~~~~~~~~~~")
    
    def visualize_boards(self):
        
        # get info
        self.median = self.fitness[self.nsurvivors][1]
        self.best   = self.fitness[-1][1]
        self.worst  = self.fitness[0][1]
       
        # visualize worst, median, best
        #print("worst ~ ", self.fitness[0])
        #self.pop[self.worst].visualize_board() 
        #print("")
        #print("median ~ ", self.fitness[self.nsurvivors])
        #self.pop[self.median].visualize_board() 
        #print("")
        print("best ~ ", self.fitness[-1])
        #self.pop[self.best].visualize_board() 
        #print("")


pop = population(10, 8, 0.0001)
pop.solve()



