# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""The tier test — is a named operation primitive, or derived from something simpler?

Four questions, in order: a count or ratio? a fixed set? does it change length? does it need an
added constraint? What survives all four is a candidate primitive.
Run:  python3 examples/04_tier_test.py
"""
from engine import decompose, root_irreducible, TIERS

# 'leverage' needs rigidity to exist — remove rigidity and the fulcrum survives, leverage does not.
d = decompose("leverage")
d["tier"], d["status"], d["descends_from"]
d["note"]

# 'fulcrum' is a fixed set: tier 2, derived.
decompose("fulcrum")["tier"]

# 'scale' is irreducible: tier 0, a primitive.
r = root_irreducible("scale")
r["tier"], r["status"], r["root"]

# Every operation rolls down to one of exactly three roots — ADD, SCALE or SIGN:
{op: decompose(op)["root"] for op in ("leverage", "reflect", "dilate", "rotate", "gcd", "sign")}
