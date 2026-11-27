# First Order Logic - Resolution (proof by refutation)
#
# Steps:
#   1. Convert every KB sentence to Conjunctive Normal Form (CNF)
#        a. eliminate  <=>  and  =>
#        b. move  ~  inwards
#        c. standardize variables
#        d. skolemize (remove  exists)
#        e. drop  forall
#        f. distribute  |  over  &
#   2. Negate the query and add it to the clause set
#   3. Resolve pairs of clauses until the empty clause {} is derived
#   4. If {} is derived the query is proved
#
# Syntax:  ~ not   & and   | or   => implies   <=> iff
#          forall x (...)   exists x (...)
# Identifiers starting with lowercase are variables, uppercase are constants.

import re
import heapq
from itertools import count


# ======================= Parsing =======================

TOKEN = re.compile(r"\s*(<=>|=>|forall|exists|[A-Za-z_]\w*|[~&|(),])")


def tokenize(text):
    pos, tokens = 0, []
    text = text.strip()
    while pos < len(text):
        m = TOKEN.match(text, pos)
        if not m:
            raise ValueError(f"Unexpected character at: {text[pos:]}")
        tokens.append(m.group(1))
        pos = m.end()
    return tokens


class Parser:
    def __init__(self, text):
        self.tokens = tokenize(text)
        self.i = 0

    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def take(self, expected=None):
        tok = self.peek()
        if expected and tok != expected:
            raise ValueError(f"Expected {expected!r} but found {tok!r}")
        self.i += 1
        return tok

    def parse(self):
        f = self.iff()
        if self.peek() is not None:
            raise ValueError(f"Unexpected token {self.peek()!r}")
        return f

    def iff(self):
        left = self.implies()
        while self.peek() == "<=>":
            self.take()
            left = ("iff", left, self.implies())
        return left

    def implies(self):
        left = self.disj()
        if self.peek() == "=>":
            self.take()
            return ("imp", left, self.implies())
        return left

    def disj(self):
        left = self.conj()
        while self.peek() == "|":
            self.take()
            left = ("or", left, self.conj())
        return left

    def conj(self):
        left = self.unary()
        while self.peek() == "&":
            self.take()
            left = ("and", left, self.unary())
        return left

    def unary(self):
        tok = self.peek()
        if tok == "~":
            self.take()
            return ("not", self.unary())
        if tok in ("forall", "exists"):
            self.take()
            var = self.take()
            return ("all" if tok == "forall" else "exists", var, self.unary())
        if tok == "(":
            self.take()
            f = self.iff()
            self.take(")")
            return f
        return self.atom()

    def atom(self):
        name = self.take()
        args = []
        if self.peek() == "(":
            self.take()
            args.append(self.term())
            while self.peek() == ",":
                self.take()
                args.append(self.term())
            self.take(")")
        return ("pred", name, tuple(args))

    def term(self):
        name = self.take()
        if self.peek() == "(":
            self.take()
            args = [self.term()]
            while self.peek() == ",":
                self.take()
                args.append(self.term())
            self.take(")")
            return ("fn", name, tuple(args))
        return name


def is_var(t):
    return isinstance(t, str) and t[0].islower()


# ======================= CNF conversion =======================

def eliminate_implications(f):
    op = f[0]
    if op == "pred":
        return f
    if op == "not":
        return ("not", eliminate_implications(f[1]))
    if op in ("all", "exists"):
        return (op, f[1], eliminate_implications(f[2]))
    a, b = eliminate_implications(f[1]), eliminate_implications(f[2])
    if op == "imp":
        return ("or", ("not", a), b)
    if op == "iff":
        return ("and", ("or", ("not", a), b), ("or", ("not", b), a))
    return (op, a, b)


