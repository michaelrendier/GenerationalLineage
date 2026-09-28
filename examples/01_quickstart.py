# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Quickstart — the engine checks itself, then does one descent and one ascent.

Run:  python3 examples/01_quickstart.py        (or, without a script:  python3 -m engine --verify)
"""
import engine
from engine import lines

# Every toolset carries its own self-check. Nothing is asserted and left unchecked.
v = lines.verify_all()
v["_ok"]
len([k for k in v if not k.startswith("_")])

# One toolset, both directions. Reading a value's scale off a reference is one division — FREE.
lines.descend("scale", 15.0, reference=3.0)["scale"]

# Rebuilding a scale from a single reading of (x, y) is underdetermined: the ascent REFUSES,
# and the refusal names exactly what it is owed.
try:
    lines.build_up("scale", {"x": 2.0, "y": 9.0})
except engine.AscentNotFree as e:
    e.owed

# Supply the owed second reading and the same call succeeds — and reports what it cost.
r = lines.build_up("scale", {"x": 2.0, "y": 9.0}, probes=[(5.0, 21.0)])
r["scale"], r["add"], r["cost"]
