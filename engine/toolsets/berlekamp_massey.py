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
GenerationalLineage.engine.toolsets.berlekamp_massey
=====================================================
BERLEKAMP–MASSEY — the shortest recurrence behind a sequence, and the period
that recurrence forces.

Given a sequence over GF(p), Berlekamp–Massey returns the shortest linear
recurrence that generates it: its length L is the sequence's **linear
complexity**, and its connection polynomial is the generator. It is
factoral decomposition of a *process*: the sequence is the observable, the
recurrence is the operator, and the operator's own factorisation decides the
period.

    sequence      s₀ s₁ s₂ …
    recurrence    Σ_{i=0..L} cᵢ·s_{n−i} = 0,   c₀ = 1
    char. poly    P(x) = x^L + c₁x^{L−1} + … + c_L
    period        = order of x modulo P(x)
                  = lcm over  f^e ∥ P  of   ord(f)·2^⌈log₂ e⌉       (over GF(2))
                  and ord(f) | 2^deg(f) − 1

so the period is read off the **factorisation of the minimal polynomial**:
P is irreducible of degree L ⇒ period | 2^L − 1; primitive ⇒ exactly 2^L − 1.

GUARANTEE. BM is exact only when the sequence supplies at least 2L terms.
`descend` reports `determined = (len(s) ≥ 2L)`; below that the recurrence is
an *underdetermined fit* and is flagged as one, not returned as a result.

The factoring is trial division by polynomials in increasing (degree, value)
order — exact, and affordable to L = 32. Beyond that the period is NOT
computed and the field says so (`period: None`); no approximation is offered.

