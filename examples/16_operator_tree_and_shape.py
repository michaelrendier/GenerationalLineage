# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""The operator-string parser and the shape diagnostic — does an equation show evidence of every tier-0 root?

The parser reads the ASCII skeletons the keypad inserts; it extracts operator STRUCTURE, it is not a CAS.
Run:  python3 examples/16_operator_tree_and_shape.py
"""
from engine import opstring_parse, opstring_operators, shape_diagnose, KEYPAD

# The keypad is the alphabet: glyph, the ASCII skeleton it inserts, and its name.
len(KEYPAD)
KEYPAD[0][:2]

# Parse a definite integral: its variable and bounds come out as fields.
n = opstring_parse("I^1_0 x dx")
n.kind, n.var, n.lo, n.hi

# Nested operators are all listed, outermost first:
opstring_operators(opstring_parse("I^b_a D_x f dx"))

# The shape diagnostic reads those operators and reports which of ADD / SCALE / SIGN the equation
# shows evidence of, and which are missing (with the adjoint requirement for a self-adjoint claim).
r = shape_diagnose("I^b_a D_x f dx", self_adjoint=True)
r["roots_present"]
r["headline"]
