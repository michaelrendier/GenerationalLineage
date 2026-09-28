# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""The unit lineage — a third domain for the same decomposition: units as points in the SI lattice.

Run:  python3 examples/12_unit_lineage.py
"""
from engine import unit_vector, unit_mul, unit_div, SI_BASE

# The seven SI base dimensions are the leaves:
SI_BASE

# A unit is an exponent vector. mol/L, then multiplying back by L, cancels EXACTLY to mol:
MOL = unit_vector((0, 0, 0, 0, 0, 1, 0), name="mol")
LITER = unit_vector((0, 3, 0, 0, 0, 0, 0), name="L")
conc = unit_div(MOL, LITER)
conc["exponents"]
unit_mul(conc, LITER)["exponents"] == MOL["exponents"]

# Newton = kg * m / s^2 as a vector:
unit_vector((1, 1, -2, 0, 0, 0, 0), name="N")["exponents"]
