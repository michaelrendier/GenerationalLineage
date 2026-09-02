"""
GenerationalLineage.engine.toolsets.scale
==========================================
SCALE — the multiplicative generator of the tier-0 floor Aff(1,R).

DECOMPOSITION (free): given a value and a reference, the scale factor is one
division — `s = value / reference`. No search.

EMERGER (work): given only that some map `x -> s*x + a` produced an output `y`
from an input `x`, recovering `s` needs a second, independent reading — one
(x, y) pair leaves `a` free. The refusal is the result: rebirth requires the
constraint the caller owes.
"""
from __future__ import annotations

import math
from typing import Any, Dict

from ..lines import AscentNotFree

NAME = "scale"
LINE = "both"


def descend(value: float, reference: float = 1.0) -> Dict[str, Any]:
    if reference == 0:
        raise ZeroDivisionError("reference must be non-zero")
    s = value / reference
    return {
        "toolset": NAME, "value": value, "reference": reference,
        "scale": s, "ln_scale": math.log(abs(s)) if s != 0 else float("-inf"),
        "sign": 0 if s == 0 else (1 if s > 0 else -1),
        "note": "one division — the free reading",
    }


def build_up(target: Dict[str, float], probes: list | None = None) -> Dict[str, Any]:
    """target: {'x': x, 'y': y} for a single application of x -> s*x + a.
    probes: optional [(x, y), ...] extra readings. With one (x, y) the system
    is x -> s*x + a with two unknowns — undetermined. Two independent readings
    fix (s, a)."""
    pts = [(target["x"], target["y"])] + list(probes or [])
    if len(pts) < 2:
        raise AscentNotFree("a second (x, y) reading",
                            "one (x, y) leaves the ADD term free — supply another probe")
    (x0, y0), (x1, y1) = pts[0], pts[1]
    if x1 == x0:
        raise AscentNotFree("two probes with distinct x",
                            "both probes share x — cannot separate s from a")
    s = (y1 - y0) / (x1 - x0)
    a = y0 - s * x0
    resid = max(abs(y - (s * x + a)) for x, y in pts)
    return {
        "toolset": NAME, "scale": s, "add": a, "n_probes": len(pts),
        "cost": len(pts), "max_residual": resid,
        "note": "recovered s only after the owed second reading",
    }


def verify() -> Dict[str, Any]:
    d = descend(15.0, 3.0)
    ok_d = math.isclose(d["scale"], 5.0)
    b = build_up({"x": 2.0, "y": 9.0}, probes=[(5.0, 21.0)])   # y = 4x + 1
    ok_b = math.isclose(b["scale"], 4.0) and math.isclose(b["add"], 1.0)
    try:
        build_up({"x": 1.0, "y": 2.0})
        ok_refuse = False
    except AscentNotFree:
        ok_refuse = True
    return {"ok": ok_d and ok_b and ok_refuse,
            "descend": ok_d, "build_up": ok_b, "refuses_underdetermined": ok_refuse}


if __name__ == "__main__":
    print(descend(15.0, 3.0))
    print(build_up({"x": 2.0, "y": 9.0}, probes=[(5.0, 21.0)]))
    print(verify())
