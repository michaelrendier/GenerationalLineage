# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""The two-ring chart — fold ANY two quantities of ANY object through the Smith-chart Möbius map.

Run:  python3 examples/11_two_ring_chart.py
"""
from engine import factor_lineage, euler_phi, two_ring_chart, number_chart_point, cross_ratio

# Choose two ring definitions for the same object (a number), and read the fold:
ring1 = lambda n: float(factor_lineage(n)["omega"])
ring2 = lambda n: euler_phi(n) / n
r = two_ring_chart(97, ring1, ring2, Z0=complex(0, 1), ring1_name="Omega", ring2_name="phi/n")
sorted(r)[:6]
round(r["abs_gamma"], 6)

# The number chart: a balanced factorisation sits near the anchor, an unbalanced one near the horizon.
round(number_chart_point(3233, a=61), 3)
round(number_chart_point(30021, a=10007), 3)

# The cross-ratio survives every choice of anchor — the invariant the raw angle is not.
cross_ratio(0, 1, 2, 3 + 0j)
