# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""The two trees — every integer is prime, composite, or one of the two identities; the sieve, and its mirror.

Run:  python3 examples/05_the_two_trees.py
"""
from engine import two_trees, sieve_lineage, un_sieve

# 2 + 168 + 831 = 1001: every integer in [0, 1000] lands in exactly one class. Exact, not statistical.
t = two_trees(1000)
t["telperion_prime"], t["laurelin_composite"], t["mingling_0_and_1"], t["total"], t["exact"]

# The sieve of Eratosthenes as a lineage: each composite dies on the pass of its smallest prime factor.
s = sieve_lineage(1000)
s["working_passes"], s["pi_sqrt_N"], s["generation_matches_pi_spf"]

# The un-sieve is its mirror: switch primes ON one at a time and watch each composite ARRIVE.
u = un_sieve(1000)
u["D_equals_reverse_A"]
u["extinction_boundary_prime"], u["birth_boundary_prime"]
round(u["H_C_minus_H_A"], 3)
