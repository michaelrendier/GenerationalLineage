# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""The Emerger — the ascent dual: bracket a 16-vector and walk the brackets in a firing order.

Run:  python3 examples/08_emerger.py
"""
from engine import emerge_brackets, legal_orders, bracketings_for, cd_is_zero_divisor

# A sedenion e1 + e10 — a classic zero-divisor pair member. Is it a zero divisor?
e = [0] * 16
e[1], e[10] = 1, 1
cd_is_zero_divisor(e)

# The Emerger brackets it five ways and walks them in a firing order. Firing order is load-bearing:
# of 120 possible orders, only 4 respect the dependencies.
len(legal_orders())
r = emerge_brackets(e)
r["input_norm"]
fo = r["firing_order"]
fo["canonical"]
fo["sigma_rb_phased"]
fo["phased_is_legal"]

# Each step names the bracket, its tier label, and what it emerges:
[(s["bracket"], s["tier"]) for s in r["steps"][:3]]
r["steps"][0]["emerges"]
