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

THE TWO CHARTS — what SCALE looks like to each jurisdiction. Not two
orthogonal Smith charts: a Smith chart ORTHOGONAL TO an Apollonian gasket.

    continuous  (Smith chart)      the GR() reading of scale — Γ = (s−1)/(s+1)
                                   on the unit disk, a conformal, gap-free
                                   ruler; carries the exact local scale factor
                                   |dΓ/ds| = 2/(s+1)² (the flattening artifact).
    discrete    (Apollonian gasket) the QM() reading of scale — s placed on the
                                   integer curvature ladder of the bounded
                                   gasket (Descartes 1643, seed (-1,2,2,3)); a
                                   quantised, tangency-packed ruler.

Matter and energy are the TILT between the two axes. That the two rulers look
like they share an axis is, at this layer, an artifact of picking two charts
that are both monotone in ln(s) for different reasons and attaching GR / QM to
them by hand — `charts()` reports it as an artifact, not an axis. A later pass
chases whether it is more than that.
"""
from __future__ import annotations

import math
from collections import deque
from typing import Any, Dict

from ..lines import AscentNotFree

NAME = "scale"
LINE = "both"


def descend(value: float, reference: float = 1.0,
            chart: bool = False) -> Dict[str, Any]:
    if reference == 0:
        raise ZeroDivisionError("reference must be non-zero")
    s = value / reference
    out = {
        "toolset": NAME, "value": value, "reference": reference,
        "scale": s, "ln_scale": math.log(abs(s)) if s != 0 else float("-inf"),
        "sign": 0 if s == 0 else (1 if s > 0 else -1),
        "note": "one division — the free reading",
    }
    if chart:
        out["charts"] = charts(s)             # both jurisdictions, still single-pass
    return out


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


# ── the two charts: continuous (Smith / GR) ⟂ discrete (gasket / QM) ─────────
_GASKET_SEED = (-1, 2, 2, 3)     # the bounded integer Apollonian gasket


def _descartes_fourth(k1: int, k2: int, k3: int, k4: int) -> int:
    """The OTHER curvature tangent to k1,k2,k3 — Descartes reflected:
    k4' = 2(k1+k2+k3) − k4. An integer seed keeps every descendant integer."""
    return 2 * (k1 + k2 + k3) - k4


def _descartes_residual(quad=_GASKET_SEED) -> int:
    """(Σk)² − 2Σk²  — the image's 'holds to 0.0E+0 on every quadruple'."""
    s = sum(quad)
    return abs(s * s - 2 * sum(k * k for k in quad))


def apollonian_curvatures(cap: int = 400, seed=_GASKET_SEED) -> Dict[int, int]:
    """Integer curvatures of the bounded gasket up to |k| ≤ cap, mapped to the
    BFS generation depth at which each first appears. Free: one sweep, no
    search."""
    first_gen: Dict[int, int] = {}
    start = tuple(sorted(seed))
    dq = deque([(start, 0)])
    seen = {start}
    while dq:
        quad, gen = dq.popleft()
        for k in quad:
            if abs(k) <= cap and (k not in first_gen or gen < first_gen[k]):
                first_gen[k] = gen
        a, b, c, d = quad
        for x, y, z, w in ((a, b, c, d), (a, b, d, c), (a, c, d, b), (b, c, d, a)):
            nw = _descartes_fourth(x, y, z, w)
            if abs(nw) > cap:
                continue
            nq = tuple(sorted((x, y, z, nw)))
            if nq not in seen:
                seen.add(nq)
                dq.append((nq, gen + 1))
    return first_gen


