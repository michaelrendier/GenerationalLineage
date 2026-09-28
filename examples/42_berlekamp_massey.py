# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Berlekamp–Massey — the shortest recurrence behind a sequence, and the period it forces.

Established (Massey 1969; Berlekamp 1968) — see wiki/References.md.
Run:  python3 examples/42_berlekamp_massey.py
"""
from engine.toolsets import berlekamp_massey as bm
from engine.lines import AscentNotFree

# A sequence produced by a 5-bit LFSR whose characteristic polynomial is x^5 + x^2 + 1 (binary 100101):
seq = bm.lfsr(0b100101, [1, 0, 0, 0, 1], 40)
seq[:16]

# descend() recovers the generator from the output alone.
r = bm.descend(seq)
r["linear_complexity"], r["determined"], r["terms_needed"]
r["char_poly_int"] == 0b100101
r["period"], r["primitive"]

# The period is read off the FACTORISATION of the minimal polynomial:
# a primitive polynomial of degree 5 gives the maximal period 2^5 - 1.
r["factors"]

# Honesty: with fewer than 2L terms the recurrence is only a fit, and it says so.
short = bm.descend(seq[:7])
short["determined"], short["linear_complexity"], short["terms_needed"]

# build_up() pays for a choice: search for a primitive polynomial of degree 16.
b = bm.build_up({"degree": 16})
b["poly"], b["period"], b["cost"]

# ...and the ascent refuses if it is given nothing to build from.
try:
    bm.build_up({})
except AscentNotFree as e:
    e.owed
