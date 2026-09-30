# 8 Puzzle using DFS

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


def dfs(start, goal):
    stack = [(start, [start])]
    visited = {start}

    while stack:
        current, path = stack.pop()

        if current == goal:
            return path

        neighbors = get_neighbors(current)

        # Check immediate goal first
        for neighbor in neighbors:
            if neighbor == goal:
                return path + [neighbor]

        for neighbor in reversed(neighbors):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))

    return None


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

solution = dfs(start, goal)

if solution:
    print("Goal Found!")
    print("Number of moves:", len(solution) - 1)

    for step, state in enumerate(solution):
        print("\nStep", step)
        print_state(state)

else:
    print("No solution found.")
