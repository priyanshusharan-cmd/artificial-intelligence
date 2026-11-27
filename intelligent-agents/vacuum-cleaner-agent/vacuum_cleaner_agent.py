# Vacuum Cleaner Agent (two-room world: A and B)
#
# 1. Simple Reflex Agent : acts only on the current percept
#                          (location, status) using condition-action rules.
# 2. Goal Based Agent    : keeps an internal model of both rooms and acts
#                          until its goal (both rooms clean) is reached.


def simple_reflex_agent(percept):
    location, status = percept

    if status == "Dirty":
        return "Suck"
    elif location == "A":
        return "Right"
    else:
        return "Left"


def run_simple_reflex(location, rooms, steps=4):
    print("\n--- SIMPLE REFLEX AGENT ---")
    rooms = dict(rooms)

    for step in range(1, steps + 1):
        percept = (location, rooms[location])
        action = simple_reflex_agent(percept)
        print(f"Step {step}: Percept = {percept} -> Action = {action}")

        if action == "Suck":
            rooms[location] = "Clean"
        elif action == "Right":
            location = "B"
        else:
            location = "A"

    print("Final State:", rooms)
    print("(A reflex agent has no goal, so it keeps moving even after cleaning.)")


def goal_test(rooms):
    return all(status == "Clean" for status in rooms.values())


def run_goal_based(location, rooms):
    print("\n--- GOAL BASED AGENT ---")
    print("Goal: Room A = Clean and Room B = Clean")
    rooms = dict(rooms)
    cost = 0
    step = 0

    while not goal_test(rooms):
        step += 1

        if rooms[location] == "Dirty":
            action = "Suck"
            rooms[location] = "Clean"
        else:
            # Move only towards a room that is still dirty
            action = "Right" if location == "A" else "Left"
            location = "B" if location == "A" else "A"

        cost += 1
        print(f"Step {step}: Action = {action:<5} | Location = {location} | "
              f"A = {rooms['A']}, B = {rooms['B']}")

    print("Goal Achieved! Both rooms are clean.")
    print("Total actions (path cost):", cost)


def read_state():
    location = input("Enter Vacuum Location (A/B): ").strip().upper()
    room_a = input("Enter Room A state (Clean/Dirty): ").strip().capitalize()
    room_b = input("Enter Room B state (Clean/Dirty): ").strip().capitalize()

    if location not in ("A", "B") or {room_a, room_b} - {"Clean", "Dirty"}:
        raise ValueError("Location must be A/B and states must be Clean/Dirty.")

    return location, {"A": room_a, "B": room_b}


def main():
    print("VACUUM CLEANER AGENT")
    location, rooms = read_state()

    print("\nInitial State")
    print("Location:", location)
    print("Room A:", rooms["A"])
    print("Room B:", rooms["B"])

    run_simple_reflex(location, rooms)
    run_goal_based(location, rooms)


if __name__ == "__main__":
    main()
