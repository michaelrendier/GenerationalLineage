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
)

MODULES = {
    "scale": scale, "units": units, "box_kite": box_kite, "noether": noether,
    "archimedes_screw": archimedes_screw, "inversion": inversion,
    "t32_nilpotency": t32_nilpotency,
}
