"""
GenerationalLineage.engine.toolsets.inversion
==============================================
INVERSION — J_N: (r, theta) -> (1/r, theta + pi/2).

This toolset is the MAP BETWEEN THE TWO JURISDICTIONS. Descent named in ascent
terms, and back, is J_N. It is an involution up to a quarter turn: apply it
four times and you are home; apply it twice and you are point-inverted, not
home. That "twice is not home" is the extinction-order-is-not-the-rebirth-order
fact, in one operator.

DECOMPOSITION (free): apply J_N once.

EMERGER (work): the number of applications to return to identity is 4 — the
cost of a full round trip between the jurisdictions.
"""
from __future__ import annotations

import math
from typing import Any, Dict, Tuple

NAME = "inversion"
LINE = "both"

_QUARTER = math.pi / 2.0


def _jn(r: float, theta: float) -> Tuple[float, float]:
    if r == 0:
        raise ZeroDivisionError("J_N is singular at r = 0 (the zero-divisor locus)")
    return (1.0 / r, (theta + _QUARTER) % (2.0 * math.pi))


def descend(point: Tuple[float, float]) -> Dict[str, Any]:
    r, theta = float(point[0]), float(point[1])
    r2, t2 = _jn(r, theta)
    return {"toolset": NAME, "point": (r, theta), "image": (r2, t2),
            "note": "one application of J_N — the free reading"}


def build_up(point: Tuple[float, float]) -> Dict[str, Any]:
    """Apply J_N until the point returns to itself; report the orbit and the
    cost (applications)."""
    r0, t0 = float(point[0]), float(point[1])
    r, t = r0, t0
    orbit = [(r, t)]
    for k in range(1, 9):
        r, t = _jn(r, t)
        orbit.append((r, t))
        if math.isclose(r, r0, abs_tol=1e-12) and math.isclose(
                math.cos(t - t0), 1.0, abs_tol=1e-12):
            return {"toolset": NAME, "orbit": orbit, "period": k, "cost": k,
                    "half_way_is_home": k == 2,
                    "note": "J_N^4 = id; J_N^2 = point inversion, not home"}
    return {"toolset": NAME, "orbit": orbit, "period": None, "cost": 8,
            "note": "did not close within 8 (unexpected)"}


def verify() -> Dict[str, Any]:
    p = (2.0, 0.3)
    d = descend(p)
    ok_d = math.isclose(d["image"][0], 0.5)
    b = build_up(p)
    ok_b = b["period"] == 4 and not b["half_way_is_home"]
    return {"ok": ok_d and ok_b, "descend": ok_d, "build_up": ok_b,
            "J_N^4 == id": b["period"] == 4}


if __name__ == "__main__":
    print(descend((2.0, 0.3)))
    print(build_up((2.0, 0.3)))
    print(verify())
