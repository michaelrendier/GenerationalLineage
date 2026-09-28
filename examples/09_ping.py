# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""ping — classify an RSA modulus by which counter-operator reaches it (the Emerger–Lineage unification).

Run:  python3 examples/09_ping.py
"""
from engine import ping

# 3233 = 53 * 61: q is small, so trial division reaches it.
r = ping(3233)
r["factored"], r["factors"], r["regime"]
[(s["op"], s["fired"]) for s in r["path"]]

# 1000003 * 1000033: the two factors are close (|p - q| = 30). Trial division fails, and Fermat's method
# — which reaches factors near sqrt(N) — fires. The path records which operator reached it.
r = ping(1000003 * 1000033)
r["factored"], r["regime"]
[(s["op"], s["fired"]) for s in r["path"]]
