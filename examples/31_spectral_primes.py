# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""spectral_primes — spin (a smooth carrier) and wobble (the oscillation that carries the primes).

Run:  python3 examples/31_spectral_primes.py
"""
from engine.toolsets import spectral_primes as sp

# descend(): the spin rate theta'(t) at one height — smooth and monotonic, no peaks by construction.
r = sp.descend(100.0)
round(r["spin_rate"], 6), r["resonant"]

# build_up(): rebuild psi(x) from n zeros. The primes emerge only as work (more zeros) is spent.
b10 = sp.build_up(30.0, n_zeros=10)
b25 = sp.build_up(30.0, n_zeros=25)
round(b10["exact"], 4)
abs(b25["difference"]) < abs(b10["difference"])
b10["cost"], b25["cost"]
