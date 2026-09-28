# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""Re-Pair — a sequence's own lineage tree, built by repeated pairing.

Established (Larsson & Moffat 2000; smallest grammar is NP-hard, Charikar et al. 2005) — wiki/References.md.
Run:  python3 examples/47_re_pair.py
"""
from engine.toolsets import re_pair

# 64 copies of one letter need only five rules: a lineage of depth 5.
r = re_pair.descend("a" * 64)
r["rules"]
r["start"], r["n_rules"], r["depth"]

# The round trip is exact:
r["round_trip_exact"]

# Repeated structure collapses; the grammar is far smaller than the text.
p = re_pair.descend("abracadabra" * 3)
p["n"], p["grammar_size"], p["depth"]

# Symbols with no repeated pair do not descend at all.
u = re_pair.descend(list(range(50)))
u["n_rules"], u["depth"]

# Honesty: the smallest grammar is NP-hard to find, so minimality is reported as unknown, not assumed.
r["minimal"] is None

# build_up() expands a grammar back to the sequence.
"".join(re_pair.build_up({"grammar": r["_grammar"]})["sequence"]) == "a" * 64
