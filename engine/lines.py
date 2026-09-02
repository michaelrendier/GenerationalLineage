"""
GenerationalLineage.engine.lines
=================================
THE TWO LINES — and why their maths differs by direction.

The Generational Lineage engine runs in two directions, and they are not the
same computation run backwards. They are two jurisdictions:

    DECOMPOSITION LINE   descent   "what built this"      anchor: lineage.py
    EMERGER LINE         ascent    "what does this build"  anchor: emerger.py

    "The extinction order is not the rebirth order. Extinction is free;
     rebirth requires work."                     — Cody Michael Allison

DESCENT is the deductive sieve of Eratosthenes: mark the multiples, read off
what is left. Single pass, no search, no stored tape. It is forward-propagating
— the instinct direction, the one the maths is built to go. `descend()` on any
toolset costs nothing: `free = True`, `cost = 0`.

ASCENT is induction: to rebuild an object you must choose — which bracketing,
which firing order (4 legal of 120), which pitch to climb, which pencil to
factor a relation into. Choice is work. `build_up()` on any toolset searches or
needs an added constraint, and reports a `cost` (steps taken) and
`free = False`.

The relativity: when the descent jurisdiction looks at an object it names it in
descent terms (tiers, roots, the two trees); when the ascent jurisdiction looks
at the same object it names it in ascent terms (domains, firing phase, gain
class). One direction is an **adjoint** of the other, not a companion — and an
adjoint is the one that costs. `inversion` is the map between the two.

TOOLSET CONTRACT
----------------
Each toolset module in `engine/toolsets/` (and the two older ports,
`add_scale_sign.py`, `oscilloscope.py`) exposes:

    NAME        str
    LINE        "decomposition" | "emerger" | "both"
    descend(x, **k)      -> dict  with free=True,  cost=0
    build_up(target, **k)-> dict  with free=False, cost=<steps>
    verify()            -> dict  with ok=<bool>

A `LINE == "decomposition"` toolset may raise `AscentNotFree` from `build_up`
if the rebuild is genuinely undetermined without the caller supplying the
missing constraint — that refusal IS the result ("rebirth requires work, and
here is the work you owe").
"""
from __future__ import annotations

import importlib
from typing import Any, Callable, Dict, List


class AscentNotFree(Exception):
    """build_up() cannot proceed without an added constraint the caller owes.
    Carries `.owed` — a short string naming what is missing."""

    def __init__(self, owed: str, msg: str = "") -> None:
        self.owed = owed
        super().__init__(msg or f"ascent requires: {owed}")


# ── the registry ─────────────────────────────────────────────────────────────
# module   = engine.<...> import path
# line     = which jurisdiction(s) the toolset serves
# free/work= one-line reading of descend() / build_up() for this toolset
TOOLSETS: Dict[str, Dict[str, str]] = {
    "add_scale_sign": {
        "module": "engine.add_scale_sign", "line": "both",
        "free": "read SCALE/SIGN/ADD off a value — three lookups",
        "work": "choose the firing order (of the [SCALE,ADD]=ADD bracket) that hits a target map",
    },
    "scale": {
        "module": "engine.toolsets.scale", "line": "both",
        "free": "s = value / reference — one division",
        "work": "solve for s under a constrained target — underdetermined, needs a second reading",
    },
    "units": {
        "module": "engine.toolsets.units", "line": "both",
        "free": "a quantity -> its point in the 7-axis SI lattice (exact vector arithmetic)",
        "work": "a dimension signature -> candidate physical laws — a search over the law index",
    },
    "box_kite": {
        "module": "engine.toolsets.box_kite", "line": "both",
        "free": "a relation -> which of the 15 zero-divisor edges / which line",
        "work": "which of the 7 pencils factors a relation into two others — a choice",
    },
    "noether": {
        "module": "engine.toolsets.noether", "line": "both",
        "free": "check J_red + J_blue is conserved along a decomposition",
        "work": "which emergence orders the conservation law permits — filter the legal set",
    },
    "archimedes_screw": {
        "module": "engine.toolsets.archimedes_screw", "line": "both",
        "free": "read the log-pitch ln p off a step",
        "work": "choose which rung to climb (the doubling ln 2 is fixed, the rung is not)",
    },
    "inversion": {
        "module": "engine.toolsets.inversion", "line": "both",
        "free": "J_N: (r, theta) -> (1/r, theta + pi/2) — one map",
        "work": "the same map IS the bridge descent<->ascent; applying it twice returns identity",
    },
    "t32_nilpotency": {
        "module": "engine.toolsets.t32_nilpotency", "line": "both",
        "free": "decode a base-97 address to its path",
        "work": "find an address that realises a desired path — a search",
    },
    "oscilloscope": {
        "module": "engine.oscilloscope", "line": "decomposition",
        "free": "stack the two facets (Fermat prompt / Riemann firing) of one number",
        "work": "—",
    },
    "emerger": {
        "module": "engine.emerger", "line": "emerger",
        "free": "—",
        "work": "bracket a 16-vector five ways; walk the brackets in a chosen firing order",
    },
    "lineage": {
        "module": "engine.lineage", "line": "decomposition",
        "free": "roll any operator down to the tier-0 floor — single pass, terminates on ASS",
        "work": "—",
    },
}

