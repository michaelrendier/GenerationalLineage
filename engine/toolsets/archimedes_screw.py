# This file is part of GenerationalLineage.
# Copyright (C) 2026 Cody Michael Allison
#
# GenerationalLineage is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, version 3 of the License.
#
# GenerationalLineage is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details. You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-only
"""
GenerationalLineage.engine.toolsets.archimedes_screw
=====================================================
ARCHIMEDES SCREW — the machine (a logarithm), distinct from the medium it
lifts. It sets the LOG-PITCH of the tier ladder: a step from a to b is a
pitch of ln(b/a), and the tier boundaries sit at a constant pitch ln 2.

DECOMPOSITION (free): read the pitch off a step. One log.

EMERGER (work): climb to a target height. The rung size (ln 2) is fixed; the
number of rungs is a choice, and the leftover has to be lifted by hand. `cost`
= rungs climbed.
"""
from __future__ import annotations

import math
from typing import Any, Dict

NAME = "archimedes_screw"
LINE = "both"

RUNG = math.log(2.0)                              # the Cayley-Dickson doubling pitch


def descend(step: tuple) -> Dict[str, Any]:
    a, b = float(step[0]), float(step[1])
    if a <= 0 or b <= 0:
        raise ValueError("both readings must be positive")
    pitch = math.log(b / a)
    return {"toolset": NAME, "step": (a, b), "pitch": pitch,
            "rungs_equiv": pitch / RUNG,
            "is_prime_gap_like": abs(pitch) < RUNG,
            "note": "one log — the free reading"}


def build_up(height: float) -> Dict[str, Any]:
    """Climb `height` (in natural-log units) using rungs of size ln 2, then
    lift the remainder by hand."""
    h = float(height)
    rungs = int(math.floor(abs(h) / RUNG))
    sign = 1 if h >= 0 else -1
    climbed = sign * rungs * RUNG
    remainder = h - climbed
    return {"toolset": NAME, "height": h, "rung": RUNG, "rungs": rungs,
            "climbed": climbed, "remainder_by_hand": remainder,
            "cost": rungs,
            "note": "rungs are ln 2; the remainder is the work the ladder can't do"}


def verify() -> Dict[str, Any]:
    d = descend((2.0, 4.0))
    ok_d = math.isclose(d["pitch"], RUNG)
    b = build_up(3.5 * RUNG)
    ok_b = b["rungs"] == 3 and math.isclose(b["remainder_by_hand"], 0.5 * RUNG)
    return {"ok": ok_d and ok_b, "descend": ok_d, "build_up": ok_b}


if __name__ == "__main__":
    print(descend((2.0, 4.0)))
    print(build_up(3.5 * RUNG))
    print(verify())
