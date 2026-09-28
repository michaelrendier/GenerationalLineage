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
GenerationalLineage.engine.toolsets.periodicity
================================================
PERIODICITY — every period of a string, EXACTLY, plus the Fine–Wilf theorem
that says why the GCD-vote works.

`cipher.py` recovers a key length by voting over the factors of the
repeat-distance gaps (Kasiski). That is an *estimate*: a coincidental short
repeat can drag the gcd to 1. This toolset is the guarantee-first
counterpart — no votes, no thresholds:

    prefix function  π[i]   longest proper border of s[:i+1]
    borders                 the chain n → π[n-1] → π[π[n-1]-1] → … → 0
    periods                 p is a period  ⇔  n−p is a border      (exact, all of them)
    Z function       z[i]   longest common prefix of s and s[i:]
                            p is a period  ⇔  z[p] = n−p           (a second, independent route)

FINE–WILF (1965)
----------------
If a string of length n has periods p and q and n ≥ p + q − gcd(p,q), then
gcd(p,q) is also a period. This is the theorem behind "the period is the
GCD of the gaps": two periods that overlap enough *force* their gcd. The
bound is tight, and `build_up` constructs the extremal word — length
p + q − gcd − 1 with both periods and not the gcd — so the tightness is
witnessed, not quoted.

DECOMPOSITION (free): one linear pass (prefix function), every period read
off the border chain. The generation length of a string is its exponent
e = n/p over its primitive period p (when p | n): a^64 is generation-6 in
the SCALE sense, (ab)^32 is the same word one letter up.

