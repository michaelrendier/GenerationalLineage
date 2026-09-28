# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""The pathway — factoring as a walk between two pinned anchors, and why the walk must be TUNED per number.

The pathway layer is real sub-exponential factoring (a CFRAC-style walk), not a metaphor; the framework's own
reading is that the tuning is a sigma-dilate and the excursion a difficulty gauge.
Run:  python3 examples/17_pathway_and_tuning.py
"""
from engine import spiral_address, pathway_residues, tune_pathway, fermat_path

# Every integer has an address on the log-spiral. The address of a product is the SUM of the addresses of its factors.
a = spiral_address(97)
round(a["log_radius"], 4), round(a["angle"], 4)

# The untuned walk (multiplier 1) reaches a factor of 3233 = 53 * 61 ...
pathway_residues(3233, mult=1)["factor"]

# ... but for 1451951 = 1009 * 1439 the untuned walk finds NOTHING within its budget:
pathway_residues(1451951, mult=1)["factor"] is None

# Tuning sweeps multipliers until one resonates onto a factor. Here multiplier 3 does, at step 86:
t = tune_pathway(1451951)
t["tuning"], t["step"], t["factor"]

# Fermat's method as a path: the "excursion" is the walk's own difficulty gauge. Balanced factors sit at the anchor ...
f = fermat_path(3233)
f["factor"], f["excursion"]

# ... and a less balanced pair wanders further before it closes:
f = fermat_path(1234007)
f["factor"], f["excursion"]
