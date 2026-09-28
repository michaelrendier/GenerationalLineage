# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""The crystal and the join — recover an unseen period from repeat structure, and a permutation's order from its cycles.

Run:  python3 examples/10_crystal_and_join.py
"""
from engine import repeat_distances, infer_period_by_stem_vote, permutation_order_direct, permutation_order_via_stems

# Repeats of a 3-gram sit at distances that are multiples of the hidden period (Kasiski's idea):
seq = [1, 2, 3, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3]
d = repeat_distances(seq, 3)
d
v = infer_period_by_stem_vote(d)
v["best_period"], v["votes"][3], v["n_distances"]

# A permutation's order is the LCM (the join) of its cycle lengths — the dual of the gcd (the meet).
perm = [1, 2, 0, 4, 3]
permutation_order_direct(perm), permutation_order_via_stems(perm)
