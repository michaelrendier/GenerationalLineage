"""
GenerationalLineage.engine.toolsets.box_kite
=============================================
BOX KITE — the domain geometry the decomposition happens in.

16 Cayley-Dickson placeholders e0..e15. The 15 nonzero XOR differences between
them are the EDGES — kinds of relation, not places. A LINE is three relations
that compose: `a ^ b = c`. A PENCIL is the 7 ways to factor one relation into
two others.

DECOMPOSITION (free): a pair of indices -> the edge between them, and the lines
that edge lies on. One XOR.

EMERGER (work): an edge -> its 7 pencils (the ordered choices of how to build
that relation from two others). Choice is work; `cost` = pencils enumerated.
"""
from __future__ import annotations

from itertools import combinations
from typing import Any, Dict, List, Tuple

NAME = "box_kite"
LINE = "both"

N = 16
EDGES = tuple(range(1, N))                       # the 15 nonzero XOR differences


def _lines_through(d: int) -> List[Tuple[int, int, int]]:
    """Every unordered {a,b,c} of nonzero edges with a ^ b = c, containing d."""
    out = []
    for a in EDGES:
        b = a ^ d
        if b in EDGES and b != a:
            tri = tuple(sorted((a, b, a ^ b)))
            if d in tri and tri not in out:
                out.append(tri)
    return out


def descend(pair: Tuple[int, int]) -> Dict[str, Any]:
    a, b = int(pair[0]), int(pair[1])
    if not (0 <= a < N and 0 <= b < N):
        raise ValueError("indices must be 0..15")
    d = a ^ b
    return {"toolset": NAME, "pair": (a, b), "edge": d,
            "is_edge": d in EDGES,
            "lines": _lines_through(d) if d in EDGES else [],
            "note": "one XOR — the free reading"}


def build_up(edge: int) -> Dict[str, Any]:
    """The 7 pencils of an edge: unordered {f, g}, f != g, both nonzero,
    f ^ g == edge."""
    d = int(edge)
    if d not in EDGES:
        raise ValueError("edge must be 1..15")
    pencils: List[Tuple[int, int]] = []
    scanned = 0
    for f, g in combinations(EDGES, 2):
        scanned += 1
        if f ^ g == d:
            pencils.append((f, g))
    return {"toolset": NAME, "edge": d, "pencils": pencils,
            "n_pencils": len(pencils), "cost": scanned,
            "note": "each pencil is one way to factor the relation into two"}


def verify() -> Dict[str, Any]:
    d = descend((3, 10))
    ok_d = d["edge"] == 9 and d["is_edge"]
    # every edge has exactly 7 pencils; 15 edges x 8 pairs = C(16,2) = 120
    counts = {e: build_up(e)["n_pencils"] for e in EDGES}
    ok_p = all(c == 7 for c in counts.values())
    total_pairs = len(list(combinations(range(N), 2)))
    ok_total = total_pairs == 120 and 15 * 8 == 120
    return {"ok": ok_d and ok_p and ok_total,
            "descend": ok_d, "all_edges_7_pencils": ok_p,
            "C(16,2)": total_pairs}


if __name__ == "__main__":
    print(descend((3, 10)))
    print(build_up(9))
    print(verify())
