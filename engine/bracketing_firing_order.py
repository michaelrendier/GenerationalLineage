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
GenerationalLineage.engine.bracketing_firing_order
=======================================================
THE BRACKETING ENGINE, THE FIRING ORDER ENGINE, AND SET MEMBERSHIP --
standalone port, this repo's module-independence convention (cf.
`engine/add_scale_sign.py`'s own note) -- same maths, ported not imported
from ValaQuenta.modules.bracketing_firing_order.

Three general-purpose, domain-independent tools -- not tied to
`add_scale_sign`'s 3 generators specifically, though that engine (and its
own `.lineage()`/`ASSWord` methods) is one consumer of tool 3a here.

    BRACKETING    -- how many unordered ways can n things be grouped?
                     exact Bell number always; exhaustive list only when
                     n<=12 (refuses above that, does not silently hang).
    FIRING PLANS  -- (tool 4) brackets that carry firing orders: (A B | 2 1) fires B
                     first; a bracket runs as one operation in its own order.
    FIRING ORDER  -- how many ways can n things be SEQUENCED? n!, and
                     applying one is a literal permutation action.
                     Verified: (3,1,2) on [Scale,Sign,Add] -> [Add,Scale,
                     Sign] -- add_scale_sign's own CAMSHAFT name, reached
                     by resequencing, not relabeling.
    SET MEMBERSHIP -- two jobs: (a) has a firing recurred (trajectory/
                     collision detection, generalizing Recaman's own
                     defining rule); (b) did a bracketing cause one
                     jurisdiction's maths to be used on an object native
                     to another -- grounded in THIS repo's own
                     `engine/lines.py` TOOLSETS/DECOMPOSITION_LINE/
                     EMERGER_LINE ("the two jurisdictions"), which this
                     module can read directly since it's the same repo.