DECOMPOSITION_LINE: List[str] = [n for n, d in TOOLSETS.items()
                                 if d["line"] in ("decomposition", "both")]
EMERGER_LINE: List[str] = [n for n, d in TOOLSETS.items()
                           if d["line"] in ("emerger", "both")]


# ── dispatch ─────────────────────────────────────────────────────────────────
def _load(name: str):
    return importlib.import_module(TOOLSETS[name]["module"])


def toolset(name: str):
    """Import and return a toolset module by name."""
    return _load(name)


def descend(name: str, x: Any, **k) -> Dict[str, Any]:
    """Run the FREE (descent) reading of a toolset. Adds free=True, cost=0."""
    m = _load(name)
    fn: Callable = getattr(m, "descend")
    out = dict(fn(x, **k))
    out.setdefault("free", True)
    out.setdefault("cost", 0)
    out["line"] = "decomposition"
    return out


def build_up(name: str, target: Any, **k) -> Dict[str, Any]:
    """Run the WORK (ascent) reading of a toolset. Adds free=False; the toolset
    reports its own `cost`. May raise AscentNotFree."""
    m = _load(name)
    fn: Callable = getattr(m, "build_up")
    out = dict(fn(target, **k))
    out.setdefault("free", False)
    out.setdefault("cost", None)
    out["line"] = "emerger"
    return out


def verify_all() -> Dict[str, Any]:
    """Self-check every toolset that exposes verify()."""
    res: Dict[str, Any] = {}
    for name, d in TOOLSETS.items():
        try:
            m = _load(name)
        except Exception as e:                                    # noqa: BLE001
            res[name] = {"ok": False, "error": f"import: {e}"}
            continue
        v = getattr(m, "verify", None)
        r = v() if callable(v) else {"ok": True, "note": "no verify()"}
        if "ok" not in r:                       # emerger.verify uses `all_pass`
            r = {**r, "ok": bool(r.get("all_pass", False))}
        res[name] = r
    res["_ok"] = all(r.get("ok", False) for k, r in res.items() if not k.startswith("_"))
    return res


def describe_lines() -> str:
    L = ["THE TWO LINES", "",
         "DECOMPOSITION (descent, deductive, extinction) — FREE:"]
    for n in DECOMPOSITION_LINE:
        L.append(f"  {n:<18} {TOOLSETS[n]['free']}")
    L += ["", "EMERGER (ascent, inductive, rebirth) — WORK:"]
    for n in EMERGER_LINE:
        L.append(f"  {n:<18} {TOOLSETS[n]['work']}")
    L += ["", "inversion (J_N) is the map between the two jurisdictions.",
          "extinction is free; rebirth requires work; the orders are not the same."]
    return "\n".join(L)


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(describe_lines())
    print()
    v = verify_all()
    for k, r in v.items():
        if not k.startswith("_"):
            print(f"  {'ok ' if r.get('ok') else 'FAIL'} {k}: {r}")
    print("\nALL OK" if v["_ok"] else "\nFAILURES ABOVE")
