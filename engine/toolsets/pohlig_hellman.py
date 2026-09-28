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
GenerationalLineage.engine.toolsets.pohlig_hellman
===================================================
POHLIG–HELLMAN — factor the GROUP, solve per prime, glue by CRT.

The discrete-log problem  gˣ ≡ h (mod p)  looks like one hard problem. It is
not: its difficulty is entirely a property of the LINEAGE OF THE GROUP ORDER.

    n = ord(g) = ∏ qᵢ^eᵢ                 the group order, factored (descent)
    x mod qᵢ^eᵢ                          solved inside the subgroup of order qᵢ^eᵢ,
                                         one base-qᵢ digit at a time, each digit a
                                         discrete log in a group of prime order qᵢ
    x mod n                              reassembled by the Chinese Remainder Theorem

The cost is Σ eᵢ·(√qᵢ) group operations, not √n: it is set by the LARGEST
PRIME FACTOR of the order and by nothing else. A smooth order collapses to
easy; a prime order (a safe-prime subgroup) is untouched — that residue is
exactly where the hardness lives.

    descend(p, g, h)    the lineage of the group order, the largest prime
                        factor, and the PREDICTED cost — no discrete log is
                        computed. Free.
    build_up(...)       does the solve, counts every group multiplication,
                        and returns x with g^x ≡ h verified. If the predicted
                        cost exceeds the caller's budget it REFUSES
                        (`AscentNotFree`) and names the owed constraint: a
                        smoother order — there is no cheaper route in this
                        toolset. That refusal is the result.

GUARANTEE. Exact and exhaustive: for the checked primes, EVERY element of the
subgroup ⟨g⟩ is solved and confirmed (`verify`). No sampling.

