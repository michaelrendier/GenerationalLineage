# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
#
# GenerationalLineage is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 3 of the License.
#
# GenerationalLineage is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details. You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-only
"""
GenerationalLineage.engine.toolsets.permutation
================================================
PERMUTATION — the invariants of a re-ordering: cycle type, order, sign,
length, and its address in the factorial number system.

A permutation is the purest "re-ordering". Everything worth knowing about it
as an operator is a function of a few numbers, all read in one pass:

    cycle type        the multiset of cycle lengths (a partition of n) —
                      the conjugacy class: two permutations are conjugate
                      exactly when their cycle types agree
    order             lcm of the cycle lengths      (the JOIN — dual of the gcd/meet)
    sign              (−1)^(n − #cycles) — the tier-0 SIGN irreducible, read off a permutation
    reflection length n − #cycles      fewest transpositions that build it
    inversions        length in adjacent transpositions (Coxeter length);
                      sign = (−1)^inversions — cross-checked, not assumed
    Lehmer code       cᵢ = #{j > i : π(j) < π(i)}; digit i lives in base (n − i)
    factoradic rank   Σ cᵢ·(n−1−i)!   — the permutation's index in 0..n!−1.
                      The factorial number system IS the mixed-radix
                      decomposition of a permutation's address.

MODULAR AFFINE PERMUTATIONS  x ↦ a·x + b  (mod m), gcd(a,m)=1
    This is the ADD ⋊ SCALE group acting on ℤ/m — the tier-0 floor as a
    permutation. Composition is (a₁,b₁)∘(a₂,b₂) = (a₁a₂, a₁b₂+b₁). For b=0
    the orbit of x has length ord_{m/gcd(x,m)}(a): a cycle structure read off
    multiplicative orders. Card shuffles are instances:
        in-shuffle  x ↦ 2x mod (2n+1)          order = ord_{2n+1}(2)
        out-shuffle x ↦ 2x mod (2n−1) on 0..2n−1 (ends fixed)

THE CHEAPEST PERMUTATION OF ORDER N
    Its minimal degree is  Σ p^e  over the prime-power factorisation of N
    (one cycle per prime power — a cycle covering several prime powers is as
    long as their product, never shorter than their sum): the lineage of N,
    paid in points. Checked here by exhaustive search over cycle types.

DECOMPOSITION (free): `descend(perm)` — one pass.
EMERGER (work): `build_up({'rank': r, 'n': n})` un-ranks; `build_up({'cycle_type':
[…]})` builds a permutation of that type (the choice is the labelling);
`build_up({'order': N})` builds the cheapest permutation of order N.
"""
from __future__ import annotations

from math import gcd
from typing import Any, Dict, List, Sequence, Tuple

from ..lines import AscentNotFree

NAME = "permutation"
LINE = "both"


def _lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def cycles(perm: Sequence[int]) -> List[List[int]]:
    seen, out = [False] * len(perm), []
    for i in range(len(perm)):
        if not seen[i]:
            c, j = [], i
            while not seen[j]:
                seen[j] = True
                c.append(j)
                j = perm[j]
            out.append(c)
    return out


def cycle_type(perm: Sequence[int]) -> Tuple[int, ...]:
    return tuple(sorted((len(c) for c in cycles(perm)), reverse=True))


def order(perm: Sequence[int]) -> int:
    o = 1
    for c in cycles(perm):
        o = _lcm(o, len(c))
    return o


def inversions(perm: Sequence[int]) -> int:
    n = len(perm)
    return sum(1 for i in range(n) for j in range(i + 1, n) if perm[i] > perm[j])


def lehmer(perm: Sequence[int]) -> List[int]:
    n = len(perm)
    return [sum(1 for j in range(i + 1, n) if perm[j] < perm[i]) for i in range(n)]


def factoradic_rank(perm: Sequence[int]) -> int:
    n, r, f = len(perm), 0, 1
    code = lehmer(perm)
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i
    for i in range(n):
        r += code[i] * fact[n - 1 - i]
    return r


def unrank(rank: int, n: int) -> List[int]:
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i
    if not 0 <= rank < fact[n]:
        raise ValueError("rank out of range 0..n!-1")
    pool, out = list(range(n)), []
    for i in range(n):
        d, rank = divmod(rank, fact[n - 1 - i])
        out.append(pool.pop(d))
    return out


