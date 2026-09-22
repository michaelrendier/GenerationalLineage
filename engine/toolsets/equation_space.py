"""
GenerationalLineage.engine.toolsets.equation_space
=====================================================
EQUATION SPACE — steering through a parametrized family of equations by
following a collapse function's own gradient, rather than searching blind.

THE OBJECT. A `rho(s) >= 0` — a "distance to the interesting/singular
locus" function, continuous, zero exactly on the locus you actually care
about (a zero-divisor firing circle, a spill threshold, any collapse
condition). `rho` is the CONTINUOUS relaxation of a discrete membership
test — "is s special" becomes "how close is s to special," a real number
you can take a gradient of.

DECOMPOSITION (free): `descend()` reads `rho(s)` and its local gradient
at a single point — one evaluation, one finite difference, no search.

EMERGER (work): `build_up()` walks from a starting point toward `rho=0`
by gradient descent — cost = steps taken, and it genuinely can refuse
(`AscentNotFree`) if the walk stalls (zero gradient nearby) or doesn't
converge in budget. That refusal is real information: the locus may not
be reachable from that start, the same way `hyper_linear`'s ascent
refuses on a bare product.

TWO DIAGNOSTICS, both load-bearing, not decoration:

  classify_singularity(rho, s0) — is the locus a FOLD (caustic, `rho`
    falls off LINEARLY on both sides — an A2 singularity, Thom's
    classification) or a SMOOTH MINIMUM (quadratic falloff)? Checked by
    the ratio `rho/|dr|` converging to the same nonzero constant from
    both sides (fold) vs. to zero (smooth). This is not cosmetic — it is
    the difference between "the equation collapses" (a fold: crossing it
    changes something structural, like rank) and "the equation merely
    gets small" (a smooth trough, no structural event).

  steering_correlation(rho, compass) — does an INDEPENDENT, cheap signal
    (a "compass" computed with no reference to `rho` at all) predict
    `|grad(rho)|`, the actual expensive steering direction? If it does,
    the compass is a genuine free head-start on a costly walk — the same
    shape as `hyper_linear`'s Wiener instance, generalized: sometimes a
    system's own intrinsic structure tells you which way the hard
    direction goes, before you've paid to compute it.

THE BUILT-IN EXAMPLE reuses `scale.py`'s own Smith-chart map — extended
here to complex `s` (that repo's own `charts()` only ever takes real `s`,
a known, previously-flagged limitation, not fixed here, worked around by
keeping the complex extension local to this toolset) — as the default
`rho`: distance from `Gamma(s)=(s-1)/(s+1)` to the diagonal ray
`{c(1+i): c real}`. Its zero locus is an exact circle, `center=i,
radius=sqrt(2)` — verified this session, independently, against a
sedenion zero-divisor construction in `SedenionSpectralRelativity/
prime_gauge_sedenion.py`. Finding that same circle here by pure
gradient descent, with no sedenion machinery at all, is this toolset's
own cross-check of that result.

stdlib only (no numpy — matches this repo's module-independence
convention).
"""
from __future__ import annotations

import math
import random
from typing import Any, Callable, Dict, Optional, Tuple

from ..lines import AscentNotFree

NAME = "equation_space"
LINE = "both"

RhoFn = Callable[[complex], float]


# ── the built-in example: Smith's Gamma, extended to complex s ─────────────
def gamma(s: complex) -> complex:
    """ESTABLISHED, GenerationalLineage/engine/toolsets/scale.py — same
    formula, extended here to complex s (scale.py's own charts() takes
    real s only, a known limitation, not touched here)."""
    return (s - 1) / (s + 1)


def _default_rho(s: complex) -> float:
    """Distance from Gamma(s) to the diagonal ray {c(1+i): c real} — the
    exact condition whose zero locus (pulled back through Gamma) is the
    circle center=i, radius=sqrt(2), verified independently this session
    against a sedenion zero-divisor construction."""
    g = gamma(s)
    return abs(g.imag - g.real) if g.real > -1e9 else float("inf")


