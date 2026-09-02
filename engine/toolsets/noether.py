"""
GenerationalLineage.engine.toolsets.noether
============================================
NOETHER — the invariant the domain conserves, on BOTH lines.

The two trees counter-rotate: along any decomposition the red current and the
blue current trade, and their sum is fixed. `J_red + J_blue = const`.

DECOMPOSITION (free): given the (j_red, j_blue) readings taken along a descent,
check the sum held. One pass over the readings.

EMERGER (work): given a set of candidate build orders and the conserved total,
keep only the orders whose running partial sums never exceed the total — the
conservation law filtering the legal ascent set. `cost` = orders scanned.
"""
from __future__ import annotations

from typing import Any, Dict, List, Sequence, Tuple

NAME = "noether"
LINE = "both"


def descend(readings: Sequence[Tuple[float, float]], tol: float = 1e-9) -> Dict[str, Any]:
    sums = [r + b for r, b in readings]
    if not sums:
        return {"toolset": NAME, "conserved": True, "sums": [], "note": "no readings"}
    ref = sums[0]
    drift = max(abs(s - ref) for s in sums)
    return {"toolset": NAME, "n_readings": len(readings), "total": ref,
            "max_drift": drift, "conserved": drift <= tol,
            "note": "one pass over the readings — the free reading"}


def build_up(orders: Sequence[Sequence[float]], total: float,
             tol: float = 1e-9) -> Dict[str, Any]:
    """orders: candidate emergence orders, each a sequence of per-step
    red-current increments. Keep those whose running sum stays within [0, total]."""
    legal: List[int] = []
    scanned = 0
    for i, order in enumerate(orders):
        scanned += 1
        run = 0.0
        ok = True
        for step in order:
            run += step
            if run < -tol or run > total + tol:
                ok = False
                break
        if ok and abs(run - total) <= tol:
            legal.append(i)
    return {"toolset": NAME, "n_orders": len(orders), "legal": legal,
            "n_legal": len(legal), "cost": scanned, "total": total,
            "note": "conservation filtered the ascent set"}


def verify() -> Dict[str, Any]:
    # constant-sum synthetic passes; a drifting one fails
    good = [(0.3, 0.7), (0.5, 0.5), (0.1, 0.9)]
    bad = [(0.3, 0.7), (0.6, 0.5)]
    ok_d = descend(good)["conserved"] and not descend(bad)["conserved"]
    b = build_up([[0.5, 0.3, 0.2], [0.9, 0.5, -0.4], [0.5, 0.6]], total=1.0)
    ok_b = b["legal"] == [0] and b["cost"] == 3
    return {"ok": ok_d and ok_b, "descend": ok_d, "build_up": ok_b}


if __name__ == "__main__":
    print(descend([(0.3, 0.7), (0.5, 0.5)]))
    print(build_up([[0.5, 0.3, 0.2], [0.9, 0.5, -0.4]], total=1.0))
    print(verify())
