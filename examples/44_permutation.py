# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Permutation — the invariants of a re-ordering, and modular affine permutations (ADD ⋊ SCALE on Z/m).

Established (cycle type, Lehmer code, factorial number system; Diaconis–Graham–Kantor 1983) — wiki/References.md.
Run:  python3 examples/44_permutation.py
"""
from engine.toolsets import permutation

# One pass reads everything: cycle type (the conjugacy class), order (the lcm), sign, factoradic rank.
r = permutation.descend([2, 0, 1, 4, 3, 5])
r["cycle_type"], r["order"], r["sign"]
r["lehmer"], r["factoradic_rank"]

# The factorial number system is a bijection onto 0..n!-1; un-ranking recovers the permutation.
permutation.build_up({"rank": r["factoradic_rank"], "n": 6})["perm"]

# Order is the lcm of the cycle lengths, so the cheapest permutation of order 60 uses one cycle per
# prime power of 60 = 4 * 3 * 5:
b = permutation.build_up({"order": 60})
b["cycle_type"], b["degree"], permutation.descend(b["perm"])["order"]

# x -> a*x + b (mod m) is the ADD ⋊ SCALE group acting on Z/m. Its cycle structure is a multiplicative order:
perm = permutation.affine_perm(3, 0, 26)
permutation.descend(perm)["cycle_type"]
permutation.mult_order(3, 26)

# Card shuffles are affine permutations. A 52-card deck: out-shuffle order 8, in-shuffle order 52.
permutation.shuffle_order(26, "out"), permutation.shuffle_order(26, "in")
