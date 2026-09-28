"""
GenerationalLineage.engine.toolsets.lyndon
===========================================
LYNDON — the unique prime factorisation of a WORD.

A Lyndon word is a string strictly smaller than every one of its proper
rotations — a necklace's canonical, primitive representative. The
Chen–Fox–Lyndon theorem: **every word factors uniquely as a concatenation of
Lyndon words in non-increasing order.** It is the string analogue of the
fundamental theorem of arithmetic — and the Lyndon words are the primes.

    integers                     words
    ----------------------       -----------------------------------
    prime                        Lyndon word
    n = p₁ ≥ p₂ ≥ … ≥ p_k        w = l₁ ≥ l₂ ≥ … ≥ l_k   (lexicographic)
    Ω(n) = k                     number of Lyndon factors
    gcd/lcm via exponents        primitive root + exponent

Duval's algorithm does the factorisation in one linear pass, no backtracking
— a FREE descent. It also hands over:

    least rotation      the canonical necklace representative (Duval on w·w)
    primitive root      smallest u with w = uᵏ ; k is the exponent
    counting            Lyndon words of length n over k letters: (1/n)Σ μ(d)·k^(n/d)
                        necklaces: (1/n) Σ φ(d)·k^(n/d)   (Burnside)

EMERGER (work): `build_up({'n': n, 'k': k})` enumerates the Lyndon words of
length n (FKM/Duval generation) — cost = words emitted, checked against the
Möbius count. `build_up({'factors': [...]})` reassembles a word from Lyndon
words (sorted non-increasing — the only legal order, so this leg is free).
"""
from __future__ import annotations

from typing import Any, Dict, List, Sequence

from ..lines import AscentNotFree

NAME = "lyndon"
LINE = "both"


def duval(s: Sequence) -> List[Sequence]:
    """Chen–Fox–Lyndon factorisation, Duval's linear-time algorithm."""
    n, i, out = len(s), 0, []
    while i < n:
        j, k = i + 1, i
        while j < n and s[k] <= s[j]:
            k = i if s[k] < s[j] else k + 1
            j += 1
        while i <= k:
            out.append(s[i:i + j - k])
            i += j - k
    return out


def is_lyndon(w: Sequence) -> bool:
    n = len(w)
    return n > 0 and all(w < w[i:] for i in range(1, n))


def least_rotation_index(s: Sequence) -> int:
    """Start index of the lexicographically least rotation (via Duval on s+s)."""
    n = len(s)
    if n == 0:
        return 0
    d = s + s
    i, ans = 0, 0
    while i < n:
        ans = i
        j, k = i + 1, i
        while j < 2 * n and d[k] <= d[j]:
            k = i if d[k] < d[j] else k + 1
            j += 1
        while i <= k:
            i += j - k
    return ans


