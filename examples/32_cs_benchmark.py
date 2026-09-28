# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""cs_benchmark — measure a callable directly, and rank candidates against a reference cost.

Timing varies from machine to machine, so this tutorial prints only facts that do not.
Run:  python3 examples/32_cs_benchmark.py
"""
from engine.toolsets import cs_benchmark

# descend(): time one callable directly (real wall-clock, one pass).
r = cs_benchmark.descend(sum, args=([1, 2, 3],), n=200)
r["n_calls"], r["s_per_call"] > 0
r["citation"]
