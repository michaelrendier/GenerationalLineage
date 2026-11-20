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
GenerationalLineage.engine.toolsets.matrix_flow
================================================
MATRIX FLOW — the nine flows of dx/dt = A·x for a real 2×2 matrix, and which
KIND of circle each one is.

Provenance: the nine-way split is the standard linear-systems classification of
the origin of a planar linear flow (eigenvalues of A on the trace/determinant
plane; any ODE text, e.g. Strogatz, Nonlinear Dynamics and Chaos, ch. 5). The
author saw it as a nine-panel reel; the panel list was not available to the
code, so the nine here are the textbook nine, and any panel that differs is a
correction to make, not a result.

DECOMPOSITION (free): a 2×2 matrix -> its class, its eigenvalues, and its split
into the four real generators

    A = a·I  +  b·J  +  h1·K1  +  h2·K2
        I = identity        (SCALE: uniform growth, a = tr/2)
        J = [[0,-1],[1,0]]  (J² = −I: the quarter turn; the circle)
        K1 = diag(1,-1), K2 = [[0,1],[1,0]]   (K² = +I: the boost; the hyperbola)

with b = (r−q)/2 and h = √(((p−s)/2)² + ((q+r)/2)²). The eigenvalues are
a ± √(h² − b²), so the sign of h² − b² decides the KIND of circle:

    b > h   elliptic    rotation wins   -> centre, spirals     (a round circle)
    b < h   hyperbolic  boost wins      -> saddle, nodes       (a hyperbola)
    b = h   parabolic   they cancel     -> shear / line        (the circle at infinity)

The nine (a = tr/2):
    centre (a=0, elliptic)              stable spiral / unstable spiral (a≠0, elliptic)
    saddle (hyperbolic, det<0)          stable node / unstable node (hyperbolic, det>0)
    star (A = λI)                       degenerate node (parabolic, A ≠ λI, λ≠0)
    line of fixed points (det = 0, A ≠ 0 — one zero eigenvalue; includes the pure shear)

EMERGER (work): scan integer matrices with entries in [−B, B] and count how
many land in each class; `cost` = matrices tried. The counts are the answer: a
random matrix is almost never a centre (it needs tr = 0 and det > 0).

