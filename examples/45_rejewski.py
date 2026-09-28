# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Rejewski — the conjugacy-class invariant that the Enigma plugboard cannot disturb.

Established (Rejewski 1980) — see wiki/References.md.
Run:  python3 examples/45_rejewski.py
"""
from engine.toolsets import rejewski

# First, the implementation is checked against the standard known-answer vector:
# Enigma I, rotors I-II-III, reflector B, ring settings AAA, positions AAA, no plugs.
rejewski.encipher("AAAAA", "AAA")

# The plugboard wraps every rotor-path permutation: S' = P S P. A product S'_i S'_(i+3) is therefore
# a CONJUGATE of S_i S_(i+3), and conjugates share a cycle type. So the characteristic
# (cycle types of the 1&4, 2&5, 3&6 products) is unchanged by any plugboard:
plain = rejewski.descend("QEV")
plugged = rejewski.descend("QEV", plugboard="AB CD EF GH IJ KL MN OP QR ST")
plain["characteristic"]
plain["characteristic"] == plugged["characteristic"], plugged["plugboard_independent"]

# Every S_i is a fixed-point-free involution, so each cycle length occurs an even number of times:
plain["even_multiplicities"]

# build_up() is the card catalogue: given an OBSERVED characteristic, scan all 26^3 start positions.
# The plugboard is never part of the search.
hit = rejewski.build_up({"characteristic": plugged["characteristic"]})
hit["cost"], hit["distinct_characteristics"]
"QEV" in hit["matches"], hit["n_matches"]