def move_not_inwards(f):
    op = f[0]
    if op == "not":
        g = f[1]
        if g[0] == "pred":
            return f
        if g[0] == "not":
            return move_not_inwards(g[1])
        if g[0] == "and":
            return ("or", move_not_inwards(("not", g[1])), move_not_inwards(("not", g[2])))
        if g[0] == "or":
            return ("and", move_not_inwards(("not", g[1])), move_not_inwards(("not", g[2])))
        if g[0] == "all":
            return ("exists", g[1], move_not_inwards(("not", g[2])))
        if g[0] == "exists":
            return ("all", g[1], move_not_inwards(("not", g[2])))
    if op in ("and", "or"):
        return (op, move_not_inwards(f[1]), move_not_inwards(f[2]))
    if op in ("all", "exists"):
        return (op, f[1], move_not_inwards(f[2]))
    return f


def subst_term(theta, t):
    if is_var(t):
        return subst_term(theta, theta[t]) if t in theta else t
    if isinstance(t, tuple):
        return ("fn", t[1], tuple(subst_term(theta, a) for a in t[2]))
    return t


def subst_formula(theta, f):
    op = f[0]
    if op == "pred":
        return ("pred", f[1], tuple(subst_term(theta, a) for a in f[2]))
    if op == "not":
        return ("not", subst_formula(theta, f[1]))
    if op in ("all", "exists"):
        return (op, f[1], subst_formula(theta, f[2]))
    return (op, subst_formula(theta, f[1]), subst_formula(theta, f[2]))


_var_id = count(1)
_skolem_id = count(1)


def standardize_variables(f):
    """Give every quantifier its own variable name."""
    op = f[0]
    if op in ("all", "exists"):
        new = f"{f[1]}{next(_var_id)}"
        body = subst_formula({f[1]: new}, f[2])
        return (op, new, standardize_variables(body))
    if op == "not":
        return ("not", standardize_variables(f[1]))
    if op in ("and", "or"):
        return (op, standardize_variables(f[1]), standardize_variables(f[2]))
    return f


def skolemize(f, universals=()):
    op = f[0]
    if op == "all":
        return ("all", f[1], skolemize(f[2], universals + (f[1],)))
    if op == "exists":
        n = next(_skolem_id)
        sk = ("fn", f"F{n}", universals) if universals else f"C{n}"
        return skolemize(subst_formula({f[1]: sk}, f[2]), universals)
    if op in ("and", "or"):
        return (op, skolemize(f[1], universals), skolemize(f[2], universals))
    return f


def drop_universals(f):
    op = f[0]
    if op == "all":
        return drop_universals(f[2])
    if op in ("and", "or"):
        return (op, drop_universals(f[1]), drop_universals(f[2]))
    return f


def distribute(f):
    op = f[0]
    if op == "and":
        return ("and", distribute(f[1]), distribute(f[2]))
    if op == "or":
        a, b = distribute(f[1]), distribute(f[2])
        if a[0] == "and":
            return ("and", distribute(("or", a[1], b)), distribute(("or", a[2], b)))
        if b[0] == "and":
            return ("and", distribute(("or", a, b[1])), distribute(("or", a, b[2])))
        return ("or", a, b)
    return f


def to_clauses(f):
    """CNF formula -> list of clauses; a clause is a frozenset of literals,
    a literal is (positive, predicate, args)."""
    if f[0] == "and":
        return to_clauses(f[1]) + to_clauses(f[2])

    literals = []

    def collect(g):
        if g[0] == "or":
            collect(g[1])
            collect(g[2])
        elif g[0] == "not":
            literals.append((False, g[1][1], g[1][2]))
        else:
            literals.append((True, g[1], g[2]))

    collect(f)
    return [frozenset(literals)]


def to_cnf(sentence):
    f = Parser(sentence).parse()
    f = eliminate_implications(f)
    f = move_not_inwards(f)
    f = standardize_variables(f)
    f = skolemize(f)
    f = drop_universals(f)
    f = distribute(f)
    return [canonical(c) for c in to_clauses(f)]


# ======================= Printing =======================

def show_term(t):
    if isinstance(t, tuple):
        return f"{t[1]}({', '.join(show_term(a) for a in t[2])})"
    return t


def show_literal(lit):
    positive, name, args = lit
    text = f"{name}({', '.join(show_term(a) for a in args)})" if args else name
    return text if positive else "¬" + text


