"""
GenerationalLineage.engine.toolsets.spectral_primes
=======================================================
SPECTRAL PRIMES — the spin/wobble split read as decomposition vs emerger.

Born 2026-09-26 from the theta(t)-rotation construction (RiemannHypothesis
Proof/ADDENDUM_toroidal_theta_structure_2026-09-25.md) and its own live
follow-up (ValaQuenta/modules/spectral_primes/). The split turns out to
already have this engine's own two-jurisdiction shape:

SPIN (major loop, theta'(t)) is the smooth, non-resonant carrier rate —
one evaluation, no search, no stored tape. Reading it off a height t is
exactly a DECOMPOSITION: free, cost=0.

WOBBLE (minor loop) is where the primes live, classically (von Mangoldt /
Weil): reconstructing psi(x) requires SUMMING over the known zeros — a
search whose cost grows with how many zeros you're willing to include.
That is exactly this engine's EMERGER shape: choice (how many terms) is
work, and the result only converges to the true step function as more
work is spent (Gibbs-phenomenon undershoot at the primes themselves is
the visible fingerprint of "not enough work yet").

Module independence (this repo's convention): stdlib + math/cmath only.
The zero table below is a small, literal, embedded set of known Riemann
zero imaginary parts (computed once via mpmath, dps=20, and frozen here as
data — not re-derived at import time). This toolset does NOT reproduce the
tilt-vs-wobble correlation test or the Real-Tilt/Axis crossing check from
ValaQuenta/modules/spectral_primes/maths.py — those need a full
arbitrary-sigma zeta evaluation, which needs mpmath, which this repo's
independence convention excludes. Those two results live in ValaQuenta;
this toolset carries only the two pieces that are honestly stdlib-only:
spin (decomposition) and wobble-via-psi-reconstruction (emerger).
"""
from __future__ import annotations

import cmath
import math
from typing import Any, Dict, List

NAME = "spectral_primes"
LINE = "both"

# First 25 nontrivial Riemann zero imaginary parts (mpmath, dps=20,
# 2026-09-26). Frozen data, not re-derived here — see module docstring.
ZEROS: List[float] = [
    14.134725141734695, 21.022039638771556, 25.01085758014569,
    30.424876125859512, 32.93506158773919, 37.586178158825675,
    40.9187190121475, 43.327073280915, 48.00515088116716,
    49.7738324776723, 52.970321477714464, 56.44624769706339,
    59.34704400260235, 60.83177852460981, 65.1125440480816,
    67.07981052949417, 69.54640171117398, 72.0671576744819,
    75.70469069908393, 77.1448400688748, 79.33737502024937,
    82.91038085408603, 84.73549298051705, 87.42527461312523,
    88.80911120763446,
]


def _theta_prime(t: float) -> float:
    """theta'(t) ~= (1/2)*ln(t/2pi) -- the classical Riemann-von Mangoldt
    mean zero density, read as the spin (carrier) rate."""
    return 0.5 * math.log(t / (2 * math.pi))


def _true_psi(x: float) -> float:
    """Exact psi(x) = sum of ln(p) over prime powers p^k <= x."""
    x = float(x)
    total = 0.0
    n = 2
    while n <= x:
        m, is_prime, d = n, True, 2
        while d * d <= m:
            if m % d == 0:
                is_prime = False
                break
            d += 1
        if is_prime:
            k = 1
            while n ** k <= x:
                total += math.log(n)
                k += 1
        n += 1
    return total


def descend(t: float) -> Dict[str, Any]:
    """SPIN, free: theta'(t) at height t -- one evaluation, no search.
    No prime content lives here; that is the point being read off."""
    t = float(t)
    if t <= 0:
        raise ValueError("t must be positive")
    spin_rate = _theta_prime(t)
    return {"toolset": NAME, "t": t, "spin_rate": spin_rate,
            "resonant": False,
            "note": "the carrier rate -- smooth, monotonic, no peaks by construction"}


def build_up(x: float, n_zeros: int = len(ZEROS)) -> Dict[str, Any]:
    """WOBBLE, work: reconstruct psi(x) from the oscillatory term of the
    von Mangoldt explicit formula, summing n_zeros known zeros. cost =
    n_zeros (the terms actually summed) -- this IS the emerger reading:
    the primes only emerge as you spend the work of including more zeros."""
    x = float(x)
    if x < 2:
        raise ValueError("x must be >= 2")
    n_zeros = min(int(n_zeros), len(ZEROS))
    zeros = ZEROS[:n_zeros]
    smooth = x - math.log(2 * math.pi) - 0.5 * math.log(1 - x ** -2)
    osc = 0.0
    for gamma in zeros:
        rho = complex(0.5, gamma)
        term = (x ** 0.5) * cmath.exp(1j * gamma * math.log(x)) / rho
        osc += 2 * term.real
    reconstructed = smooth - osc
    exact = _true_psi(x)
    return {"toolset": NAME, "x": x, "n_zeros_used": n_zeros,
            "cost": n_zeros, "reconstructed": reconstructed, "exact": exact,
            "difference": reconstructed - exact,
            "note": ("Gibbs-phenomenon undershoot expected exactly at prime "
                     "jumps with finite work -- classical signature, not error")}


def verify() -> Dict[str, Any]:
    """Self-check: (1) spin is monotonic (no resonance) across the embedded
    zero heights; (2) the wobble/build_up reconstruction is close to exact
    strictly BETWEEN primes (where no jump is being approximated) and
    honestly farther off exactly AT primes (Gibbs undershoot) -- both
    checked numerically, not asserted."""
    spins = [descend(t)["spin_rate"] for t in ZEROS]
    ok_spin = all(spins[i + 1] > spins[i] for i in range(len(spins) - 1))

    between_primes = [2.5, 6, 10, 12]
    at_primes = [2, 3, 5, 7, 11]
    between_diffs = [abs(build_up(x)["difference"]) for x in between_primes]
    at_diffs = [abs(build_up(x)["difference"]) for x in at_primes]
    ok_between = all(d < 0.05 for d in between_diffs)
    ok_at_larger = (sum(at_diffs) / len(at_diffs)) > (sum(between_diffs) / len(between_diffs))

    return {
        "ok": ok_spin and ok_between and ok_at_larger,
        "spin_monotonic": ok_spin,
        "spin_range": (spins[0], spins[-1]),
        "wobble_accurate_between_primes": ok_between,
        "wobble_worse_at_primes": ok_at_larger,
        "mean_diff_between_primes": sum(between_diffs) / len(between_diffs),
        "mean_diff_at_primes": sum(at_diffs) / len(at_diffs),
        "note": ("Two results this toolset cannot reproduce standalone (need "
                 "mpmath, excluded by this repo's stdlib-only convention): "
                 "tilt-vs-wobble correlation (REFUTED AS TESTED, corr~0.037) "
                 "and the Real-Tilt/Axis crossing (pinned at sigma=0.5 to "
                 "machine precision, 5 zeros tested) -- both in "
                 "ValaQuenta/modules/spectral_primes/maths.py."),
    }


if __name__ == "__main__":
    print(descend(ZEROS[0]))
    print(build_up(7))
    print(verify())
