"""Ch 8 box: checking structural identifiability before fitting (Springer review 3, point 4).

Companion text: Foundations and Pitfalls in Epidemic Modeling (hyman2026avoiding), Chapter 8.
Writes figs_src/ch8_structural_identifiability_values.txt. No figure.

Method: the Lie-derivative (observability) rank test for local structural identifiability. Parameters
are adjoined as constant states; the output and its first n_x + n_theta - 1 Lie derivatives along the
vector field are differentiated with respect to every unknown (initial states and parameters); the
unknowns are locally structurally identifiable exactly when this Jacobian has full generic rank. The rank
is evaluated exactly, in rational arithmetic, at a random rational point (a generic-rank certificate with
probability one). StructuralIdentifiability.jl (Dong, Goodbrake, Harrington and Pogudin 2023) answers the
same local question, and the global one, by differential elimination; the Julia call printed in the book is
the reader's cross-check.

Model A: SIR with weekly incidence counted exactly:   y = beta S I / N
Model B: the same, with an unknown reporting fraction rho:  y = rho beta S I / N  (the code's symbol q)
S' = -beta S I/N,  I' = beta S I/N - gamma I;  unknowns S(0), I(0), beta, gamma, N (and q in B).

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University (code drafted with Claude)
Date:    2026-11-08   Version 1.0 (Session 280)
"""
import os
import random
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ch8_structural_identifiability_values.txt")


def lie_rank(f, states, params, h, seed=1):
    X = list(states) + list(params)
    F = list(f) + [0] * len(params)
    rows = [h]
    for _ in range(len(X) - 1):
        rows.append(sp.expand(sum(sp.diff(rows[-1], X[i]) * F[i] for i in range(len(X)))))
    J = sp.Matrix(rows).jacobian(X)
    rnd = random.Random(seed)
    pt = {x: sp.Rational(rnd.randint(2, 40), rnd.randint(2, 9)) for x in X}
    Jn = J.subs(pt)
    rank = Jn.rank()
    null = Jn.nullspace()
    return rank, len(X), null, X


def lie_rank_constrained(f, states, params, h, S, N, seed=1):
    """Same test with S(0) = N - I(0) imposed: rows are computed freely, then S is replaced by N - I
    and the Jacobian is taken with respect to I(0) and the parameters only."""
    X = list(states) + list(params)
    F = list(f) + [0] * len(params)
    rows = [h]
    for _ in range(len(X) - 1):
        rows.append(sp.expand(sum(sp.diff(rows[-1], X[i]) * F[i] for i in range(len(X)))))
    I = [x for x in states if x != S][0]
    Y = [I] + list(params)
    J = sp.Matrix([r.subs(S, N - I) for r in rows]).jacobian(Y)
    rnd = random.Random(seed)
    pt = {x: sp.Rational(rnd.randint(2, 40), rnd.randint(2, 9)) for x in Y}
    pt[N] = pt[N] + 50
    Jn = J.subs(pt)
    return Jn.rank(), len(Y), Jn.nullspace(), Y


def main():
    S, I, b, g, N, q = sp.symbols("S I beta gamma N q", positive=True)
    f = [-b * S * I / N, b * S * I / N - g * I]
    lines = []
    for name, params, h in (("A0", [b, g, N], b * S * I / N), ("B0", [b, g, N, q], q * b * S * I / N)):
        r, n, null, Y = lie_rank_constrained(f, [S, I], params, h, S, N)
        lines.append(f"model {name} (S(0) = N - I(0)): unknowns {', '.join(map(str, Y))}; Jacobian rank {r} of {n}")
        for v in null:
            v = v / max(abs(c) for c in v if c != 0)
            lines.append(f"  unidentifiable direction (at the test point): " + ", ".join(f"{x}:{c}" for x, c in zip(Y, v)))
    for name, params, h in (("A", [b, g, N], b * S * I / N), ("B", [b, g, N, q], q * b * S * I / N)):
        r, n, null, X = lie_rank(f, [S, I], params, h)
        lines.append(f"model {name}: unknowns {', '.join(map(str, X))}; Jacobian rank {r} of {n}")
        for v in null:
            v = v / max(abs(c) for c in v if c != 0)
            lines.append(f"  unidentifiable direction (at the test point): " + ", ".join(f"{x}:{c}" for x, c in zip(X, v)))
    # the symmetry behind model B: S, I, N -> lam S, lam I, lam N and q -> q/lam leave y and the dynamics fixed
    lam = sp.symbols("lam", positive=True)
    hB = q * b * S * I / N
    inv = sp.simplify(hB.subs({S: lam * S, I: lam * I, N: lam * N, q: q / lam}, simultaneous=True) - hB)
    fI = b * S * I / N - g * I
    invf = sp.simplify(fI.subs({S: lam * S, I: lam * I, N: lam * N}, simultaneous=True) - lam * fI)
    lines.append(f"model B symmetry check: y change {inv}; I' scales by lam: residual {invf}")
    with open(OUT, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
