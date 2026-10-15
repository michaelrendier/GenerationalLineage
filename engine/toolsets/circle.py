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
GenerationalLineage.engine.toolsets.circle
===========================================
CIRCLE — a cataloguing and relating toolset: every kind of unit circle, the
circumference / diameter / radius / area each one gives, the seven ways a
circle is drawn (six operators + the norm-changing seventh), and what the
numbers do to the equations downstream.

A circle is the Add:Scale:Sign floor read geometrically:

    Add   = centre        (where it sits)
    Scale = radius        (how big)
    Sign  = orientation   (which way round; the sign of the area's square root,
                           the antipode e^{iπ} = −1)

DECOMPOSITION (free): a number plus the ROLE it plays (radius / diameter /
circumference / area) -> the whole circle row (r, d, C, A), its π-unit
reading, whether it lies in the exact lattice {2^a·π^b}, its imaginary
counterpart and its ℓ_p dual. One pass, cost 0.

EMERGER (work): a target measure (e.g. "area = 1") -> which catalogued
constants, in which role, produce it. A scan over constants × roles; `cost` =
candidates tried.

The six operators (each is the circle plus a transform that leaves one
pathway) are ORBIT, UNFOLD, CUT, FOLD, PROJECT, SHUFFLE. The SEVENTH circle is
the ℓ_p unit circle {|x|^p + |y|^p = 1}: the circle with the NORM changed
rather than the drawing changed (π_p, the Adler–Tanton p↔q duality, and the
Cayley–Klein elliptic/parabolic/hyperbolic triple).

Imaginary circles (radius iρ): d = 2iρ, C = 2πiρ, A = −πρ². The law of sines
and the law of cosines are unchanged in form (they are homogeneous); what
flips is the SIGN of every area (degree-2 quantity), and a sphere of radius
iρ is the hyperbolic plane — area = ρ²(π − A − B − C), the angle DEFICIT.

