# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Matrix flow — the nine flows of dx/dt = A x, and which kind of circle each one is.

Established (linear-systems classification; Cayley–Klein elliptic/parabolic/hyperbolic) — see wiki/References.md.
Run:  python3 examples/51_matrix_flow.py
"""
from engine.toolsets import matrix_flow

# One matrix per flow: its class, the kind of circle, and the split A = a·I + b·J + h1·K1 + h2·K2
# (a = SCALE, b = the quarter turn J with J² = −I, h = the boost K with K² = +I).
for name, M in matrix_flow.EXAMPLES.items():
    r = matrix_flow.descend(M)
    sp = r["split"]
    print(f"{name:22s} {r['kind']:26s} a={sp['a_scale']:+.2f} b={sp['b_turn']:+.2f} h={sp['h']:.2f}")

# The sign of h² − b² decides the kind: rotation wins -> circle, boost wins -> hyperbola, tie -> shear.
for M in ([[0, -1], [1, 0]], [[1, 0], [0, -1]], [[1, 1], [0, 1]]):
    print(M, "h² − b² =", matrix_flow.split(M)["kind_gap"], "->", matrix_flow.classify(M))

# exp(tA) in closed form: a centre turns through t radians; a saddle keeps x·y; a shear is I + tN.
[[round(v, 4) for v in row] for row in matrix_flow.expm([[0, -1], [1, 0]], 3.141592653589793 / 2)]

# The emerger direction: how many integer matrices with entries in [−2, 2] fall in each class?
b = matrix_flow.build_up(2)
b["counts"], b["cost"]
