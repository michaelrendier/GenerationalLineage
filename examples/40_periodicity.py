# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Periodicity — every period of a string, exactly, and why the GCD-vote works.

Established algorithm (KMP prefix function; Fine & Wilf 1965) — see wiki/References.md.
Run:  python3 examples/40_periodicity.py
"""
from engine.toolsets import periodicity

# descend(): every period of the string, read off one linear pass. Nothing is voted.
r = periodicity.descend("abcabcabca")
r["periods"]
r["min_period"], r["borders"]

# A string made by repeating a root has the root as its primitive period;
# the exponent counts the copies — the string's "generation length".
r = periodicity.descend("ab" * 32)
r["min_period"], r["primitive_root"], r["exponent"]

# Two independent routes (prefix function, Z function) must agree:
r["agrees_with_z_function"]

# Fine–Wilf: a string of length ≥ p + q − gcd(p, q) with periods p and q also has period gcd(p, q).
# build_up() constructs the extremal word ONE LETTER SHORT of that bound, with both periods but not the gcd:
w = periodicity.build_up({"p": 5, "q": 8})["string"]
w, len(w)
periodicity.periods(w)

# It cannot be extended by even one letter and keep both periods:
# the next letter would have to equal both w[-5] and w[-8], and they differ.
w[-5], w[-8]

# The ascent is a choice; asked for nothing, it refuses and names what it is owed.
try:
    periodicity.build_up({})
except Exception as e:
    type(e).__name__, e.owed
