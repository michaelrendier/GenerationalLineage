# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""archimedes_screw — the logarithm as a screw: one turn is one prime, a lift of ln p.

Run:  python3 examples/24_archimedes_screw.py
"""
from engine.toolsets import archimedes_screw as screw

# descend(): the log-pitch of a step, read with one logarithm.
r = screw.descend((2, 6))
round(r["pitch"], 6), round(r["rungs_equiv"], 6)

# build_up(): climb to a target height in rungs of ln 2; whatever is left is the work the ladder cannot do.
b = screw.build_up(5.0)
b["rungs"], round(b["climbed"], 6), round(b["remainder_by_hand"], 6)
