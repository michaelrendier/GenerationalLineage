# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Jordan–Chevalley — split an operator into a part that only scales and a part that only shifts and dies.

Established (Jordan–Chevalley decomposition; see Humphreys, Linear Algebraic Groups) — wiki/References.md.
Run:  python3 examples/46_jordan_chevalley.py
"""
from engine.toolsets import jordan_chevalley as jc

# Build a matrix with a chosen Jordan structure: a 2-chain at eigenvalue 1, and a lone point at eigenvalue 3.
A = jc.build_up({"blocks": [(1, 2), (3, 1)]})["A"]
[[str(x) for x in row] for row in A]

# descend() splits A = S + N exactly, in rational arithmetic (no floating point anywhere).
r = jc.descend(A)
[[str(x) for x in row] for row in r["S"]]
[[str(x) for x in row] for row in r["N"]]

# N is nilpotent: it lives for `nilpotency_index` generations and then dies.
r["nilpotency_index"], r["jordan_block_sizes_of_N"]

# Everything was re-checked, not trusted:
r["checks"]

# A diagonalisable matrix has N = 0; a nilpotent one has S = 0.
d = jc.descend(jc.build_up({"blocks": [(1, 1), (2, 1), (3, 1)]})["A"])
d["is_semisimple"], d["nilpotency_index"]
