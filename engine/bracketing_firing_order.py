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
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple

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
    return {"ok": all((ok_bell, ok_parts, ok_fire, ok_collide, ok_would, ok_jur)),
            "bell": ok_bell, "partitions": ok_parts, "firing_order": ok_fire,
            "collisions": ok_collide, "would_collide": ok_would, "jurisdiction": ok_jur}


if __name__ == "__main__":
    print(verify())
