location = input("Enter Vacuum Location (A/B): ").upper()

roomA = input("Enter Room A state (Clean/Dirty): ").capitalize()
roomB = input("Enter Room B state (Clean/Dirty): ").capitalize()

print("\nInitial State")
print("Location:", location)
print("Room A:", roomA)
print("Room B:", roomB)

while roomA == "Dirty" or roomB == "Dirty":

    if location == "A":

        if roomA == "Dirty":
            print("\nSuck Dirt in Room A")
            roomA = "Clean"
        else:
            print("\nMove Right to Room B")
            location = "B"

    elif location == "B":

        if roomB == "Dirty":
            print("\nSuck Dirt in Room B")
            roomB = "Clean"
        else:
            print("\nMove Left to Room A")
            location = "A"

print("\nGoal Achieved!")
print("Room A:", roomA)
print("Room B:", roomB)
print("Both Rooms are Clean")
