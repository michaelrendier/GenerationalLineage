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
GenerationalLineage.engine.toolsets
====================================
The toolset ports that feed the Generational Lineage engine, each standalone
(stdlib + math only, this repo's module-independence convention — NOT a
cross-repo import of ValaQuenta's copy).

Every toolset here follows the contract in `engine/lines.py`:

    NAME        str
    LINE        "decomposition" | "emerger" | "both"
    descend(x, **k)       -> dict   (the FREE reading — single pass, cost 0)
    build_up(target, **k) -> dict   (the WORK reading — search / added
                                     constraint; reports `cost`; may raise
                                     lines.AscentNotFree)
    verify()             -> dict    (self-check, ok=<bool>)

Two older ports keep their historic filenames one level up:
`engine/add_scale_sign.py` (the tier-0 floor as a value type) and
`engine/oscilloscope.py` (the two-facet instrument).
"""
from . import (                                                  # noqa: F401
    scale, units, box_kite, noether, archimedes_screw, inversion, t32_nilpotency,
    cipher, comma_sequence, stencil, hyper_linear, equation_space, spectral_primes,
    cs_benchmark,
    periodicity, lyndon, berlekamp_massey, logperiodic, permutation, rejewski,
    jordan_chevalley, re_pair, pohlig_hellman, unicity,
)

MODULES = {
    "scale": scale, "units": units, "box_kite": box_kite, "noether": noether,
    "archimedes_screw": archimedes_screw, "inversion": inversion,
    "t32_nilpotency": t32_nilpotency, "cipher": cipher,
    "comma_sequence": comma_sequence, "stencil": stencil,
    "hyper_linear": hyper_linear, "equation_space": equation_space,
    "spectral_primes": spectral_primes, "cs_benchmark": cs_benchmark,
    "periodicity": periodicity, "lyndon": lyndon, "berlekamp_massey": berlekamp_massey,
    "logperiodic": logperiodic, "permutation": permutation, "rejewski": rejewski,
    "jordan_chevalley": jordan_chevalley, "re_pair": re_pair,
    "pohlig_hellman": pohlig_hellman, "unicity": unicity,
}
