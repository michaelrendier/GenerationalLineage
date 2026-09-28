# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""The generational lineage of a Clay Millennium Problem — what it builds, and what it imports.

This is a structural reading of each problem's central operation, not a solution of any of them.
Run:  python3 examples/15_clay.py
"""
from engine import CLAY, generational_lineage_of, clay_lineage_report

list(CLAY)

# Each problem's central operation is rolled down to the tier-0 floor:
r = generational_lineage_of("poincare")
r["status"], r["tier"], r["root"]
r["central_operation"]

# Only the solved problem is purely definitional; every open problem imports exactly one piece.
generational_lineage_of("riemann")["status"]