def charts(s: float, cap: int = 400) -> Dict[str, Any]:
    """SCALE read in both jurisdictions at once — both single-pass, so still
    the FREE (descent) reading.

    continuous (Smith chart, GR):  Γ = (s−1)/(s+1) on the unit disk + the exact
                                   local scale factor |dΓ/ds| = 2/(s+1)².
    discrete   (gasket, QM):       s on the integer Apollonian curvature ladder
                                   — nearest rung, bracketing rungs, the
                                   generation depth, the gaps.
    """
    s = float(s)
    gamma = (s - 1.0) / (s + 1.0)                     # the Smith fold
    dgamma = 2.0 / (s + 1.0) ** 2 if s != -1.0 else float("inf")

    fg = apollonian_curvatures(cap)
    rungs = sorted(k for k in fg if k > 0)
    mag = abs(s)
    below = [k for k in rungs if k <= mag]
    above = [k for k in rungs if k >= mag]
    k_lo = below[-1] if below else None
    k_hi = above[0] if above else None
    nearest = min(rungs, key=lambda k: abs(k - mag))

    return {
        "toolset": NAME, "scale": s,
        "continuous": {                               # Smith chart — GR() jurisdiction
            "gamma": gamma, "abs_gamma": abs(gamma),
            "local_scale_factor": dgamma,
            "ruler": "conformal, gap-free",
        },
        "discrete": {                                 # Apollonian gasket — QM() jurisdiction
            "nearest_curvature": nearest,
            "bracket": (k_lo, k_hi),
            "gap_below": None if k_lo is None else mag - k_lo,
            "gap_above": None if k_hi is None else k_hi - mag,
            "generation": fg.get(nearest),
            "ruler": "integer curvature ladder, tangency-packed",
        },
        "orthogonal": True,
        "tilt": "matter/energy is the tilt between the continuous and discrete "
                "axes — not computed at this layer",
        "shared_axis": "artifact — both rulers are monotone in ln(s); the "
                       "GR/QM attachment is a hand choice here",
        "note": "not two Smith charts — a Smith chart orthogonal to a gasket",
    }


def sedenion_locus_orthogonality() -> Dict[str, Any]:
    """Run the two charts across the sedenion locus split by the Two Trees —
    lower octonion (indices 1..7; the tree that holds e0, the anchor) and upper
    octonion (8..15; pure imaginary). If the continuous order and the discrete
    order of the indices coincide on BOTH trees, the 'shared axis' is an
    artifact of both charts being monotone in ln(s), not an emergent axis.
    """
    trees = {"lower_octonion": range(1, 8), "upper_octonion": range(8, 16)}
    out: Dict[str, Any] = {}
    for name, idx in trees.items():
        rows = [(i, charts(float(i))) for i in idx]
        cont = [i for i, _ in sorted(rows, key=lambda r: r[1]["continuous"]["gamma"])]
        disc = [i for i, _ in sorted(rows, key=lambda r: r[1]["discrete"]["nearest_curvature"])]
        out[name] = {"continuous_order": cont, "discrete_order": disc,
                     "coincide": cont == disc}
    allc = all(v["coincide"] for v in out.values())
    return {"trees": out, "all_coincide": allc,
            "verdict": ("METHOD — shared axis is an artifact of two monotone "
                        "charts; not an emergent UFT axis at this layer")
                       if allc else "ANOMALY — chase to a verdict"}


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

    # the two charts
    fg = apollonian_curvatures(200)
    ok_descartes = _descartes_residual() == 0
    ok_integer = all(isinstance(k, int) for k in fg) and \
        {6, 11, 14, 15, 18, 23}.issubset(fg)          # known (-1,2,2,3) curvatures
    c = charts(5.0)
    s_back = (1.0 + c["continuous"]["gamma"]) / (1.0 - c["continuous"]["gamma"])
    ok_cayley = math.isclose(s_back, 5.0)              # Smith fold round-trips
    loc = sedenion_locus_orthogonality()
    ok_locus = loc["all_coincide"] and loc["verdict"].startswith("METHOD")

    return {"ok": ok_d and ok_b and ok_refuse and ok_descartes and ok_integer
            and ok_cayley and ok_locus,
            "descend": ok_d, "build_up": ok_b, "refuses_underdetermined": ok_refuse,
            "descartes_exact": ok_descartes, "integer_start_stays_integer": ok_integer,
            "cayley_roundtrip": ok_cayley, "sedenion_locus_artifact": ok_locus}


if __name__ == "__main__":
    print(descend(15.0, 3.0))
    print(build_up({"x": 2.0, "y": 9.0}, probes=[(5.0, 21.0)]))
    import json
    print(json.dumps(charts(2.5), indent=2, default=str))
    print(json.dumps(sedenion_locus_orthogonality(), indent=2, default=str))
    print(verify())
