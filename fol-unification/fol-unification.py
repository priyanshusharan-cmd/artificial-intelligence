
from dataclasses import dataclass
import re


# Variables used in First Order Logic
# Other single-letter symbols like 'a' are treated as constants.
VARIABLES = {
    "x", "y", "z", "u", "v", "w",
    "X", "Y", "Z", "U", "V", "W"
}


# Representation of a predicate, function or constant
@dataclass(frozen=True)
class Term:
    symbol: str
    args: tuple = ()


# Split arguments while considering nested functions
def split_arguments(text):
    if not text.strip():
        return []

    result = []
    start = 0
    depth = 0

    for i, ch in enumerate(text):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                raise ValueError("Unbalanced parentheses.")
        elif ch == "," and depth == 0:
            part = text[start:i].strip()
            if not part:
                raise ValueError("Empty argument.")
            result.append(part)
            start = i + 1

    if depth != 0:
        raise ValueError("Unbalanced parentheses.")

    last = text[start:].strip()
    if not last:
        raise ValueError("Empty argument.")

    result.append(last)
    return result


# Convert input expression into a Term
def parse_term(text):
    text = text.strip()

    if not text:
        raise ValueError("Expression cannot be empty.")

    open_index = text.find("(")

    # Constant or variable
    if open_index == -1:
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", text):
            raise ValueError(f"Invalid symbol: {text}")
        return Term(text)

    # Predicate or function
    if not text.endswith(")"):
        raise ValueError(f"Invalid expression: {text}")

    name = text[:open_index].strip()

    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", name):
        raise ValueError(f"Invalid predicate/function name: {name}")

    inner = text[open_index + 1:-1].strip()

    args = tuple(
        parse_term(part)
        for part in split_arguments(inner)
    )

    return Term(name, args)


# Check whether a term is a variable
def is_variable(term):
    return not term.args and term.symbol in VARIABLES


# Apply substitutions to an expression
def apply_substitution(term, substitutions):
    if is_variable(term) and term.symbol in substitutions:
        return apply_substitution(
            substitutions[term.symbol], substitutions
        )

    return Term(
        term.symbol,
        tuple(
            apply_substitution(arg, substitutions)
            for arg in term.args
        )
    )


# Occurs check
def occurs(variable, term, substitutions):
    term = apply_substitution(term, substitutions)

    if is_variable(term):
        return term.symbol == variable

    return any(
        occurs(variable, arg, substitutions)
        for arg in term.args
    )


# Add a new substitution
def extend_substitution(variable, value, substitutions):
    value = apply_substitution(value, substitutions)

    if occurs(variable.symbol, value, substitutions):
        return None

    updated = dict(substitutions)
    updated[variable.symbol] = value

    # Apply the new substitution to existing substitutions
    for key in list(updated):
        updated[key] = apply_substitution(
            updated[key], updated
        )

    return updated


# Main Unification Algorithm
def unify(first, second, substitutions=None):

    if substitutions is None:
        substitutions = {}

    first = apply_substitution(first, substitutions)
    second = apply_substitution(second, substitutions)

    # Step 1: If both expressions are identical
    if first == second:
        return substitutions

    # Step 2: Handle variables
    if is_variable(first):
        return extend_substitution(first, second, substitutions)

    if is_variable(second):
        return extend_substitution(second, first, substitutions)

    # Step 3: Check predicate/function symbols
    if first.symbol != second.symbol:
        return None

    # Step 4: Check number of arguments
    if len(first.args) != len(second.args):
        return None

    # Step 5: Recursively unify corresponding arguments
    for arg1, arg2 in zip(first.args, second.args):

        substitutions = unify(
            arg1, arg2, substitutions
        )

        if substitutions is None:
            return None

    # Step 6: Return substitution set
    return substitutions


# Convert Term into readable expression
def format_term(term):
    if not term.args:
        return term.symbol

    args = ", ".join(
        format_term(arg) for arg in term.args
    )

    return f"{term.symbol}({args})"


# Main program
def main():

    print("=" * 45)
    print(" FIRST ORDER LOGIC - UNIFICATION")
    print("=" * 45)

    expression1 = input("\nEnter first expression: ")
    expression2 = input("Enter second expression: ")

    try:
        term1 = parse_term(expression1)
        term2 = parse_term(expression2)

        substitutions = unify(term1, term2)

        print("\n--- UNIFICATION RESULT ---")

        if substitutions is None:
            print("Unification FAILED!")

        else:
            if substitutions:
                print("\nSubstitution Set:")
                for variable, value in substitutions.items():
                    print(f"{variable} = {format_term(value)}")
            else:
                print("\nSubstitution Set: NIL")

            # Apply substitutions to both expressions
            result1 = apply_substitution(term1, substitutions)
            result2 = apply_substitution(term2, substitutions)

            print("\nUnified Expression 1:",
                  format_term(result1))

            print("Unified Expression 2:",
                  format_term(result2))

            print("\nUnification SUCCESSFUL!")

    except ValueError as error:
        print("Invalid input:", error)


if __name__ == "__main__":
    main()
