"""
GenerationalLineage.engine.toolsets.units
==========================================
UNITS — a quantity as a point in the 7-axis SI base-dimension lattice
(kg, m, s, A, K, mol, cd). The same decomposition, in a third domain.

DECOMPOSITION (free): a compound unit -> its exponent vector is exact vector
arithmetic. `N` -> (1, 1, -2, 0, 0, 0, 0). One pass.

EMERGER (work): a bare exponent vector -> which named physical laws have that
dimension. A scan over the law index; `cost` = entries scanned.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

NAME = "units"
LINE = "both"

AXES = ("kg", "m", "s", "A", "K", "mol", "cd")

# named compound -> exponent vector over AXES
COMPOUNDS: Dict[str, Tuple[int, ...]] = {
    "N":   (1, 1, -2, 0, 0, 0, 0),      # force
    "J":   (1, 2, -2, 0, 0, 0, 0),      # energy
    "W":   (1, 2, -3, 0, 0, 0, 0),      # power
    "Pa":  (1, -1, -2, 0, 0, 0, 0),     # pressure
    "C":   (0, 0, 1, 1, 0, 0, 0),       # charge
    "V":   (1, 2, -3, -1, 0, 0, 0),     # potential
    "Ohm": (1, 2, -3, -2, 0, 0, 0),     # resistance
    "F":   (-1, -2, 4, 2, 0, 0, 0),     # capacitance
    "Wb":  (1, 2, -2, -1, 0, 0, 0),     # magnetic flux
    "T":   (1, 0, -2, -1, 0, 0, 0),     # magnetic flux density
    "H":   (1, 2, -2, -2, 0, 0, 0),     # inductance
    "Hz":  (0, 0, -1, 0, 0, 0, 0),      # frequency
}
# exponent vector -> the physical law(s) that read that way
LAW_INDEX: Dict[Tuple[int, ...], List[str]] = {
    (1, 1, -2, 0, 0, 0, 0): ["F = m a", "F = dp/dt", "F = -k x (Hooke)"],
    (1, 2, -2, 0, 0, 0, 0): ["E = 1/2 m v^2", "E = m c^2", "W = F d", "E = q V"],
    (1, 2, -3, 0, 0, 0, 0): ["P = dE/dt", "P = F v", "P = I V"],
    (1, -1, -2, 0, 0, 0, 0): ["p = F / A", "p = rho g h", "p = n k T / V"],
    (0, 0, -1, 0, 0, 0, 0): ["f = 1 / T", "omega = 2 pi f"],
}


def _vec(unit: str | Dict[str, int] | Tuple[int, ...]) -> Tuple[int, ...]:
    if isinstance(unit, (tuple, list)):
        return tuple(int(x) for x in unit)
    if isinstance(unit, dict):
        return tuple(int(unit.get(a, 0)) for a in AXES)
    if unit in COMPOUNDS:
        return COMPOUNDS[unit]
    if unit in AXES:
        return tuple(1 if a == unit else 0 for a in AXES)
    raise KeyError(f"unknown unit {unit!r}")


def descend(unit: str | Dict[str, int]) -> Dict[str, Any]:
    v = _vec(unit)
    trace = " · ".join(f"{a}^{e}" for a, e in zip(AXES, v) if e) or "1 (dimensionless)"
    return {"toolset": NAME, "unit": unit, "axes": AXES, "vector": v,
            "trace": trace, "note": "exact vector arithmetic — the free reading"}


def build_up(signature: str | Dict[str, int] | Tuple[int, ...]) -> Dict[str, Any]:
    """A dimension signature -> candidate named laws. Scans the law index."""
    v = _vec(signature)
    scanned = 0
    hits: List[str] = []
    for key, laws in LAW_INDEX.items():
        scanned += 1
        if key == v:
            hits = list(laws)
            break
    named = [n for n, vec in COMPOUNDS.items() if vec == v]
    return {"toolset": NAME, "vector": v, "named_unit": named,
            "candidate_laws": hits, "cost": scanned,
            "note": ("scanned the law index" if hits
                     else "no law of that dimension in the index")}


def verify() -> Dict[str, Any]:
    d = descend("N")
    ok_d = d["vector"] == (1, 1, -2, 0, 0, 0, 0)
    b = build_up("J")
    ok_b = "E = m c^2" in b["candidate_laws"] and b["cost"] >= 1
    # mol/L * L = mol  (cancellation is exact)
    cancel = tuple(a + b for a, b in zip(_vec({"mol": 1, "m": -3}), _vec({"m": 3})))
    ok_c = cancel == _vec({"mol": 1})
    return {"ok": ok_d and ok_b and ok_c,
            "descend": ok_d, "build_up": ok_b, "cancellation_exact": ok_c}


if __name__ == "__main__":
    print(descend("N"))
    print(build_up("J"))
    print(verify())
