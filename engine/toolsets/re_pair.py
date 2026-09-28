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
GenerationalLineage.engine.toolsets.re_pair
============================================
RE-PAIR — a sequence's own lineage tree, built by repeated pairing.

Re-Pair (Larsson–Moffat) compresses a sequence by repeatedly replacing its most
frequent adjacent pair with a fresh symbol. What it emits is a *straight-line
program*: a set of rules  Rₖ → (left, right)  plus a short residual start
sequence. That is exactly a lineage:

    terminal symbol        generation 0        (a leaf: irreducible)
    rule Rₖ → (x, y)       generation 1 + max(gen x, gen y)
    grammar depth          the number of generations the sequence needs
    grammar size           |start| + 2·|rules|  — the sequence's Ω-analogue,
                           the cost of writing it down through its own repeats

    a⁶⁴   →  R₁=aa, R₂=R₁R₁, … R₅   start = R₅R₅       5 rules, depth 5
    (abc)²⁰                           collapses to a handful of rules
    random-looking data               almost no rules: it does not descend

It is the string version of `factor_lineage`: the derivation tree IS the
factorisation, and how deep it goes measures how much structure repeated.

HONESTY. Finding the *smallest* such grammar is NP-hard (Charikar et al.,
2005). Re-Pair is a greedy heuristic, so `descend` reports the grammar it
found and states `minimal: None` — unknown — rather than claiming
optimality. What IS guaranteed, exactly and checked exhaustively, is the
round trip: expand(grammar) == input.

