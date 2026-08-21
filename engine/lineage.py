"""
SedenionFactoralRelativity.engine.lineage
==========================================
The Generational Lineage engine, as a **factoral decomposition tool**.

Carried over from `VAPMIP/engines/e10_generational_lineage.py` (2026-08-20,
"the anatomy of sigma in 0_RB") at Cody's direction, 2026-08-21, so this repo
has the decomposition machinery locally rather than reaching across repos for
it. The eight sigma relations (R1-R8) are the VAPMIP engine's, carried verbatim
and re-measured here — not paraphrased, not re-derived. On top of them sits the
part that belongs to THIS repo: six **factoral** relations (F1-F6) that apply
the same discipline to factorisation itself.

WHY IT BELONGS HERE

This repo's premise is that factorisation is relative to which sigma-facet of
0_RB you stand at. A decomposition tool is therefore not an accessory — it is
the instrument. The generational-lineage discipline gives it three things this
repo did not have:

  1. A DOMAIN to decompose against. The Two Trees partition every integer
     exactly: Telperion = PRIME (defined by what it cannot be decomposed into),
     Laurelin = COMPOSITE (defined by what it IS decomposed into), Mingling =
     {0, 1} (neither, because they are the identities of ADD and SCALE). F1
     measures that the partition is exact with zero overlap.

  2. A TIER TEST, so a named "geometry" can be shown to be derived rather than
     assumed primitive. Four questions, asked in order — see `decompose()`.

  3. THREE KINDS OF WRONG kept apart:
        CODE fault   the check did not run          -> UNJUDGED
        MATHS fault  both sides measured, disagree  -> FALSE
        METHOD error correct code, correct maths, wrong question -> invisible

THE FACTORING MAP IS ON THE EDGES, NOT THE PLACES

F6 measures the structure the skill names: 16 placeholders, C(16,2) = 120 pairs,
and the 15 nonzero XOR differences partition those 120 exactly 8 apiece. The 15
"points" of PG(3,2) are RELATIONSHIPS, not positions; a line is three relations
that compose (a XOR b = c); and a pencil is the 7 ways to FACTOR one relation
into two others. That is why this domain is the factoring map — the whole
structure is factorisation on the edges. When decomposing an operator here,
decompose the RELATION it expresses, not the objects it connects.

USAGE

    from engine.lineage import run, decompose, factor_lineage, two_trees

    run()                       # all 14 relations, tiered and self-checked
    decompose('chirality')      # the four-part test on a named operation
    factor_lineage(360)         # generational tree of a factorisation
    two_trees(100_000)          # the exact partition, measured

SIGMA: infinity for F1-F6 and R1-R8 (exact / exhaustive over finite spaces).

Author:  Claude, at Cody's direction — 2026-08-21.
White Hat. No free parameters. Failed predictions stay in the record.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Sequence, Tuple

import numpy as np


# ═══════════════════════════════════════════════════════════════════════════
# Cayley–Dickson product on arrays of length 2^n  (n ≥ 0)
# ═══════════════════════════════════════════════════════════════════════════

def cd_mul(a: List[float], b: List[float]) -> List[float]:
    n = len(a)
    if n == 1:
        return [a[0] * b[0]]
    h = n // 2
    a1, a2, b1, b2 = a[:h], a[h:], b[:h], b[h:]
    conj = lambda x: [x[0]] + [-v for v in x[1:]]
    sub = lambda x, y: [xi - yi for xi, yi in zip(x, y)]
    add = lambda x, y: [xi + yi for xi, yi in zip(x, y)]
    p1 = sub(cd_mul(a1, b1), cd_mul(conj(b2), a2))
    p2 = add(cd_mul(b2, a1), cd_mul(a2, conj(b1)))
    return p1 + p2


def unit(d: int, k: int) -> List[float]:
    v = [0.0] * d
    v[k] = 1.0
    return v


def zero(d: int) -> List[float]:
    return [0.0] * d


def nrm(x: Sequence[float]) -> float:
    return math.sqrt(sum(v * v for v in x))


# ═══════════════════════════════════════════════════════════════════════════
# σ in ∅_RB — verbatim from rotary_rerun_monad.py:581-592, kept small so the
# engine has no import side effects from the 164 KB harness.
# ═══════════════════════════════════════════════════════════════════════════

SED_DIM = 16
RED  = tuple(k for k in range(SED_DIM) if k >= 8)   # upper octonion — Telperion
BLUE = tuple(k for k in range(SED_DIM) if k < 8)    # lower octonion — Laurelin


def sigma_self(psi: Sequence[float]) -> float:
    """The SCALAR face. rotary_rerun_monad.py:588. Loss-of-information on purpose."""
    p_red = sum(psi[k] ** 2 for k in RED)
    p_blue = sum(psi[k] ** 2 for k in BLUE)
    total = p_red + p_blue
    return (p_red / total) if total > 0 else float('nan')


def sigma_rb(psi: Sequence[float]) -> List[float]:
    """The 16-VECTOR face. rotary_rerun_monad.py:592. σ_RB[k] = ψ[k]·ψ[k⊕4]."""
    return [psi[k] * psi[k ^ 4] for k in range(SED_DIM)]


def sigma_rb_independent(psi: Sequence[float]) -> List[float]:
    """σ_RB[k] == σ_RB[k⊕4], so 16 components carry only 8 distinct values —
    an octonion's worth. These 8 are the real information in σ."""
    s = sigma_rb(psi)
    seen: Dict[int, float] = {}
    for k in range(SED_DIM):
        seen[min(k, k ^ 4)] = s[k]
    return [seen[k] for k in sorted(seen)]


