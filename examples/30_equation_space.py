# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""equation_space — steer by a collapse function's own gradient; is the locus a fold or a smooth minimum?

Run:  python3 examples/30_equation_space.py
"""
from engine.toolsets import equation_space as eqs

# descend(): rho (distance to the interesting locus) and its local gradient at one point — free.
r = eqs.descend(0.5 + 0.1j)
round(r["rho"], 6), round(r["|gradient|"], 6)

# build_up(): walk from a start point down to rho = 0 by gradient descent; cost = steps.
b = eqs.build_up({"start": 0.5 + 0.1j})
b["converged"], b["cost"]

# The zero locus of this built-in rho is a fold caustic (linear falloff), not a smooth minimum:
eqs.classify_singularity(b["s"])["is_fold_caustic"]
