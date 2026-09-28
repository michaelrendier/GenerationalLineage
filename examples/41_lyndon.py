# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Lyndon — the unique prime factorisation of a word.

Established (Chen–Fox–Lyndon 1958; Duval 1983) — see wiki/References.md.
Run:  python3 examples/41_lyndon.py
"""
from engine.toolsets import lyndon

# Every word factors uniquely into Lyndon words in non-increasing order.
r = lyndon.descend("banana")
r["factors"], r["omega"]
r["all_lyndon"], r["nonincreasing"], r["reassembles"]

# The canonical necklace representative and the primitive root come for free:
r = lyndon.descend("abababab")
r["primitive_root"], r["exponent"], r["necklace_representative"]

# A rotation of a word has the same necklace representative:
lyndon.descend("ababab")["necklace_representative"] == lyndon.descend("bababa")["necklace_representative"]

# build_up() enumerates the Lyndon words of a length; the count is checked against the Moebius formula.
b = lyndon.build_up({"n": 6, "k": 2})
b["count"], b["expected_count"], b["necklaces"]
b["words"][:4]

# Reassembling is free: non-increasing order is the only legal one.
lyndon.build_up({"factors": ["a", "ab", "b"]})["word"]
