# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
# SPDX-License-Identifier: GPL-3.0-only
"""ADD : SCALE : SIGN — the tier-0 floor as a value you can hold, and what SIGN does (and does not) decide.

The group is  x ↦ sign·scale·x + add  =  ADD ⋊ (SCALE × SIGN).
Run:  python3 examples/06_add_scale_sign.py
"""
import math
from engine import ASS, fisr_word

# Compose (the right-hand element fires first), invert, and strip generators:
T = ASS(add=3.0, scale=2.5, sign=-1)
T(2.0)
(~T)(T(2.0))
T.parts()
T.residual("SIGN")

# The word is u = sign*ln(scale) + add, and the fold is gamma = tanh(u/2):
T.u(), T.gamma()

# The firing defect (g - 1) * ln(s) is zero exactly when SIGN or SCALE is at its identity:
ASS(add=0.0, scale=1.0, sign=-1).firing_defect()
ASS(add=0.0, scale=2.0, sign=-1).firing_defect(), -2 * math.log(2.0)

# SIGN commutes with SCALE, but not with ADD (it reflects the offset); SCALE does not commute with ADD either.
S, A, G = ASS.SCALE(2.0), ASS.ADD(3.0), ASS.SIGN(-1)
((G @ S).add, (G @ S).scale, (G @ S).sign), ((S @ G).add, (S @ G).scale, (S @ G).sign)
(G @ A).add, (A @ G).add

# Noether currents: the direction of the net flow is sign * scale * offset, an exact identity.
# ln F - ln B = E(1 - 2*sigma) = ASS(0, 2E, -1) applied to (sigma - 1/2)
E, sigma = 2.0, 0.25
F, B = math.exp(-sigma * E), math.exp(-(1 - sigma) * E)
math.log(F) - math.log(B), ASS(0.0, 2 * E, -1)(sigma - 0.5)

# The fast inverse square root (Quake III) is a three-generator ADD:SCALE:SIGN word on ln x:
w = fisr_word(4.0)
w["ASS_word_on_ln_x"]
round(w["FISR raw (no Newton)"], 4), round(w["FISR + 1 Newton"], 4), w["1/√x exact"]
