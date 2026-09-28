# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""scale — pull SCALE out of a quantity, and put it back (a second reading pays for the offset).

Run:  python3 examples/20_scale.py
"""
from engine.toolsets import scale

# descend(): scale = value / reference. One division.
r = scale.descend(15.0, reference=3.0)
r["scale"], r["sign"], round(r["ln_scale"], 6)

# build_up(): one (x, y) reading cannot fix both a scale and an offset. It refuses, naming what it is owed.
try:
    scale.build_up({"x": 2.0, "y": 9.0})
except Exception as e:
    e.owed

# With a second reading the line y = s*x + a is determined:
r = scale.build_up({"x": 2.0, "y": 9.0}, probes=[(5.0, 21.0)])
r["scale"], r["add"], r["max_residual"]