Stdlib + math + cmath only (this repo's module-independence convention).
"""
from __future__ import annotations

import cmath
import math
from typing import Any, Dict, List, Optional, Tuple

NAME = "circle"
LINE = "both"

CITATIONS: Dict[str, str] = {
    "Adler-Tanton-2000":  "C. L. Adler & J. Tanton, 'π is the minimum value for pi', College Math. J. 31(2) (2000) 102-106",
    "Golab-1932":         "S. Gołąb, 'Quelques problèmes métriques de la géométrie de Minkowski', Trav. Acad. Mines Cracovie 6 (1932) 1-79 "
                          "(the duality π_p = π_q for 1/p + 1/q = 1)",
    "Jaynes-1957":        "E. T. Jaynes, 'Information Theory and Statistical Mechanics', Phys. Rev. 106 (1957) 620",
    "Shannon-1948":       "C. E. Shannon, 'A Mathematical Theory of Communication', Bell Syst. Tech. J. 27 (1948) 379",
    "von-Mises-1918":     "R. von Mises, 'Über die Ganzzahligkeit der Atomgewichte', Phys. Z. 19 (1918) 490 (von Mises distribution)",
    "Langevin-1905":      "P. Langevin, 'Magnétisme et théorie des électrons', Ann. Chim. Phys. 5 (1905) 70",
    "Curie-1895":         "P. Curie, 'Propriétés magnétiques des corps à diverses températures', Ann. Chim. Phys. 5 (1895) 289",
    "Biot-Savart-1820":   "J.-B. Biot & F. Savart (1820); A.-M. Ampère (1826): field of a straight current, B ∝ 1/r",
    "Kelvin-1845":        "W. Thomson (Lord Kelvin), 'Extrait d'une lettre', J. Math. Pures Appl. 10 (1845) 364 (inversion / images)",
    "Lorentz-1895":       "H. A. Lorentz, Versuch einer Theorie der electrischen und optischen Erscheinungen in bewegten Körpern (1895)",
    "Riemann-1859":       "B. Riemann, 'Über die Anzahl der Primzahlen unter einer gegebenen Grösse' (1859)",
    "Riemann-Siegel":     "H. M. Edwards, Riemann's Zeta Function (1974), ch. 7 (the Riemann-Siegel formula)",
    "Gauss-Bonnet":       "C. F. Gauss, Disquisitiones generales circa superficies curvas (1827); area of a spherical triangle = R²(A+B+C−π)",
    "Lambert-1766":       "J. H. Lambert, Theorie der Parallellinien (written 1766, pub. 1786): area = angle deficit; the sphere of imaginary radius",
    "Cayley-Klein":       "F. Klein, 'Über die sogenannte Nicht-Euklidische Geometrie', Math. Ann. 4 (1871) 573; "
                          "I. M. Yaglom, A Simple Non-Euclidean Geometry and its Physical Basis (1979)",
    "Mandelbrot-1980":    "B. B. Mandelbrot, 'Fractal aspects of the iteration of z→λz(1−z)', Ann. N.Y. Acad. Sci. 357 (1980) 249",
}

# ── constants ────────────────────────────────────────────────────────────────
def _omega() -> float:
    x = 0.5671
    for _ in range(60):
        x -= (x * math.exp(x) - 1.0) / (math.exp(x) * (1.0 + x))
    return x


OMEGA_ZS = _omega()                       # Lambert W(1), x·e^x = 1
LN10 = math.log(10.0)
PHI = (1.0 + math.sqrt(5.0)) / 2.0
D_STAR = OMEGA_ZS / LN10                  # d*_taut = Ω/ln10 (0.24631)
D_STAR_SPEC = 0.2460                      # disputed fifth d* (spectral)
GAP = 1.0 / (1000.0 * math.sqrt(2.0))

CONSTANTS: Dict[str, complex] = {
    "1/2": 0.5, "1": 1.0, "2": 2.0, "pi": math.pi, "2pi": 2 * math.pi,
    "1/pi": 1 / math.pi, "phi": PHI, "e": math.e, "ln10": LN10,
    "sqrt2": math.sqrt(2.0), "Omega_ZS": OMEGA_ZS, "d*": D_STAR,
    "d*_spec": D_STAR_SPEC, "GAP": GAP, "i": 1j,
}
ROLES = ("radius", "diameter", "circumference", "area")

# π as the UNIT, placed at three different measures (proposed Add:Scale:Sign
# assignment — Cody to confirm; the three circles are computed either way).
PI_PLACEMENT = {
    "Add":   "circumference C = π·d      (d = 1,  the half-radius circle r = ½)",
    "Scale": "area          A = π·r²     (r = 1,  the unit-radius circle)",
    "Sign":  "diameter      d = π        (antipodal pair; e^{iπ} = −1)",
}


class Circle:
    """Centre (Add), radius (Scale), orientation (Sign); measures derived."""

    def __init__(self, radius: complex, centre: complex = 0j, orient: int = 1):
        self.radius = radius
        self.centre = centre
        self.orient = 1 if orient >= 0 else -1

    @property
    def diameter(self) -> complex:
        return 2 * self.radius

    @property
    def circumference(self) -> complex:
        return 2 * math.pi * self.radius

    @property
    def area(self) -> complex:
        return math.pi * self.radius * self.radius

    def measures(self) -> Dict[str, complex]:
        return {"radius": self.radius, "diameter": self.diameter,
                "circumference": self.circumference, "area": self.area}

    def ass(self) -> Dict[str, Any]:
        return {"Add": self.centre, "Scale": self.radius, "Sign": self.orient}


def from_role(value: complex, role: str) -> Circle:
    """Build the circle whose `role` measure equals `value`."""
    if role == "radius":
        return Circle(value)
    if role == "diameter":
        return Circle(value / 2)
    if role == "circumference":
        return Circle(value / (2 * math.pi))
    if role == "area":
        return Circle(cmath.sqrt(value / math.pi) if isinstance(value, complex) or value < 0
                      else math.sqrt(value / math.pi))
    raise KeyError(role)


def pi_unit_circles() -> Dict[str, Dict[str, Any]]:
    """The three circles in which π is the unit at one measure (see PI_PLACEMENT)."""
    out = {}
    for slot, (value, role) in {"Add": (math.pi, "circumference"),
                                "Scale": (math.pi, "area"),
                                "Sign": (math.pi, "diameter")}.items():
        c = from_role(value, role)
        out[slot] = {"role": role, **{k: v for k, v in c.measures().items()}}
    return out


def pi_lattice(x: float, tol: float = 1e-12) -> Optional[Tuple[float, int]]:
    """(a, b) with x = 2^a·π^b exactly (a in half-integers, b integer), else None."""
    if not isinstance(x, (int, float)) or x <= 0:
        return None
    for b in range(-5, 6):
        for a2 in range(-24, 25):                       # a = a2/2 (admits √2)
            if abs(x - 2.0 ** (a2 / 2) * math.pi ** b) <= tol * abs(x):
                return (a2 / 2, b)
    return None


# ── DECOMPOSITION ────────────────────────────────────────────────────────────
def descend(x: Any, role: str = "radius", **_: Any) -> Dict[str, Any]:
    """Number (or UNS-constant name) + role -> the full circle row."""
    value = CONSTANTS[x] if isinstance(x, str) else x
    c = from_role(value, role)
    m = c.measures()
    row: Dict[str, Any] = {"input": x, "role": role, "cost": 0, **m,
                           "C_over_d": (m["circumference"] / m["diameter"]) if m["diameter"] else None,
                           "isoperimetric_C2_over_4piA": (m["circumference"] ** 2 / (4 * math.pi * m["area"]))
                           if m["area"] else None,
                           "ass": c.ass(), "imaginary": isinstance(value, complex) and value.imag != 0}
    row["pi_units"] = {k: (v / math.pi) for k, v in m.items()}
    row["lattice"] = {k: pi_lattice(v.real if isinstance(v, complex) and v.imag == 0 else v)
                      for k, v in m.items() if not isinstance(v, complex) or v.imag == 0}
    row["lp_dual_exponent_if_p"] = (value / (value - 1)) if isinstance(value, (int, float)) and value > 1 else None
    return row


def catalogue(names: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Every constant in every role: the 'type of unit per circle' table."""
    return [descend(n, r) for n in (names or list(CONSTANTS)) for r in ROLES]


# ── EMERGER ──────────────────────────────────────────────────────────────────
def build_up(target: float, role: str = "area", tol: float = 1e-9, **_: Any) -> Dict[str, Any]:
    """Which (constant, role) circles have `role`-measure == target? Scan; cost = tried."""
    hits, cost = [], 0
    for name, v in CONSTANTS.items():
        for r in ROLES:
            cost += 1
            m = from_role(v, r).measures()[role]
            if isinstance(m, complex) and m.imag != 0:
                continue
            mv = m.real if isinstance(m, complex) else m
            if abs(mv - target) <= tol * max(1.0, abs(target)):
                hits.append({"constant": name, "as": r, "measure": role, "value": mv})
    return {"target": target, "role": role, "hits": hits, "cost": cost}


# ── the six operators (the circle drawn six ways) ────────────────────────────
def bessel_i(n: int, k: float, terms: int = 60) -> float:
    return sum((k / 2) ** (2 * j + n) / (math.factorial(j) * math.factorial(j + n)) for j in range(terms))


def orbit(theta: float, r: float = 1.0) -> Dict[str, Any]:
    """IDENTITY — the circle itself: (r cosθ, r sinθ). One pathway: the angle."""
    return {"op": "orbit", "point": (r * math.cos(theta), r * math.sin(theta)),
            "law": "x² + y² = r²", "invariant": "radius"}


def unfold(theta: float, pitch: float = 1.0, r: float = 1.0) -> Dict[str, Any]:
    """HELIX — circle × drift: (r cosθ, r sinθ, pitch·θ/2π). The circle with its period unrolled."""
    return {"op": "unfold", "point": (r * math.cos(theta), r * math.sin(theta), pitch * theta / (2 * math.pi)),
            "law": "circle × line (Lorentz force: v⊥ circles, v∥ drifts)",
            "invariant": "gyroradius r, pitch per turn"}


def cut(theta: float, r: float = 1.0) -> Dict[str, Any]:
    """ARC — partition: keep an angular window. s = rθ, chord = 2r sin(θ/2); B ∝ θ for a current arc."""
    return {"op": "cut", "arc": r * theta, "chord": 2 * r * math.sin(theta / 2),
            "sagitta": r * (1 - math.cos(theta / 2)), "law": "B ∝ θ (Biot–Savart on an arc)",
            "invariant": "arc/radius = θ"}


def fold(r: float, R: float = 1.0) -> Dict[str, Any]:
    """WIRE — circle inversion r -> R²/r. Profile B/Bmax = e^{−|u|}, u = ln(r/R): the Laplace shape in the log chart."""
    u = math.log(r / R)
    return {"op": "fold", "image_radius": R * R / r, "u": u, "profile": math.exp(-abs(u)),
            "law": "B = μ0 I /(2π r) outside, ∝ r inside; exact inversion symmetry only in n=2",
            "invariant": "the circle r = R (fixed set)"}


def project(theta: float, r: float = 1.0) -> Dict[str, Any]:
    """DIPOLE — project the circle on an axis: x = r cosθ. 2-to-1 fold (θ, −θ); density 1/(π√(r²−x²)) (arcsine)."""
    x = r * math.cos(theta)
    dens = 1.0 / (math.pi * math.sqrt(r * r - x * x)) if abs(x) < r else math.inf
    return {"op": "project", "x": x, "density": dens, "preimages": 2 if abs(x) < r else 1,
            "law": "U = −MB cosθ (cosine well); P(x) arcsine", "invariant": "projected extent ±r"}


def shuffle(kappa: float, dim: int = 2) -> Dict[str, Any]:
    """MAGNETIC MATTER — randomise the angle at coupling κ = MB/kT. ⟨cos⟩ = I1(κ)/I0(κ) (2D von Mises);
    3D Langevin L(κ) = coth κ − 1/κ ≈ κ/3. Small κ: χ ∝ 1/T (Curie). Large κ: sd(θ) -> 1/√κ (normal)."""
    if dim == 2:
        mean_cos = bessel_i(1, kappa) / bessel_i(0, kappa)
        small = kappa / 2
        sd = 1 / math.sqrt(kappa) if kappa > 0 else math.inf
    else:
        mean_cos = (1 / math.tanh(kappa) - 1 / kappa) if kappa > 0 else 0.0
        small = kappa / 3
        sd = 1 / math.sqrt(kappa) if kappa > 0 else math.inf
    return {"op": "shuffle", "kappa": kappa, "dim": dim, "mean_cos": mean_cos, "small_kappa_limit": small,
            "sd_theta_large_kappa": sd, "law": "Boltzmann e^{κ cosθ} = von Mises; Curie χ = C/T",
            "invariant": "entropy-maximising distribution at fixed ⟨cosθ⟩ (Jaynes 1957)"}


OPERATORS = {"orbit": orbit, "unfold": unfold, "cut": cut, "fold": fold, "project": project, "shuffle": shuffle}


# ── the seventh circle: ℓ_p ──────────────────────────────────────────────────
def pi_p(p: float, n: int = 20000) -> float:
    """C/d of the ℓ_p unit circle, measured in its own norm. π_2 = π; π_1 = π_∞ = 4; π_p = π_q (1/p+1/q=1)."""
    if p == 1 or math.isinf(p):
        return 4.0
    # x = cos^{2/p}t, y = sin^{2/p}t ; t = (π/4)s^p tames the endpoint singularity; π_p = 4∫₀^{π/4} ds_ℓp
    h = 1.0 / n

    def f(s: float) -> float:
        if s == 0.0:
            return 0.0                    # integrand -> 0 as s -> 0 for every p > 1
        t = (math.pi / 4) * s ** p
        dt = (math.pi / 4) * p * s ** (p - 1)
        c, sn = math.cos(t), math.sin(t)
        dx = (2 / p) * c ** (2 / p - 1) * sn
        dy = (2 / p) * sn ** (2 / p - 1) * c
        return ((dx ** p + dy ** p) ** (1 / p)) * dt

    total = f(0.0) + f(1.0) + sum((4 if k % 2 else 2) * f(k * h) for k in range(1, n))
    return 4 * total * h / 3


def lp_circle(p: float) -> Dict[str, Any]:
    """The seventh circle: π_p, area, and the dual exponent q."""
    area = math.inf if math.isinf(p) else 4 * math.gamma(1 + 1 / p) ** 2 / math.gamma(1 + 2 / p)
    if math.isinf(p):
        area = 4.0
    q = math.inf if p == 1 else (1.0 if math.isinf(p) else p / (p - 1))
    return {"p": p, "q_dual": q, "pi_p": pi_p(p), "area": area,
            "area_over_pi_p": area / pi_p(p), "self_dual": p == 2}


CAYLEY_KLEIN = {
    +1: ("elliptic",   "x²+y²=1 circle",         "rotation (|tr|<2, periodic)", "complex i²=−1"),
    0:  ("parabolic",  "x²=1 pair of lines",     "shear (|tr|=2)",              "dual ε²=0"),
    -1: ("hyperbolic", "x²−y²=1 hyperbola",      "boost / dilation (|tr|>2)",   "split-complex j²=+1"),
}


def classify_sl2(a: float, b: float, c: float, d: float) -> str:
    """Elliptic / parabolic / hyperbolic by |trace| of a unit-determinant 2×2 (first-line test)."""
    if abs(a * d - b * c - 1) > 1e-9:
        raise ValueError("det != 1")
    tr = abs(a + d)
    return "elliptic" if tr < 2 - 1e-12 else "parabolic" if abs(tr - 2) <= 1e-12 else "hyperbolic"


# ── imaginary circles and the laws of sines / cosines ────────────────────────
def imaginary_circle(rho: float = 1.0) -> Dict[str, Any]:
    """Radius iρ: d = 2iρ, C = 2πiρ, A = −πρ²; isoperimetric C² = 4πA holds exactly (both −4π²ρ²)."""
    c = Circle(1j * rho)
    return {"radius": c.radius, "diameter": c.diameter, "circumference": c.circumference, "area": c.area,
            "C2_minus_4piA": c.circumference ** 2 - 4 * math.pi * c.area}


def sphere_triangle_angle(a: complex, b: complex, c: complex, R: complex) -> complex:
    """Angle C opposite side c on a surface of radius R, from the spherical law of cosines
    cos(c/R) = cos(a/R)cos(b/R) + sin(a/R)sin(b/R)cos C.  R real -> sphere; R = iρ -> hyperbolic plane
    (cos(x/iρ) = cosh(x/ρ)); R -> ∞ -> the flat law."""
    num = cmath.cos(c / R) - cmath.cos(a / R) * cmath.cos(b / R)
    return cmath.acos(num / (cmath.sin(a / R) * cmath.sin(b / R)))


def triangle(a: complex, b: complex, c: complex, R: complex) -> Dict[str, Any]:
    """Angles, law-of-sines ratios and Gauss–Bonnet area of a triangle on radius R (real, imaginary or complex)."""
    A = sphere_triangle_angle(b, c, a, R)
    B = sphere_triangle_angle(a, c, b, R)
    C = sphere_triangle_angle(a, b, c, R)
    sines = [cmath.sin(x / R) / cmath.sin(y) for x, y in ((a, A), (b, B), (c, C))]
    return {"A": A, "B": B, "C": C, "sine_ratios": sines, "angle_sum": A + B + C,
            "area": R * R * (A + B + C - math.pi)}


def flat_laws(a: complex, b: complex, C: float) -> Dict[str, Any]:
    """Flat triangle with sides a,b and included angle C: c from the law of cosines, then the law of
    sines ratio and area ½ab sinC.  Pass a,b imaginary (a = iα, b = iβ): c² = −(α²+β²−2αβcosC) so c = iγ,
    the law keeps its form, and the area is −½αβ sinC (degree 2 -> sign flip)."""
    c2 = a * a + b * b - 2 * a * b * math.cos(C)
    c = cmath.sqrt(c2)
    return {"c": c, "c_squared": c2, "area": 0.5 * a * b * math.sin(C),
            "sin_C": math.sin(C), "ratio_c_over_sinC": c / math.sin(C)}


def heron_squared(a: complex, b: complex, c: complex) -> complex:
    """16·Area² = (a+b+c)(−a+b+c)(a−b+c)(a+b−c) — degree 4, so unchanged by a→ia; the SIGN of the area is the
    branch of the square root, i.e. the Sign component of Add:Scale:Sign."""
    return (a + b + c) * (-a + b + c) * (a - b + c) * (a + b - c)


# ── sigma reading (each catalogued value as a σ_RB coupling) ──────────────────
_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71)


