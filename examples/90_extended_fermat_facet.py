# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""EXTENDED layer — the Fermat-facet inventory and the control test (needs the four sibling repos).

This tutorial only runs in an EXTENDED install (see README, 'Extended install'); on a plain clone it
prints one line and stops.
Run:  python3 examples/90_extended_fermat_facet.py
"""
import engine

if not engine.EXTENDED:
    print("EXTENDED layer not installed — skipping (see README, 'Extended install').")
else:
    p = engine.quantized_pieces()
    p["cd_tower_levels"], p["leaf_level"]
    # The control: real prime counts by residue class mod 16, against Dirichlet equidistribution.
    engine.pathway_root_system_class(13)
