import heapq


def input_state(name):
    print(f"\nEnter {name} State:")

    state = []

    for i in range(3):
        row = list(map(int, input(f"Row {i + 1}: ").split()))
        state.extend(row)

    return tuple(state)


def print_state(state):
    for i in range(0, 9, 3):
        print(*state[i:i + 3])


def manhattan_distance(state, goal):
    distance = 0

    for tile in range(9):
        current_position = state.index(tile)
        goal_position = goal.index(tile)

        current_row = current_position // 3
        current_col = current_position % 3

        goal_row = goal_position // 3
        goal_col = goal_position % 3

        distance += (
            abs(current_row - goal_row)
            +
            abs(current_col - goal_col)
        )

    return distance


def generate_children(state):
    children = []

    blank = state.index(0)

    row = blank // 3
    col = blank % 3

    moves = [
        (-1, 0, "UP"),
        (1, 0, "DOWN"),
        (0, -1, "LEFT"),
        (0, 1, "RIGHT")
    ]

    for dr, dc, move in moves:
        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_position = new_row * 3 + new_col

            new_state = list(state)

            new_state[blank], new_state[new_position] = (
                new_state[new_position],
                new_state[blank]
            )

            children.append((tuple(new_state), move))

    return children


def a_star(initial, goal):
    open_list = []

    h = manhattan_distance(initial, goal)

    heapq.heappush(open_list, (h, 0, initial))

    parent = {initial: None}
    move_used = {initial: "START"}
    g_value = {initial: 0}

    nodes_expanded = 0

    while open_list:
        f, g, current = heapq.heappop(open_list)

        if g != g_value[current]:
            continue

        if current == goal:
            path = []

            while current is not None:
                path.append((current, move_used[current]))
                current = parent[current]

            path.reverse()

            return path, nodes_expanded

        nodes_expanded += 1

        for child, move in generate_children(current):
            new_g = g + 1

            if child not in g_value or new_g < g_value[child]:
                g_value[child] = new_g
                parent[child] = current
                move_used[child] = move

                h = manhattan_distance(child, goal)
                f = new_g + h

                heapq.heappush(
                    open_list,
                    (f, new_g, child)
                )

    return None, nodes_expanded


def display_solution(path, goal, nodes_expanded):
    print("\nA* Search Solution")
    print("Manhattan Distance Heuristic")

    moves = []

    for step, (state, move) in enumerate(path):
        g = step
        h = manhattan_distance(state, goal)
        f = g + h

        print(f"\nStep {step}")
        print("Move:", move)
        print("g(n) =", g)
        print("h(n) =", h)
        print("f(n) =", f)

        print_state(state)

        if move != "START":
            moves.append(move)

    print("\nResult")
    print("Goal State Reached: YES")
    print("Solution Depth:", len(path) - 1)
    print("Nodes Expanded:", nodes_expanded)
    print("Solution Path:", " -> ".join(moves))


def main():
    print("8-Puzzle using A* Search")
    print("Manhattan Distance Heuristic")
    print("Use 0 for the blank space.")

    initial = input_state("Initial")
    goal = input_state("Goal")

    print("\nInitial State:")
    print_state(initial)

    print("\nGoal State:")
    print_state(goal)

    path, nodes_expanded = a_star(initial, goal)

    if path:
        display_solution(path, goal, nodes_expanded)
    else:
        print("\nNo solution found.")


if __name__ == "__main__":
    main()
