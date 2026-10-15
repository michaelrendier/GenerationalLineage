# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Circle — every unit circle, what its numbers do downstream, and the seven ways to draw one.

Established (circle geometry; Gauss–Bonnet; Adler–Tanton ℓ_p duality) — see wiki/References.md.
Run:  python3 examples/50_circle.py
"""
import math
from engine.toolsets import circle

# A circle is Add (centre) : Scale (radius) : Sign (orientation). Give a number AND the role it plays.
r = circle.descend(0.5, "radius")
r["diameter"], round(r["circumference"], 6), round(r["area"], 6)

# The same constant in every role — "radius = 1/2" and "diameter = 1" are the same circle; "area = 1" is not.
for role in circle.ROLES:
    row = circle.descend(1.0, role)
    print(role, "= 1 ->", "r =", round(row["radius"], 6), " C =", round(row["circumference"], 6), " A =", round(row["area"], 6))

# π as the UNIT, placed at three different measures:
for slot, c in circle.pi_unit_circles().items():
    print(slot, c["role"], "= π ->", {k: round(v, 5) for k, v in c.items() if k != "role"})

# Is a coincidence between two constants structure, or just {2^a·π^b} algebra? (first-line test)
circle.pi_lattice(2 * math.pi), circle.pi_lattice(1 / math.pi), circle.pi_lattice(circle.PHI)

# The emerger direction: which catalogued circle has area exactly π?
b = circle.build_up(math.pi, "area")
[(h["constant"], h["as"]) for h in b["hits"]], b["cost"]

# The imaginary circle: radius i. d = 2i, C = 2πi, A = −π — and C² = 4πA still holds exactly.
im = circle.imaginary_circle(1.0)
im["diameter"], im["circumference"], round(im["area"].real, 6), abs(im["C2_minus_4piA"]) < 1e-9

# Law of cosines / sines with imaginary sides (a, b -> ia, ib): the law keeps its FORM, the sides stay imaginary,
# and the area (degree 2) flips sign. Heron's 16A² (degree 4) is unchanged — the sign is the Sign component.
real, imag = circle.flat_laws(3.0, 4.0, 1.1), circle.flat_laws(3j, 4j, 1.1)
round(abs(imag["c"]) - abs(real["c"]), 12), round(real["area"], 6), round(imag["area"].real, 6)
circle.heron_squared(3, 4, 5), circle.heron_squared(3j, 4j, 5j).real

# A sphere of radius R has angle EXCESS; a sphere of radius iρ is the hyperbolic plane and has angle DEFICIT:
sph = circle.triangle(0.5, 0.6, 0.7, 1.0)
hyp = circle.triangle(0.5, 0.6, 0.7, 1j)
round(sph["angle_sum"].real - math.pi, 6), round(math.pi - hyp["angle_sum"].real, 6)
round(sph["area"].real, 6), round(hyp["area"].real, 6)

# The six drawings of one circle, and the seventh (change the NORM, not the drawing):
circle.fold(0.5)["image_radius"], round(circle.fold(0.5)["profile"], 6)
round(circle.shuffle(1e-3, 2)["mean_cos"] / 1e-3, 4), round(circle.shuffle(1e-3, 3)["mean_cos"] / 1e-3, 4)
for p in (1.0, 1.5, 2.0, 3.0, math.inf):
    c = circle.lp_circle(p)
    print("p =", p, " pi_p =", round(c["pi_p"], 5), " area =", round(c["area"], 5), " dual q =", c["q_dual"])

# Any catalogued value as a Σ_RB coupling σ (G_p = p^−σ over the first primes):
for name in ("1/2", "d*", "1", "i"):
    s = circle.sigma_reading(circle.CONSTANTS[name])
    print("sigma =", name, "->", s["regime"], " |sum G_p| =", round(abs(s["coupling_sum"]), 5))