def primitive_root(s: Sequence):
    n = len(s)
    for p in range(1, n + 1):
        if n % p == 0 and s == s[:p] * (n // p):
            return s[:p], n // p
    return s, 1


def _mobius(n: int) -> int:
    m, d, r = n, 2, 1
    while d * d <= m:
        if m % d == 0:
            m //= d
            if m % d == 0:
                return 0
            r = -r
        d += 1
    return -r if m > 1 else r


def _phi(n: int) -> int:
    r, m, d = n, n, 2
    while d * d <= m:
        if m % d == 0:
            while m % d == 0:
                m //= d
            r -= r // d
        d += 1
    if m > 1:
        r -= r // m
    return r


def lyndon_count(n: int, k: int) -> int:
    return sum(_mobius(d) * k ** (n // d) for d in range(1, n + 1) if n % d == 0) // n


def necklace_count(n: int, k: int) -> int:
    return sum(_phi(d) * k ** (n // d) for d in range(1, n + 1) if n % d == 0) // n


def generate_lyndon(n: int, k: int):
    """All Lyndon words of length exactly n over {0..k-1}, lexicographic (Duval)."""
    w = [-1]
    while w:
        w[-1] += 1
        m = len(w)
        if m == n:
            yield tuple(w)
        while len(w) < n:
            w.append(w[-m])
        while w and w[-1] == k - 1:
            w.pop()


def descend(x, **_) -> Dict[str, Any]:
    s = x if isinstance(x, (str, tuple, list)) else list(x)
    if isinstance(s, list):
        s = tuple(s)
    facs = duval(s)
    nonincreasing = all(facs[i] >= facs[i + 1] for i in range(len(facs) - 1))
    joined = facs[0][:0].join(facs) if isinstance(s, str) else tuple(c for f in facs for c in f)
    r = least_rotation_index(s)
    root, exp = primitive_root(s)
    return {
        "toolset": NAME, "n": len(s),
        "factors": facs, "omega": len(facs),
        "all_lyndon": all(is_lyndon(f) for f in facs),
        "nonincreasing": nonincreasing,
        "reassembles": joined == s,
        "least_rotation_index": r,
        "necklace_representative": s[r:] + s[:r],
        "primitive_root": root, "exponent": exp,
        "guarantee": "unique: exactly one non-increasing Lyndon factorisation exists",
        "note": "Lyndon words are the primes of the word monoid; omega = number of factors",
    }


def build_up(target, **_) -> Dict[str, Any]:
    if isinstance(target, dict) and "n" in target and "k" in target:
        n, k = int(target["n"]), int(target["k"])
        words = list(generate_lyndon(n, k))
        return {"toolset": NAME, "direction": "enumerate Lyndon words",
                "words": words, "count": len(words),
                "expected_count": lyndon_count(n, k),
                "necklaces": necklace_count(n, k),
                "cost": len(words),
                "note": "count matches (1/n) Σ μ(d) k^(n/d) — checked, not assumed"}
    if isinstance(target, dict) and "factors" in target:
        fs = list(target["factors"])
        if not all(is_lyndon(f) for f in fs):
            raise ValueError("every factor must be a Lyndon word")
        fs.sort(reverse=True)
        w = fs[0][:0].join(fs) if isinstance(fs[0], str) else tuple(c for f in fs for c in f)
        return {"toolset": NAME, "direction": "factors -> word",
                "word": w, "cost": len(fs),
                "note": "non-increasing order is the only legal one — this leg is free"}
    raise AscentNotFree("{'n','k'} to enumerate, or {'factors': [...]} to assemble")


def _all_nonincreasing_factorisations(s: str) -> int:
    """Brute-force count of splits into non-increasing Lyndon words (for the uniqueness check)."""
    n = len(s)

    def rec(i: int, prev):
        if i == n:
            return 1
        tot = 0
        for j in range(i + 1, n + 1):
            f = s[i:j]
            if is_lyndon(f) and (prev is None or f <= prev):
                tot += rec(j, f)
        return tot
    return rec(0, None)


def verify() -> Dict[str, Any]:
    # 1. uniqueness, exhaustively: every binary string up to length 10 has EXACTLY ONE
    #    non-increasing Lyndon factorisation, and Duval finds it.
    ok_unique, n_checked = True, 0
    for n in range(1, 11):
        for m in range(1 << n):
            s = format(m, "0{}b".format(n))
            if _all_nonincreasing_factorisations(s) != 1:
                ok_unique = False
            d = descend(s)
            if not (d["all_lyndon"] and d["nonincreasing"] and d["reassembles"]):
                ok_unique = False
            n_checked += 1

    # 2. counts: generation matches the Möbius formula and every word is Lyndon
    ok_count = True
    for n in range(1, 9):
        for k in (2, 3):
            ws = list(generate_lyndon(n, k))
            if not (len(ws) == lyndon_count(n, k) and all(is_lyndon(w) for w in ws)):
                ok_count = False
    # Burnside: necklaces = sum of Lyndon words over divisors
    ok_neck = all(necklace_count(n, 2) == sum(lyndon_count(d, 2) for d in range(1, n + 1) if n % d == 0)
                  for n in range(1, 13))

    # 3. least rotation is the minimum over all rotations
    ok_rot = True
    for n in range(1, 10):
        for m in range(1 << n):
            s = format(m, "0{}b".format(n))
            r = least_rotation_index(s)
            if s[r:] + s[:r] != min(s[i:] + s[:i] for i in range(n)):
                ok_rot = False

    # 4. hand-checked
    ok_known = [str(f) for f in duval("banana")] == ["b", "an", "an", "a"]
    ok_root = primitive_root("abababab") == ("ab", 4)
    try:
        build_up({})
        ok_refuse = False
    except AscentNotFree:
        ok_refuse = True

    return {"ok": all([ok_unique, ok_count, ok_neck, ok_rot, ok_known, ok_root, ok_refuse]),
            "unique_factorisation_binary_le_10": ok_unique, "strings_checked": n_checked,
            "lyndon_count_formula": ok_count, "burnside_necklaces": ok_neck,
            "least_rotation_exhaustive": ok_rot, "banana": ok_known,
            "primitive_root": ok_root, "refuses_without_target": ok_refuse}


if __name__ == "__main__":
    print(descend("abracadabra"))
    print(build_up({"n": 4, "k": 2}))
    print(verify())
