from itertools import combinations

def cost(x):  # number of attacking pairs (same row or same diagonal)
    return sum(1 for i, j in combinations(range(len(x)), 2)
               if x[i] == x[j] or abs(x[i]-x[j]) == j-i)

def hill_climb(x):
    n = len(x)
    while True:
        cur = cost(x)
        print(f"\nCurrent {x}  cost = {cur}")
        best, best_cost, best_pair = None, cur, None
        for i, j in combinations(range(n), 2):        # (0,1),(0,2)... smallest pair first
            nb = x[:]
            nb[i], nb[j] = nb[j], nb[i]
            c = cost(nb)
            print(f"  swap(x{i},x{j}) -> {nb}  cost = {c}")
            if c < best_cost:                          # strict '<' keeps first (smallest) pair on ties
                best, best_cost, best_pair = nb, c, (i, j)
        if best is None:                               # no better neighbour
            return x
        print(f"  -> move to {best} (swap x{best_pair[0]},x{best_pair[1]}), cost {best_cost}")
        x = best

start = [3, 1, 2, 0]
result = hill_climb(start)
print(f"\nFinal {result}  cost = {cost(result)}",
      "-> GOAL" if cost(result) == 0 else "-> stuck at local minimum")
