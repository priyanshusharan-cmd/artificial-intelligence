# 8 Puzzle using IDS
# Iterative Deepening Search

def print_state(state):
    for i in range(0, 9, 3):
        print(state[i], state[i + 1], state[i + 2])
    print()


def get_neighbors(state):
    neighbors = []

    zero = state.index(0)
    row = zero // 3
    col = zero % 3

    moves = [
        (-1, 0),  # Up
        (1, 0),   # Down
        (0, -1),  # Left
        (0, 1)    # Right
    ]

    for dr, dc in moves:
        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < 3 and 0 <= new_col < 3:

            new_pos = new_row * 3 + new_col

            new_state = list(state)

            new_state[zero], new_state[new_pos] = \
                new_state[new_pos], new_state[zero]

            neighbors.append(tuple(new_state))

    return neighbors



# A state can reach the goal only if both have the same
# inversion-count parity (blank tile ignored)
def is_solvable(start, goal):
    def inversions(state):
        tiles = [t for t in state if t != 0]
        return sum(1 for i in range(len(tiles))
                   for j in range(i + 1, len(tiles))
                   if tiles[i] > tiles[j])

    return inversions(start) % 2 == inversions(goal) % 2


def dls(current, goal, limit, path):

    if current == goal:
        return path

    if limit == 0:
        return None

    for neighbor in get_neighbors(current):

        if neighbor not in path:

            result = dls(
                neighbor,
                goal,
                limit - 1,
                path + [neighbor]
            )

            if result is not None:
                return result

    return None


def ids(start, goal):

    depth = 0

    while True:

        print("Searching at depth:", depth)

        result = dls(
            start,
            goal,
            depth,
            [start]
        )

        if result is not None:
            return result

        depth += 1


def enter_state(name):

    print("\nEnter", name, "State:")

    state = []

    for i in range(3):

        row = list(
            map(
                int,
                input("Enter row " + str(i + 1) + ": ").split()
            )
        )

        state.extend(row)

    return tuple(state)


# Main Program

start = enter_state("Initial")
goal = enter_state("Goal")

print("\nInitial State:")
print_state(start)

print("Goal State:")
print_state(goal)

if not is_solvable(start, goal):
    print("This puzzle is not solvable (inversion parity differs).")
    raise SystemExit

print("Searching using IDS...\n")

solution = ids(start, goal)

if solution:

    print("\nGoal Found!")
    print("Number of moves:", len(solution) - 1)

    for step, state in enumerate(solution):

        print("\nStep", step)
        print_state(state)

else:

    print("No solution found.")
