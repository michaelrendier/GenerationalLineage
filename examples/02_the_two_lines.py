# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""The two lines — what is free, and what must be paid for.

Every toolset has descend() (read the object down: free, cost 0) and build_up() (build it up:
a search or an added constraint, so it reports a cost and may refuse).
Run:  python3 examples/02_the_two_lines.py
"""
from engine import lines

# The registry: which toolsets serve which line.
lines.DECOMPOSITION_LINE[:4]
lines.EMERGER_LINE[-4:]

# descend() always sets free=True, cost=0 — it is a single forward pass with no stored tape.
d = lines.descend("noether", [(0.3, 0.7), (0.5, 0.5), (0.1, 0.9)])
d["free"], d["cost"], d["conserved"]

# build_up() sets free=False and reports the work it did: here, scanning candidate orders.
b = lines.build_up("noether", [[0.5, 0.3, 0.2], [0.9, 0.5, -0.4], [0.5, 0.6]], total=1.0)
b["free"], b["cost"], b["legal"]

# The registry text for any toolset says in one line what each direction does:
lines.TOOLSETS["hyper_linear"]["free"]
lines.TOOLSETS["hyper_linear"]["work"]

# hyper_linear's ascent is REFUSED from the bare product — recovering it is as hard as factoring —
# and becomes free again the moment one factor is supplied:
p = lines.descend("hyper_linear", 1546854629, 7283619945)["product"]
try:
    lines.build_up("hyper_linear", {"product": p})
except lines.AscentNotFree as e:
    e.owed
lines.build_up("hyper_linear", {"product": p, "a": 1546854629})["b"]
