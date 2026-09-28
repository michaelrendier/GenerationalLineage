# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""box_kite — the 15 zero-divisor edges of the sedenions, and the 7 ways to factor a relation.

Run:  python3 examples/22_box_kite.py
"""
from engine.toolsets import box_kite

# descend(): an index pair becomes its edge — one XOR. (1, 10) -> edge 1 XOR 10 = 11.
r = box_kite.descend((1, 10))
r["edge"], r["is_edge"]

# build_up(): an edge has 7 pencils — the seven ways to factor the relation into two others.
b = box_kite.build_up(11)
b["n_pencils"], b["cost"]