Stdlib + math + cmath only (this repo's module-independence convention).
"""
from __future__ import annotations

import itertools
import math
from typing import Any, Dict, List, Sequence, Tuple

NAME = "matrix_flow"
LINE = "both"

CITATIONS: Dict[str, str] = {
    "Strogatz-2015": "S. H. Strogatz, Nonlinear Dynamics and Chaos, 2nd ed. (2015), ch. 5 (linear systems; the trace-determinant plane)",
    "Yaglom-1979":   "I. M. Yaglom, A Simple Non-Euclidean Geometry and its Physical Basis (1979) (elliptic / parabolic / hyperbolic rotation)",
}

CLASSES = ("centre", "stable spiral", "unstable spiral", "saddle", "stable node",
           "unstable node", "star", "degenerate node", "line of fixed points")

# the kind of circle (Cayley-Klein) and the Add:Scale:Sign reading of each class
KIND = {
    "centre": "elliptic", "stable spiral": "elliptic", "unstable spiral": "elliptic",
    "saddle": "hyperbolic", "stable node": "hyperbolic", "unstable node": "hyperbolic",
    "star": "scalar (no rotation, no boost)", "degenerate node": "parabolic",
    "line of fixed points": "parabolic or scalar-zero",
}
_EPS = 1e-12


def _m(A: Sequence[Sequence[float]]) -> Tuple[float, float, float, float]:
    (p, q), (r, s) = A
    return float(p), float(q), float(r), float(s)


def split(A) -> Dict[str, float]:
    """A = a·I + b·J + h1·K1 + h2·K2 (exact for every real 2×2)."""
    p, q, r, s = _m(A)
    a, b = (p + s) / 2.0, (r - q) / 2.0
    h1, h2 = (p - s) / 2.0, (q + r) / 2.0
    return {"a_scale": a, "b_turn": b, "h1_boost": h1, "h2_boost": h2,
            "h": math.hypot(h1, h2), "kind_gap": math.hypot(h1, h2) ** 2 - b * b}


def eigenvalues(A) -> Tuple[complex, complex]:
    p, q, r, s = _m(A)
    tr, det = p + s, p * s - q * r
    disc = tr * tr / 4.0 - det
    root = complex(disc) ** 0.5
    return tr / 2.0 + root, tr / 2.0 - root


def classify(A) -> str:
    """One of CLASSES. Tolerance _EPS (scaled) on the exact-zero tests."""
    p, q, r, s = _m(A)
    scale = max(1.0, abs(p), abs(q), abs(r), abs(s))
    tr, det = p + s, p * s - q * r
    disc = tr * tr - 4.0 * det
    tol = _EPS * scale * scale
    if abs(det) <= tol:
        return "line of fixed points"          # one zero eigenvalue (A ≠ 0 or the zero flow: all fixed)
    if abs(disc) <= tol:                      # repeated eigenvalue λ = tr/2
        diag_scalar = abs(q) <= _EPS * scale and abs(r) <= _EPS * scale and abs(p - s) <= _EPS * scale
        return "star" if diag_scalar else "degenerate node"
    if disc < 0:                              # complex pair
        if abs(tr) <= _EPS * scale:
            return "centre"
        return "stable spiral" if tr < 0 else "unstable spiral"
    if det < 0:
        return "saddle"
    return "stable node" if tr < 0 else "unstable node"


def expm(A, t: float = 1.0) -> List[List[float]]:
    """exp(tA) in closed form (Cayley-Hamilton), no series, no linear-algebra library.
    With N = A − (tr/2)·I:  N² = Δ·I, Δ = tr²/4 − det.  exp(tA) = e^{at}·(c·I + sn·N),
    (c, sn) = (cosh, sinh(√Δ t)/√Δ) for Δ>0, (cos, sin(√−Δ t)/√−Δ) for Δ<0, (1, t) for Δ=0."""
    p, q, r, s = _m(A)
    a = (p + s) / 2.0
    n11, n12, n21, n22 = p - a, q, r, s - a
    delta = a * a - (p * s - q * r)
    if abs(delta) < 1e-14:
        c, sn = 1.0, t
    elif delta > 0:
        w = math.sqrt(delta)
        c, sn = math.cosh(w * t), math.sinh(w * t) / w
    else:
        w = math.sqrt(-delta)
        c, sn = math.cos(w * t), math.sin(w * t) / w
    e = math.exp(a * t)
    return [[e * (c + sn * n11), e * sn * n12], [e * sn * n21, e * (c + sn * n22)]]


def integrate(A, x0: Sequence[float], t: float, steps: int = 4000) -> Tuple[float, float]:
    """Independent check on expm: classical RK4 on dx/dt = A x."""
    p, q, r, s = _m(A)
    x, y = float(x0[0]), float(x0[1])
    h = t / steps
    f = lambda u, v: (p * u + q * v, r * u + s * v)
    for _ in range(steps):
        k1 = f(x, y)
        k2 = f(x + h / 2 * k1[0], y + h / 2 * k1[1])
        k3 = f(x + h / 2 * k2[0], y + h / 2 * k2[1])
        k4 = f(x + h * k3[0], y + h * k3[1])
        x += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        y += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
    return x, y


# one representative matrix per class
EXAMPLES: Dict[str, List[List[float]]] = {
    "centre":              [[0, -1], [1, 0]],
    "stable spiral":       [[-0.2, -1], [1, -0.2]],
    "unstable spiral":     [[0.2, -1], [1, 0.2]],
    "saddle":              [[1, 0], [0, -1]],
    "stable node":         [[-1, 0], [0, -2]],
    "unstable node":       [[1, 0], [0, 2]],
    "star":                [[1, 0], [0, 1]],
    "degenerate node":     [[1, 1], [0, 1]],
    "line of fixed points": [[0, 1], [0, 0]],
}


def descend(A, **_: Any) -> Dict[str, Any]:
    """A 2×2 matrix -> class, kind of circle, eigenvalues, the I/J/K split, and the invariant that shows the circle."""
    cls = classify(A)
    sp = split(A)
    ev = eigenvalues(A)
    inv = {
        "centre": "x² + y² (in the basis where A = bJ) is constant: the orbit is a circle, period 2π/b",
        "stable spiral": "radius shrinks as e^{a t}, angle advances at b: a circle times a SCALE",
        "unstable spiral": "radius grows as e^{a t}, angle advances at b: a circle times a SCALE",
        "saddle": "u·v is constant along each orbit (u, v the eigen-coordinates): a hyperbola, the boost",
        "stable node": "every orbit decays to the origin along the slow eigendirection: pure SCALE, no turn",
        "unstable node": "every orbit leaves the origin along the fast eigendirection: pure SCALE, no turn",
        "star": "A = λI: every ray is an orbit; the flow is one SCALE",
        "degenerate node": "N = A − λI is nilpotent (N² = 0): exp = e^{λt}(I + tN); a shear, the ADD generator",
        "line of fixed points": "a zero eigenvalue: the kernel of A is fixed pointwise, the rest runs along the other eigenvector",
    }[cls]
    return {"matrix": [list(map(float, row)) for row in A], "class": cls, "kind": KIND[cls],
            "eigenvalues": ev, "trace": float(_m(A)[0] + _m(A)[3]),
            "det": float(_m(A)[0] * _m(A)[3] - _m(A)[1] * _m(A)[2]), "split": sp,
            "invariant": inv, "free": True, "cost": 0}


def build_up(target: Any = 3, **_: Any) -> Dict[str, Any]:
    """Scan every integer matrix with entries in [−B, B] (B = target); count the classes. cost = matrices tried."""
    bound = int(target)
    counts = {c: 0 for c in CLASSES}
    tried = 0
    for p, q, r, s in itertools.product(range(-bound, bound + 1), repeat=4):
        tried += 1
        counts[classify([[p, q], [r, s]])] += 1
    return {"bound": bound, "counts": counts, "cost": tried, "free": False}


def verify() -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    checks["each example is its own class"] = all(classify(M) == c for c, M in EXAMPLES.items())
    checks["nine classes, nine examples"] = len(CLASSES) == len(EXAMPLES) == 9
    # closed-form exp(tA) agrees with RK4 on all nine, at a generic start point
    worst = 0.0
    for c, M in EXAMPLES.items():
        E = expm(M, 1.3)
        x0 = (0.7, -0.4)
        ex = (E[0][0] * x0[0] + E[0][1] * x0[1], E[1][0] * x0[0] + E[1][1] * x0[1])
        rk = integrate(M, x0, 1.3)
        worst = max(worst, abs(ex[0] - rk[0]) + abs(ex[1] - rk[1]))
    checks["expm = RK4 (all nine, to 1e-9)"] = worst < 1e-9
    # the circle: centre preserves x²+y²; spiral radius is e^{a t}
    E = expm(EXAMPLES["centre"], 2.1)
    checks["centre: x²+y² conserved, det exp = 1"] = abs(E[0][0] * E[1][1] - E[0][1] * E[1][0] - 1.0) < 1e-12 \
        and abs(math.hypot(E[0][0] * 0.6 + E[0][1] * 0.8, E[1][0] * 0.6 + E[1][1] * 0.8) - 1.0) < 1e-12
    M = EXAMPLES["stable spiral"]
    E = expm(M, 3.0)
    x1 = (E[0][0], E[1][0])                                 # image of (1, 0)
    checks["spiral: |x(t)| = e^{a t}"] = abs(math.hypot(*x1) - math.exp(-0.2 * 3.0)) < 1e-12
    # the boost: u·v conserved on the saddle
    E = expm(EXAMPLES["saddle"], 1.7)
    checks["saddle: x·y conserved"] = abs((E[0][0] * 2.0) * (E[1][1] * 3.0) - 6.0) < 1e-12
    # the shear: nilpotent part, exp = I + tN
    E = expm(EXAMPLES["line of fixed points"], 5.0)
    checks["shear: exp(tN) = I + tN"] = E == [[1.0, 5.0], [0.0, 1.0]]
    # the split is exact and the kind gap decides the eigenvalues
    ok = True
    for M in ([[2, -3], [5, 1]], [[1, 4], [2, -3]], [[3, 1], [-1, 3]], [[0.5, 2], [-2, 0.5]]):
        sp = split(M)
        p, q, r, s = _m(M)
        rebuilt = (sp["a_scale"] + sp["h1_boost"], -sp["b_turn"] + sp["h2_boost"],
                   sp["b_turn"] + sp["h2_boost"], sp["a_scale"] - sp["h1_boost"])
        ok &= all(abs(x - y) < 1e-12 for x, y in zip(rebuilt, (p, q, r, s)))
        ev = eigenvalues(M)
        ok &= abs(ev[0] - (sp["a_scale"] + complex(sp["kind_gap"]) ** 0.5)) < 1e-9
    checks["I/J/K split reconstructs A; eigenvalues = a ± √(h²−b²)"] = ok
    # the scan finds all nine classes at B = 2, and centres are rare
    r = build_up(2)
    checks["B=2 scan reaches all nine classes"] = all(v > 0 for v in r["counts"].values()) and r["cost"] == 5 ** 4
    checks["centres are rarer than spirals"] = r["counts"]["centre"] < r["counts"]["stable spiral"] + r["counts"]["unstable spiral"]
    return {"ok": all(checks.values()), "checks": checks, "worst_expm_vs_rk4": worst}
