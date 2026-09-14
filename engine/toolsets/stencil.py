"""
GenerationalLineage.engine.toolsets.stencil
=============================================
STENCIL — the digit-by-digit decomposition machine.

Cody, 2026-09-13: "i don't care about pruning...this is a decomposition
machine" — "RSA was just common context to use." Not a race against
exhaustive search (that comparison is the wrong axis, and this module does
not make it); a CONSTRUCTIVE, EXACT, GUARANTEED pathway from N to its
factors, the same way long multiplication is a constructive, exact,
traceable pathway from (p,q) to N — carries and all, nothing skipped,
nothing approximated. The hand-worked photograph of 1546854629 x 7283619945
(an hour, two caught errors from a single dropped carry propagating) is
literally what DESCEND looks like when the pathway is walked by hand rather
than assumed free — it is cost-0 in the sense that no SEARCH is needed, not
in the sense that no WORK exists. BUILD_UP is that same kind of pathway,
walked in the other direction, and it is allowed to be long: `cost` reports
how long, honestly, never minimised.

DESCEND (free): given p and q, N = p*q — one multiplication, no search.

BUILD_UP (work): given only N, construct candidate factor pairs digit by
digit. Two slides over the same (p,q) domain, kept SEPARATE here on
purpose (they build from opposite ends of the number — combining them
needs an actual meet-in-the-middle overlap check, not a splice of two
different partial representations; that combination is real, open design
work, not done in this pass — see the module TODO at the bottom):

  SLIDE 1 (bottom-up, exact — `_slide1`): a candidate (P,Q) prefix-pair
  survives from depth k-1 to k only if P*Q matches N's low k+1 digits
  EXACTLY (an integer equality — "can't propagate any borrowing from 10").
  Run to full depth (k = len(str(N))), this is already a COMPLETE,
  GUARANTEED, EXACT decomposition procedure: the exact-equality filter at
  the end is trivial once depth == digit length, and every genuine divisor
  pair of N survives by construction (proved, not assumed — a candidate
  can only be eliminated by failing an EXACT modular equality that every
  real divisor pair satisfies at every depth). It reports every divisor
  pair, not just the "intended" one — a real, correct-by-construction
  side effect of doing this exactly rather than heuristically.

  SLIDE 2 (top-down, magnitude + primality — `_slide2_candidates`):
  hypothesize p's LEADING m digits; the corresponding q = N/p window,
  computed EXACTLY (Fraction, never float), either contains no integer at
  all (a real, provable elimination — not a heuristic) or contains one or
  more; requiring at least one PRIME in that window is a second, different,
  exact filter, kept here as an independent generator over the same domain,
  not yet stitched to slide 1's low-digit output.

Guarantee: slide 1 run to full depth is exhaustive and exact. If N has a
nontrivial factorization it WILL be found; if N is prime, build_up raises
AscentNotFree — the refusal is the result, not a failure (scale.py's own
phrasing for the same idea).
"""
from __future__ import annotations

import math
from fractions import Fraction
from typing import Any, Dict, List, Tuple

from ..lines import AscentNotFree

NAME = "stencil"
LINE = "both"


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    for d in range(3, math.isqrt(n) + 1, 2):
        if n % d == 0:
            return False
    return True


def descend(p: int, q: int) -> Dict[str, Any]:
    """FREE: multiply. One pass, cost 0 — the same pathway the hand-worked
    long multiplication walks explicitly, carry by carry."""
    if p < 2 or q < 2:
        raise ValueError("p and q must each be >= 2")
    return {"toolset": NAME, "p": p, "q": q, "N": p * q, "cost": 0}


def _slide1(N: int, depth: int) -> Tuple[List[Tuple[int, int]], int]:
    """bottom-up: exact low-digit congruence, depth by depth (0-indexed —
    depth=len(str(N)) resolves every digit). Returns (survivors, cost),
    cost = total prefix-pairs ever constructed and tested, reported
    honestly — this is the ascent, being expensive is not a defect."""
    candidates = [(0, 0)]
    cost = 0
    for k in range(depth):
        mod = 10 ** (k + 1)
        nxt = []
        for P, Q in candidates:
            for dp in range(10):
                for dq in range(10):
                    cost += 1
                    Pk, Qk = P + dp * 10**k, Q + dq * 10**k
                    if (Pk * Qk) % mod == N % mod:
                        nxt.append((Pk, Qk))
        candidates = nxt
    return candidates, cost