Standalone (stdlib only): Miller–Rabin (deterministic bases), trial division
and Pollard–Brent for factoring, baby-step giant-step for the prime-order
subgroups.
"""
from __future__ import annotations

from functools import lru_cache
from math import gcd, isqrt
from typing import Any, Dict, List, Tuple

from ..lines import AscentNotFree

NAME = "pohlig_hellman"
LINE = "both"


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0:
            return n == q
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):        # deterministic for n < 3.3e24
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    c = 1
    while True:
        x = y = 2
        d = 1
        f = lambda v: (v * v + c) % n
        while d == 1:
            x, y = f(x), f(f(y))
            d = gcd(abs(x - y), n)
        if d != n:
            return d
        c += 1


def factor(n: int) -> Dict[int, int]:
    return dict(_factor_t(n))


@lru_cache(maxsize=None)
def _factor_t(n: int) -> Tuple[Tuple[int, int], ...]:
    out: Dict[int, int] = {}
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        while n % q == 0:
            out[q] = out.get(q, 0) + 1
            n //= q
    stack = [n] if n > 1 else []
    while stack:
        m = stack.pop()
        if m == 1:
            continue
        if is_prime(m):
            out[m] = out.get(m, 0) + 1
            continue
        d = _rho(m)
        stack += [d, m // d]
    return tuple(sorted(out.items()))


def element_order(g: int, p: int, fac: Dict[int, int]) -> int:
    n = p - 1
    o = n
    for q in fac:
        while o % q == 0 and pow(g, o // q, p) == 1:
            o //= q
    return o


class _Counter:
    def __init__(self) -> None:
        self.mults = 0


def _bsgs(gamma: int, delta: int, q: int, p: int, ctr: _Counter) -> int:
    """x in [0,q) with gamma^x = delta (mod p), gamma of prime order q."""
    m = isqrt(q) + 1
    table, cur = {}, 1
    for j in range(m):
        table.setdefault(cur, j)
        cur = cur * gamma % p
        ctr.mults += 1
    factor_ = pow(gamma, -m, p)
    ctr.mults += m.bit_length()
    cur = delta
    for i in range(m + 1):
        if cur in table:
            return (i * m + table[cur]) % q
        cur = cur * factor_ % p
        ctr.mults += 1
    raise ValueError("no discrete log in subgroup: h is not in <g>")


def _crt(rs: List[Tuple[int, int]]) -> Tuple[int, int]:
    x, M = 0, 1
    for r, m in rs:
        t = ((r - x) * pow(M, -1, m)) % m if m > 1 else 0
        x += M * t
        M *= m
    return x % M, M


def predicted_cost(fac: Dict[int, int]) -> int:
    """Σ eᵢ · 2√qᵢ group operations (baby steps + giant steps)."""
    return sum(e * 2 * (isqrt(q) + 1) for q, e in fac.items())


def descend(x, **_) -> Dict[str, Any]:
    p, g, h = x if not isinstance(x, dict) else (x["p"], x["g"], x["h"])
    if not is_prime(p):
        raise ValueError("p must be prime")
    fac_all = factor(p - 1)
    n = element_order(g, p, fac_all)
    fac = factor(n)
    return {
        "toolset": NAME, "p": p,
        "group_order_p_minus_1": p - 1, "factorisation_p_minus_1": fac_all,
        "order_of_g": n, "order_lineage": fac,
        "omega": sum(fac.values()),
        "largest_prime_factor": max(fac) if fac else 1,
        "h_in_subgroup": pow(h, n, p) == 1,
        "predicted_cost_group_ops": predicted_cost(fac),
        "naive_bsgs_cost": 2 * (isqrt(n) + 1),
        "note": "the cost is set by the largest prime factor of the order — not by the order",
    }


def build_up(target, budget: int = 5_000_000, **_) -> Dict[str, Any]:
    if not (isinstance(target, dict) and {"p", "g", "h"} <= set(target)):
        raise AscentNotFree("{'p': prime, 'g': base, 'h': target, 'budget': group-op cap}")
    budget = int(target.get("budget", budget))
    p, g, h = target["p"], target["g"], target["h"]
    d = descend({"p": p, "g": g, "h": h})
    if not d["h_in_subgroup"]:
        raise ValueError("h is not in the subgroup generated by g — no discrete log exists")
    if d["predicted_cost_group_ops"] > budget:
        raise AscentNotFree(
            f"a smoother group order: the largest prime factor {d['largest_prime_factor']} "
            f"needs ≈{d['predicted_cost_group_ops']} group operations, over the budget {budget}",
            "Pohlig–Hellman reduces the cost to the largest prime factor and no further; "
            "that residue is where the hardness lives")
    n, fac = d["order_of_g"], d["order_lineage"]
    ctr = _Counter()
    residues = []
    for q, e in fac.items():
        ord_ = q ** e
        g_sub = pow(g, n // ord_, p)
        h_sub = pow(h, n // ord_, p)
        gamma = pow(g_sub, q ** (e - 1), p)
        x = 0
        for k in range(e):
            t = pow(pow(g_sub, -x, p) * h_sub % p, q ** (e - 1 - k), p)
            ctr.mults += 2 * ord_.bit_length()
            dig = _bsgs(gamma, t, q, p, ctr)
            x += dig * q ** k
        residues.append((x, ord_))
    x, M = _crt(residues)
    assert M == n
    ok = pow(g, x, p) == h % p
    return {"toolset": NAME, "direction": "solve gˣ = h", "x": x, "modulus": n,
            "verified": ok, "cost": ctr.mults, "predicted_cost": d["predicted_cost_group_ops"],
            "order_lineage": fac,
            "note": "per-prime-power digits by BSGS in prime-order subgroups, glued by CRT"}


def verify() -> Dict[str, Any]:
    # 1. EXHAUSTIVE: every element of <g> solved and confirmed, for smooth-order primes
    ok_exh, total = True, 0
    for p in (97, 1009, 8101, 10501):
        assert is_prime(p)
        fac = factor(p - 1)
        g = next(a for a in range(2, p) if element_order(a, p, fac) == p - 1)
        cur = 1
        for x0 in range(p - 1):
            r = build_up({"p": p, "g": g, "h": cur})
            if not (r["verified"] and r["x"] == x0):
                ok_exh = False
            cur = cur * g % p
            total += 1

    # 2. an element of NON-full order: g of order dividing p-1, h in <g>
    p = 8101
    fac = factor(p - 1)
    gfull = next(a for a in range(2, p) if element_order(a, p, fac) == p - 1)
    g = pow(gfull, 12, p)                              # order (p-1)/12 = 675
    n = element_order(g, p, fac)
    h = pow(g, 400, p)
    r = build_up({"p": p, "g": g, "h": h})
    ok_sub = n == 675 and r["x"] == 400 and r["verified"]

    # 3. a large smooth prime (NTT prime 7·2²⁶+1): solved in a handful of operations
    P = 469762049
    assert is_prime(P)
    r = build_up({"p": P, "g": 3, "h": pow(3, 123456789, P)})
    ok_big = r["verified"] and r["x"] == 123456789 and r["cost"] < 200_000

    # 4. the honest refusal: a safe prime has a prime factor ≈ p/2 — over budget, refused
    p_safe = 1000000007                                # (p-1)/2 = 500000003 is prime
    d = descend({"p": p_safe, "g": 5, "h": 12345})
    ok_lin = d["largest_prime_factor"] == 500000003
    try:
        build_up({"p": p_safe, "g": 5, "h": pow(5, 999, p_safe), "budget": 10_000})
        ok_refuse = False
    except AscentNotFree as e:
        ok_refuse = "500000003" in e.owed

    # 5. descend predicts, build_up measures — measured cost is within 4× the prediction
    r = build_up({"p": 8101, "g": next(a for a in range(2, 8101)
                                       if element_order(a, 8101, factor(8100)) == 8100), "h": 4321})
    ok_pred = r["cost"] <= 4 * r["predicted_cost"] + 200

    try:
        build_up({})
        ok_refuse2 = False
    except AscentNotFree:
        ok_refuse2 = True

    return {"ok": all([ok_exh, ok_sub, ok_big, ok_lin, ok_refuse, ok_pred, ok_refuse2]),
            "every_element_solved": ok_exh, "elements_checked": total,
            "subgroup_of_order_675": ok_sub, "ntt_prime_469762049": ok_big,
            "big_prime_cost": r["cost"],
            "safe_prime_largest_factor_found": ok_lin, "safe_prime_refused_over_budget": ok_refuse,
            "measured_cost_within_prediction": ok_pred, "refuses_without_target": ok_refuse2}


if __name__ == "__main__":
    print(descend({"p": 469762049, "g": 3, "h": 5}))
    print(verify())
