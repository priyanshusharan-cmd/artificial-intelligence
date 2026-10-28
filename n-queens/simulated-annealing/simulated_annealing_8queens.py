import random, math
from itertools import combinations

def cost(x):  # number of attacking pairs
    return sum(1 for i, j in combinations(range(len(x)), 2)
               if x[i] == x[j] or abs(x[i]-x[j]) == j-i)

def neighbour(x):  # move one random queen to a random row
    nb = x[:]
    nb[random.randrange(len(x))] = random.randrange(len(x))
    return nb

def simulated_annealing(n=8, T=100.0, alpha=0.999, T_min=0.01):
    cur = [random.randrange(n) for _ in range(n)]
    while T > T_min and cost(cur) > 0:
        nxt = neighbour(cur)
        dE = cost(cur) - cost(nxt)                       # >0 means nxt is better
        if dE > 0 or random.random() < math.exp(dE / T):
            cur = nxt
        T *= alpha                                       # cool down
    return cur

sol = simulated_annealing()
print("Solution:", sol, "| cost =", cost(sol))
for r in range(8):
    print(' '.join('Q' if sol[c] == r else '.' for c in range(8)))