def sigma_reading(sigma: complex, n_primes: int = 20) -> Dict[str, Any]:
    """Use `sigma` as the Σ_RB coupling exponent: G_p = p^{−σ} over the first primes, distance from the
    critical value ½, the truncated Euler product, and the regime label. σ complex -> a rotation per prime
    (p^{−it} = e^{−it ln p}); Re σ is what sets the weight, Im σ is the phase."""
    ps = _PRIMES[:n_primes]
    G = [p ** (-sigma) for p in ps]
    euler = 1 + 0j
    for g in G:
        euler *= 1 / (1 - g) if abs(1 - g) > 1e-15 else 1
    re = sigma.real if isinstance(sigma, complex) else sigma
    regime = ("GR-like (σ≥2)" if re >= 1.9 else "Yang–Mills-like (σ≈1)" if abs(re - 1) < 0.05 else
              "critical (σ≈½)" if abs(re - .5) < 0.05 else "forbidden/Fermat zone (0<σ<½)" if 0 < re < .5 else
              "trivial (σ≤0)" if re <= 0 else "intermediate")
    return {"sigma": sigma, "coupling_sum": sum(G), "G2": G[0], "G_last": G[-1], "offset_from_half": sigma - 0.5,
            "euler_product": euler, "converges_absolutely": re > 1, "regime": regime}


