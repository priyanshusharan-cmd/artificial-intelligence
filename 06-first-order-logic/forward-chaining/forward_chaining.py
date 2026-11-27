# First Order Logic - Forward Chaining (FOL-FC-ASK)
#
# Knowledge base (case study):
#   "As per the law, it is a crime for an American to sell weapons to
#    hostile nations. Country A, an enemy of America, has some missiles,
#    and all the missiles were sold to it by Robert, who is an American
#    citizen."
#   Prove: Criminal(Robert)
#
# Convention: identifiers starting with a lowercase letter are variables,
# identifiers starting with an uppercase letter are constants.

import re
from itertools import count


# ---------- Parsing and printing ----------

def parse_atom(text):
    """'Sells(Robert, x, A)' -> ('Sells', ('Robert', 'x', 'A'))"""
    match = re.fullmatch(r"\s*(\w+)\s*\((.*)\)\s*", text)
    if not match:
        raise ValueError(f"Invalid atom: {text}")
    name, args = match.groups()
    return name, tuple(a.strip() for a in args.split(","))


def parse_rule(text):
    """'A(x) & B(x) => C(x)' -> ([A(x), B(x)], C(x))"""
    premises, conclusion = text.split("=>")
    return ([parse_atom(p) for p in premises.split("&")],
            parse_atom(conclusion))


def show(atom):
    return f"{atom[0]}({', '.join(atom[1])})"


def is_variable(term):
    return term[0].islower()


# ---------- Unification ----------

def unify(x, y, theta):
    """Unify two atoms / terms and return the extended substitution."""
    if theta is None:
        return None
    if x == y:
        return theta
    if isinstance(x, str) and is_variable(x):
        return unify_var(x, y, theta)
    if isinstance(y, str) and is_variable(y):
        return unify_var(y, x, theta)
    if isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y):
        for a, b in zip(x, y):
            theta = unify(a, b, theta)
        return theta
    return None


def unify_var(var, value, theta):
    if var in theta:
        return unify(theta[var], value, theta)
    if isinstance(value, str) and value in theta:
        return unify(var, theta[value], theta)
    return {**theta, var: value}


def substitute(theta, atom):
    name, args = atom
    return name, tuple(theta.get(a, a) for a in args)


# ---------- Forward chaining ----------

_fresh = count(1)


def standardize(rule):
    """Rename the variables of a rule so they never clash."""
    premises, conclusion = rule
    n = next(_fresh)
    rename = lambda atom: (atom[0], tuple(
        f"{a}{n}" if is_variable(a) else a for a in atom[1]))
    return [rename(p) for p in premises], rename(conclusion)


def match_premises(premises, facts, theta):
    """Yield every substitution that satisfies all premises."""
    if not premises:
        yield theta
        return
    first, rest = premises[0], premises[1:]
    for fact in facts:
        new_theta = unify(first, fact, dict(theta))
        if new_theta is not None:
            yield from match_premises(rest, facts, new_theta)


def fol_fc_ask(facts, rules, query):
    known = list(facts)
    derived_from = {}             # fact -> (rule number, facts used)
    iteration = 0

    while True:
        iteration += 1
        new = []
        print(f"\nIteration {iteration}:")

        for number, rule in enumerate(rules, start=1):
            premises, conclusion = standardize(rule)

            for theta in match_premises(premises, known, {}):
                inferred = substitute(theta, conclusion)
                if inferred in known or inferred in new:
                    continue

                used = [substitute(theta, p) for p in premises]
                derived_from[inferred] = (number, used)
                new.append(inferred)
                print(f"  Rule {number}: {' & '.join(show(u) for u in used)}"
                      f"  =>  {show(inferred)}")

                if unify(inferred, query, {}) is not None:
                    known.extend(new)
                    return inferred, derived_from

        if not new:
            print("  No new facts can be inferred.")
            return None, derived_from

        known.extend(new)


def print_proof_tree(atom, derived_from, prefix="", last=True):
    connector = "" if prefix == "" and last else ("└── " if last else "├── ")
    if atom in derived_from:
        number, used = derived_from[atom]
        print(f"{prefix}{connector}{show(atom)}   [Rule {number}]")
        child_prefix = prefix + ("    " if last else "│   ")
        for i, child in enumerate(used):
            print_proof_tree(child, derived_from, child_prefix,
                             i == len(used) - 1)
    else:
        print(f"{prefix}{connector}{show(atom)}   [Fact]")


# ---------- Knowledge base ----------

FACTS = [
    "American(Robert)",
    "Enemy(A, America)",
    "Owns(A, T1)",          # Existential instantiation of: ∃x Owns(A,x) ∧ Missile(x)
    "Missile(T1)",
]

RULES = [
    "American(p) & Weapon(q) & Sells(p, q, r) & Hostile(r) => Criminal(p)",
    "Missile(x) & Owns(A, x) => Sells(Robert, x, A)",
    "Missile(x) => Weapon(x)",
    "Enemy(x, America) => Hostile(x)",
]

QUERY = "Criminal(Robert)"


def main():
    print("=" * 60)
    print(" FIRST ORDER LOGIC - FORWARD CHAINING")
    print("=" * 60)

    facts = [parse_atom(f) for f in FACTS]
    rules = [parse_rule(r) for r in RULES]
    query = parse_atom(QUERY)

    print("\nFacts:")
    for f in facts:
        print("  ", show(f))

    print("\nRules:")
    for i, r in enumerate(RULES, start=1):
        print(f"   {i}. {r}")

    print("\nQuery:", show(query))

    result, derived_from = fol_fc_ask(facts, rules, query)

    if result:
        print(f"\nQuery {show(query)} is PROVED.")
        print("\nProof Tree:")
        print_proof_tree(result, derived_from)
    else:
        print(f"\nQuery {show(query)} cannot be proved.")


if __name__ == "__main__":
    main()