"""
from __future__ import annotations

import itertools
import math
from fractions import Fraction as F
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple

from .emerger import cd_mul, left_matrix

ENUMERATION_CEILING_N = 12


# ── TOOL 1 — BRACKETING ─────────────────────────────────────────────────

def bell_number(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    triangle = [[1]]
    for i in range(1, n + 1):
        row = [triangle[i - 1][-1]]
        for j in range(1, i + 1):
            row.append(row[j - 1] + triangle[i - 1][j - 1])
        triangle.append(row)
    return triangle[n][0]


def set_partitions(items: Sequence[Any]) -> List[List[List[Any]]]:
    n = len(items)
    if n > ENUMERATION_CEILING_N:
        raise ValueError(
            f"set_partitions refuses n={n} > {ENUMERATION_CEILING_N} -- "
            f"Bell({n})={bell_number(n)} partitions is not a listable quantity. "
            f"Use bell_number({n}) for the exact count.")
    if n == 0:
        return [[]]
    first, rest = items[0], items[1:]
    out: List[List[List[Any]]] = []
    for smaller in set_partitions(rest):
        for i in range(len(smaller)):
            new_partition = [g[:] for g in smaller]
            new_partition[i] = [first] + new_partition[i]
            out.append(new_partition)
        out.append([[first]] + [g[:] for g in smaller])
    return out


def bracketing_report(items: Sequence[Any]) -> Dict[str, Any]:
    n = len(items)
    count = bell_number(n)
    feasible = n <= ENUMERATION_CEILING_N
    report = {"n": n, "bell_number": count, "enumerable": feasible, "items": list(items)}
    if feasible:
        report["partitions"] = set_partitions(list(items))
    else:
        report["note"] = (f"Bell({n})={count} exceeds the enumeration ceiling "
                           f"({ENUMERATION_CEILING_N}) -- counted exactly, not listed.")
    return report


# ── TOOL 2 — FIRING ORDER ───────────────────────────────────────────────

def firing_order_count(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    return math.factorial(n)


def apply_firing_order(written: Sequence[Any], firing_order: Sequence[int]) -> List[Any]:
    n = len(written)
    if sorted(firing_order) != list(range(1, n + 1)):
        raise ValueError(f"firing_order must be a permutation of 1..{n}, got {firing_order}")
    return [written[i - 1] for i in firing_order]


def all_firing_orders(items: Sequence[Any]) -> List[Tuple[Any, ...]]:
    return list(itertools.permutations(items))


# ── TOOL 3a — SET MEMBERSHIP: has a firing occurred before? ────────────

def trajectory(steps: Sequence[Callable[[float], float]], x0: float = 1.0) -> Tuple[float, ...]:
    pos = [x0]
    x = x0
    for s in steps:
        x = s(x)
        pos.append(x)
    return tuple(pos)


def visited_positions(steps: Sequence[Callable[[float], float]], x0: float = 1.0,
                       tol: float = 1e-9) -> Dict[float, List[int]]:
    traj = trajectory(steps, x0)
    seen: Dict[float, List[int]] = {}
    for i, x in enumerate(traj):
        key = round(x / tol) * tol if tol else x
        seen.setdefault(key, []).append(i)
    return seen


def collisions(steps: Sequence[Callable[[float], float]], x0: float = 1.0,
               tol: float = 1e-9) -> List[Tuple[int, int, float]]:
    seen = visited_positions(steps, x0, tol)
    out = []
    for pos, idxs in seen.items():
        if len(idxs) > 1:
            for a, b in zip(idxs, idxs[1:]):
                out.append((a, b, pos))
    return sorted(out)


def would_collide(steps_so_far: Sequence[Callable[[float], float]],
                   candidate_next: Callable[[float], float],
                   x0: float = 1.0, tol: float = 1e-9) -> bool:
    traj = trajectory(steps_so_far, x0)
    candidate = candidate_next(traj[-1])
    visited = {round(x / tol) * tol if tol else x for x in traj}
    key = round(candidate / tol) * tol if tol else candidate
    return key in visited


# ── TOOL 3b — SET MEMBERSHIP: jurisdiction violation ────────────────────
# This repo's own jurisdiction map is real and importable directly here
# (same repo, not a cross-repo reach) -- engine/lines.py's TOOLSETS dict,
# read into {name: {legal_ops}} shape rather than duplicated by hand.

def jurisdiction_violation(object_name: str, requested_operation: str,
                            jurisdiction_map: Dict[str, Set[str]]) -> Dict[str, Any]:
    legal_ops = jurisdiction_map.get(object_name)
    if legal_ops is None:
        return {"object": object_name, "operation": requested_operation,
                "known": False, "violation": None,
                "note": f"'{object_name}' not present in the supplied jurisdiction map"}
    violated = requested_operation not in legal_ops
    return {
        "object": object_name, "operation": requested_operation,
        "known": True, "legal_operations": sorted(legal_ops), "violation": violated,
        "note": (f"'{requested_operation}' is NOT legal for '{object_name}' "
                 f"(legal set: {sorted(legal_ops)})" if violated else
                 f"'{requested_operation}' is legal for '{object_name}'"),
    }


def this_repos_jurisdiction_map() -> Dict[str, Set[str]]:
    """Builds the real jurisdiction map from THIS repo's own engine/lines.py
    -- not a hardcoded duplicate. 'both' toolsets get {'descend','build_up'};
    decomposition-only gets {'descend'}; emerger-only gets {'build_up'}."""
    from .lines import TOOLSETS
    out: Dict[str, Set[str]] = {}
    for name, d in TOOLSETS.items():
        ops = set()
        if d["line"] in ("decomposition", "both"):
            ops.add("descend")
        if d["line"] in ("emerger", "both"):
            ops.add("build_up")
        out[name] = ops
    return out


# ── TOOL 4 — FIRING PLANS: brackets that carry firing orders ───────────
# Ported from SedenionSpectralRelativity/firing_plan.py (same maths, this repo's
# module-independence convention). exact Fractions; cd_mul/left_matrix from .emerger.
# A bracket is one operation; its children fire in its own order (2,1) = second
# child first); nested brackets run as one operation inside their parent.
# See wiki/Firing-Plans.md.

def _identity(n):
    return [[F(int(r == c)) for c in range(n)] for r in range(n)]


def _matmul(A, B):
    n = len(A)
    Bt = list(zip(*B))
    return [[sum((a * b for a, b in zip(row, col)), F(0)) for col in Bt] for row in A]


def _equal(A, B):
    return all(a == b for ra, rb in zip(A, B) for a, b in zip(ra, rb))


def _key(A):
    return tuple(tuple(r) for r in A)


# ── the plan ────────────────────────────────────────────────────────────────
class Leaf:
    """one operator.  `matrix` is its operator reading (operator()); `vec` is its element reading
    (value()).  Either may be absent if only the other reading is used."""
    def __init__(self, name, matrix=None, vec=None):
        self.name, self.matrix, self.vec = name, matrix, vec

    def __repr__(self):
        return self.name


class Bracket:
    def __init__(self, children, order=None):
        k = len(children)
        order = tuple(range(1, k + 1)) if order is None else tuple(order)
        if sorted(order) != list(range(1, k + 1)):
            raise ValueError(f"order must be a permutation of 1..{k}, got {order}")
        self.children, self.order = list(children), order

    def fired(self):
        """the children in the order they fire"""
        return [self.children[i - 1] for i in self.order]

    def __repr__(self):
        return notation(self)


def notation(plan):
    if isinstance(plan, Leaf):
        return plan.name
    body = " ".join(notation(c) for c in plan.children)
    if plan.order != tuple(range(1, len(plan.children) + 1)):
        body += " | " + " ".join(str(i) for i in plan.order)
    return f"({body})"


def fire_sequence(plan):
    """leaf names in the exact order they fire, internal bracket orders included"""
    if isinstance(plan, Leaf):
        return [plan.name]
    return [name for c in plan.fired() for name in fire_sequence(c)]


def operator(plan):
    """the plan as ONE operator: fired children composed, first fired applied first"""
    if isinstance(plan, Leaf):
        return plan.matrix
    n = len(plan.children[0].matrix) if isinstance(plan.children[0], Leaf) else len(operator(plan.children[0]))
    M = _identity(n)
    for c in plan.fired():
        M = _matmul(operator(c), M)
    return M


def value(plan):
    """the ELEMENT reading: a bracket is the algebra product of its fired children, folded left to
    right in firing order ((f1 f2) f3 …); nested brackets give the other groupings.  Unlike
    operator(), this is non-associative in the sedenions, so here the bracketing itself matters."""
    if isinstance(plan, Leaf):
        return tuple(plan.vec)
    kids = [value(c) for c in plan.fired()]
    acc = kids[0]
    for k in kids[1:]:
        acc = tuple(cd_mul(acc, k))
    return acc


def apply_plan(plan, x):
    M = operator(plan)
    return tuple(sum((m * v for m, v in zip(row, x)), F(0)) for row in M)


def parse(text, leaves):
    """'((A B | 2 1) C)' with leaves = {name: matrix} -> plan.  Whitespace-separated tokens."""
    toks = text.replace("(", " ( ").replace(")", " ) ").replace("|", " | ").split()
    pos = 0

    def group():
        nonlocal pos
        assert toks[pos] == "("; pos += 1
        kids, order = [], None
        while toks[pos] != ")":
            if toks[pos] == "(":
                kids.append(group())
            elif toks[pos] == "|":
                pos += 1; order = []
                while toks[pos] != ")":
                    order.append(int(toks[pos])); pos += 1
            else:
                kids.append(Leaf(toks[pos], leaves[toks[pos]])); pos += 1
        pos += 1
        return Bracket(kids, order)
    plan = group()
    assert pos == len(toks), "trailing tokens"
    return plan


# ── counting and enumeration ────────────────────────────────────────────────
def count_plans(n, kind="nary"):
    """How many plans over n leaves written in order.  kind:
         'flat'    one bracket, all n leaves, any order                      n!
         'binary'  every bracket has two children: Catalan(n-1) shapes, 2 orders per bracket
         'nary'    every bracket has ≥2 children and its own k! orders (ordered Schröder shapes)"""
    if kind == "flat":
        return math.factorial(n)
    if kind == "binary":
        return math.comb(2 * (n - 1), n - 1) // n * 2 ** (n - 1)
    T = {1: 1}

    def f(s, j):                      # ways to cut s leaves into j consecutive parts, each part a plan
        if j == 1:
            return T[s]
        return sum(T[p] * f(s - p, j - 1) for p in range(1, s - j + 2))
    for m in range(2, n + 1):
        T[m] = sum(f(m, j) * math.factorial(j) for j in range(2, m + 1))
    return T[n]


def binary_plans(leaves):
    """every binary bracketing of the leaves, written order kept, both orders at each bracket"""
    n = len(leaves)
    if n == 1:
        yield leaves[0]; return
    for cut in range(1, n):
        for L in binary_plans(leaves[:cut]):
            for R in binary_plans(leaves[cut:]):
                for order in ((1, 2), (2, 1)):
                    yield Bracket([L, R], order)


def permuted_shapes(leaves):
    """every binary tree shape over every ordering of the leaves, each bracket in written order.
    Reaches groupings a written-order plan cannot (e.g. (A C) B); for 3 leaves: 6 × 2 = 12."""
    for perm in itertools.permutations(leaves):
        yield from (p for p in binary_plans(list(perm)) if _is_default(p))


def _is_default(p):
    return isinstance(p, Leaf) or (p.order == (1, 2) and all(_is_default(c) for c in p.children))


def flat_plans(leaves):
    for order in itertools.permutations(range(1, len(leaves) + 1)):
        yield Bracket(list(leaves), order)


def distinct_results(plans):
    """{operator: [plans that produce it]} — how many different things the orders make available"""
    out = {}
    for p in plans:
        out.setdefault(_key(operator(p)), []).append(notation(p))
    return out


# ── the sedenion plans ──────────────────────────────────────────────────────
def two_octonion_leaves(a):
    """a = (a1, a2): R = L((a1,0)) real octonion half, I = L((0,a2)) imaginary octonion half"""
    h = len(a) // 2
    real = tuple(a[:h]) + (F(0),) * h
    imag = (F(0),) * h + tuple(a[h:])
    return Leaf("R", left_matrix(real)), Leaf("I", left_matrix(imag))


def two_octonions(a, order=(1, 2)):
    """the bracket of the two octonion halves, fired in `order`; (2, 1) = imaginary first, real second"""
    R, I = two_octonion_leaves(a)
    return Bracket([R, I], order)


def policy_written(node_vec, kids):
    return (1, 2)


def policy_reversed(node_vec, kids):
    return (2, 1)


def policy_smaller_norm(node_vec, kids):
    """the existing engine's rule: the smaller-norm child fires first; a tie breaks left"""
    nl, nr = (sum((c * c for c in k), F(0)) for k in kids)
    return (1, 2) if nl <= nr else (2, 1)