DECOMPOSITION (free): `descend(seq)` — polynomial time, deterministic
(ties broken by earliest first occurrence).
EMERGER (work): `build_up({'grammar': …})` expands a grammar back to the
sequence (cost = symbols produced). It refuses a cyclic grammar.
"""
from __future__ import annotations

from typing import Any, Dict, List, Sequence, Tuple

from ..lines import AscentNotFree

NAME = "re_pair"
LINE = "both"


def _count_pairs(seq: List[int]) -> Dict[Tuple[int, int], List[int]]:
    """pair → non-overlapping left-to-right start positions (handles runs like aaaa)."""
    pos: Dict[Tuple[int, int], List[int]] = {}
    i = 0
    n = len(seq)
    last_taken: Dict[Tuple[int, int], int] = {}
    for i in range(n - 1):
        pr = (seq[i], seq[i + 1])
        if last_taken.get(pr, -2) >= i - 1 and pr[0] == pr[1]:
            continue                                     # overlaps the previous aa
        pos.setdefault(pr, []).append(i)
        last_taken[pr] = i
    return pos


def compress(items: Sequence) -> Dict[str, Any]:
    alphabet: List[Any] = []
    index: Dict[Any, int] = {}
    seq: List[int] = []
    for it in items:
        if it not in index:
            index[it] = len(alphabet)
            alphabet.append(it)
        seq.append(index[it])
    base = len(alphabet)
    rules: Dict[int, Tuple[int, int]] = {}
    while True:
        pos = _count_pairs(seq)
        if not pos:
            break
        best = max(pos.items(), key=lambda kv: (len(kv[1]), -kv[1][0]))
        pr, starts = best
        if len(starts) < 2:
            break
        nt = base + len(rules)
        rules[nt] = pr
        starts_set = set(starts)
        out, i = [], 0
        while i < len(seq):
            if i in starts_set:
                out.append(nt)
                i += 2
            else:
                out.append(seq[i])
                i += 1
        seq = out
    return {"alphabet": alphabet, "rules": rules, "start": seq, "base": base}


def expand(g: Dict[str, Any]) -> List[Any]:
    base, rules, alphabet = g["base"], g["rules"], g["alphabet"]
    for nt, (l, r) in rules.items():                 # acyclic by construction: a rule may only
        if nt < base or l >= nt or r >= nt:          # reference symbols that already exist
            raise ValueError(f"rule {nt} references a symbol that does not precede it (cyclic)")
    out: List[Any] = []
    stack = list(reversed(g["start"]))
    guard = 0
    limit = 10_000_000
    while stack:
        s = stack.pop()
        if s < base:
            out.append(alphabet[s])
        else:
            l, r = rules[s]
            stack.append(r)
            stack.append(l)
        guard += 1
        if guard > limit:
            raise ValueError("grammar does not terminate (cyclic?)")
    return out


def generations(g: Dict[str, Any]) -> Dict[int, int]:
    base, rules = g["base"], g["rules"]
    gen: Dict[int, int] = {}
    for nt in sorted(rules):                    # rules only reference earlier symbols
        l, r = rules[nt]
        gl = 0 if l < base else gen[l]
        gr = 0 if r < base else gen[r]
        gen[nt] = 1 + max(gl, gr)
    return gen


def descend(x, **_) -> Dict[str, Any]:
    items = list(x)
    g = compress(items)
    gen = generations(g)
    size = len(g["start"]) + 2 * len(g["rules"])
    return {
        "toolset": NAME, "n": len(items),
        "rules": {f"R{nt - g['base'] + 1}": tuple(
            (g["alphabet"][s] if s < g["base"] else f"R{s - g['base'] + 1}") for s in pr)
            for nt, pr in g["rules"].items()},
        "start": [(g["alphabet"][s] if s < g["base"] else f"R{s - g['base'] + 1}") for s in g["start"]],
        "n_rules": len(g["rules"]),
        "depth": max(gen.values()) if gen else 0,
        "generation_of_rules": {f"R{nt - g['base'] + 1}": v for nt, v in gen.items()},
        "grammar_size": size, "compression_ratio": size / max(1, len(items)),
        "round_trip_exact": expand(g) == items,
        "minimal": None,
        "_grammar": g,
        "note": "depth = generations of repeated structure; smallest-grammar is NP-hard, "
                "so minimality is reported as unknown, not assumed",
    }


def build_up(target, **_) -> Dict[str, Any]:
    if isinstance(target, dict) and "grammar" in target:
        g = target["grammar"]
        try:
            out = expand(g)
        except (KeyError, RecursionError, ValueError) as e:
            raise AscentNotFree("an acyclic grammar (each rule may only use earlier symbols)", str(e))
        return {"toolset": NAME, "direction": "grammar -> sequence", "sequence": out,
                "cost": len(out), "note": "expansion is a forward pass; the choice was the grammar"}
    raise AscentNotFree("{'grammar': <grammar from descend()['_grammar']>}")


def verify() -> Dict[str, Any]:
    # 1. exhaustive round trip: every binary string up to length 12, and every string over
    #    {a,b,c} up to length 7
    ok_rt, count = True, 0
    for n in range(0, 13):
        for m in range(1 << n):
            s = [(m >> i) & 1 for i in range(n)]
            if expand(compress(s)) != s:
                ok_rt = False
            count += 1
    from itertools import product
    for n in range(0, 8):
        for s in product("abc", repeat=n):
            if expand(compress(list(s))) != list(s):
                ok_rt = False
            count += 1

    # 2. structure: a^(2^k) has k-1 rules... concretely a^64 → 5 rules, depth 5, start length 2
    d = descend("a" * 64)
    ok_pow = d["n_rules"] == 5 and d["depth"] == 5 and len(d["start"]) == 2

    # 3. periodic text collapses; grammar size ≪ n
    p = descend("abc" * 20)
    ok_period = p["grammar_size"] < 0.4 * p["n"] and p["round_trip_exact"]

    # 4. incompressible-by-pairs data does not descend: all-distinct symbols → no rules
    u = descend(list(range(50)))
    ok_flat = u["n_rules"] == 0 and u["depth"] == 0

    # 5. build_up expands; a cyclic grammar is refused
    g = d["_grammar"]
    ok_up = build_up({"grammar": g})["sequence"] == list("a" * 64)
    bad = {"alphabet": ["a"], "base": 1, "rules": {1: (1, 0)}, "start": [1]}
    try:
        build_up({"grammar": bad})
        ok_cyc = False
    except AscentNotFree:
        ok_cyc = True
    try:
        build_up({})
        ok_refuse = False
    except AscentNotFree:
        ok_refuse = True

    return {"ok": all([ok_rt, ok_pow, ok_period, ok_flat, ok_up, ok_cyc, ok_refuse]),
            "exhaustive_round_trip": ok_rt, "sequences_checked": count,
            "a64_is_5_rules_depth_5": ok_pow, "periodic_collapses": ok_period,
            "distinct_symbols_do_not_descend": ok_flat, "expand_round_trip": ok_up,
            "cyclic_grammar_refused": ok_cyc, "refuses_without_grammar": ok_refuse}


if __name__ == "__main__":
    r = descend("abracadabra_abracadabra")
    r.pop("_grammar")
    print(r)
    print(verify())
