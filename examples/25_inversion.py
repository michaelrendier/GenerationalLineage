# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""inversion — J_N: (r, theta) -> (1/r, theta + pi/2). Four applications return home; two do not.

Run:  python3 examples/25_inversion.py
"""
from engine.toolsets import inversion

# descend(): one application.
r = inversion.descend((2.0, 0.0))
r["image"]

# build_up(): the orbit. Period 4 — and half of it (J_N squared) is a point inversion, NOT home.
b = inversion.build_up((2.0, 0.0))
b["period"], b["half_way_is_home"]