def component_plan(a, policy=policy_written, lo=0, hi=None):
    """The full Cayley-Dickson tree as a plan: leaves are the 16 single-component operators
    L(a_k e_k) (identity where a_k = 0, so an absent component is neutral), brackets are the
    halving of the index range, and `policy(vec, (left_vec, right_vec))` names each bracket's
    order.  This is the 'product reading' of a vector; it is NOT L_a (L_a is the SUM of the
    leaves).  The old engine's rule is policy_smaller_norm."""
    n = len(a)
    hi = n if hi is None else hi
    if hi - lo == 1:
        v = tuple(F(a[lo]) if i == lo else F(0) for i in range(n))
        return Leaf(f"e{lo}", left_matrix(v) if a[lo] != 0 else _identity(n))
    mid = (lo + hi) // 2
    kids = [component_plan(a, policy, lo, mid), component_plan(a, policy, mid, hi)]
    return Bracket(kids, policy(tuple(a[lo:hi]), (tuple(a[lo:mid]), tuple(a[mid:hi]))))



def verify_plans() -> Dict[str, bool]:
    import random
    random.seed(7)
    res: Dict[str, bool] = {}
    a = tuple(F(random.randint(-3, 3)) for _ in range(16))
    R, I = two_octonion_leaves(a)
    La = left_matrix(a)
    res["L_a = R + I"] = all(La[r][c] == R.matrix[r][c] + I.matrix[r][c] for r in range(16) for c in range(16))
    p12, p21 = two_octonions(a, (1, 2)), two_octonions(a, (2, 1))
    res["(R I) = I.R"] = _equal(operator(p12), _matmul(I.matrix, R.matrix))
    res["(R I | 2 1) = R.I"] = _equal(operator(p21), _matmul(R.matrix, I.matrix))
    res["order matters for a generic sedenion"] = not _equal(operator(p12), operator(p21))
    A, B, C = (Leaf(n, left_matrix(tuple(F(int(i == k)) for i in range(16)))) for n, k in (("A", 1), ("B", 2), ("C", 12)))
    outer = Bracket([Bracket([A, B], (2, 1)), C], (2, 1))
    res["nested firing sequence"] = fire_sequence(outer) == ["C", "B", "A"]
    res["parse round trip"] = notation(parse("((A B | 2 1) C | 2 1)", {"A": A.matrix, "B": B.matrix, "C": C.matrix})) == "((A B | 2 1) C | 2 1)"
    res["counts"] = (count_plans(3, "flat") == 6 and count_plans(3, "binary") == 8 and count_plans(3, "nary") == 14)
    res["written-order binary plans reach 6, 22, 90 orders"] = [
        len({tuple(fire_sequence(p)) for p in binary_plans([Leaf(str(i)) for i in range(n)])}) for n in (3, 4, 5)] == [6, 22, 90]
    E1, E2, E3 = (Leaf(n, vec=tuple(F(int(i == k)) for i in range(16))) for n, k in (("A", 1), ("B", 10), ("C", 12)))
    res["element reading: some regrouping changes the result"] = any(
        value(Bracket([Bracket([x, y]), z])) != value(Bracket([x, Bracket([y, z])]))
        for x, y, z in itertools.permutations([E1, E2, E3]))
    return res


