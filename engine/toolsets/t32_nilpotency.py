"""
GenerationalLineage.engine.toolsets.t32_nilpotency
===================================================
T32 NILPOTENCY — address = path. Hyperwebster-style base-B addressing: an
integer address decodes (Horner) to a digit path; a path that, stepped
repeatedly, reaches 0 is NILPOTENT — a path that returns nothing (an
extinction).

DECOMPOSITION (free): decode an address to its path. One Horner sweep.

EMERGER (work): given a target digit pattern, find the smallest address whose
path matches it — placing digits one at a time. `cost` = digits placed.
"""
from __future__ import annotations

from typing import Any, Dict, List

NAME = "t32_nilpotency"
LINE = "both"

BASE = 97                                         # the Hyperwebster base-97 alphabet


def _digits(n: int, base: int = BASE) -> List[int]:
    if n < 0:
        raise ValueError("address must be >= 0")
    if n == 0:
        return [0]
    out: List[int] = []
    while n:
        out.append(n % base)
        n //= base
    return list(reversed(out))


def _from_digits(ds: List[int], base: int = BASE) -> int:
    n = 0
    for d in ds:                                  # Horner
        n = n * base + int(d)
    return n


def descend(address: int, base: int = BASE) -> Dict[str, Any]:
    ds = _digits(int(address), base)
    # NILPOTENT = the path ends on a zero step: it returns nothing. Equivalently
    # the address is a pure multiple of the top place (trailing zero digits).
    trailing_zeros = 0
    for d in reversed(ds):
        if d == 0 and len(ds) > 1:
            trailing_zeros += 1
        else:
            break
    nil = trailing_zeros > 0
    return {"toolset": NAME, "address": int(address), "base": base,
            "path": ds, "length": len(ds),
            "nilpotent": nil, "trailing_zeros": trailing_zeros,
            "note": "one Horner sweep — the free reading"}


def build_up(pattern: List[int], base: int = BASE) -> Dict[str, Any]:
    """Place digits one at a time to realise `pattern` (a list of ints, each
    0..base-1), left to right; the address is the Horner value. `cost` = digits
    placed."""
    placed: List[int] = []
    for d in pattern:
        d = int(d)
        if not (0 <= d < base):
            raise ValueError(f"digit {d} out of range for base {base}")
        placed.append(d)
    address = _from_digits(placed, base)
    round_trip = _digits(address, base) == ([0] if not placed else
                                            [x for x in placed] if placed[0] != 0
                                            else placed)
    return {"toolset": NAME, "pattern": list(pattern), "address": address,
            "digits_placed": len(placed), "cost": len(placed),
            "round_trips": _digits(address, base)[-len(placed):] == placed if placed else True,
            "note": "digits placed one at a time — the work reading"}


def verify() -> Dict[str, Any]:
    d = descend(97 * 97 * 5)                       # 5,0,0 in base 97
    ok_d = d["path"] == [5, 0, 0] and d["nilpotent"]
    d2 = descend(97 * 3 + 11)                      # 3,11 — not a top-place multiple
    ok_d2 = d2["path"] == [3, 11] and not d2["nilpotent"]
    b = build_up([7, 42, 1])
    ok_b = b["address"] == _from_digits([7, 42, 1]) and b["cost"] == 3 and b["round_trips"]
    return {"ok": ok_d and ok_d2 and ok_b,
            "descend_nilpotent": ok_d, "descend_non_nilpotent": ok_d2, "build_up": ok_b}


if __name__ == "__main__":
    print(descend(97 * 97 * 5))
    print(build_up([7, 42, 1]))
    print(verify())