def _slide2_window_primes(N: int, P: int, m: int, n_p: int) -> List[int]:
    """top-down: q-window implied by p's leading m digits (prefix P out of
    an eventual n_p-digit p), exact via Fraction — the primes it contains,
    if any. An empty result is a proof, not a guess: no integer q in that
    window can possibly pair with any p in [P*10^(n_p-m), (P+1)*10^(n_p-m))."""
    lo_p = P * 10 ** (n_p - m)
    hi_p = (P + 1) * 10 ** (n_p - m)
    q_lo, q_hi = Fraction(N, hi_p), Fraction(N, lo_p)
    first_int, last_int = math.floor(q_lo) + 1, math.floor(q_hi)
    return [q for q in range(first_int, last_int + 1) if _is_prime(q)]


def _slide2(N: int, n_p: int) -> Tuple[List[int], int]:
    """top-down, run to full depth n_p: surviving leading-digit prefixes of
    p whose implied q-window contains at least one prime, at every depth
    along the way. Returns (survivors, cost)."""
    candidates = [0]
    cost = 0
    for m in range(1, n_p + 1):
        nxt = []
        for P in candidates:
            for d in range(10):
                if m == 1 and d == 0:
                    continue
                cost += 1
                newP = P * 10 + d
                if _slide2_window_primes(N, newP, m, n_p):
                    nxt.append(newP)
        candidates = nxt
    return candidates, cost


def build_up(N: int, run_slide2: bool = False) -> Dict[str, Any]:
    """WORK: construct N's factor pairs digit by digit (slide 1, exact,
    exhaustive). Reports `cost` honestly. Raises AscentNotFree if N is
    prime — no nontrivial (p,q) exists, and that is the correct answer,
    not a search failure. Pass run_slide2=True to also run the top-down
    construction (over one factor's own digit length) and report its
    surviving leading-digit prefixes alongside — the two slides are NOT
    combined here (see the module docstring's meet-in-the-middle note)."""
    if N < 4:
        raise ValueError("N must be >= 4")
    if _is_prime(N):
        raise AscentNotFree(f"N={N} is prime", f"{N} has no nontrivial (p,q)")

    n_digits = len(str(N))
    survivors, cost1 = _slide1(N, n_digits)
    pairs = sorted({tuple(sorted((P, Q))) for P, Q in survivors
                    if P * Q == N and P > 1 and Q > 1})

    out: Dict[str, Any] = {
        "toolset": NAME, "N": N, "pairs": pairs,
        "cost": cost1, "slide1_final_prefixes": len(survivors),
    }
    if run_slide2:
        n_p = n_digits // 2
        s2_survivors, cost2 = _slide2(N, n_p)
        out["slide2_leading_prefixes"] = s2_survivors
        out["slide2_cost"] = cost2
        out["cost"] += cost2
    return out


def verify() -> Dict[str, Any]:
    checks: Dict[str, bool] = {}

    d = descend(37, 41)
    checks["descend_multiplies_exactly"] = d["N"] == 1517

    b = build_up(1517)
    checks["build_up_finds_the_pair"] = (37, 41) in b["pairs"]

    b_multi = build_up(60)   # 2^2*3*5 -- several nontrivial pairs
    checks["build_up_finds_every_divisor_pair"] = set(b_multi["pairs"]) >= {
        (2, 30), (3, 20), (4, 15), (5, 12), (6, 10),
    }

    try:
        build_up(97)          # prime
        checks["prime_raises_ascent_not_free"] = False
    except AscentNotFree:
        checks["prime_raises_ascent_not_free"] = True

    ok = all(checks.values())
    return {"toolset": NAME, "ok": ok, "checks": checks}


# ── TODO (open, not done here) ──────────────────────────────────────────
# The meet-in-the-middle combination of slide 1 (low digits, growing from
# the bottom) and slide 2 (high digits, growing from the top): once a
# slide-1 prefix of depth j and a slide-2 prefix of depth m satisfy
# j + m >= n_digits, their digits overlap in the middle by (j+m-n_digits)
# positions -- checking that overlap for agreement, rather than re-deriving
# it from scratch, is what would let the two slides actually cut each
# other's cost instead of running side by side. Real design work, flagged
# rather than forced.
