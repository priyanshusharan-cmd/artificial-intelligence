# Alpha-Beta Pruning on a game tree (root is a MAX node)
#
# alpha = best value MAX can guarantee so far (lower bound)
# beta  = best value MIN can guarantee so far (upper bound)
# A branch is pruned as soon as alpha >= beta.

import math
from itertools import count
from string import ascii_uppercase

# Game tree from the lab PPT: MAX -> MIN -> MAX -> leaves
DEFAULT_LEAVES = [10, 9, 14, 18, 5, 4, 50, 3]


class Node:
    def __init__(self, name, children=None, value=None):
        self.name = name
        self.children = children or []
        self.value = value

    def is_leaf(self):
        return not self.children


def build_tree(leaves, branching=2):
    """Build a complete tree bottom-up and name internal nodes A, B, C..."""
    level = [Node(str(v), value=v) for v in leaves]
    levels = []
    while len(level) > 1:
        level = [Node("", level[i:i + branching])
                 for i in range(0, len(level), branching)]
        levels.append(level)

    names = (ascii_uppercase[i] if i < 26 else f"N{i - 25}" for i in count())
    for lvl in reversed(levels):            # root gets 'A'
        for node in lvl:
            node.name = next(names)
    return level[0]


def fmt(x):
    if x == math.inf:
        return "+inf"
    if x == -math.inf:
        return "-inf"
    return str(x)


def leaves_under(node):
    if node.is_leaf():
        return [node.value]
    return [v for c in node.children for v in leaves_under(c)]


pruned = []


def alpha_beta(node, alpha, beta, maximizing, depth=0):
    pad = "    " * depth
    if node.is_leaf():
        print(f"{pad}Leaf {node.value}")
        return node.value, [node.name]

    role = "MAX" if maximizing else "MIN"
    print(f"{pad}{node.name} ({role})  alpha = {fmt(alpha)}, beta = {fmt(beta)}")

    best = -math.inf if maximizing else math.inf
    best_path = []

    for i, child in enumerate(node.children):
        value, path = alpha_beta(child, alpha, beta, not maximizing, depth + 1)

        if (maximizing and value > best) or (not maximizing and value < best):
            best, best_path = value, path

        if maximizing:
            if best > alpha:
                alpha = best
                print(f"{pad}  {node.name}: alpha updated to {fmt(alpha)}")
        else:
            if best < beta:
                beta = best
                print(f"{pad}  {node.name}: beta updated to {fmt(beta)}")

        if alpha >= beta:
            rest = node.children[i + 1:]
            if rest:
                for r in rest:
                    cut = f"{r.name} {leaves_under(r)}" if not r.is_leaf() else r.name
                    pruned.append(cut)
                    print(f"{pad}  alpha ({fmt(alpha)}) >= beta ({fmt(beta)})"
                          f" -> PRUNE {cut}")
            break

    print(f"{pad}{node.name} returns {fmt(best)}")
    node.value = best
    return best, [node.name] + best_path


def print_tree(node, prefix="", last=True, root=True, maximizing=True):
    connector = "" if root else ("└── " if last else "├── ")
    if node.is_leaf():
        print(f"{prefix}{connector}{node.value}")
        return
    role = "MAX" if maximizing else "MIN"
    print(f"{prefix}{connector}{node.name} ({role})")
    child_prefix = prefix if root else prefix + ("    " if last else "│   ")
    for i, c in enumerate(node.children):
        print_tree(c, child_prefix, i == len(node.children) - 1, False,
                   not maximizing)


def read_leaves():
    text = input("Enter leaf values separated by spaces "
                 "(press Enter for the PPT example): ").strip()
    if not text:
        return DEFAULT_LEAVES
    leaves = [int(v) for v in text.split()]
    n = len(leaves)
    if n < 2 or n & (n - 1):
        raise ValueError("Number of leaves must be a power of 2 (binary tree).")
    return leaves


def main():
    print("=" * 50)
    print(" ALPHA-BETA PRUNING")
    print("=" * 50)

    leaves = read_leaves()
    root = build_tree(leaves)

    print("\nGame Tree:")
    print_tree(root)

    print("\nAlpha-Beta Search Trace:")
    value, path = alpha_beta(root, -math.inf, math.inf, True)

    print("\nResult")
    print("Value of root (MAX) node :", value)
    print("Best path from root      :", " -> ".join(path))
    print("Pruned branches          :", ", ".join(pruned) if pruned else "None")


if __name__ == "__main__":
    main()
