# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""units — a physical unit as a point in the 7-axis SI lattice; a dimension signature narrowed to candidate laws.

Run:  python3 examples/21_units.py
"""
from engine.toolsets import units

# descend(): a unit name (or dict) becomes its exponent vector — exact vector arithmetic.
r = units.descend("N")
r["vector"], r["trace"]
units.descend({"kg": 1, "m": 1, "s": -2})["vector"] == r["vector"]

# build_up(): the reverse question — which named unit and which laws have this dimension signature?
b = units.build_up("N")
b["named_unit"], b["candidate_laws"]

# Any unit reads the same way — the joule is kg * m^2 / s^2:
units.descend("J")["vector"]
