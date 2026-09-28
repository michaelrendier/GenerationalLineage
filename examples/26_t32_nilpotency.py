# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""t32_nilpotency — a base-97 address is a path; trailing zeros make it nilpotent.

Run:  python3 examples/26_t32_nilpotency.py
"""
from engine.toolsets import t32_nilpotency as t32

# descend(): decode an address to its path — one Horner sweep.
r = t32.descend(123456)
r["path"], r["nilpotent"], r["trailing_zeros"]

# build_up(): place digits one at a time to realise a chosen path, and confirm it round-trips.
b = t32.build_up([1, 2, 3])
b["address"], b["round_trips"]