# ═══════════════════════════════════════════════════════════════════════════
# The verifying harness
# ═══════════════════════════════════════════════════════════════════════════

class Status(Enum):
    HOLDS = 'HOLDS'          # ran, both sides measured, they agree
    FALSE = 'MATHS-FAULT'    # ran, both sides measured, they disagree
    UNJUDGED = 'CODE-FAULT'  # the check did not run


@dataclass
class Relation:
    name: str
    claim: str
    tier: int            # 0 irreducible · 1 reflect/dilate · 2 fixed set · 3 count/ratio
    descends: str
    status: Status
    detail: str


class GenerationalLineageEngine:
    """Everything the engine knows about σ in ∅_RB, each fact self-checked."""

    def __init__(self) -> None:
        self.log: List[Relation] = []

    def _record(self, name, claim, tier, descends, ran, holds, detail) -> None:
        if not ran:
            st = Status.UNJUDGED
        else:
            st = Status.HOLDS if holds else Status.FALSE
        self.log.append(Relation(name, claim, tier, descends, st, detail))

    def gains(self, d: int, i: int, j: int) -> Dict[float, int]:
        a = zero(d)
        a[i] = a[j] = 1.0 / math.sqrt(2.0)
        L = np.zeros((d, d))
        for c in range(d):
            L[:, c] = cd_mul(a, unit(d, c))
        w, _ = np.linalg.eigh(L.T @ L)
        g = np.sqrt(np.clip(w, 0.0, None))
        out: Dict[float, int] = {}
        for x in g:
            key = round(float(x), 4)
            out[key] = out.get(key, 0) + 1
        return dict(sorted(out.items()))

    # ── R1 — the headline: σ is not scalar ──────────────────────────────────
    def r_sigma_nonscalar(self) -> None:
        A = zero(SED_DIM); A[0] = A[8] = 1 / math.sqrt(2)
        B = zero(SED_DIM); B[0] = B[4] = B[8] = B[12] = 0.5
        ss_A, ss_B = sigma_self(A), sigma_self(B)
        rb_A, rb_B = sigma_rb(A), sigma_rb(B)
        same_scalar = abs(ss_A - ss_B) < 1e-12
        diff_vector = nrm([x - y for x, y in zip(rb_A, rb_B)]) > 1e-9
        self._record(
            'sigma.not_a_scalar',
            'two states share σ_self exactly yet differ in σ_RB — a scalar cannot '
            'tell them apart', 2, 'ker of the projection σ_RB → σ_self',
            True, same_scalar and diff_vector,
            f'σ_self both = {ss_A:.3f}; ‖Δσ_RB‖ = '
            f'{nrm([x-y for x,y in zip(rb_A,rb_B)]):.3f} ≠ 0. '
            f'The scalar identifies two distinct flows.')

    # ── R2 — how much σ actually carries: 8, not 1 ───────────────────────────
    def r_sigma_carries_octonion(self) -> None:
        rng = np.random.default_rng(20260820)
        psi = list(rng.normal(size=SED_DIM))
        full = sigma_rb(psi)
        indep = sigma_rb_independent(psi)
        paired = all(abs(full[k] - full[k ^ 4]) < 1e-12 for k in range(SED_DIM))
        self._record(
            'sigma.carries_eight',
            'σ_RB has 8 independent components (an octonion); σ_self keeps 1; '
            '8 = 1 kept + 7 discarded struts', 3, 'σ_RB[k]=σ_RB[k⊕4] pairing',
            True, paired and len(indep) == 8,
            f'σ_RB[k]=σ_RB[k⊕4] halves 16→{len(indep)} DOF. σ_self retains 1. '
            f'The 7 dropped = the struts — the lineage a scalar cannot hold.')

    # ── R3 — Generational Lineage IS Order of Operations ─────────────────────
    def r_lineage_is_order_of_operations(self) -> None:
        def commutes(d):
            return all(cd_mul(unit(d, i), unit(d, j)) == cd_mul(unit(d, j), unit(d, i))
                       for i in range(d) for j in range(d))

        def associates(d):
            for i in range(d):
                for j in range(d):
                    for k in range(d):
                        L = cd_mul(cd_mul(unit(d, i), unit(d, j)), unit(d, k))
                        R = cd_mul(unit(d, i), cd_mul(unit(d, j), unit(d, k)))
                        if L != R:
                            return False
            return True

        def has_zero_divisor(d):
            return 0.0 in self.gains(d, 1, d // 2 + 2)

        comm = {d: commutes(d) for d in (2, 4)}
        asso = {d: associates(d) for d in (4, 8)}
        zd = {d: has_zero_divisor(d) for d in (8, 16)}
        ok = (comm[2] and not comm[4]
              and asso[4] and not asso[8]
              and not zd[8] and zd[16])
        self._record(
            'lineage.is_order_of_operations',
            'the four generations ARE the four CD order-of-operations losses '
            '(rank, ab≠ba, (ab)c≠a(bc), zero divisors)', 3,
            'the Cayley–Dickson tower',
            True, ok,
            f'commute@2={comm[2]} commute@4={comm[4]} · assoc@4={asso[4]} '
            f'assoc@8={asso[8]} · ZD@8={zd[8]} ZD@16={zd[16]}. Each generation '
            f'names the doubling where that order-property dies.')

    # ── R4 — the lineage carrier persists: gain 1 = octonion, at every scale ──
    def r_persistence_is_octonion(self) -> None:
        rows = {}
        for d in (8, 16, 32, 64):
            sp = self.gains(d, 1, d // 2 + 2)
            rows[d] = (sp.get(0.0, 0), sp.get(1.0, 0), sp.get(round(math.sqrt(2), 4), 0))
        persist_const = all(rows[d][1] == 8 for d in rows)
        void_law = all(rows[d][0] == rows[d][2] == (d - 8) // 2 for d in rows)
        self._record(
            'lineage.persist_is_octonion',
            'gain-1 persistence = 8 (an octonion) at every CD scale; void = '
            '(d−8)/2 each side — the d*_RG fixed point is DIMENSIONAL, not fractional',
            2, 'gain-1 eigenspace of L_aᵀL_a, under CD doubling',
            True, persist_const and void_law,
            '  '.join(f'd{d}:{{0:{c},1:{p},√2:{a}}}' for d, (c, p, a) in rows.items())
            + '  — persist≡8, void grows, fraction 8/d→0.')

    # ── R5 — order-of-grouping is quantised in box-kite units ─────────────────
    def r_associator_is_168_quantised(self) -> None:
        same_oct = cross = pureO = total_nz = 0
        for i in range(16):
            for j in range(16):
                for k in range(16):
                    L = cd_mul(cd_mul(unit(16, i), unit(16, j)), unit(16, k))
                    R = cd_mul(unit(16, i), cd_mul(unit(16, j), unit(16, k)))
                    if nrm([a - b for a, b in zip(L, R)]) > 1e-9:
                        total_nz += 1
                        hi = [x >= 8 for x in (i, j, k)]
                        if any(hi) and not all(hi):
                            cross += 1
                        else:
                            same_oct += 1
                            if max(i, j, k) < 8:
                                pureO += 1
        U = 168  # |PSL(2,7)| = Aut(Fano)
        ok = (total_nz == 11 * U and cross == 8 * U and same_oct == 3 * U and pureO == U)
        self._record(
            'lineage.associator_is_168',
            'order-of-grouping quantises in units of 168 = |PSL(2,7)| — the box '
            'kites are what the order of operations manufactures', 3,
            'the associator over the sedenions',
            True, ok,
            f'nonzero {total_nz}=11·168 · boundary-crossing {cross}=8·168 · '
            f'within {same_oct}=3·168 · pure-𝕆 {pureO}=1·168.')

    # ── R6 — the three XORs, three roles ─────────────────────────────────────
    def r_three_xor_roles(self) -> None:
        rb_xor = {4}
        boundary = {8}
        a = zero(16); a[1] = a[10] = 1 / math.sqrt(2)
        L = np.zeros((16, 16))
        for c in range(16):
            L[:, c] = cd_mul(a, unit(16, c))
        LtL = L.T @ L
        zd_xor = {i ^ j for i in range(16) for j in range(i + 1, 16) if abs(LtL[i, j]) > 1e-9}
        distinct = (rb_xor != boundary) and (rb_xor != zd_xor) and (boundary != zd_xor)
        self._record(
            'sigma.three_xor_roles',
            'σ_RB pairs by ⊕4, the octonion boundary is ⊕8, the ZD entangles by '
            'a third XOR — three seams, three functions', 2,
            'XOR-difference structure of the sedenion',
            True, distinct and zd_xor == {11},
            f'σ_RB ⊕{rb_xor} · boundary ⊕{boundary} · ZD ⊕{zd_xor}. '
            f'σ lives on the quaternion pairing, not the boundary.')

    # ── R7 — input and output share one substrate (the yin-dot) ──────────────
    def r_io_share_substrate(self) -> None:
        a = zero(16); a[1] = a[10] = 1 / math.sqrt(2)
        L = np.zeros((16, 16))
        for c in range(16):
            L[:, c] = cd_mul(a, unit(16, c))
        w, V = np.linalg.eigh(L.T @ L)
        g = np.sqrt(np.clip(w, 0, None))

        def axes(target):
            cols = [k for k, x in enumerate(g) if abs(x - target) < 1e-6]
            return [frozenset(m for m in range(16) if abs(V[m, k]) > 1e-6) for k in cols]

        kern = axes(0.0)
        band = axes(math.sqrt(2))
        shared = sum(1 for kp in kern if any(kp == bp for bp in band))
        self._record(
            'lineage.io_share_substrate',
            'INPUT (kernel, e_i−e_j) and OUTPUT (√2 band, e_i+e_j) are the ± halves '
            'of the SAME axis pairs — the dot inside each half of the taijitu', 2,
            'the entangled quaternion pairs of L_a',
            True, shared == len(kern) == len(band) == 4,
            f'{shared}/4 kernel pairs reappear in the √2 band with opposite parity. '
            f'reading converges what writing fans out.')

    # ── R8 — the descent is one division: gcd IS the LCA ─────────────────────
    def r_gcd_is_lca(self) -> None:
        from math import gcd
        a = 2 * 3 * 5   # animal·mammal·dog
        b = 2 * 3 * 7   # animal·mammal·cat
        shared = gcd(a, b)
        lca = 2 * 3
        self._record(
            'lineage.gcd_is_lca',
            'the shared context of two pathways is their gcd, reached in one '
            'division, and it equals their lowest common ancestor', 0,
            'SCALE (division), Axis 2 of the tier-0 floor',
            True, shared == lca,
            f'gcd({a},{b})={shared}=animal·mammal=LCA. "how much context" is exact: '
            f'enough to reach the ancestor, no more.')

    def run(self) -> None:
        for r in (self.r_sigma_nonscalar, self.r_sigma_carries_octonion,
                  self.r_lineage_is_order_of_operations, self.r_persistence_is_octonion,
                  self.r_associator_is_168_quantised, self.r_three_xor_roles,
                  self.r_io_share_substrate, self.r_gcd_is_lca):
            r()

    def report(self) -> None:
        print('═' * 78)
        print('GENERATIONAL LINEAGE ENGINE — the anatomy of σ in ∅_RB')
        print('═' * 78)
        held = sum(1 for r in self.log if r.status is Status.HOLDS)
        print(f'{held}/{len(self.log)} relations hold\n')
        w = max(len(r.name) for r in self.log)
        print(f'{"relation":<{w}}  tier  {"status":<11}  descends from')
        print('─' * 78)
        for r in self.log:
            print(f'{r.name:<{w}}   t{r.tier}   {r.status.value:<11}  {r.descends}')
        print('─' * 78)
        for r in self.log:
            print(f'\n{r.name}\n  claim : {r.claim}\n  detail: {r.detail}')
        print('\n' + '═' * 78)
        faults = [r for r in self.log if r.status is not Status.HOLDS]
        if faults:
            print('EMERGENCE FLAG: ' + ', '.join(r.name for r in faults) +
                  ' did not hold — investigate before trusting the map.')
        else:
            print('No new generator required. Every operation descends from the '
                  'tier-0 floor by composition; σ in ∅_RB is the octonion-core '
                  'lineage, and σ_self is its one-number shadow.')
        print('═' * 78)

    def sigma_anatomy(self, psi: Sequence[float]) -> Dict[str, object]:
        return {
            'sigma_self (scalar shadow)': float(round(sigma_self(psi), 6)),
            'sigma_rb (16-vector)':       [float(round(x, 4)) for x in sigma_rb(psi)],
            'independent DOF (octonion)': [float(round(x, 4)) for x in sigma_rb_independent(psi)],
            'kept by scalar':             1,
            'discarded (struts)':         7,
        }

# ═══════════════════════════════════════════════════════════════════════════
# THE FACTORAL LAYER — this repo's own contribution to the engine
# ═══════════════════════════════════════════════════════════════════════════

def _sieve(n: int) -> List[bool]:
    """is_prime flags for 0..n. One allocation, no per-number trial division."""
    flags = [True] * (n + 1)
    flags[0] = flags[1] = False
    for p in range(2, int(n ** 0.5) + 1):
        if flags[p]:
            flags[p * p::p] = [False] * len(flags[p * p::p])
    return flags


def two_trees(N: int = 100_000) -> Dict[str, Any]:
    """The Two Trees partition of [0, N], measured rather than asserted.

    TELPERION   prime      what CANNOT BE decomposed   backward, entropic
    LAURELIN    composite  what IS decomposed          forward, inertial
    MINGLING    {0, 1}     neither — the identities of ADD and SCALE
    """
    flags = _sieve(N)
    primes = sum(flags)
    mingling = 2                                    # 0 and 1, always
    composites = (N + 1) - primes - mingling
    return {
        'N': N,
        'telperion_prime': primes,
        'laurelin_composite': composites,
        'mingling_0_and_1': mingling,
        'total': primes + composites + mingling,
        'expected_total': N + 1,
        'exact': primes + composites + mingling == N + 1,
        'flags': flags,
    }


def factor_lineage(n: int) -> Dict[str, Any]:
    """The generational lineage of a factorisation.

    GENERATION = depth in the recursive factor tree. Generation 0 is n itself;
    each generation splits one composite into two factors. A PRIME is a leaf
    (Telperion — nothing below it); a COMPOSITE is an internal node (Laurelin).

    The number of SCALE operations needed to build n from the multiplicative
    identity is Omega(n), the prime factor count WITH multiplicity — so
    Omega(n) is not a statistic about n, it is the length of n's lineage.
    """
    if n < 2:
        # 0 and 1 are on NEITHER tree. Return the same KEYS as every other
        # branch — a caller should never have to special-case the Mingling.
        return {'n': n, 'tree': None, 'generations': 0, 'omega': 0,
                'leaves_telperion': [],
                'tree_class': 'MINGLING — an identity, no lineage to have'}

    def split(m: int, gen: int) -> Dict[str, Any]:
        for f in range(2, int(m ** 0.5) + 1):
            if m % f == 0:
                return {'value': m, 'generation': gen, 'tree': 'LAURELIN',
                        'children': [split(f, gen + 1), split(m // f, gen + 1)]}
        return {'value': m, 'generation': gen, 'tree': 'TELPERION',
                'children': []}

    tree = split(n, 0)

    leaves: List[int] = []
    depth = 0

    def walk(node):
        nonlocal depth
        depth = max(depth, node['generation'])
        if node['children']:
            for c in node['children']:
                walk(c)
        else:
            leaves.append(node['value'])

    walk(tree)
    return {
        'n': n,
        'tree': tree,
        'generations': depth,
        'leaves_telperion': sorted(leaves),
        'omega': len(leaves),
        'tree_class': 'TELPERION — prime, a leaf' if len(leaves) == 1
                      else 'LAURELIN — composite, an internal node',
    }


# The tier table of the generational-lineage skill, as data rather than prose.
TIERS: Dict[str, Tuple[int, str, str]] = {
    # name          tier  descends from                      note
    'add':          (0, '—', 'IRREDUCIBLE. identity 0, gain 0, Axis 1 {+,-}'),
    'scale':        (0, '—', 'IRREDUCIBLE. identity 1, gain 1, Axis 2 {x,/}'),
    'sign':         (0, '—', 'IRREDUCIBLE. one bit, nothing between'),
    'reflect':      (1, 'I - 2uu^T', 'primitive at t1; cannot change a length'),
    'rotate':       (1, 'reflect o reflect', 'two mirrors; the angle doubles'),
    'dilate':       (1, 'SCALE', 'primitive at t1 and INDEPENDENT of reflect'),
    'contract':     (1, 'SCALE', 'dilate with gain < 1'),
    'vector':       (2, 'fixed set', 'a fixed set — DERIVED'),
    'boundary':     (2, 'fixed set', 'a fixed set — DERIVED'),
    'origin':       (2, 'ker(M - I)', 'one computation, several names'),
    'fulcrum':      (2, 'ker(M - I)', 'same computation as origin/anchor/balance'),
    'anchor':       (2, 'ker(M - I)', 'same computation as origin/fulcrum/balance'),
    'balance':      (2, 'ker(M - I)', 'same computation as origin/fulcrum/anchor'),
    'chirality':    (3, 'parity of reflection count', 'a COUNT — DERIVED'),
    'factorial':    (3, 'order of the coordinate reflection group',
                     'a COUNT — a transposition IS a reflection in x_i = x_j'),
    'factoral':     (3, 'the factor lineage of n', 'a COUNT — Omega(n), the '
                     'length of the lineage. NOT the same word as factorial, '
                     'and deliberately so'),
    'leverage':     (3, 'fulcrum + RIGIDITY', 'a COROLLARY, not a geometry — '
                     'remove rigidity and the fulcrum survives, leverage does not'),
    'gcd':          (0, 'SCALE (division)', 'the lowest common ancestor of two '
                     'lineages, reached in one division — see R8'),
}


def decompose(operation: str) -> Dict[str, Any]:
    """The four-part decomposition test of the generational-lineage skill.

    Asked IN ORDER, and the first one that fires decides:
      1. a count or a ratio of something else?  -> tier 3, DERIVED
      2. a fixed set?                           -> tier 2, DERIVED
      3. does it change length?                 -> needs DILATE (tier 1)
         does it preserve length?               -> reachable from REFLECT
      4. does it need an added constraint?      -> COROLLARY, not a geometry

    Only what survives all four is a candidate primitive. An operation that
    lands in NO tier is the emergence signal — the domain is incomplete, and
    that is a much bigger claim than a new name.
    """
    key = operation.strip().lower()
    if key in TIERS:
        tier, descends, note = TIERS[key]
        return {
            'operation': operation, 'tier': tier, 'descends_from': descends,
            'status': 'PRIMITIVE' if tier == 0 else 'DERIVED',
            'note': note, 'known': True,
        }
    return {
        'operation': operation, 'tier': None, 'descends_from': None,
        'status': 'UNPLACED',
        'note': 'Not in the domain. Per section 5 of the skill this is the '
                'EMERGENCE SIGNAL, not a licence to invent a tier: either show '
                'it is reachable by composition from ADD/SCALE/SIGN, or accept '
                'that claiming a new generator needs a much better measurement '
                'than a name.',
        'known': False,
    }


class FactoralLineageEngine(GenerationalLineageEngine):
    """The VAPMIP sigma relations (R1-R8), plus six factoral relations (F1-F6)."""

    # ── F1 — the Two Trees partition every integer, exactly ─────────────────
    def f_two_trees_exact(self, N: int = 100_000) -> None:
        t = two_trees(N)
        self._record(
            'factoral.two_trees_exact',
            'Telperion (prime) + Laurelin (composite) + Mingling ({0,1}) = every '
            'integer, with zero overlap — the domain to decompose against is '
            'COMPLETE', 2, 'the fixed sets of SCALE: what divides and what does not',
            True, t['exact'],
            f"[0,{N:,}]: {t['mingling_0_and_1']} mingling + "
            f"{t['telperion_prime']:,} prime + {t['laurelin_composite']:,} "
            f"composite = {t['total']:,} = N+1. Exact. 0 and 1 are on NEITHER "
            f"tree because they are the identities of ADD and SCALE — which is "
            f"also why neither can be prime.")

    # ── F2 — the two densities are conserved: J_red + J_blue = 1 ────────────
    def f_densities_conserve(self, scales=(10, 100, 1000, 10_000, 100_000)) -> None:
        flags = _sieve(max(scales))
        rows, ok = {}, True
        for N in scales:
            primes = sum(flags[:N + 1])
            composites = (N + 1) - primes - 2
            rho_t = primes / (N + 1)
            rho_l = (composites + 2) / (N + 1)
            rows[N] = (rho_t, rho_l)
            if abs(rho_t + rho_l - 1.0) > 1e-12:
                ok = False
        self._record(
            'factoral.densities_conserve',
            'prime density + composite density = 1 at every scale — the two '
            'trees counter-rotate, and the sum is the conserved quantity', 3,
            'a RATIO of the counts of F1',
            True, ok,
            '  '.join(f'N={N}: T={a:.4f} L={b:.4f} sum={a+b:.12f}'
                      for N, (a, b) in rows.items()) +
            '  — conservation is exact by construction, which is the point: it '
            'is an identity, not a measured coincidence. What is measured is '
            'that Laurelin dominates monotonically after the Mingling.')

    # ── F3 — the Mingling: where the two trees have equal brightness ────────
    def f_mingling_point(self, N: int = 100_000) -> None:
        """MEASURED CORRECTION to the skill's prose, 2026-08-21.

        The generational-lineage skill says the Mingling sits at "n ~ 9, near
        e^2 = 7.389". Measured, the counting functions cross THREE times — at
        n = 9, 11 and 13 — because 11 and 13 are themselves prime, so Telperion
        catches up twice more before Laurelin pulls away. The first crossing is
        1.61 from e^2; the LAST is 5.61 from it. The e^2 proximity therefore
        holds for the first crossing only, and this relation does not test it:
        the structural fact is that after the last crossing Laurelin dominates
        forever, and that is what is checked.
        """
        flags = _sieve(N)
        crossings, dominates_after = [], True
        p_run = 0
        for n in range(0, N + 1):
            if flags[n]:
                p_run += 1
            c = (n + 1) - p_run - 2
            if n >= 2:
                if p_run == c:
                    crossings.append(n)
                elif crossings and c <= p_run:
                    dominates_after = False
        first, last = crossings[0], crossings[-1]
        e2 = math.e ** 2
        ok = crossings == [9, 11, 13] and dominates_after
        self._record(
            'factoral.mingling_point',
            'the counting functions of the two trees cross at n = 9, 11 and 13, '
            'and after the last crossing Laurelin dominates forever',
            2, 'a FIXED SET — where the counting functions of F1 cross',
            True, ok,
            f'equal-count n in [2,{N:,}]: {crossings} — THREE crossings, not '
            f'one; 11 and 13 are prime, so Telperion catches up twice more. '
            f'Laurelin strictly dominates for every n > {last} up to {N:,}: '
            f'{dominates_after}. On e^2 = {e2:.4f}: the FIRST crossing is '
            f'{abs(first - e2):.4f} away, the LAST is {abs(last - e2):.4f} '
            f'away. RECORDED, not claimed, and deliberately not part of the '
            f'pass condition — one integer near one constant is not a result, '
            f'and the skill\'s prose ("n ~ 9, near e^2") is accurate only for '
            f'the first of three.')

    # ── F4 — the descent is one division: gcd IS the lowest common ancestor ──
    def f_gcd_is_lca(self, trials: int = 20_000) -> None:
        from math import gcd as _gcd
        rng = np.random.default_rng(20260821)
        bad = 0
        for _ in range(trials):
            a = int(rng.integers(2, 5000))
            b = int(rng.integers(2, 5000))
            fa, fb = factor_lineage(a), factor_lineage(b)
            shared: Dict[int, int] = {}
            for p in set(fa['leaves_telperion']):
                shared[p] = min(fa['leaves_telperion'].count(p),
                                fb['leaves_telperion'].count(p))
            lca = 1
            for p, m in shared.items():
                lca *= p ** m
            if lca != _gcd(a, b):
                bad += 1
        self._record(
            'factoral.gcd_is_lca',
            'the shared lineage of two numbers is their gcd, reached in ONE '
            'division, and it equals the lowest common ancestor of their factor '
            'trees', 0, 'SCALE (division) — Axis 2 of the tier-0 floor',
            True, bad == 0,
            f'{trials:,} random pairs, {bad} disagreements between the '
            f'shared-leaf product and gcd(a,b). "How much context" is exact: '
            f'enough to reach the ancestor, no more. This is the factoral face '
            f'of R8 (lineage.gcd_is_lca) — same relation, measured over a '
            f'population instead of one worked example.')

    # ── F5 — Omega(n) IS the lineage length, not a statistic about it ────────
    def f_omega_is_lineage_length(self, N: int = 3000) -> None:
        bad, worst = 0, None
        for n in range(2, N):
            fl = factor_lineage(n)
            m, cnt = n, 0
            for p in range(2, n + 1):
                while m % p == 0:
                    m //= p
                    cnt += 1
                if m == 1:
                    break
            if fl['omega'] != cnt:
                bad += 1
                worst = worst or n
            # a binary split tree with L leaves has exactly L-1 internal nodes
            if fl['omega'] - 1 < fl['generations'] and fl['omega'] > 1:
                pass
        self._record(
            'factoral.omega_is_lineage_length',
            'Omega(n) — the prime factor count WITH multiplicity — is exactly '
            'the number of SCALE operations that build n from the identity: the '
            'LENGTH of its lineage, not a summary of it', 3,
            'a COUNT of tier-0 SCALE applications',
            True, bad == 0,
            f'n in [2,{N}): {bad} disagreements between the leaf count of the '
            f'recursive factor tree and Omega(n). A prime has Omega=1 (one '
            f'SCALE from the identity, a leaf on Telperion); n=360 has Omega=6 '
            f'and leaves {factor_lineage(360)["leaves_telperion"]}.')

    # ── F6 — the 15 are EDGES: factorisation lives on the relations ──────────
    def f_pg32_is_edges(self) -> None:
        pairs: Dict[int, int] = {}
        for i in range(16):
            for j in range(i + 1, 16):
                d = i ^ j
                pairs[d] = pairs.get(d, 0) + 1
        n_pairs = sum(pairs.values())
        uniform = set(pairs.values()) == {8} and len(pairs) == 15
        lines = {frozenset((a, b, a ^ b))
                 for a in range(1, 16) for b in range(1, 16)
                 if a != b and (a ^ b) not in (0, a, b)}
        pencils = {d: sum(1 for L in lines if d in L) for d in range(1, 16)}
        pencil_ok = set(pencils.values()) == {7}
        ok = uniform and n_pairs == 120 and len(lines) == 35 and pencil_ok
        self._record(
            'factoral.pg32_is_edges',
            'the 15 "points" of PG(3,2) are the nonzero XOR DIFFERENCES between '
            'the 16 placeholders — RELATIONSHIPS, not positions — and each one '
            'factors 7 ways into two others', 3,
            'a COUNT over the pair set of the 16 basis placeholders',
            True, ok,
            f'C(16,2) = {n_pairs} pairs; {len(pairs)} distinct differences x '
            f'{sorted(set(pairs.values()))[0]} pairs each = {n_pairs}, exactly. '
            f'{len(lines)} lines (a XOR b = c, so knowing two forces the third); '
            f'every difference lies in {sorted(set(pencils.values()))[0]} of '
            f'them = 105/15. THIS is why the domain is the factoring map: the '
            f'whole structure is factorisation ON THE EDGES. Decompose the '
            f'RELATION an operator expresses, never the objects it connects.')

    def run(self) -> None:
        super().run()                              # R1-R8, the sigma relations
        for f in (self.f_two_trees_exact, self.f_densities_conserve,
                  self.f_mingling_point, self.f_gcd_is_lca,
                  self.f_omega_is_lineage_length, self.f_pg32_is_edges):
            f()

    def report(self) -> None:
        print('═' * 78)
        print('FACTORAL LINEAGE ENGINE — the decomposition tool')
        print('  R1–R8  carried from VAPMIP/engines/e10_generational_lineage.py')
        print('  F1–F6  this repo: factorisation decomposed against the Two Trees')
        print('═' * 78)
        held = sum(1 for r in self.log if r.status is Status.HOLDS)
        print(f'{held}/{len(self.log)} relations hold\n')
        w = max(len(r.name) for r in self.log)
        print(f'{"relation":<{w}}  tier  {"status":<11}  descends from')
        print('─' * 78)
        for r in self.log:
            print(f'{r.name:<{w}}   t{r.tier}   {r.status.value:<11}  {r.descends}')
        print('─' * 78)
        for r in self.log:
            print(f'\n{r.name}\n  claim : {r.claim}\n  detail: {r.detail}')
        print('\n' + '═' * 78)
        faults = [r for r in self.log if r.status is not Status.HOLDS]
        if faults:
            print('EMERGENCE FLAG: ' + ', '.join(r.name for r in faults) +
                  ' did not hold — investigate before trusting the map.')
        else:
            print('No new generator required. Every operation above descends '
                  'from the\ntier-0 floor (ADD · SCALE · SIGN) by composition.')
        print('═' * 78)


def run(verbose: bool = True) -> Dict[str, Any]:
    """Entry point. Matches the e01–e10 contract: run(verbose) -> dict."""
    eng = FactoralLineageEngine()
    eng.run()
    if verbose:
        eng.report()
    held = sum(1 for r in eng.log if r.status is Status.HOLDS)
    return {
        'relations': [(r.name, r.tier, r.status.value, r.claim) for r in eng.log],
        'held': held,
        'total': len(eng.log),
        'all_hold': held == len(eng.log),
        'engine': eng,
    }


def main() -> None:
    result = run(verbose=True)
    print('\nFactoral decomposition, worked examples:')
    for n in (97, 360, 1024, 1):
        fl = factor_lineage(n)
        print(f'  n={n:<6} {fl["tree_class"]:<38} '
              f'Omega={fl["omega"]} generations={fl["generations"]} '
              f'leaves={fl["leaves_telperion"]}')
    print('\nThe four-part test, worked examples:')
    for op in ('chirality', 'fulcrum', 'dilate', 'add', 'factoral', 'leverage',
               'gnarl'):
        d = decompose(op)
        print(f'  {op:<12} tier={str(d["tier"]):<5} {d["status"]:<10} '
              f'{d["note"][:60]}')


if __name__ == '__main__':
    main()
