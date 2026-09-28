# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""The factoral spiral — factoral decomposition as chart geometry: any collection with two numeric readings.

An eigendecomposition factors an operator into (eigenvalue, eigenvector) pairs the way integer factorisation splits N into
primes; factoral_spiral() points the same idea at ANY collection and returns its structure as discrete cells ("windows of order").
This tutorial needs no plotting library; the picture-making reports are in README section 4.9 (EXTENDED layer + matplotlib).
Run:  python3 examples/18_factoral_spiral.py
"""
from engine import factoral_spiral, chart_scale_factor, factor_lineage, euler_phi

# Two readings of each of the numbers 2..39: Omega(n) (the lineage length) and phi(n)/n (the unit density).
r = factoral_spiral(range(2, 40), lambda n: float(factor_lineage(n)["omega"]),
                    lambda n: euler_phi(n) / n, Z0=complex(0, 1), ring1_name="Omega", ring2_name="phi/n")
len(r["readings"])
sorted(r)

# Each reading is a point folded through the Smith-chart map: its gamma, |gamma|, and the local scale factor.
x = r["readings"][0]
x["Z"], round(x["abs_gamma"], 4)

# Objects also fall into integer "windows of order": the cell key is (round(ring1), round(ring2)), and each
# cell lists the INDICES (input order) of the objects that landed in it. Index 0 is the number 2, index 1 is 3, ...
len(r["cells"])
r["cells"][(1, 1)][:6]          # round(Omega) = 1 and round(phi/n) = 1: the primes 3, 5, 7, 11, 13, 17
r["cells"][(1, 0)]              # 2 is prime too, but phi(2)/2 = 0.5 rounds (to even) to 0

# chart_scale_factor(Z, Z0) = |dGamma/dZ| is the fold's own derivative in closed form — the "phase" a flat reading loses.
round(chart_scale_factor(1 + 0.5j, 1j), 6)