def conjugate(perm: Sequence[int], sigma: Sequence[int]) -> List[int]:
    """σ ∘ π ∘ σ⁻¹."""
    inv = [0] * len(sigma)
    for i, s in enumerate(sigma):
        inv[s] = i
    return [sigma[perm[inv[i]]] for i in range(len(perm))]


# ── modular affine permutations: the ADD ⋊ SCALE group on ℤ/m ───────────────
def affine_perm(a: int, b: int, m: int) -> List[int]:
    if gcd(a, m) != 1:
        raise ValueError("a must be a unit mod m for x -> ax+b to be a permutation")
    return [(a * x + b) % m for x in range(m)]


def affine_compose(f: Tuple[int, int], g: Tuple[int, int], m: int) -> Tuple[int, int]:
    """(a1,b1)∘(a2,b2) = (a1·a2, a1·b2 + b1) mod m."""
    return (f[0] * g[0] % m, (f[0] * g[1] + f[1]) % m)


def mult_order(a: int, m: int) -> int:
    if m == 1:
        return 1
    if gcd(a, m) != 1:
        raise ValueError("a not a unit")
    k, x = 1, a % m
    while x != 1:
        x = x * a % m
        k += 1
    return k


def shuffle_order(n_pairs: int, kind: str) -> int:
    """Order of the perfect in- or out-shuffle of a 2n-card deck."""
    n2 = 2 * n_pairs
    if kind == "in":
        # positions 1..2n under x -> 2x mod (2n+1)
        perm = [((2 * (x + 1)) % (n2 + 1)) - 1 for x in range(n2)]
    elif kind == "out":
        # positions 0..2n-1: x -> 2x mod (2n-1), last card fixed
        perm = [(2 * x) % (n2 - 1) if x < n2 - 1 else x for x in range(n2)]
    else:
        raise ValueError("kind is 'in' or 'out'")
    return order(perm)


# ── cheapest permutation of a given order ───────────────────────────────────
def _prime_powers(n: int) -> Dict[int, int]:
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def min_degree_for_order(N: int) -> int:
    """Σ p^e over the prime-power factorisation of N (N = 1 → 1)."""
    if N == 1:
        return 1
    return sum(p ** e for p, e in _prime_powers(N).items())


def _partitions(n: int, maxpart: int | None = None):
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield ()
        return
    for k in range(min(n, maxpart), 0, -1):
        for rest in _partitions(n - k, k):
            yield (k,) + rest


def from_cycle_type(ct: Sequence[int]) -> List[int]:
    perm, start = [], 0
    n = sum(ct)
    perm = list(range(n))
    for L in ct:
        for i in range(L):
            perm[start + i] = start + (i + 1) % L
        start += L
    return perm


def descend(x, **_) -> Dict[str, Any]:
    perm = list(x)
    n = len(perm)
    if sorted(perm) != list(range(n)):
        raise ValueError("input is not a permutation of 0..n-1")
    cyc = cycles(perm)
    inv = inversions(perm)
    refl = n - len(cyc)
    return {
        "toolset": NAME, "n": n,
        "cycles": cyc, "cycle_type": cycle_type(perm),
        "order": order(perm),
        "sign": -1 if refl % 2 else 1,
        "sign_agrees_with_inversions": (inv % 2 == refl % 2),
        "reflection_length": refl, "inversions": inv,
        "fixed_points": sum(1 for c in cyc if len(c) == 1),
        "derangement": all(len(c) > 1 for c in cyc),
        "lehmer": lehmer(perm), "factoradic_rank": factoradic_rank(perm),
        "note": "cycle type = conjugacy class; order = lcm of cycle lengths (the join)",
    }


