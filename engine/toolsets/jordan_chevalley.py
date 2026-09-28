"""
GenerationalLineage.engine.toolsets.jordan_chevalley
=====================================================
JORDAN–CHEVALLEY — split an operator into its semisimple and nilpotent parts.

Every square matrix A over a perfect field is, uniquely,

        A = S + N,     S·N = N·S,     S semisimple (diagonalisable over the
                                       algebraic closure),   N nilpotent,

and both S and N are *polynomials in A*. S is the part of A that only scales;
N is the part that only shifts down a chain and dies after k steps. It is
factoral decomposition of an operator into its two irreducible behaviours —
SCALE and a finite-lifetime "leaf that falls":

    S  the eigen-scaling      (SCALE, on each generalised eigenspace)
    N  the nilpotent radical  (a chain of generations; N^k = 0 — the T32 / GF(2)
       radical of `lineage.py`, here over ℚ)

    nilpotency index k = the number of generations N lives.
    dim ker Nʲ − dim ker Nʲ⁻¹ counts Jordan blocks of size ≥ j → the block-size
    partition of N (size-1 blocks included: the points N acts as 0 on) is
    recovered from ranks alone.

METHOD (exact rational arithmetic, no floating point anywhere):
    1. χ(t) by Faddeev–LeVerrier.
    2. r = χ / gcd(χ, χ′)  — the squarefree part (same roots, all simple).
    3. Newton on matrices:  S ← S − r(S)·r′(S)⁻¹,  starting at S = A. Each
       step doubles the accuracy of "r(S) = 0"; in exact arithmetic it
       reaches r(S) = 0 exactly in ≤ ⌈log₂ n⌉ steps.
    4. N = A − S.
Everything is then CHECKED, not trusted: S+N = A, SN = NS, N^n = 0,
r(S) = 0 (S has a squarefree minimal polynomial ⇒ semisimple).

DECOMPOSITION (free): `descend(A)` — S, N, the index, the block sizes.
EMERGER (work): `build_up({'blocks': [(λ,size),…], 'basis': P})` — build the
matrix with that Jordan structure in a chosen basis. The basis is the added
constraint: A alone does not return P.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Any, Dict, List, Sequence, Tuple

from ..lines import AscentNotFree

NAME = "jordan_chevalley"
LINE = "both"

Mat = List[List[Fraction]]
Poly = List[Fraction]                              # low → high


def _F(M) -> Mat:
    return [[Fraction(x) for x in row] for row in M]


def eye(n: int) -> Mat:
    return [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]


def zeros(n: int) -> Mat:
    return [[Fraction(0)] * n for _ in range(n)]


def mm(A: Mat, B: Mat) -> Mat:
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def madd(A: Mat, B: Mat, sign: int = 1) -> Mat:
    return [[a + sign * b for a, b in zip(ra, rb)] for ra, rb in zip(A, B)]


def mscale(A: Mat, c) -> Mat:
    return [[c * x for x in row] for row in A]


def trace(A: Mat):
    return sum(A[i][i] for i in range(len(A)))


def is_zero(A: Mat) -> bool:
    return all(x == 0 for row in A for x in row)


def minv(A: Mat) -> Mat:
    n = len(A)
    M = [row[:] + eye(n)[i] for i, row in enumerate(A)]
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None:
            raise ZeroDivisionError("singular matrix")
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [x / pv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [row[n:] for row in M]


def rank(A: Mat) -> int:
    M = [row[:] for row in A]
    n, m, r = len(M), len(M[0]), 0
    for c in range(m):
        piv = next((i for i in range(r, n) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(r + 1, n):
            if M[i][c] != 0:
                f = M[i][c] / M[r][c]
                M[i] = [x - f * y for x, y in zip(M[i], M[r])]
        r += 1
    return r


def mpow(A: Mat, k: int) -> Mat:
    R = eye(len(A))
    for _ in range(k):
        R = mm(R, A)
    return R


def charpoly(A: Mat) -> Poly:
    """Faddeev–LeVerrier. Returns low→high coefficients of det(tI − A)."""
    n = len(A)
    c = [Fraction(0)] * (n + 1)
    c[n] = Fraction(1)
    Mk = zeros(n)
    for k in range(1, n + 1):
        Mk = madd(mm(A, Mk), mscale(eye(n), c[n - k + 1]))
        c[n - k] = -trace(mm(A, Mk)) / k
    return c


def _trim(p: Poly) -> Poly:
    while len(p) > 1 and p[-1] == 0:
        p = p[:-1]
    return p


def pdivmod(a: Poly, b: Poly) -> Tuple[Poly, Poly]:
    a, b = _trim(a[:]), _trim(b[:])
    if len(b) == 1 and b[0] == 0:
        raise ZeroDivisionError("polynomial division by zero")
    q = [Fraction(0)] * max(1, len(a) - len(b) + 1)
    while len(a) >= len(b) and not (len(a) == 1 and a[0] == 0):
        sh = len(a) - len(b)
        f = a[-1] / b[-1]
        q[sh] = f
        for i, x in enumerate(b):
            a[i + sh] -= f * x
        a = _trim(a)                       # the leading coefficient is now exactly 0
    return _trim(q), a


def pgcd(a: Poly, b: Poly) -> Poly:
    a, b = _trim(a[:]), _trim(b[:])
    while not (len(b) == 1 and b[0] == 0):
        _, r = pdivmod(a, b)
        a, b = b, r
    return [x / a[-1] for x in a]


def deriv(p: Poly) -> Poly:
    return _trim([i * p[i] for i in range(1, len(p))] or [Fraction(0)])


def peval_mat(p: Poly, A: Mat) -> Mat:
    n = len(A)
    R = zeros(n)
    for c in reversed(p):
        R = madd(mm(R, A), mscale(eye(n), c))
    return R


def descend(x, **_) -> Dict[str, Any]:
    A = _F(x)
    n = len(A)
    chi = charpoly(A)
    g = pgcd(chi, deriv(chi))
    r, rem = pdivmod(chi, g)
    assert len(rem) == 1 and rem[0] == 0
    r = [c / r[-1] for c in r]
    dr = deriv(r)

    S, steps = A, 0
    while not is_zero(peval_mat(r, S)):
        S = madd(S, mm(peval_mat(r, S), minv(peval_mat(dr, S))), -1)
        steps += 1
        if steps > n + 2:
            raise RuntimeError("Newton iteration failed to terminate (should be ≤ ⌈log₂ n⌉ + 1)")
    N = madd(A, S, -1)

    # nilpotency index and block sizes from ranks of powers of N
    ranks, P, k = [n], eye(n), 0
    while not is_zero(P) and k <= n:
        P = mm(P, N)
        ranks.append(rank(P))
        k += 1
    index = k if is_zero(P) else None
    ge = [ranks[j - 1] - ranks[j] for j in range(1, len(ranks))]      # blocks of size ≥ j
    ge.append(0)
    sizes: List[int] = []
    for j in range(1, len(ge)):
        sizes += [j] * (ge[j - 1] - ge[j])
    sizes.sort(reverse=True)

    checks = {
        "S_plus_N_equals_A": madd(S, N) == A,
        "S_N_commute": mm(S, N) == mm(N, S),
        "N_nilpotent": index is not None and is_zero(mpow(N, n)),
        "S_semisimple_squarefree_minpoly": is_zero(peval_mat(r, S)),
    }
    return {
        "toolset": NAME, "n": n,
        "S": S, "N": N,
        "charpoly": chi, "squarefree_part": r,
        "newton_steps": steps,
        "nilpotency_index": index,
        "jordan_block_sizes_of_N": sizes,
        "is_semisimple": is_zero(N), "is_nilpotent": is_zero(S),
        "checks": checks, "ok": all(checks.values()),
        "note": "S scales, N shifts down a chain and dies after `nilpotency_index` steps; "
                "both are polynomials in A",
    }


def build_up(target, **_) -> Dict[str, Any]:
    if isinstance(target, dict) and "blocks" in target:
        blocks = [(Fraction(l), int(s)) for l, s in target["blocks"]]
        n = sum(s for _, s in blocks)
        J = zeros(n)
        i = 0
        for lam, sz in blocks:
            for k in range(sz):
                J[i + k][i + k] = lam
                if k + 1 < sz:
                    J[i + k][i + k + 1] = Fraction(1)
            i += sz
        P = _F(target["basis"]) if "basis" in target else eye(n)
        A = mm(mm(P, J), minv(P))
        return {"toolset": NAME, "direction": "Jordan structure + basis -> matrix",
                "A": A, "J": J, "cost": n ** 3,
                "note": "the basis P is the added constraint — A alone does not return it"}
    raise AscentNotFree("{'blocks': [(λ, size), …], 'basis': P}")


def verify() -> Dict[str, Any]:
    cases = {}
    unimod = [[1, 2, 0, 1], [0, 1, 3, 0], [1, 0, 1, 2], [0, 0, 1, 1]]
    # det of the basis must be non-zero
    assert rank(_F(unimod)) == 4

    # (name, blocks, expected nilpotency index, expected block sizes of N —
    #  size-1 blocks are the semisimple points N acts as 0 on)
    specs = {
        "single_J3": ([(2, 3)], 3, [3]),
        "mixed_conjugated": ([(1, 2), (3, 1), (3, 1)], 2, [2, 1, 1]),
        "two_eigenvalues_two_chains": ([(1, 2), (5, 2)], 2, [2, 2]),
        "diagonalisable": ([(1, 1), (2, 1), (3, 1), (4, 1)], 1, [1, 1, 1, 1]),
        "nilpotent": ([(0, 3), (0, 1)], 3, [3, 1]),
        "repeated_eigenvalue_chain_and_point": ([(7, 3), (7, 1)], 3, [3, 1]),
    }
    ok_all = True
    for name, (blocks, idx, sizes) in specs.items():
        n = sum(s for _, s in blocks)
        B = build_up({"blocks": blocks, **({"basis": unimod} if n == 4 else {})})
        d = descend(B["A"])
        good = (d["ok"] and d["nilpotency_index"] == idx
                and d["jordan_block_sizes_of_N"] == sizes
                and d["is_semisimple"] == (name == "diagonalisable")
                and d["is_nilpotent"] == (name == "nilpotent"))
        cases[name] = good
        ok_all = ok_all and good

    # irrational eigenvalues: companion of t²−2 ⊕ nilpotent J₂ — S is rational anyway (S ∈ ℚ[A])
    A = [[0, 2, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 0]]
    d = descend(A)
    ok_irr = d["ok"] and d["nilpotency_index"] == 2 and d["jordan_block_sizes_of_N"] == [2, 1, 1]
    cases["irrational_eigenvalues"] = ok_irr
    ok_all = ok_all and ok_irr

    # S and N are polynomials in A ⇒ they commute with anything that commutes with A.
    # The precondition is asserted, so this cannot pass by skipping.
    A2 = build_up({"blocks": [(2, 2), (3, 1)]})["A"]
    d2 = descend(A2)
    C = _F([[1, 5, 0], [0, 1, 0], [0, 0, 2]])
    ok_poly = (mm(C, A2) == mm(A2, C)
               and mm(C, d2["S"]) == mm(d2["S"], C)
               and mm(C, d2["N"]) == mm(d2["N"], C))
    try:
        build_up({})
        ok_refuse = False
    except AscentNotFree:
        ok_refuse = True
    return {"ok": all([ok_all, ok_poly, ok_refuse]), "cases": cases,
            "polynomial_in_A": ok_poly, "refuses_without_blocks": ok_refuse}


if __name__ == "__main__":
    A = build_up({"blocks": [(1, 2), (3, 1)]})["A"]
    r = descend(A)
    print({k: r[k] for k in ("nilpotency_index", "jordan_block_sizes_of_N", "newton_steps", "ok")})
    print(verify())
