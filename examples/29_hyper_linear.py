# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""hyper_linear — long multiplication as one SCALE operation per digit; the bare product hides the rows.

Run:  python3 examples/29_hyper_linear.py
"""
from engine.toolsets import hyper_linear as hl

# descend(): a*b read as a regular representation — one tier-0 SCALE op per digit of b.
d = hl.descend(1546854629, 7283619945)
d["product"]
d["n_spilling_rows"], d["dft_reconstruction_exact"]
d["rows"][0]["operator"]

# From the bare product, "which rows spilled" is as hard as factoring it: the ascent refuses.
try:
    hl.build_up({"product": d["product"]})
except Exception as e:
    e.owed

# One factor supplied makes it free again — one division.
hl.build_up({"product": d["product"], "a": 1546854629})["b"]
