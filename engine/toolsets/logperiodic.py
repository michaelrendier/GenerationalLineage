"""
GenerationalLineage.engine.toolsets.logperiodic
================================================
LOG-PERIODIC + MELLIN — the spring, read in its own coordinate.

A quantity that repeats every time x is multiplied by a fixed factor λ is
NOT periodic in x. Viewed on a linear axis its oscillations bunch up toward
small x and stretch out at large x, and a Fourier transform in x smears the
one true frequency across a broad band. That is the flattening artifact:
a spring (spiral) squashed through a lossy flat projection.

In the coordinate u = ln x the same signal is an ordinary sinusoid:

        y(x) = c + d·ln x + A·cos(ω·ln x + φ)         (spin d, wobble A)
        one turn ⇔ x → λx,   λ = e^{2π/ω}             (the pitch of the spring)

    ADD ⋊ SCALE has two dual transforms — one for each irreducible axis:

        Fourier   on ADD    (x → x + a)    f̂(ξ) = ∫ f(x) e^{−iξx} dx
        Mellin    on SCALE  (x → λ·x)      M[f](s) = ∫₀^∞ f(x) x^{s−1} dx

    and Mellin IS Fourier in u: M[f](σ+it) = ∫ f(eᵘ) e^{σu} e^{itu} du.
    A log-periodic signal is a pure line in the Mellin domain and a smear in
    the Fourier one.

Two exact identities are checked, not assumed:
    M[e^{−x}](s) = Γ(s)                       (the definition's own test)
    M[f(a·x)](s) = a^{−s}·M[f](s)             (scaling ↔ multiplication)

DECOMPOSITION (free): `descend((xs, ys))` fits, in u = ln x, a trend plus one
sinusoid: scans ω, refines by golden section, returns ω, the scale ratio λ,
amplitude, phase, trend, residual — and with `compare_flat=True` the SAME fit
attempted in linear x, so the size of the flattening artifact is a number.
Least squares at each ω means uneven sampling costs nothing extra.

EMERGER (work): `build_up({...})` synthesises the spring (the choice of ω, A,
φ, trend); cost = samples.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Sequence, Tuple

from ..lines import AscentNotFree

NAME = "logperiodic"
LINE = "both"


def mellin(f, s: float, x_lo: float = 1e-9, x_hi: float = 80.0, n: int = 40000) -> float:
    """M[f](s) = ∫ f(x) x^{s−1} dx = ∫ f(eᵘ) e^{su} du  (trapezoid in u)."""
    a, b = math.log(x_lo), math.log(x_hi)
    h = (b - a) / n
    tot = 0.0
    for i in range(n + 1):
        u = a + i * h
        w = 0.5 if i in (0, n) else 1.0
        tot += w * f(math.exp(u)) * math.exp(s * u)
    return tot * h


def _solve(M: List[List[float]], v: List[float]) -> List[float] | None:
    n = len(v)
    A = [row[:] + [v[i]] for i, row in enumerate(M)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(A[r][c]))
        if abs(A[piv][c]) < 1e-12:
            return None
        A[c], A[piv] = A[piv], A[c]
        for r in range(c + 1, n):
            f = A[r][c] / A[c][c]
            for k in range(c, n + 1):
                A[r][k] -= f * A[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (A[r][n] - sum(A[r][k] * x[k] for k in range(r + 1, n))) / A[r][r]
    return x


def _fit(us: Sequence[float], ys: Sequence[float], w: float, trend: bool = True):
    """Least-squares  y ≈ c + d·u + a·cos(wu) + b·sin(wu). Returns (sse, coeffs)."""
    cols = 4 if trend else 3
    S = [[0.0] * cols for _ in range(cols)]
    T = [0.0] * cols
    for u, y in zip(us, ys):
        row = [1.0, math.cos(w * u), math.sin(w * u)] + ([u] if trend else [])
        for i in range(cols):
            T[i] += row[i] * y
            for j in range(i, cols):
                S[i][j] += row[i] * row[j]
    for i in range(cols):
        for j in range(i):
            S[i][j] = S[j][i]
    sol = _solve(S, T)
    if sol is None:
        return float("inf"), None
    sse = 0.0
    for u, y in zip(us, ys):
        row = [1.0, math.cos(w * u), math.sin(w * u)] + ([u] if trend else [])
        sse += (y - sum(c * r for c, r in zip(sol, row))) ** 2
    return sse, sol


def _scan(us, ys, w_lo, w_hi, steps, trend=True):
    best = (float("inf"), None, None)
    for i in range(steps + 1):
        w = w_lo + (w_hi - w_lo) * i / steps
        sse, sol = _fit(us, ys, w, trend)
        if sse < best[0]:
            best = (sse, w, sol)
    dw = (w_hi - w_lo) / steps
    lo, hi = max(w_lo, best[1] - dw), min(w_hi, best[1] + dw)
    g = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    c, d = b - g * (b - a), a + g * (b - a)
    fc, fd = _fit(us, ys, c, trend)[0], _fit(us, ys, d, trend)[0]
    for _ in range(40):
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - g * (b - a)
            fc = _fit(us, ys, c, trend)[0]
        else:
            a, c, fc = c, d, fd
            d = a + g * (b - a)
            fd = _fit(us, ys, d, trend)[0]
    w = (a + b) / 2
    sse, sol = _fit(us, ys, w, trend)
    return sse, w, sol


def descend(data, w_range: Tuple[float, float] = (0.5, 30.0), steps: int = 240,
            compare_flat: bool = False, **_) -> Dict[str, Any]:
    xs, ys = data
    if min(xs) <= 0:
        raise ValueError("x must be > 0 (u = ln x)")
    us = [math.log(x) for x in xs]
    mean = sum(ys) / len(ys)
    tot = sum((y - mean) ** 2 for y in ys) or 1e-300
    sse, w, sol = _scan(us, ys, *w_range, steps)
    c, a, b, d = sol
    out = {
        "toolset": NAME, "n": len(xs),
        "omega": w, "period_in_u": 2 * math.pi / w,
        "scale_ratio_lambda": math.exp(2 * math.pi / w),
        "amplitude": math.hypot(a, b),
        "phase": math.atan2(-b, a),
        "constant": c, "trend_per_ln_x": d,
        "sse": sse, "r_squared": 1 - sse / tot,
        "coordinate": "u = ln x  (anti-flattening)",
        "note": "one turn of the spring = x multiplied by scale_ratio_lambda",
    }
    if compare_flat:
        # the SAME model (trend + one sinusoid) in linear x, best ω_x over
        # [2π/span, 1.0] rad per unit x — a fair, generous window, not a straw man
        span = max(xs) - min(xs)
        flat = _scan(list(xs), ys, 2 * math.pi / span, 1.0, 500, trend=True)
        out["flat_x_best_sse"] = flat[0]
        out["flat_x_r_squared"] = 1 - flat[0] / tot
        out["flattening_ratio"] = flat[0] / max(sse, 1e-300)
    return out


def build_up(target, **_) -> Dict[str, Any]:
    if isinstance(target, dict) and "omega" in target:
        w = float(target["omega"])
        A_ = float(target.get("amp", 1.0))
        ph = float(target.get("phase", 0.0))
        c = float(target.get("const", 0.0))
        d = float(target.get("trend", 0.0))
        lo, hi = float(target.get("x_lo", 1.0)), float(target.get("x_hi", 1000.0))
        n = int(target.get("n", 400))
        xs = [lo + (hi - lo) * i / (n - 1) for i in range(n)]
        ys = [c + d * math.log(x) + A_ * math.cos(w * math.log(x) + ph) for x in xs]
        return {"toolset": NAME, "direction": "parameters -> spring signal",
                "x": xs, "y": ys, "cost": n,
                "scale_ratio_lambda": math.exp(2 * math.pi / w),
                "note": "the choice is (ω, A, φ, trend) — the pitch is fixed by ω"}
    raise AscentNotFree("{'omega': ω, 'amp', 'phase', 'const', 'trend', 'x_lo', 'x_hi', 'n'}")


def verify() -> Dict[str, Any]:
    # 1. Mellin of e^{-x} is Γ(s)
    ok_gamma = all(abs(mellin(lambda x: math.exp(-x), s) - math.gamma(s)) < 1e-4
                   for s in (1.5, 2.0, 3.5))
    # 2. scaling identity  M[f(a·x)](s) = a^{-s} M[f](s)
    f = lambda x: math.exp(-x)
    a_ = 2.5
    s = 2.0
    lhs = mellin(lambda x: f(a_ * x), s, x_hi=40.0)
    rhs = a_ ** (-s) * mellin(f, s, x_hi=100.0)
    ok_scale = abs(lhs - rhs) < 1e-4

    # 3. recover a planted spring, x uniform on [1, 2000] (the hard, flattened sampling)
    w0, A0, ph0, c0, d0 = 6.0, 1.3, 0.7, 0.4, 0.25
    sig = build_up({"omega": w0, "amp": A0, "phase": ph0, "const": c0, "trend": d0,
                    "x_lo": 1.0, "x_hi": 2000.0, "n": 700})
    r = descend((sig["x"], sig["y"]), compare_flat=True)
    ok_w = abs(r["omega"] - w0) < 1e-4
    ok_amp = abs(r["amplitude"] - A0) < 1e-4 and abs(r["trend_per_ln_x"] - d0) < 1e-4
    ok_lambda = abs(r["scale_ratio_lambda"] - math.exp(2 * math.pi / w0)) < 1e-2
    # noise-free data makes the SSE ratio degenerate (denominator ~1e-27): judge by the R² pair
    ok_flat = r["flat_x_r_squared"] < 0.9 * r["r_squared"]

    # 4. a signal with NO log-periodicity should not fit well — the control
    xs = [1.0 + 1999.0 * i / 699 for i in range(700)]
    ys = [math.sin(0.37 * x) for x in xs]                 # periodic in x, not in ln x
    ctl = descend((xs, ys))
    ok_control = ctl["r_squared"] < 0.5

    try:
        build_up({})
        ok_refuse = False
    except AscentNotFree:
        ok_refuse = True

    return {"ok": all([ok_gamma, ok_scale, ok_w, ok_amp, ok_lambda, ok_flat, ok_control, ok_refuse]),
            "mellin_is_gamma": ok_gamma, "mellin_scaling": ok_scale,
            "omega_recovered": ok_w, "omega_error": abs(r["omega"] - w0),
            "amplitude_and_trend": ok_amp, "lambda": ok_lambda,
            "lambda_value": r["scale_ratio_lambda"],
            "flat_r2": r["flat_x_r_squared"], "u_r2": r["r_squared"],
            "flat_control_rejected": ok_control, "control_r2": ctl["r_squared"],
            "refuses_without_params": ok_refuse}


if __name__ == "__main__":
    print(verify())