# ── the mechanism ────────────────────────────────────────────────────────
def gradient(rho: RhoFn, s: complex, h: float = 1e-4) -> complex:
    rx = (rho(s + h) - rho(s - h)) / (2 * h)
    ry = (rho(s + 1j * h) - rho(s - 1j * h)) / (2 * h)
    return complex(rx, ry)


def descend(s: complex, rho: Optional[RhoFn] = None) -> Dict[str, Any]:
    """One point: rho(s) and its local gradient. Free — one evaluation,
    one finite difference, no search."""
    rho = rho or _default_rho
    s = complex(s)
    r = rho(s)
    g = gradient(rho, s)
    return {
        "toolset": NAME, "s": s, "rho": r, "gradient": g, "|gradient|": abs(g),
        "note": "one evaluation + a local finite-difference gradient — the free reading",
    }


def build_up(target: Dict[str, Any], rho: Optional[RhoFn] = None,
             max_steps: int = 500, step_scale: float = 0.5,
             tol: float = 1e-4) -> Dict[str, Any]:
    """Walk from target['start'] toward rho=0 by gradient descent, with a
    decaying step to handle the fact that rho is a FOLD (linear, not
    quadratic) at its own zero locus -- a plain Newton step overshoots
    and oscillates right at the target precisely because the function
    isn't smooth there, so the step size is annealed rather than fixed.
    cost = steps taken. Refuses (AscentNotFree) if the walk stalls (zero
    gradient) or doesn't converge in budget — a real result, not a bug,
    the same shape as every other toolset's ascent refusal."""
    rho = rho or _default_rho
    start = target.get("start")
    if start is None:
        raise AscentNotFree("a start point", "no 'start' given in target")
    s = complex(start)
    best_s, best_r = s, rho(s)
    for step in range(max_steps):
        r = rho(s)
        if r < best_r:
            best_s, best_r = s, r
        if r < tol:
            return {"toolset": NAME, "converged": True, "s": s, "rho": r, "cost": step}
        g = gradient(rho, s)
        if abs(g) < 1e-12:
            raise AscentNotFree(
                "a nonzero gradient",
                f"stalled at s={s}, rho={r}, after {step} steps — the locus "
                f"may not be reachable from this start")
        anneal = step_scale / (1.0 + step / 20.0)
        s = s - anneal * r * g / (abs(g) ** 2)
    if best_r < tol * 20:
        return {"toolset": NAME, "converged": True, "s": best_s, "rho": best_r,
                "cost": max_steps, "note": "converged to within 20x tol via best-seen"}
    raise AscentNotFree(
        f"more than {max_steps} steps",
        f"did not converge; best s={best_s}, rho={best_r}")


def classify_singularity(s0: complex, rho: Optional[RhoFn] = None,
                          direction: complex = 1 + 0j, h: float = 0.03) -> Dict[str, Any]:
    """Fold (caustic, linear falloff) or smooth minimum (quadratic
    falloff) of rho transverse to a point s0 believed to sit on (or near)
    its zero locus. Checked both sides, not assumed."""
    rho = rho or _default_rho
    direction = direction / abs(direction)
    ratios = {}
    for dr in (-h, -h / 3, h / 3, h):
        s = s0 + dr * direction
        ratios[dr] = rho(s) / abs(dr)
    vals = list(ratios.values())
    mean_v = sum(vals) / len(vals) if vals else 0.0
    spread = (max(vals) - min(vals)) / mean_v if mean_v > 1e-12 else float("inf")
    is_fold = spread < 0.2
    return {
        "toolset": NAME, "s0": s0, "ratios": ratios, "is_fold_caustic": is_fold,
        "note": "ratios converging to the same nonzero constant from both sides "
                "= a fold (A2 caustic, the equation genuinely collapses there); "
                "converging to 0 = a smooth minimum (rho merely gets small)",
    }


