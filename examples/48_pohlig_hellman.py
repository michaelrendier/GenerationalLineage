# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Pohlig–Hellman — a discrete log is only as hard as the largest prime factor of the group order.

Established (Pohlig & Hellman 1978; baby-step giant-step, Shanks 1971) — wiki/References.md.
Run:  python3 examples/48_pohlig_hellman.py
"""
from engine.toolsets import pohlig_hellman as ph
from engine.lines import AscentNotFree

# 469762049 = 7 * 2^26 + 1 is a prime whose group order is smooth. descend() reads the LINEAGE of the
# order and predicts the cost of a discrete log without computing one.
p, g = 469762049, 3
d = ph.descend({"p": p, "g": g, "h": 5})
d["order_lineage"], d["largest_prime_factor"], d["predicted_cost_group_ops"]

# build_up() solves g^x = h, counting every group multiplication, and verifies the answer.
h = pow(g, 123456789, p)
r = ph.build_up({"p": p, "g": g, "h": h})
r["x"], r["verified"], r["cost"]

# A prime whose group order has a huge prime factor is a different matter: 1000000007 - 1 = 2 * 500000003.
d = ph.descend({"p": 1000000007, "g": 5, "h": 12345})
d["order_lineage"], d["predicted_cost_group_ops"]

# Over a budget, build_up() REFUSES and names the owed constraint. That residue is where the hardness lives.
try:
    ph.build_up({"p": 1000000007, "g": 5, "h": pow(5, 999, 1000000007), "budget": 10_000})
except AscentNotFree as e:
    e.owed
