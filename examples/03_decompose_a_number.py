# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Decompose a number — its lineage tree, its primary decomposition, and whether it falls.

Run:  python3 examples/03_decompose_a_number.py
"""
from engine import decompose_number, factor_lineage, primary_decomposition, fall_test, arith_deriv

# A prime is generation 0 (a leaf: it cannot be decomposed). A composite is an internal node.
# 3233 = 53 * 61:
r = decompose_number(3233)
r["ring_fall_survive"]["verdict"], r["ring_fall_survive"]["quotient"]
r["cepstral_primary"], r["Omega_lineage_length"]

# The lineage tree of a number with repeated factors: 360 = 2^3 * 3^2 * 5
t = factor_lineage(360)
t["omega"], t["generations"], t["leaves_telperion"]
primary_decomposition(360)

# "Fall or survive": Z/(n) has zero divisors exactly when n is composite; a prime survives as a field.
fall_test(15)["verdict"], fall_test(15)["n_zero_divisors"]
fall_test(13)["verdict"], fall_test(13)["quotient"]

# The arithmetic derivative reads the same lineage: n' = n * sum(e_i / p_i).
arith_deriv(12)
