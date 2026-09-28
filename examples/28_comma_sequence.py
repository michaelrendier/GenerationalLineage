# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""comma_sequence — the lexicographically-earliest comma walk; each gap is read off the digits at the comma.

Run:  python3 examples/28_comma_sequence.py
"""
from engine.toolsets import comma_sequence as cs

# build_up(): walk the earliest valid comma sequence forward; the cost is the number of terms placed.
b = cs.build_up(12)
b["sequence"], b["cost"], b["died_at"]

# descend(): read a sequence back — is it a valid comma walk, and does the base survive?
r = cs.descend(b["sequence"])
r["valid_comma_walk"], r["mortal_base"], r["resolution_ratio"]