# ── self-check ───────────────────────────────────────────────────────────────
def verify() -> Dict[str, Any]:
    checks: Dict[str, bool] = {}
    c = from_role(0.5, "radius")
    checks["r=1/2: d=1, C=π, A=π/4"] = (c.diameter == 1 and abs(c.circumference - math.pi) < 1e-15
                                         and abs(c.area - math.pi / 4) < 1e-15)
    checks["C(r=1/2) = A(r=1) = π"] = abs(from_role(1.0, "radius").area - from_role(0.5, "radius").circumference) < 1e-15
    checks["role round-trip"] = all(abs(from_role(v, r).measures()[r] - v) < 1e-12
                                    for v in (0.3, 1.7, math.pi) for r in ROLES)
    checks["π-lattice detects 2π, 1/π, √2"] = all(pi_lattice(x) is not None for x in (2 * math.pi, 1 / math.pi, math.sqrt(2.0)))
    checks["π-lattice rejects φ, e, ln10, Ω"] = all(pi_lattice(x) is None for x in (PHI, math.e, LN10, OMEGA_ZS))
    im = imaginary_circle(1.0)
    checks["imaginary circle A = −π, C² = 4πA"] = abs(im["area"] + math.pi) < 1e-12 and abs(im["C2_minus_4piA"]) < 1e-9
    # flat laws invariant under a,b -> i·a, i·b ; area flips sign
    real = flat_laws(3.0, 4.0, 1.1)
    imag = flat_laws(3j, 4j, 1.1)
    checks["law of cosines keeps form (c -> ic)"] = abs(imag["c"] - 1j * real["c"]) < 1e-9 or abs(imag["c"] + 1j * real["c"]) < 1e-9
    checks["law of sines ratio: c/sinC -> i·c/sinC"] = abs(abs(imag["ratio_c_over_sinC"]) - abs(real["ratio_c_over_sinC"])) < 1e-9
    checks["imaginary-side area = −real area"] = abs(imag["area"] + real["area"]) < 1e-9
    checks["Heron 16A² unchanged by a->ia"] = abs(heron_squared(3j, 4j, 5j) - heron_squared(3, 4, 5)) < 1e-9
    # sphere (real R) vs hyperbolic (R = iρ): area sign and deficit
    sph = triangle(0.5, 0.6, 0.7, 1.0)
    hyp = triangle(0.5, 0.6, 0.7, 1j)
    checks["sphere: angle excess > 0, area R²E"] = sph["angle_sum"].real > math.pi and abs(sph["area"].real - (sph["angle_sum"].real - math.pi)) < 1e-9
    checks["hyperbolic (R=i): angle deficit, area = π − ΣA > 0"] = (
        hyp["angle_sum"].real < math.pi and abs(hyp["area"].real - (math.pi - hyp["angle_sum"].real)) < 1e-9)
    checks["law of sines holds on both"] = all(abs(x - s["sine_ratios"][0]) < 1e-9 for s in (sph, hyp) for x in s["sine_ratios"])
    # flat limit: large R recovers π and the flat law
    big = triangle(3.0, 4.0, 5.0, 1e3)
    checks["R -> ∞: Gauss–Bonnet area -> flat area 6 (R=1e3)"] = abs(big["area"].real - 6.0) < 1e-3
    # KNOWN LIMIT (kept, not hidden): the cosine form cancels catastrophically for R ≳ 1e5 — the excess is
    # ~area/R² and falls below double rounding, so area = R²·excess is noise (R=1e6 gave −1.7e5). Remedy: haversine form.
    checks["known limit: R=1e6 cosine form is NOT accurate"] = abs(triangle(3.0, 4.0, 5.0, 1e6)["area"].real - 6.0) > 1.0
    # operators
    f = fold(0.5)
    checks["fold: inversion image R²/r, profile e^{−|u|}"] = abs(f["image_radius"] - 2.0) < 1e-15 and abs(f["profile"] - 0.5) < 1e-15
    checks["fold symmetric: profile(r) = profile(R²/r)"] = abs(fold(0.3)["profile"] - fold(1 / 0.3)["profile"]) < 1e-15
    checks["project is 2-to-1"] = project(0.7)["preimages"] == 2
    checks["shuffle small-κ: ⟨cos⟩ -> κ/2 (2D), κ/3 (3D)"] = (
        abs(shuffle(1e-3, 2)["mean_cos"] / 1e-3 - 0.5) < 1e-6 and abs(shuffle(1e-3, 3)["mean_cos"] / 1e-3 - 1 / 3) < 1e-6)
    checks["cut: chord = 2r sin(θ/2)"] = abs(cut(math.pi)["chord"] - 2.0) < 1e-15
    # seventh circle
    checks["π_2 = π"] = abs(pi_p(2.0) - math.pi) < 1e-7
    checks["π_p = π_q (3, 3/2)"] = abs(pi_p(3.0) - pi_p(1.5)) < 1e-5
    checks["π_1 = π_∞ = 4"] = pi_p(1.0) == 4.0 and pi_p(math.inf) == 4.0
    checks["π_p ≥ π (p=1.5, 4)"] = pi_p(1.5) > math.pi and pi_p(4.0) > math.pi
    checks["SL2 classifier"] = (classify_sl2(math.cos(.4), -math.sin(.4), math.sin(.4), math.cos(.4)) == "elliptic"
                                and classify_sl2(1, 1, 0, 1) == "parabolic"
                                and classify_sl2(math.cosh(.4), math.sinh(.4), math.sinh(.4), math.cosh(.4)) == "hyperbolic")
    s = sigma_reading(0.5)
    checks["σ=½ regime critical; σ=i has |p^{-σ}|=1"] = (s["regime"].startswith("critical")
                                                        and abs(abs(sigma_reading(1j)["G2"]) - 1) < 1e-12)
    checks["build_up(area=π) finds radius=1"] = any(h["constant"] == "1" and h["as"] == "radius"
                                                    for h in build_up(math.pi, "area")["hits"])
    return {"ok": all(checks.values()), "checks": checks, "n": len(checks)}


if __name__ == "__main__":
    r = verify()
    for k, v in r["checks"].items():
        print(("PASS " if v else "FAIL ") + k)
    print("ok =", r["ok"], f"({r['n']} checks)")