def steering_correlation(compass: Callable[[complex], float], rho: Optional[RhoFn] = None,
                          n_samples: int = 150,
                          domain: Tuple[float, float, float, float] = (-3, 3, -2, 4),
                          seed: int = 0) -> Dict[str, Any]:
    """Does an independent, cheap compass signal predict |grad(rho)|, the
    actual costly steering direction? Pearson correlation over random
    samples — checked, not assumed."""
    rho = rho or _default_rho
    rng = random.Random(seed)
    x0, x1, y0, y1 = domain
    xs, ys = [], []
    for _ in range(n_samples):
        s = complex(rng.uniform(x0, x1), rng.uniform(y0, y1))
        try:
            c = abs(compass(s))
            g = abs(gradient(rho, s))
        except (ZeroDivisionError, ValueError, OverflowError):
            continue
        xs.append(c)
        ys.append(g)
    n = len(xs)
    if n < 3:
        return {"toolset": NAME, "n": n, "pearson": None}
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    pearson = cov / (sx * sy) if sx > 1e-12 and sy > 1e-12 else None
    return {"toolset": NAME, "n": n, "pearson": pearson}


def _gamma_curvature(s: complex) -> float:
    """dGamma/ds's imaginary part *2 -- Gamma's own intrinsic curvature,
    computed with NO reference to rho at all. The compass for the
    built-in steering_correlation example."""
    dgamma = 2 / (s + 1) ** 2
    return 2 * dgamma.imag


def verify() -> Dict[str, Any]:
    """1) descend() and build_up() agree — walking to rho=0 lands where
    descend() independently confirms rho~0.
    2) The found locus matches the known exact answer: |s - i| = sqrt(2).
    3) The firing circle is a genuine fold (caustic), not a smooth min.
    4) Gamma's own curvature is a real compass for the walk (correlation
    clearly positive, not incidental)."""
    d = descend(0.5 + 0.1j)
    ok_descend = d["rho"] >= 0 and math.isfinite(d["|gradient|"])

    b = build_up({"start": 0.5 + 0.1j})
    ok_converge = b.get("converged", False) and b["rho"] < 1e-4

    dist_from_i = abs(b["s"] - 1j)
    ok_matches_circle = abs(dist_from_i - math.sqrt(2)) < 1e-3

    try:
        build_up({"start": 100 + 100j}, max_steps=2)
        ok_refuse = False
    except AscentNotFree:
        ok_refuse = True

    fold = classify_singularity(b["s"])
    ok_fold = fold["is_fold_caustic"]

    corr = steering_correlation(_gamma_curvature)
    ok_corr = corr["pearson"] is not None and corr["pearson"] > 0.5

    ok = ok_descend and ok_converge and ok_matches_circle and ok_refuse and ok_fold and ok_corr
    return {
        "ok": ok, "ok_descend": ok_descend, "ok_converge": ok_converge,
        "ok_matches_known_circle": ok_matches_circle,
        "converged_distance_from_i": dist_from_i,
        "ok_refuses_when_unreachable": ok_refuse,
        "ok_fold_caustic": ok_fold,
        "steering_correlation_pearson": corr["pearson"],
        "ok_correlation_positive": ok_corr,
    }


if __name__ == "__main__":
    print("descend(0.5+0.1j):", descend(0.5 + 0.1j))
    print()
    b = build_up({"start": 0.5 + 0.1j})
    print("build_up (walk to rho=0):", b)
    print(f"distance from s=i: {abs(b['s']-1j):.6f}  (expected sqrt(2)={math.sqrt(2):.6f})")
    print()
    print("classify_singularity at the found point:", classify_singularity(b["s"]))
    print()
    print("steering_correlation (Gamma's own curvature vs |grad(rho)|):",
          steering_correlation(_gamma_curvature))
    print()
    print("verify():", verify())