def build_up(target, **_) -> Dict[str, Any]:
    if isinstance(target, dict) and "rank" in target and "n" in target:
        p = unrank(int(target["rank"]), int(target["n"]))
        return {"toolset": NAME, "direction": "factoradic rank -> permutation",
                "perm": p, "cost": len(p) ** 2,
                "note": "un-ranking peels one mixed-radix digit per position"}
    if isinstance(target, dict) and "cycle_type" in target:
        ct = tuple(sorted(target["cycle_type"], reverse=True))
        p = from_cycle_type(ct)
        return {"toolset": NAME, "direction": "cycle type -> a permutation of that class",
                "perm": p, "cost": len(p),
                "note": "the choice is the labelling — every labelling is conjugate"}
    if isinstance(target, dict) and "order" in target:
        N = int(target["order"])
        cts = [p ** e for p, e in _prime_powers(N).items()] or [1]
        p = from_cycle_type(tuple(sorted(cts, reverse=True)))
        return {"toolset": NAME, "direction": "order -> cheapest permutation",
                "perm": p, "degree": len(p), "cycle_type": tuple(sorted(cts, reverse=True)),
                "cost": len(p),
                "note": "one cycle per prime power of N — the lineage of N, paid in points"}
    raise AscentNotFree("{'rank','n'} | {'cycle_type': […]} | {'order': N}")


def verify() -> Dict[str, Any]:
    from itertools import permutations
    # 1. exhaustive over S_1..S_7: sign, factoradic round-trip, conjugation invariance of type
    ok_sign = ok_rank = ok_conj = True
    count = 0
    for n in range(1, 8):
        ranks = set()
        sigma = list(range(1, n)) + [0]                    # a fixed n-cycle to conjugate by
        for p in permutations(range(n)):
            p = list(p)
            d = descend(p)
            if not d["sign_agrees_with_inversions"]:
                ok_sign = False
            r = d["factoradic_rank"]
            ranks.add(r)
            if unrank(r, n) != p:
                ok_rank = False
            if cycle_type(conjugate(p, sigma)) != cycle_type(p):
                ok_conj = False
            count += 1
        if ranks != set(range(len(ranks))) or len(ranks) != len(list(permutations(range(n)))):
            ok_rank = False                                # rank must be a bijection onto 0..n!-1

    # 2. affine permutations: composition law, and orbit length = ord_{m/gcd(x,m)}(a)
    ok_aff_law = ok_aff_orbit = True
    for m in (7, 12, 15, 26, 30):
        units = [a for a in range(1, m) if gcd(a, m) == 1] or [1]
        for a1 in units:
            for a2 in units[:4]:
                for b1, b2 in ((0, 3 % m), (2 % m, 5 % m)):
                    f, g = affine_perm(a1, b1, m), affine_perm(a2, b2, m)
                    comp = [f[g[x]] for x in range(m)]
                    if comp != affine_perm(*affine_compose((a1, b1), (a2, b2), m), m):
                        ok_aff_law = False
        for a in units:
            perm = affine_perm(a, 0, m)
            for x in range(m):
                orbit_len = len(next(c for c in cycles(perm) if x in c))
                if orbit_len != mult_order(a, m // gcd(x, m)):
                    ok_aff_orbit = False

    # 3. the card shuffles — published orders for a 52-card deck: out-shuffle 8, in-shuffle 52
    ok_shuffle = shuffle_order(26, "out") == 8 and shuffle_order(26, "in") == 52

    # 4. cheapest permutation of order N: exhaustive over cycle types up to degree 14
    best: Dict[int, int] = {}
    for n in range(1, 15):
        for ct in _partitions(n):
            o = 1
            for L in ct:
                o = _lcm(o, L)
            if o not in best:
                best[o] = n
    ok_min = all(best[N] == min_degree_for_order(N) for N in range(1, 31) if N in best
                 and min_degree_for_order(N) <= 14)
    ok_min &= all(descend(build_up({"order": N})["perm"])["order"] == N for N in range(1, 61))

    try:
        build_up({})
        ok_refuse = False
    except AscentNotFree:
        ok_refuse = True

    return {"ok": all([ok_sign, ok_rank, ok_conj, ok_aff_law, ok_aff_orbit, ok_shuffle,
                       ok_min, ok_refuse]),
            "permutations_checked_S1_S7": count,
            "sign_equals_inversion_parity": ok_sign,
            "factoradic_bijection_and_unrank": ok_rank,
            "cycle_type_conjugation_invariant": ok_conj,
            "affine_composition_law": ok_aff_law, "affine_orbit_is_mult_order": ok_aff_orbit,
            "shuffle_orders_52_cards": ok_shuffle,
            "cheapest_permutation_of_order_N": ok_min, "refuses_without_target": ok_refuse}


if __name__ == "__main__":
    print(descend([2, 0, 1, 4, 3, 5]))
    print(verify())
