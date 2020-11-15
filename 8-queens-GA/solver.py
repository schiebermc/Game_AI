# 8-queens solver with genetic algorithm implementation
# solver

import matplotlib.pyplot as plt
from player import creature, population

niters = 200
pop = population(300, 8, 0.001)
worst, medians, best = pop.solve(niters)

x = [_ for _ in range(niters)]
plt.plot(x, worst, 'r--', medians, 'bs', best, 'g^')
plt.legend()
plt.show()

