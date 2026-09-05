"""
GenerationalLineage.engine.toolsets.comma_sequence
=================================================
THE COMMA GROUP (separator) decomposition — the step lives IN the separator.

Numberphile "The Immortal Kangaroo Sequence"; Angelini, Guy & Sloane,
"The Comma Sequence: A Simple Sequence With Bizarre Properties"
(arXiv:2401.14346); "The Comma Sequence is Finite in Other Bases"
(arXiv:2408.03434).

RULE (base b): write the walk with commas.  The gap across a comma is the
two-digit number straddling it —

    a(n+1) - a(n)  =  b * L  +  R ,
      L = last digit of a(n)   (just LEFT of the comma)
      R = leading digit of a(n+1)  (just RIGHT of the comma), R in 1..b-1

so a(n+1) is forced into a window of width b-1, and the earliest valid R
wins.  When no R makes the leading digit match, the kangaroo has hit a
landmine — the walk is MORTAL.  Base 10 dies at 99,999,945 (2,137,453
terms).  Bases 3..633 all die; b >= 634 (and a rule tweak) go immortal.

DECOMPOSITION (free): read a given sequence's steps straight off its commas
in one pass — is it a valid comma walk, and where (if ever) does it die?
"Spectral resolution" here is a RATIO, not a bandwidth: the step alphabet
is b*b values, the comma window is 2 digits — resolution = b:2, a
local:global magnification (the Flashlight), and mortality is the coarse
end of it.

EMERGER (work): generate the lexicographically-earliest comma walk forward,
placing one term at a time until it dies or n_terms is reached.  cost =
terms placed.
"""
from __future__ import annotations

from typing import Any, Dict, List, Sequence

NAME = "comma_sequence"
LINE = "both"

IMMORTAL_BASE = 634          # first base with no landmine (arXiv:2408.03434)


def _lead(n: int, base: int) -> int:
    n = abs(int(n))
    while n >= base:
        n //= base
    return n


def _next_term(cur: int, base: int) -> int | None:
    """The one forced successor, or None if the kangaroo dies here."""
    lo = cur % base
    for r in range(1, base):                 # earliest valid R wins
        cand = cur + base * lo + r
        if _lead(cand, base) == r:
            return cand
    return None


# ── decomposition (free) — one pass over the commas ────────────────────────
def descend(seq: Sequence[int], base: int = 10) -> Dict[str, Any]:
    s = [int(x) for x in seq]
    if len(s) < 2:
        raise ValueError("need at least two terms to read a comma")
    steps: List[Dict[str, Any]] = []
    valid = True
    first_break = None
    for i in range(len(s) - 1):
        a, b_ = s[i], s[i + 1]
        L = a % base
        R = _lead(b_, base)
        gap = b_ - a
        want = base * L + R
        ok = (gap == want) and (1 <= R < base) and (b_ > a)
        steps.append({"i": i, "a": a, "b": b_, "gap": gap,
                      "L": L, "R": R, "reads_as": want, "ok": ok})
        if not ok and valid:
            valid = False
            first_break = i
    # would the (valid prefix of the) walk have a next term, or is it a landmine?
    landmine = None
    if valid:
        nxt = _next_term(s[-1], base)
        landmine = (nxt is None)
    return {
        "toolset": NAME, "line": "decomposition",
        "base": base, "n_terms": len(s),
        "valid_comma_walk": valid, "first_break": first_break,
        "steps": steps,
        "at_landmine": landmine,                 # None if the walk was already invalid
        "resolution_ratio": f"{base * base}:2",  # step alphabet : comma window
        "step_alphabet": base * base,
        "mortal_base": base < IMMORTAL_BASE,
        "note": "one pass — the gap is read from the two digits straddling each comma",
    }


# ── emerger (work) — walk it forward, one term at a time ───────────────────
def build_up(n_terms: int, base: int = 10, start: int = 1) -> Dict[str, Any]:
    if n_terms < 1:
        raise ValueError("n_terms must be >= 1")
    seq = [int(start)]
    died_at = None
    while len(seq) < n_terms:
        nxt = _next_term(seq[-1], base)
        if nxt is None:
            died_at = len(seq)                   # length reached before the landmine
            break
        seq.append(nxt)
    return {
        "toolset": NAME, "line": "emerger",
        "base": base, "start": int(start),
        "sequence": seq, "length": len(seq),
        "cost": len(seq),                        # terms placed
        "reached_target": len(seq) == n_terms,
        "died_at": died_at,                      # None => still alive at n_terms
        "immortal_base": base >= IMMORTAL_BASE,
        "note": "lexicographically-earliest comma walk, one term per step",
    }


def verify() -> Dict[str, Any]:
    # independently attested head (Numberphile / arXiv:2401.14346 / the
    # worked example 12,35 -> 35-12 = 23 = concat(2,3))
    HEAD = [1, 12, 35, 94, 135]
    b = build_up(len(HEAD), base=10)
    ok_b = b["sequence"] == HEAD and b["cost"] == len(HEAD)

    walk = build_up(400, base=10)["sequence"]                # a longer valid prefix
    d = descend(walk, base=10)
    ok_d = d["valid_comma_walk"] and d["first_break"] is None and d["at_landmine"] is False

    bad = descend([1, 12, 36], base=10)          # 36-12 = 24, but the comma reads 2,3 -> 23
    ok_bad = (not bad["valid_comma_walk"]) and bad["first_break"] == 1

    # base 10 is MORTAL — the landmine is exactly at 99,999,945 (2,137,453 terms)
    ok_mortal = (_next_term(99999945, 10) is None
                 and _next_term(99999995, 10) is not None)

    # a large base is IMMORTAL — no landmine reachable
    ok_immortal = all(_next_term(x, IMMORTAL_BASE) is not None
                      for x in (5, 12345, IMMORTAL_BASE ** 2 + 7))

    return {"ok": all([ok_b, ok_d, ok_bad, ok_mortal, ok_immortal]),
            "build_up_head": ok_b,
            "descend_valid_over_400": ok_d,
            "descend_catches_break": ok_bad,
            "base10_landmine_at_99999945": ok_mortal,
            "base634_immortal": ok_immortal}


if __name__ == "__main__":
    import json
    print(json.dumps(build_up(11), indent=1))
    print(json.dumps(descend([1, 12, 35, 94, 155]), indent=1))
    print(verify())
