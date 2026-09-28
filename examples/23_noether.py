# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""noether — check a conserved sum along a descent; filter ascent orders by the conservation law.

Run:  python3 examples/23_noether.py
"""
from engine.toolsets import noether

# descend(): red + blue readings taken along a decomposition. Was the sum conserved?
noether.descend([(0.3, 0.7), (0.5, 0.5), (0.1, 0.9)])["conserved"]
noether.descend([(0.3, 0.7), (0.6, 0.5)])["conserved"]

# build_up(): candidate build orders (per-step increments); keep those whose running sum stays in [0, total]
# and ends exactly on the total.
b = noether.build_up([[0.5, 0.3, 0.2], [0.9, 0.5, -0.4], [0.5, 0.6]], total=1.0)
b["legal"], b["cost"]