def verify() -> Dict[str, Any]:
    ok_bell = bell_number(3) == 5 and bell_number(16) == 10_480_142_147
    ok_parts = len(set_partitions(["Add", "Scale", "Sign"])) == 5
    ok_fire = (firing_order_count(3) == 6 and
               apply_firing_order(["Scale", "Sign", "Add"], (3, 1, 2)) == ["Add", "Scale", "Sign"])
    steps = [lambda x: x + 2, lambda x: x - 2]
    ok_collide = collisions(steps, x0=1.0) == [(0, 2, 1.0)]
    ok_would = (would_collide([lambda x: x + 2], lambda x: x - 2, x0=1.0) is True and
                would_collide([lambda x: x + 2], lambda x: x + 5, x0=1.0) is False)
    jmap = this_repos_jurisdiction_map()
    ok_jur = (jurisdiction_violation("lineage", "build_up", jmap)["violation"] is True and
              jurisdiction_violation("emerger", "build_up", jmap)["violation"] is False)
    ok_plan = verify_plans()
    return {"ok": all((ok_bell, ok_parts, ok_fire, ok_collide, ok_would, ok_jur)) and all(ok_plan.values()), "plans": ok_plan,
            "bell": ok_bell, "partitions": ok_parts, "firing_order": ok_fire,
            "collisions": ok_collide, "would_collide": ok_would, "jurisdiction": ok_jur}


if __name__ == "__main__":
    print(verify())