def show_clause(clause):
    if not clause:
        return "{}  (empty clause)"
    return " ∨ ".join(show_literal(l) for l in sorted(clause, key=lambda l: (l[1], not l[0])))


def show_theta(theta):
    if not theta:
        return "{}"
    return "{" + ", ".join(f"{v}/{show_term(t)}" for v, t in theta.items()) + "}"


# ======================= Unification =======================

def unify(x, y, theta):
    if theta is None:
        return None
    if x == y:
        return theta
    if is_var(x):
        return unify_var(x, y, theta)
    if is_var(y):
        return unify_var(y, x, theta)
    if isinstance(x, tuple) and isinstance(y, tuple):
        if x[1] != y[1] or len(x[2]) != len(y[2]):
            return None
        for a, b in zip(x[2], y[2]):
            theta = unify(a, b, theta)
        return theta
    return None


def occurs(var, t, theta):
    if var == t:
        return True
    if is_var(t) and t in theta:
        return occurs(var, theta[t], theta)
    if isinstance(t, tuple):
        return any(occurs(var, a, theta) for a in t[2])
    return False


def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    if is_var(x) and x in theta:
        return unify(var, theta[x], theta)
    if occurs(var, x, theta):
        return None
    return {**theta, var: x}


# ======================= Resolution =======================

def term_vars(t, out):
    if is_var(t):
        if t not in out:
            out.append(t)
    elif isinstance(t, tuple):
        for a in t[2]:
            term_vars(a, out)


def clause_vars(clause):
    out = []
    for lit in sorted(clause, key=lambda l: (l[1], not l[0], str(l[2]))):
        for a in lit[2]:
            term_vars(a, out)
    return out


def rename_clause(clause, mapping):
    return frozenset((p, n, tuple(subst_term(mapping, a) for a in args))
                     for p, n, args in clause)


def canonical(clause):
    """Rename variables to x, y, z, ... so equal clauses compare equal."""
    names = ["x", "y", "z", "u", "v", "w"]
    vars_ = clause_vars(clause)
    mapping = {v: (names[i] if i < len(names) else f"v{i}")
               for i, v in enumerate(vars_)}
    return rename_clause(clause, mapping)


def resolve(c1, c2):
    """Yield (resolvent, substitution) for every complementary pair."""
    # standardize apart: give c2 fresh variable names
    c2 = rename_clause(c2, {v: v + "'" for v in clause_vars(c2)})
    for l1 in c1:
        for l2 in c2:
            if l1[0] != l2[0] and l1[1] == l2[1] and len(l1[2]) == len(l2[2]):
                theta = {}
                for a, b in zip(l1[2], l2[2]):
                    theta = unify(a, b, theta)
                if theta is None:
                    continue
                rest = (c1 - {l1}) | (c2 - {l2})
                resolvent = rename_clause(rest, {v: subst_term(theta, v) for v in theta})
                yield canonical(resolvent), readable_theta(theta)


def strip_primes(t):
    if isinstance(t, tuple):
        return ("fn", t[1], tuple(strip_primes(a) for a in t[2]))
    return t.rstrip("'")


def readable_theta(theta):
    """Substitution for display: fully applied, primes removed where
    that causes no clash between the two clauses' variable names."""
    shown = {}
    for v in sorted(theta, key=lambda v: v.endswith("'")):
        name = v.rstrip("'")
        if name in shown:
            name = v
        shown[name] = strip_primes(subst_term(theta, v))
    return shown


def is_tautology(clause):
    return any((not p, n, a) in clause for p, n, a in clause)


