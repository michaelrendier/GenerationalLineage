"""
GenerationalLineage.engine.operator_tree
=========================================
THE OPERATOR TREE — a graph of every named operation, placed on a tier and
rooted on one of the three tier-0 engineered operators (ADD, SCALE, SIGN),
carrying its fold signature. Rendered for the console as three pillars.

Not a rooted tree — a graph: operations share parents, several names cover one
computation, and an operation is often reachable by more than one composition.
Layout borrows the three-pillar shape: one pillar per ROOT_OF class, the three
generators at the head, rows by tier.

    build_tree()                 -> Tree      (nodes + edges + pillars)
    fold_signature(name)         -> (n_add, n_scale, n_sign, tier)   [coarse]
    render_ascii(tree, cols, rows, pad=5) -> list[str]
    to_json(tree)                -> dict
    route_targets(tree, name)    -> dict      (jurisdictional routing)
    word_wrap(text, width)       -> list[str] (never truncates)

Geometry is a fraction of the live terminal; only `pad` (side margin) is fixed.
Every box word-wraps to its inner width and grows downward — no overflow. Sub-
labels are indented 2 spaces from the title text.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from .lineage import TIERS, ROOT_OF

_AXES = ("ADD", "SCALE", "SIGN")


# ── text helpers ────────────────────────────────────────────────────────────
def word_wrap(text: str, width: int) -> List[str]:
    """Greedy word wrap. Never truncates: a word longer than `width` gets its
    own (over-long) line rather than being cut."""
    width = max(1, int(width))
    out: List[str] = []
    for para in str(text).split("\n"):
        line = ""
        for w in para.split(" "):
            if not line:
                line = w
            elif len(line) + 1 + len(w) <= width:
                line += " " + w
            else:
                out.append(line)
                line = w
        out.append(line)
    return out or [""]


def box(title: str, subs: List[str], inner_w: int, marker: str = "") -> List[str]:
    """A bordered box. `title` wraps to inner_w; each sub wraps to inner_w-2 and
    is printed indented 2. Height grows to fit — the box never clips."""
    inner_w = max(6, int(inner_w))
    top = "┌" + "─" * inner_w + "┐"
    bot = "└" + "─" * inner_w + "┘"
    rows = [top]
    for ln in word_wrap(title, inner_w):
        pad = " " * (inner_w - len(ln))
        rows.append("│" + ln[:inner_w] + pad + "│")
    for s in subs:
        for ln in word_wrap(s, inner_w - 2):
            body = "  " + ln
            body = body[:inner_w] + " " * (inner_w - len(body))
            rows.append("│" + body + "│")
    if marker:
        m = ("◀ " + marker)[:inner_w]
        rows.append("│" + m + " " * (inner_w - len(m)) + "│")
    rows.append(bot)
    return rows


# ── the graph ───────────────────────────────────────────────────────────────
@dataclass
class Node:
    name: str
    tier: int
    root: str                      # ADD | SCALE | SIGN | None
    descends_from: str = ""
    fold: Tuple[int, int, int, int] = (0, 0, 0, 0)
    note: str = ""
    engines: List[str] = field(default_factory=list)
    status: str = "placed"         # placed | generator | unplaced(emergence)
    code: str = ""


@dataclass
class Tree:
    nodes: Dict[str, Node]
    edges: List[Tuple[str, str, str]]         # (child, parent, kind)
    pillars: Dict[str, List[str]]             # axis -> node names, tier order

    def by_pillar(self, axis: str) -> List[Node]:
        return [self.nodes[n] for n in self.pillars.get(axis, [])]


def fold_signature(name: str) -> Tuple[int, int, int, int]:
    """Coarse (n_ADD, n_SCALE, n_SIGN, tier) until opstring feeds real ASS
    words: the root axis carries the tier depth; a REFLECT / parity mention in
    `descends_from` adds one SIGN; a length-change mention adds one SCALE."""
    key = name.strip().lower()
    if key in _AXES or key.upper() in _AXES:
        i = _AXES.index(key.upper())
        return tuple(1 if j == i else 0 for j in range(3)) + (0,)
    tinfo = TIERS.get(key)
    if not tinfo:
        return (0, 0, 0, -1)
    tier, descends, _ = tinfo
    root = ROOT_OF.get(key)
    v = [0, 0, 0]
    if root in _AXES:
        v[_AXES.index(root)] += tier + 1
    d = (descends or "").lower()
    if "reflect" in d or "parity" in d or "sign" in d:
        v[2] += 1
    if "scale" in d or "dilate" in d or "length" in d:
        v[1] += 1
    return (v[0], v[1], v[2], tier)


def build_tree(manifests: List[Dict[str, Any]] | None = None) -> Tree:
    """Build from the engine's own TIERS / ROOT_OF vocabulary. `manifests` is
    the seam for the per-engine `valaquenta.plugin/1` harvest — stubbed: pass a
    list of {name, tier, root, engines, code} dicts to fold extra nodes in."""
    nodes: Dict[str, Node] = {}
    edges: List[Tuple[str, str, str]] = []

    for ax in _AXES:
        nodes[ax] = Node(ax, 0, ax, "—", fold_signature(ax),
                         "irreducible generator", status="generator")

    for key, (tier, descends, note) in TIERS.items():
        if key in ("add", "scale", "sign"):
            continue
        root = ROOT_OF.get(key)
        nodes[key] = Node(key, tier, (root or "").upper() or None,
                          descends, fold_signature(key), note)
        parent = (root or "").upper()
        if parent in nodes:
            edges.append((key, parent, "roots-on"))
        if descends and descends not in ("—",):
            edges.append((key, descends, "descends-from"))

    for m in manifests or []:
        nm = m["name"].strip().lower()
        nodes[nm] = Node(nm, int(m.get("tier", 3)),
                         (m.get("root") or "").upper() or None,
                         m.get("descends_from", ""),
                         tuple(m.get("fold", (0, 0, 0, int(m.get("tier", 3))))),
                         m.get("note", ""), list(m.get("engines", [])),
                         "placed", m.get("code", ""))
        if nodes[nm].root in nodes:
            edges.append((nm, nodes[nm].root, "roots-on"))

    pillars: Dict[str, List[str]] = {ax: [] for ax in _AXES}
    for n in nodes.values():
        if n.root in pillars and n.status != "generator":
            pillars[n.root].append(n.name)
    for ax in _AXES:
        pillars[ax].sort(key=lambda k: (nodes[k].tier, k))
        pillars[ax].insert(0, ax)                      # generator heads its pillar
    return Tree(nodes, edges, pillars)


# ── ascii render ────────────────────────────────────────────────────────────
_HEADS = {"ADD": "ADD · Kether", "SCALE": "SCALE · Chokmah", "SIGN": "SIGN · Binah"}


def render_ascii(tree: Tree, cols: int, rows: int, pad: int = 5,
                 cursor: str = "", max_per_pillar: int = 6) -> List[str]:
    canvas_cols = max(24, cols - 2 * pad)
    canvas_rows = max(8, rows - 3)
    pillar_w = canvas_cols // 3
    box_inner = max(10, int(pillar_w * 0.90) - 2)
    lead = " " * pad
    gap = " " * max(1, (canvas_cols - 3 * (box_inner + 2)) // 2)

    cols_text: List[List[str]] = []
    for ax in _AXES:
        col: List[str] = []
        names = tree.pillars.get(ax, [])
        shown, hidden = names[:max_per_pillar], names[max_per_pillar:]
        for nm in shown:
            n = tree.nodes[nm]
            title = (_HEADS[ax] if n.status == "generator"
                     else f"{n.name}   tier ·{n.tier}")
            subs = []
            if n.note:
                subs.append(n.note)
            f = n.fold
            subs.append(f"fold ({f[0]}·ADD {f[1]}·SCALE {f[2]}·SIGN)  root {n.root}")
            if n.engines:
                subs.append("engines: " + " · ".join(n.engines))
            if n.code:
                subs.append(n.code)
            col += box(title, subs, box_inner, marker=("cursor" if nm == cursor else ""))
            col.append(" " * (box_inner + 2))                 # spacer / edge slot
        if hidden:
            col.append(f"  (+{len(hidden)} more — scroll)".ljust(box_inner + 2))
        cols_text.append(col)

    height = min(canvas_rows, max((len(c) for c in cols_text), default=0))
    for c in cols_text:
        c += [" " * (box_inner + 2)] * (height - len(c))

    out: List[str] = []
    bar = f"{lead}Operator Tree — 3 pillars = the three engineered operators (ADD · SCALE · SIGN)"
    out.append(bar[:cols])
    for r in range(height):
        line = lead + cols_text[0][r][:box_inner + 2] + gap \
            + cols_text[1][r][:box_inner + 2] + gap \
            + cols_text[2][r][:box_inner + 2]
        out.append(line[:cols])
    cur = tree.nodes.get(cursor)
    crumb = (f"{lead}▸ {cur.root} pillar ▸ {cur.name}   ⏎ route   ↑↓←→ move"
             if cur else f"{lead}↑↓←→ move   ⏎ route   Tab tabs")
    out.append(crumb[:cols])
    return out


# ── json + routing ─────────────────────────────────────────────────────────
def to_json(tree: Tree) -> Dict[str, Any]:
    return {
        "nodes": [
            {"name": n.name, "tier": n.tier, "root": n.root,
             "descends_from": n.descends_from, "fold": list(n.fold),
             "note": n.note, "engines": n.engines, "status": n.status,
             "code": n.code}
            for n in tree.nodes.values()
        ],
        "edges": [{"child": c, "parent": p, "kind": k} for c, p, k in tree.edges],
        "pillars": tree.pillars,
    }


def route_targets(tree: Tree, name: str) -> Dict[str, Any]:
    """Jurisdictional routing: appropriateness = shares a root, a tier, or an
    engine. Returns the analysis pathway plus the in-jurisdiction neighbours."""
    key = name.strip().lower()
    n = tree.nodes.get(key)
    if n is None:
        return {"error": f"no node {name!r}",
                "analyse": "shape",  # unknown -> the missing-operator diagnostic
                "note": "not placed — route to Find evidence for missing operators"}
    same_pillar = [m for m in tree.pillars.get(n.root or "", []) if m != key][:12]
    same_tier = [m for m, nd in tree.nodes.items()
                 if nd.tier == n.tier and m != key][:12]
    analyse = ("ass_fold" if n.status == "generator"
               else "shape" if n.tier == -1 or n.status.startswith("unplaced")
               else "decompose")
    return {
        "node": key, "tier": n.tier, "root": n.root, "fold": list(n.fold),
        "analyse": analyse,
        "toolsets": {"scale": ["scale"], "gcd": ["scale"], "factoral": ["lineage"],
                     "associator": ["box_kite", "emerger"], "unit": ["units"],
                     }.get(key, []),
        "wiki": {"add": "ADD-SCALE-SIGN-Datatype", "scale": "Scale",
                 "sign": "ADD-SCALE-SIGN-Datatype"}.get(key,
                 "The-Operator-Tree"),
        "same_pillar": same_pillar, "same_tier": same_tier,
        "engines": n.engines,
    }


def verify() -> Dict[str, Any]:
    t = build_tree()
    ok_gen = all(t.nodes[a].status == "generator" for a in _AXES)
    ok_pillars = all(t.pillars[a][0] == a for a in _AXES)
    ok_place = t.nodes["associator"].root == "SIGN" and t.nodes["gcd"].root == "SCALE"
    r80 = render_ascii(t, 80, 24, cursor="associator")
    r240 = render_ascii(t, 240, 64, cursor="scale")
    ok_render = (all(len(x) <= 80 for x in r80) and all(len(x) <= 240 for x in r240)
                 and len(r80) > 4 and len(r240) > 4)
    j = to_json(t)
    ok_json = len(j["nodes"]) == len(t.nodes) and "pillars" in j
    rt = route_targets(t, "associator")
    ok_route = rt["root"] == "SIGN" and rt["analyse"] == "decompose" \
        and "emerger" in rt["toolsets"]
    ok_unplaced = route_targets(t, "nonesuch")["analyse"] == "shape"
    ok_wrap = word_wrap("a b c d e f g h", 5) == ["a b c", "d e f", "g h"]
    return {"ok": all([ok_gen, ok_pillars, ok_place, ok_render, ok_json,
                       ok_route, ok_unplaced, ok_wrap]),
            "generators": ok_gen, "pillars": ok_pillars, "placement": ok_place,
            "render_80_and_240": ok_render, "json": ok_json, "routing": ok_route,
            "unplaced_routes_to_shape": ok_unplaced, "word_wrap": ok_wrap}


if __name__ == "__main__":
    t = build_tree()
    print("\n".join(render_ascii(t, 80, 30, cursor="associator")))
    print()
    print(verify())