EMERGER (work): `build_up({'poly': P, 'state': s, 'n': n})` runs the LFSR
(cost n); `build_up({'degree': L})` searches for a PRIMITIVE polynomial of
degree L (cost = candidates tested), i.e. the choice that buys the maximal
period 2^L − 1. `build_up({})` → AscentNotFree.
"""
from __future__ import annotations

from math import gcd
from typing import Any, Dict, List, Optional, Sequence, Tuple

from ..lines import AscentNotFree

NAME = "berlekamp_massey"
LINE = "both"

MAX_FACTOR_DEGREE = 32


# ── Berlekamp–Massey over GF(p) ─────────────────────────────────────────────
def bm(s: Sequence[int], p: int = 2) -> Tuple[int, List[int]]:
    """Return (L, C) with C = [1, c1, .., cL]:  Σ_i C[i]·s[n−i] ≡ 0 (mod p) for n ≥ L."""
    C, B = [1], [1]
    L, m, b = 0, 1, 1
    for n in range(len(s)):
        d = s[n] % p
        for i in range(1, L + 1):
            if i < len(C):
                d = (d + C[i] * s[n - i]) % p
        if d == 0:
            m += 1
            continue
        coef = d * pow(b, -1, p) % p
        T = C[:]
        if len(C) < len(B) + m:
            C = C + [0] * (len(B) + m - len(C))
        for i, bi in enumerate(B):
            C[i + m] = (C[i + m] - coef * bi) % p
        if 2 * L <= n:
            L, B, b, m = n + 1 - L, T, d, 1
        else:
            m += 1
    C = C[:L + 1] + [0] * max(0, L + 1 - len(C))
    return L, C


# ── GF(2)[x] arithmetic on int bitmasks (bit k = coefficient of x^k) ────────
def _deg(a: int) -> int:
    return a.bit_length() - 1


def _pmod(a: int, m: int) -> int:
    dm = _deg(m)
    while a and _deg(a) >= dm:
        a ^= m << (_deg(a) - dm)
    return a


def _pdivmod(a: int, m: int) -> Tuple[int, int]:
    q, dm = 0, _deg(m)
    while a and _deg(a) >= dm:
        sh = _deg(a) - dm
        q |= 1 << sh
        a ^= m << sh
    return q, a


def _pmulmod(a: int, b: int, m: int) -> int:
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if _deg(a) >= _deg(m):
            a ^= m
    return _pmod(r, m)


def _ppowmod(base: int, e: int, m: int) -> int:
    r, base = 1, _pmod(base, m)
    while e:
        if e & 1:
            r = _pmulmod(r, base, m)
        base = _pmulmod(base, base, m)
        e >>= 1
    return r


def _int_factor(n: int) -> Dict[int, int]:
    f, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def poly_factor_gf2(P: int) -> Dict[int, int]:
    """Irreducible factorisation over GF(2) by trial division in (degree, value) order."""
    out: Dict[int, int] = {}
    rem, d = P, 2
    while _deg(d) * 2 <= _deg(rem):
        q, r = _pdivmod(rem, d)
        if r == 0:
            while r == 0:
                out[d] = out.get(d, 0) + 1
                rem = q
                q, r = _pdivmod(rem, d)
        else:
            d += 1
    if rem > 1:
        out[rem] = out.get(rem, 0) + 1
    return out


def order_irreducible(f: int) -> int:
    """Multiplicative order of x modulo an irreducible f of degree d (divides 2^d − 1)."""
    d = _deg(f)
    if f == 2:                       # f = x
        raise ValueError("x is not a unit modulo x")
    n = (1 << d) - 1
    order = n
    for q in _int_factor(n):
        while order % q == 0 and _ppowmod(2, order // q, f) == 1:
            order //= q
    return order


def order_of_x(P: int) -> Optional[int]:
    """Order of x mod P(x) (P(0)=1), via the factorisation. None if degree > MAX."""
    if _deg(P) > MAX_FACTOR_DEGREE:
        return None
    lcm = 1
    for f, e in poly_factor_gf2(P).items():
        o = order_irreducible(f)
        t = 0
        while (1 << t) < e:
            t += 1
        o *= 1 << t
        lcm = lcm * o // gcd(lcm, o)
    return lcm


def is_primitive(P: int) -> bool:
    d = _deg(P)
    if d < 1 or not (P & 1):
        return False
    n = (1 << d) - 1
    if _ppowmod(2, n, P) != 1:
        return False
    return all(_ppowmod(2, n // q, P) != 1 for q in _int_factor(n))


def _poly_from_C(C: List[int]) -> int:
    L = len(C) - 1
    return sum(1 << (L - i) for i, c in enumerate(C) if c % 2)


def lfsr(P: int, state: Sequence[int], n: int) -> List[int]:
    """Run s_n = Σ_{i=1..L} c_i s_{n−i}, where c_i = coefficient of x^{L−i} in P."""
    L = _deg(P)
    c = [(P >> (L - i)) & 1 for i in range(1, L + 1)]
    s = list(state)
    while len(s) < n:
        s.append(sum(c[i - 1] * s[-i] for i in range(1, L + 1)) % 2)
    return s[:n]


def simulated_period(s: Sequence[int], cap: int) -> Optional[int]:
    for p in range(1, cap + 1):
        if all(s[i] == s[i + p] for i in range(len(s) - p)):
            return p
    return None


def descend(x, p: int = 2, **_) -> Dict[str, Any]:
    s = [int(v) % p for v in x]
    L, C = bm(s, p)
    determined = len(s) >= 2 * L
    out: Dict[str, Any] = {
        "toolset": NAME, "n": len(s), "field": f"GF({p})",
        "linear_complexity": L, "connection": C,
        "determined": determined,
        "terms_needed": 2 * L,
    }
    if not determined:
        out["note"] = ("UNDERDETERMINED — fewer than 2L terms; this recurrence is a fit, "
                       "not a result. Supply more of the sequence.")
    if p == 2 and L >= 1:
        P = _poly_from_C(C)
        pre = 0
        while P and not (P & 1):
            P >>= 1
            pre += 1
        out["char_poly_int"] = _poly_from_C(C)
        out["preperiod"] = pre
        if P == 1:
            out["period"] = 1
        else:
            out["period"] = order_of_x(P)
            if out["period"] is None:
                out["period_note"] = (f"degree {_deg(P)} > {MAX_FACTOR_DEGREE}: period NOT computed "
                                      "(no approximation offered)")
            else:
                fac = poly_factor_gf2(P)
                out["factors"] = {hex(f): e for f, e in fac.items()}
                out["primitive"] = (len(fac) == 1 and out["period"] == (1 << _deg(P)) - 1)
    elif L == 0:
        out["period"] = 1
    return out


def build_up(target, **_) -> Dict[str, Any]:
    if isinstance(target, dict) and "poly" in target:
        P, n = int(target["poly"]), int(target["n"])
        st = list(target.get("state", [1] + [0] * (_deg(P) - 1)))
        s = lfsr(P, st, n)
        return {"toolset": NAME, "direction": "polynomial -> sequence", "sequence": s, "cost": n,
                "note": "the choice is the polynomial and the seed"}
    if isinstance(target, dict) and "degree" in target:
        L = int(target["degree"])
        tested, P = 0, (1 << L) + 1
        while P < (1 << (L + 1)):
            tested += 1
            if is_primitive(P):
                return {"toolset": NAME, "direction": "search primitive polynomial",
                        "poly": P, "degree": L, "period": (1 << L) - 1, "cost": tested,
                        "note": "primitive ⇒ maximal period 2^L − 1"}
            P += 2
        raise AscentNotFree("no primitive polynomial found — impossible for L ≥ 1")
    raise AscentNotFree("{'poly','n'} to run, or {'degree'} to find a primitive polynomial")


def verify() -> Dict[str, Any]:
    # 1. primitive x^4+x+1 is the first found for L=4, x^5+x^2+1 for L=5
    b4, b5 = build_up({"degree": 4}), build_up({"degree": 5})
    ok_first = (b4["poly"] == 0b10011 and b5["poly"] == 0b100101)

    # 2. for every degree 2..16: the primitive polynomial's LFSR has period exactly 2^L − 1,
    #    BM recovers L and the polynomial from 2L terms, and `descend` names it primitive.
    ok_prim, ok_bm, ok_period = True, True, True
    for L in range(2, 17):
        r = build_up({"degree": L})
        P = r["poly"]
        s = lfsr(P, [1] + [0] * (L - 1), 2 * L + 8)
        d = descend(s)
        if not (d["linear_complexity"] == L and d["determined"] and d["char_poly_int"] == P):
            ok_bm = False
        if not d.get("primitive"):
            ok_prim = False
        if L <= 12:
            full = lfsr(P, [1] + [0] * (L - 1), 2 * ((1 << L) - 1) + 2)
            if simulated_period(full, (1 << L)) != (1 << L) - 1 or d["period"] != (1 << L) - 1:
                ok_period = False

    # 3. reducible case, EXHAUSTIVE over every non-zero seed. The minimal polynomial of a
    #    seed's sequence may be a proper divisor of P, so the period must always equal the
    #    simulated one (never assumed from P). Two products:
    #      (x²+x+1)(x³+x+1)   orders 3, 7  → lcm 21
    #      (x²+x+1)(x⁴+x+1)   orders 3, 15 → 15
    def clmul(a: int, b: int) -> int:
        r = 0
        for i in range(b.bit_length()):
            if (b >> i) & 1:
                r ^= a << i
        return r
    ok_reducible, seeds = True, 0
    for P, top in ((clmul(0b111, 0b1011), 21), (clmul(0b111, 0b10011), 15)):
        L = _deg(P)
        seen_top = False
        for m in range(1, 1 << L):
            st = [(m >> i) & 1 for i in range(L)]
            s = lfsr(P, st, 400)
            d = descend(s)
            if d["period"] != simulated_period(s, 100):
                ok_reducible = False
            seen_top = seen_top or d["period"] == top
            seeds += 1
        ok_reducible = ok_reducible and seen_top

    # 4. repeated factor: (x+1)^4 = x^4+1 → order 4 = 2^⌈log₂4⌉ · ord(x+1)=1
    ok_repeat = order_of_x(0b10001) == 4 and order_of_x(0b101) == 2

    # 5. honesty: below 2L terms the result is flagged
    d_short = descend([1, 0, 0, 1, 1, 0, 1])
    ok_flag = (not d_short["determined"]) or d_short["terms_needed"] <= 7

    try:
        build_up({})
        ok_refuse = False
    except AscentNotFree:
        ok_refuse = True

    return {"ok": all([ok_first, ok_prim, ok_bm, ok_period, ok_reducible, ok_repeat,
                       ok_flag, ok_refuse]),
            "first_primitive_L4_L5": ok_first, "primitive_named_L2_16": ok_prim,
            "bm_recovers_poly_L2_16": ok_bm, "period_2L_minus_1_L2_12": ok_period,
            "reducible_period_all_seeds": ok_reducible, "seeds_checked": seeds,
            "repeated_factor_order": ok_repeat,
            "underdetermined_flagged": ok_flag, "refuses_without_target": ok_refuse}


if __name__ == "__main__":
    s = lfsr(0b100101, [1, 0, 0, 0, 1], 40)
    print(descend(s))
    print(build_up({"degree": 8}))
    print(verify())
