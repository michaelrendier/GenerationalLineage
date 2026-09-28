# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Unicity — how much ciphertext makes the decomposition unique (Shannon).

Established (Shannon 1949) — see wiki/References.md.
Run:  python3 examples/49_unicity.py
"""
from engine.toolsets import unicity

# U = H(K) / D : key entropy over the plaintext's redundancy. For a general substitution cipher on English:
r = unicity.descend("substitution")
round(r["key_entropy_bits"], 3)
round(r["U_shannon_estimate"], 1)

# The literature estimate (Shannon's D = 3.2 bits/char) and a rigorous bound are kept apart.
# The order-0 letter table gives D0 exactly; since true redundancy can only be higher, U <= H(K)/D0.
round(r["D0_order0"], 4), round(r["U_upper_bound_rigorous"], 1)

# Other ciphers, same call:
for spec in ({"kind": "caesar"}, {"kind": "vigenere", "period": 7}, {"kind": "enigma"}):
    x = unicity.descend(spec)
    print(spec["kind"], round(x["key_entropy_bits"], 1), "bits ->", round(x["U_shannon_estimate"], 1), "chars (estimate)")

# build_up(): the ciphertext you must PAY FOR so the expected number of spurious keys is at most epsilon.
b = unicity.build_up({"kind": "substitution", "max_spurious": 1e-3})
b["characters_needed"], round(b["expected_spurious_at_n"], 6)
