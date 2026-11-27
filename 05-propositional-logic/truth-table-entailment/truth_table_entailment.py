
from itertools import product


# Evaluate implication: P -> Q
def implies(p, q):
    return (not p) or q


# Check whether the Knowledge Base is true
def check_kb(p, q, r):
    sentence1 = implies(q, p)       # Q -> P
    sentence2 = implies(p, not q)  # P -> NOT Q
    sentence3 = q or r              # Q OR R

    return sentence1 and sentence2 and sentence3


# Truth Table Enumeration Algorithm
def tt_entails(query_function):
    symbols = ["P", "Q", "R"]

    print("\nTruth Table:")
    print("-" * 75)
    print("P\tQ\tR\tKB\tQuery")
    print("-" * 75)

    entailment = True

    # Generate all possible truth assignments
    for p, q, r in product([False, True], repeat=3):

        kb = check_kb(p, q, r)
        query = query_function(p, q, r)

        print(
            f"{p}\t{q}\t{r}\t{kb}\t{query}"
        )

        # Check query only when KB is true
        if kb and not query:
            entailment = False

    return entailment


# Queries
query1 = lambda p, q, r: r
query2 = lambda p, q, r: implies(r, p)
query3 = lambda p, q, r: implies(q, r)


# Main program
print("WEEK 6: PROPOSITIONAL LOGIC")
print("Knowledge Base:")
print("Q -> P")
print("P -> NOT Q")
print("Q OR R")

print("\nChecking KB entails R:")
print("Result:", tt_entails(query1))

print("\nChecking KB entails R -> P:")
print("Result:", tt_entails(query2))

print("\nChecking KB entails Q -> R:")
print("Result:", tt_entails(query3))
------