EMERGER (work): `build_up({'root': w, 'length': n})` writes the periodic
string (the choice is the root word); `build_up({'p': p, 'q': q})` builds the
Fine–Wilf extremal word. Neither given → AscentNotFree.
"""
from __future__ import annotations

from math import gcd
from typing import Any, Dict, List, Sequence

from ..lines import AscentNotFree

NAME = "periodicity"
LINE = "both"


def prefix_function(s: Sequence) -> List[int]:
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        k = pi[i - 1]
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


def z_function(s: Sequence) -> List[int]:
    n = len(s)
    z = [0] * n
    if n:
        z[0] = n
    l = r = 0
    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]
    return z


def borders(s: Sequence) -> List[int]:
    """All proper borders (prefix that is also a suffix), longest first."""
    pi = prefix_function(s)
    out, k = [], pi[-1] if pi else 0
    while k:
        out.append(k)
        k = pi[k - 1]
    return out


def periods(s: Sequence) -> List[int]:
    """Every period p in 1..n, ascending (n itself is always a period)."""
    n = len(s)
    if n == 0:
        return []
    return sorted([n - b for b in borders(s)] + [n])


def periods_bruteforce(s: Sequence) -> List[int]:
    n = len(s)
    return [p for p in range(1, n + 1)
            if all(s[i] == s[i + p] for i in range(n - p))]


def periods_via_z(s: Sequence) -> List[int]:
    n = len(s)
    if n == 0:
        return []
    z = z_function(s)
    return [p for p in range(1, n) if z[p] == n - p] + [n]


def fine_wilf_holds(s: Sequence) -> bool:
    """For every pair of periods p,q with p+q-gcd <= n, gcd(p,q) is a period."""
    n = len(s)
    P = set(periods(s))
    for p in P:
        for q in P:
            if p <= q and p + q - gcd(p, q) <= n and gcd(p, q) not in P:
                return False
    return True


def fine_wilf_extremal(p: int, q: int) -> str:
    """Word of length p+q-gcd-1 with periods p and q but NOT period gcd(p,q).
    Positions i~i+p and i~i+q are unioned; each component gets its own letter.
    Requires neither of p, q to divide the other (else gcd is trivially forced)."""
    g = gcd(p, q)
    if p % q == 0 or q % p == 0:
        raise ValueError("p divides q (or vice versa): the gcd is a period of anything with period p")
    n = p + q - g - 1
    parent = list(range(n))

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i in range(n):
        for d in (p, q):
            if i + d < n:
                parent[find(i)] = find(i + d)
    label: Dict[int, int] = {}
    out = []
    for i in range(n):
        r = find(i)
        label.setdefault(r, len(label))
        out.append(label[r])
    return "".join(chr(ord("a") + c) if c < 26 else chr(0x3b1 + c - 26) for c in out)


def descend(x, **_) -> Dict[str, Any]:
    """The FREE read: every period, exactly, by one linear pass."""
    s = list(x) if not isinstance(x, str) else x
    n = len(s)
    P = periods(s)
    if not P:
        return {"toolset": NAME, "n": 0, "periods": [], "note": "empty input"}
    pmin = P[0]
    exact_root = (n % pmin == 0)
    return {
        "toolset": NAME, "n": n,
        "periods": P, "min_period": pmin,
        "borders": borders(s),
        "primitive_root": s[:pmin] if exact_root else None,
        "exponent": n // pmin if exact_root else None,
        "fractional_exponent": n / pmin,
        "is_primitive": not (exact_root and n // pmin > 1),
        "agrees_with_z_function": P == periods_via_z(s),
        "fine_wilf_holds": fine_wilf_holds(s),
        "guarantee": "exact and exhaustive — every period listed, none voted",
        "note": "exponent = generation length: how many copies of the primitive root",
    }


def build_up(target, **_) -> Dict[str, Any]:
    if isinstance(target, dict) and "root" in target and "length" in target:
        root, n = target["root"], int(target["length"])
        if not root:
            raise ValueError("root is empty")
        w = (root * (n // len(root) + 1))[:n]
        return {"toolset": NAME, "direction": "root -> periodic string",
                "string": w, "cost": n,
                "note": "the choice is the root word; every period then follows"}
    if isinstance(target, dict) and "p" in target and "q" in target:
        w = fine_wilf_extremal(int(target["p"]), int(target["q"]))
        return {"toolset": NAME, "direction": "Fine-Wilf extremal word",
                "string": w, "length": len(w), "periods": periods(w),
                "cost": len(w),
                "note": "one letter short of forcing gcd(p,q) — the bound is tight"}
    raise AscentNotFree("a root word and length, or a period pair {'p','q'}",
                        "descend() lists every period of a string for free; "
                        "to build one you must choose the root")


def verify() -> Dict[str, Any]:
    # 1. hand-checked value
    ok_known = periods("abcabcabca") == [3, 6, 9, 10]

    # 2. exhaustive: all binary strings up to length 14 — three independent routes agree,
    #    and Fine–Wilf holds for every one.
    n_checked = 0
    ok_all = True
    for n in range(1, 15):
        for m in range(1 << n):
            s = [(m >> i) & 1 for i in range(n)]
            b = periods_bruteforce(s)
            if not (periods(s) == b == periods_via_z(s) and fine_wilf_holds(s)):
                ok_all = False
                break
            n_checked += 1
        if not ok_all:
            break

    # 3. tightness: the extremal word has both periods, not the gcd
    ok_tight, pairs = True, 0
    for p in range(2, 10):
        for q in range(p + 1, 10):
            if p % q == 0 or q % p == 0:
                continue
            w = fine_wilf_extremal(p, q)
            P = periods(w)
            g = gcd(p, q)
            if not (len(w) == p + q - g - 1 and p in P and q in P and g not in P):
                ok_tight = False
            pairs += 1

    # 4. the ascent contract
    d = descend("ab" * 32)
    ok_desc = d["min_period"] == 2 and d["exponent"] == 32 and d["agrees_with_z_function"]
    try:
        build_up({})
        ok_refuse = False
    except AscentNotFree:
        ok_refuse = True
    ok_up = build_up({"root": "abc", "length": 10})["string"] == "abcabcabca"

    return {"ok": all([ok_known, ok_all, ok_tight, ok_desc, ok_refuse, ok_up]),
            "hand_checked": ok_known,
            "exhaustive_binary_strings_le_14": ok_all, "strings_checked": n_checked,
            "fine_wilf_tight": ok_tight, "pairs_checked": pairs,
            "descend_exponent": ok_desc, "refuses_without_root": ok_refuse,
            "build_up_root": ok_up}


if __name__ == "__main__":
    print(descend("abaababaabaababaababa"))
    print(build_up({"p": 5, "q": 8}))
    print(verify())
