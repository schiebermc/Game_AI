# 8-queens solver with genetic algorithm implementation
# solver

import matplotlib.pyplot as plt
from player import creature, population

niters = 200
pop = population(100, 8, 0.001, niters)
worst, medians, best = pop.solve()

x = [_ for _ in range(niters)]
plt.plot(x, worst, 'r--', medians, 'bs', best, 'g^')
plt.legend()
plt.show()

