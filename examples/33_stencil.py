# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""stencil — the digit-by-digit decomposition machine: exact, exhaustive, never a heuristic.

Run:  python3 examples/33_stencil.py
"""
from engine.toolsets import stencil
from engine.lines import AscentNotFree

# descend(): N = p*q — one multiplication, no search.
stencil.descend(53, 61)["N"]

# build_up(): given only N, construct the factor pairs digit by digit. Slide 1 to full depth is exact,
# so EVERY divisor pair is found.
b = stencil.build_up(3233)
b["pairs"], b["cost"]
stencil.build_up(360)["pairs"][:4]

# A prime has no pair, and the refusal is the result:
try:
    stencil.build_up(3229)
except AscentNotFree as e:
    type(e).__name__