def resolution(kb_clauses, negated_goal):
    """Given-clause algorithm with set of support and unit preference."""
    origin = {}            # clause -> description / parents
    usable = []
    for c in kb_clauses:
        origin.setdefault(c, ("KB",))
        usable.append(c)

    tie = count()
    sos = []
    for c in negated_goal:
        origin[c] = ("Negated query",)
        heapq.heappush(sos, (len(c), next(tie), c))

    seen = set(kb_clauses) | set(negated_goal)

    while sos:
        _, _, given = heapq.heappop(sos)
        for other in list(usable):
            for resolvent, theta in resolve(given, other):
                if is_tautology(resolvent) or resolvent in seen:
                    continue
                seen.add(resolvent)
                origin[resolvent] = ("Resolved", given, other, theta)
                if not resolvent:
                    return origin
                heapq.heappush(sos, (len(resolvent), next(tie), resolvent))
        usable.append(given)
    return None


def proof_steps(origin):
    """Return the resolution steps leading to the empty clause, in order."""
    steps = []

    def visit(clause):
        info = origin[clause]
        if info[0] != "Resolved":
            return
        _, c1, c2, theta = info
        visit(c1)
        visit(c2)
        step = (c1, c2, theta, clause)
        if step not in steps:
            steps.append(step)

    visit(frozenset())
    return steps


def print_tree(clause, origin, prefix="", last=True, root=True):
    info = origin[clause]
    connector = "" if root else ("└── " if last else "├── ")
    label = show_clause(clause)
    if info[0] == "Resolved":
        if info[3]:
            label += f"   {show_theta(info[3])}"
    else:
        label += f"   [{info[0]}]"
    print(prefix + connector + label)
    if info[0] == "Resolved":
        child_prefix = prefix if root else prefix + ("    " if last else "│   ")
        print_tree(info[1], origin, child_prefix, False, False)
        print_tree(info[2], origin, child_prefix, True, False)


# ======================= Knowledge base =======================

KB = [
    ("John likes all kind of food",
     "forall x (Food(x) => Likes(John, x))"),
    ("Apple and vegetables are food",
     "Food(Apple) & Food(Vegetables)"),
    ("Anything anyone eats and not killed is food",
     "forall x forall y (Eats(x, y) & ~Killed(x) => Food(y))"),
    ("Anil eats peanuts and still alive",
     "Eats(Anil, Peanuts) & Alive(Anil)"),
    ("Harry eats everything that Anil eats",
     "forall x (Eats(Anil, x) => Eats(Harry, x))"),
    ("Anyone who is alive implies not killed",
     "forall x (Alive(x) => ~Killed(x))"),
    ("Anyone who is not killed implies alive",
     "forall x (~Killed(x) => Alive(x))"),
]

QUERY = ("John likes peanuts", "Likes(John, Peanuts)")


def main():
    print("=" * 64)
    print(" FIRST ORDER LOGIC - RESOLUTION")
    print("=" * 64)

    print("\nKnowledge Base (FOL):")
    for i, (english, fol) in enumerate(KB):
        print(f"  {chr(97 + i)}. {english}")
        print(f"     {fol}")
    print(f"\nQuery: {QUERY[0]}\n     {QUERY[1]}")

    print("\nStep 1: Convert to CNF")
    kb_clauses = []
    for i, (_, fol) in enumerate(KB):
        clauses = to_cnf(fol)
        kb_clauses.extend(clauses)
        print(f"  {chr(97 + i)}. " + "\n     ".join(show_clause(c) for c in clauses))

    negated = to_cnf(f"~({QUERY[1]})")
    print("\nStep 2: Negate the query")
    for c in negated:
        print("  ", show_clause(c))

    print("\nStep 3: Resolve clauses")
    origin = resolution(kb_clauses, negated)

    if origin is None:
        print("  Empty clause cannot be derived.")
        print(f"\nResult: '{QUERY[0]}' is NOT proved.")
        return

    for n, (c1, c2, theta, res) in enumerate(proof_steps(origin), start=1):
        print(f"  {n}. {show_clause(c1)}")
        print(f"     {show_clause(c2)}")
        print(f"     {show_theta(theta)}  =>  {show_clause(res)}")

    print("\nProof Tree (root is the empty clause):")
    print_tree(frozenset(), origin)

    print(f"\nEmpty clause derived, so the negated query is a contradiction.")
    print(f"Result: '{QUERY[0]}' is PROVED by resolution.")


if __name__ == "__main__":
    main()
