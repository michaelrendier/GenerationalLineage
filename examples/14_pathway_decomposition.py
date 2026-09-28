# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Pathway decomposition — factoring a PROCESS (a dependency graph of operators), not a number.

Run:  python3 examples/14_pathway_decomposition.py
"""
from engine import ProcessOperator, pathway_decomposition

# RSA's CRT decryption is a genuine fan-out: m1 and m2 depend only on the input, h on BOTH, m on h and m2.
# (p, q, e, c toy values: p=61, q=53, e=17, message 65 encrypted to 2790.)
p, q, e, c = 61, 53, 17, 2790
d = pow(e, -1, (p - 1) * (q - 1))
# Each operator's function receives the outputs of the operators it depends on, positionally, in order.
ops = [
    ProcessOperator("m1", lambda inp: pow(inp, d % (p - 1), p), depends_on=("input",)),
    ProcessOperator("m2", lambda inp: pow(inp, d % (q - 1), q), depends_on=("input",)),
    ProcessOperator("h", lambda m1, m2: ((m1 - m2) * pow(q, -1, p)) % p, depends_on=("m1", "m2")),
    ProcessOperator("m", lambda h, m2: m2 + h * q, depends_on=("h", "m2")),
]
r = pathway_decomposition(c, ops, output_name="m")
r["real"]
r["dim"]
r["order"]
