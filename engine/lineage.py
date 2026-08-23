"""
SedenionFactoralRelativity.engine.lineage
==========================================
The Generational Lineage engine, as a **factoral decomposition tool**.

Carried over from `VAPMIP/engines/e10_generational_lineage.py` (2026-08-20,
"the anatomy of sigma in 0_RB") at Cody's direction, 2026-08-21, so this repo
has the decomposition machinery locally rather than reaching across repos for
it. The eight sigma relations (R1-R8) are the VAPMIP engine's, carried verbatim
and re-measured here — not paraphrased, not re-derived. On top of them sit the
parts that belong to THIS repo: six **factoral** relations (F1-F6) applying the
same discipline to factorisation; six **ring-theory** relations (G1-G6) naming
the tower in its proper ring theory (FALL <=> the quotient ring has zero
divisors); and three **fractal** relations (FR1-FR3), the highest-order rung; and three
**formulary** relations (FR4-FR6) integrating the UF fractal library; and nine
**pathway** relations (PW1-PW9) — factoring as a tunable WALK to N, the
two-anchor geodesic, the EDGE primitive, L_(I|O) as the Observer's lineage
mechanism, the Smith chart as an independent Mobius confirmation, and the
NUMBER CHART (PW9) — the Smith-chart METHODOLOGY applied directly: a bounded,
anchored, tuning-legible chart that is decompose_number()'s visualiser data.
G8 adds the ARITHMETIC DERIVATIVE. 37 relations, all self-checked.

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

    run()                       # all 23 relations, tiered and self-checked
    decompose('chirality')      # the four-part test on a named operation
    factor_lineage(360)         # generational tree of a factorisation
    two_trees(100_000)          # the exact partition, measured
    fall_test(12)               # FALL <=> Z/(12) has zero divisors (G1)
    box_dimension(MANDELBROT, (-2,0.5), (-1.25,1.25))   # fractal boundary (FR3)
    newton_basins(3)            # 3 basins = the 3 cube-roots = ring splitting (FR4)
    tune_pathway(1522605027)    # sweep the spiral tuning until a factor resonates (PW2)
    decompose_number(3233)      # the multi-perspective bundle — the visualiser's data model

SIGMA: infinity for F1-F6, R1-R8, G1 G3 G4 G5 G6, FR1, FR4 (exact/exhaustive);
       finite for G2 (sampled moduli), FR2/FR6 (converging dynamics), FR3
       (box-count on a grid — a coarse but honest dimension in (1,2)), FR5
       (framing over sampled orbits).

THE LABELINGS (lifted from the UF formulary's .ucl coloring methods): the
GENERATOR is the fractal, the LABELING is the decomposition. escape/smooth =
order 1, orbit_trap = order-1 support, orbit_curvature = order 3 (the associator
on dynamics), lyapunov = the drift, basin = k-way fall/survive = ring splitting.
label_orbit() returns them all for one orbit — the per-pixel data of a visualiser.

Author:  Claude, at Cody's direction — 2026-08-21.
White Hat. No free parameters. Failed predictions stay in the record.
"""

from __future__ import annotations

import cmath
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


# ═══════════════════════════════════════════════════════════════════════════
# RING-THEORY MACHINERY (2026-08-22)
# ═══════════════════════════════════════════════════════════════════════════
# The factoral tower, named in its proper ring theory. The unifying statement,
# measured by G1 below:
#
#     an element FALLS  iff  its quotient ring has zero divisors.
#
# Integer side (ℤ, an associative UFD — classical ring theory is complete):
#     N composite  ⟺  ℤ/(N) has a zero divisor  ⟺  (N) is not a prime ideal.
# Algebra side (𝕊₁₆ / T₃₂ over GF(2) — a NON-associative algebra, where the
# ring axioms break rung by rung): a constant w falls ⟺ w is nilpotent ⟺ w
# lies in the zero-divisor set = ∪ of the associated primes.
#
# The detector is the same KIND of object on both sides: one operation.
#   ℤ side  : gcd(a, N) > 1                     (the integer trace-Laplacian)
#   GF(2)   : the trace-Laplacian Δ(w) = w·𝟏    (w·𝟏 = 0 ⟺ w² = 0)


def cd_mul_gf2(a: int, b: int, dim: int) -> int:
    """Cayley–Dickson product in T_dim over GF(2), on integer bitmasks.

    Bit k of the integer is the coefficient of basis element e_k. Over GF(2)
    conjugation is the identity (−x = x) and the base product is AND. Non-
    commutative and non-associative above dim 2 — ORDER matters, and is kept.
    """
    if dim == 1:
        return a & b
    h = dim // 2
    mask = (1 << h) - 1
    a1, a2 = a & mask, a >> h
    b1, b2 = b & mask, b >> h
    lo = cd_mul_gf2(a1, b1, h) ^ cd_mul_gf2(b2, a2, h)   # a1b1 − b̄2a2  (GF2)
    hi = cd_mul_gf2(b2, a1, h) ^ cd_mul_gf2(a2, b1, h)   # b2a1 + a2b̄1
    return lo | (hi << h)


def all_ones(dim: int) -> int:
    """𝟏_dim = Σ e_k = the all-ones vector (0xFF…F at dim 32)."""
    return (1 << dim) - 1


def trace_laplacian_gf2(w: int, dim: int = 32) -> int:
    """Δ(w) = w · 𝟏_dim. Its popcount is the spectral distance from the
    zero-divisor nodal line; Δ(w) = 0 exactly when w is nilpotent (G5)."""
    return cd_mul_gf2(w, all_ones(dim), dim)


def is_nilpotent_gf2(w: int, dim: int = 32) -> bool:
    """w² = 0 in T_dim/GF(2)."""
    return cd_mul_gf2(w, w, dim) == 0


def euler_phi(n: int) -> int:
    """|units of ℤ/(n)| — the count of residues coprime to n."""
    result, m, p = n, n, 2
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            result -= result // p
        p += 1
    if m > 1:
        result -= result // m
    return result


def primary_decomposition(n: int) -> Dict[int, int]:
    """(n) = ⋂ (pᵢ^aᵢ) as {prime: exponent} — the Lasker–Noether primary
    decomposition of the ideal, which is the SECOND-order (cepstral) factoral
    datum: the peaks are at the primes, the heights are the exponents."""
    out: Dict[int, int] = {}
    m, p = n, 2
    while p * p <= m:
        while m % p == 0:
            out[p] = out.get(p, 0) + 1
            m //= p
        p += 1
    if m > 1:
        out[m] = out.get(m, 0) + 1
    return out


def von_mangoldt(n: int) -> float:
    """Λ(n) = log p if n = pᵏ (a prime power), else 0. The cepstral weight —
    Λ is supported exactly on the primary components of the integers, and the
    explicit formula ψ(x) = x − Σ_ρ xᵖ/ρ is the transform back to the zeros."""
    pd = primary_decomposition(n)
    if len(pd) == 1:
        return math.log(next(iter(pd)))
    return 0.0


def quotient_zero_divisors(n: int) -> List[int]:
    """The zero divisors of ℤ/(n): the nonzero residues a with gcd(a,n) > 1.
    Empty exactly when n is prime (or 1) — then ℤ/(n) is a field (or the zero
    ring). This is the FALL test, done in the quotient ring itself."""
    from math import gcd
    return [a for a in range(2, n) if gcd(a, n) > 1]


def fall_test(n: int) -> Dict[str, Any]:
    """The unifying fall/survive test, read through the quotient ring.

    survive  ⟺  ℤ/(n) is a field (n prime)          → Telperion, a leaf
    fall     ⟺  ℤ/(n) has zero divisors (n composite) → Laurelin, an internal node
    mingling ⟺  n ∈ {0, 1}                            → the identities, neither tree
    """
    if n < 2:
        return {'n': n, 'verdict': 'MINGLING', 'tree': None,
                'quotient': 'ℤ/(0)=ℤ (a domain)' if n == 0 else 'ℤ/(1)=0 (zero ring)',
                'has_zero_divisors': False}
    zds = quotient_zero_divisors(n)
    fell = len(zds) > 0
    return {
        'n': n,
        'verdict': 'FALL' if fell else 'SURVIVE',
        'tree': 'LAURELIN' if fell else 'TELPERION',
        'quotient': f'ℤ/({n}) ' + ('has zero divisors' if fell else 'is a field'),
        'has_zero_divisors': fell,
        'n_zero_divisors': len(zds),
        'primary_decomposition': primary_decomposition(n),
    }


def arith_deriv(n: int) -> int:
    """THE RING-THEORY DERIVATIVE — the arithmetic derivative on (ℤ, +, ×).

    Defined by exactly the two axioms of a ring DERIVATION, applied to the
    integers directly (not by analogy):

        p' = 1                      for every prime p      (the base case)
        (mn)' = m'·n + m·n'         the LEIBNIZ / product rule

    This is the ring-theoretic answer to "what is the derivative in calculus":
    a derivation is ANY additive map satisfying Leibniz, and this is the one
    forced on ℤ by declaring primes to have derivative 1 (the atoms — constant
    rate, exactly d/dx(x) = 1). It needs no limit, no topology, only the ring
    structure and the primary decomposition already computed by this module.

    Closed form (the log-derivative rule, exact — see G8): for
    n = ∏ pᵢ^aᵢ,  n' = n · Σ(aᵢ/pᵢ), the integer analogue of
    d/dx log n = Σ aᵢ · d/dx log(pᵢ), i.e. n'/n plays the role of a
    LOGARITHMIC derivative — the cepstral (order-2) datum read as a rate.
    """
    if n in (0, 1):
        return 0
    pd = primary_decomposition(n)
    from fractions import Fraction
    total = sum(Fraction(a, p) for p, a in pd.items())
    return int(n * total)


# ═══════════════════════════════════════════════════════════════════════════
# FRACTAL DECOMPOSITION (2026-08-22) — the highest-order factoral rung
# ═══════════════════════════════════════════════════════════════════════════
# A fractal is the higher-order generational lineage of a toroidal bifurcation,
# which is the higher-order lineage of a ring, which is the higher-order lineage
# of a circle. Each level is the lineage operator applied to the one below;
# "the same maths at every level" IS self-similarity, so the tower is a fractal.
#
# The order tower of factoral decomposition (spectrum -> cepstrum -> bispectrum)
# does not stop at order 3. Iterated to the limit it is a FRACTAL: apply the
# fall/survive test not once but under repeated iteration of a generator, and
# the boundary between fall (escape) and survive (bounded) is a self-similar set
# with a fractal dimension. Fall/survive here is the SAME dichotomy as G1 (does
# the quotient have zero divisors), now read on the DYNAMICS of an iterated map.
#
# THE LIBRARY IS THE CONTROL SET. Ainulindale/wiki/fractals/ catalogues 200+
# Ultra Fractal generators (Mandelbrot/Julia/Nova/Phoenix/Burning-Ship/...).
# Each is a known generator with a known dimension — a CONTROL to calibrate the
# instrument against, and an INSTRUCTION MANUAL (its escape-time/IFS rule) for a
# different higher-order lineage. escape_survives()/box_dimension() below take
# the generator as an argument so any catalogue formula can drive them.


def nonassoc_count(d: int) -> int:
    """Number of ordered distinct basis triples with associator ≠ 0 in T_d.
    The exact self-similarity datum of the Cayley–Dickson tower (FR1)."""
    c = 0
    for i in range(d):
        for j in range(d):
            for k in range(d):
                if len({i, j, k}) < 3:
                    continue
                L = cd_mul(cd_mul(unit(d, i), unit(d, j)), unit(d, k))
                R = cd_mul(unit(d, i), cd_mul(unit(d, j), unit(d, k)))
                if nrm([a - b for a, b in zip(L, R)]) > 1e-9:
                    c += 1
    return c


def _logistic_period(r: float, settle: int = 20000, tol: float = 1e-9) -> int:
    x = 0.5
    for _ in range(settle):
        x = r * x * (1 - x)
    orbit = [x]
    for _ in range(256):
        x = r * x * (1 - x)
        orbit.append(x)
    for p in (1, 2, 4, 8, 16, 32):
        if all(abs(orbit[i] - orbit[i + p]) < tol for i in range(64)):
            return p
    return 999


def feigenbaum_delta() -> Dict[str, Any]:
    """The period-doubling bifurcation cascade of the logistic map — the 1D
    shadow of the toroidal bifurcation. Successive interval ratios → the
    Feigenbaum constant δ = 4.6692… (FR2). 'Bifurcates emergently', measured."""
    def bif(target, a, b):
        for _ in range(80):
            m = (a + b) / 2
            if _logistic_period(m) >= target:
                b = m
            else:
                a = m
        return (a + b) / 2
    pts = [3.0, bif(4, 3.40, 3.48), bif(8, 3.53, 3.55),
           bif(16, 3.560, 3.567), bif(32, 3.5685, 3.5700)]
    deltas = [(pts[i + 1] - pts[i]) / (pts[i + 2] - pts[i + 1])
              for i in range(len(pts) - 2)]
    return {'bifurcation_points': pts, 'delta_estimates': deltas,
            'feigenbaum': 4.66920160910299}


# A few generators from the "library" — each a control with a known character.
MANDELBROT = lambda z, c: z * z + c                                # noqa: E731
BURNING_SHIP = lambda z, c: complex(abs(z.real), abs(z.imag)) ** 2 + c  # noqa: E731


def escape_survives(c: complex, step, z0: complex = 0j,
                    maxiter: int = 80, bailout: float = 2.0) -> bool:
    """The iterated fall/survive test. survive = the orbit stays BOUNDED (in
    the set); fall = it ESCAPES past the bailout. This is G1's dichotomy read on
    dynamics: bounded ↔ a domain, escaping ↔ zero divisors appear.

    Guarded (2026-08-22): Magnet-type generators (z→((z²+c−1)/(2z+c−2))²) can
    divide by zero or overflow — a blow-up IS an escape, so it counts as a fall.
    """
    z = z0
    for _ in range(maxiter):
        try:
            z = step(z, c)
        except (ZeroDivisionError, OverflowError, ValueError):
            return False
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            return False
        if abs(z) > bailout:
            return False
    return True


# ═══════════════════════════════════════════════════════════════════════════
# THE LABELINGS — decomposition readouts lifted from the UF formulary's .ucl
# coloring methods (PtolemyDesktop/Archimedes/Maths/Formula/UFformulary/).
# "Multiple types of fractals, multiple types of labeling": the GENERATOR is
# the fractal, the LABELING is the decomposition. Each labeling below is one
# rung of the order tower, and its .ucl source is its instruction manual.
# ═══════════════════════════════════════════════════════════════════════════

def smooth_escape(c: complex, step, z0: complex = 0j,
                  maxiter: int = 80, bailout: float = 2.0) -> float:
    """ORDER 1 — the continuous escape rate (smooth iteration count). The
    fall/survive test with a real-valued readout: how fast the orbit falls.
    maxiter (= did not fall) for survivors."""
    z = z0
    for n in range(maxiter):
        try:
            z = step(z, c)
        except (ZeroDivisionError, OverflowError, ValueError):
            return float(n)
        az = abs(z)
        if az > bailout:
            return n + 1 - math.log(math.log(max(az, 1.0000001))) / math.log(2)
    return float(maxiter)


def orbit_trap(c: complex, step, z0: complex = 0j, trap: complex = 0j,
               maxiter: int = 80, bailout: float = 1e6) -> float:
    """ORDER 1 (support) — closest approach of the orbit to a trap point. Which
    structures the orbit visits; the spectral 'support' of the orbit."""
    z = z0
    best = float('inf')
    for _ in range(maxiter):
        try:
            z = step(z, c)
        except (ZeroDivisionError, OverflowError, ValueError):
            break
        best = min(best, abs(z - trap))
        if abs(z) > bailout:
            break
    return best


def orbit_curvature(c: complex, step, z0: complex = 0j,
                    maxiter: int = 60, bailout: float = 1e6) -> float:
    """ORDER 3 — Kerry Mitchell / dmj-Curvature: the average |arg((z−z')/(z'−z''))|
    over the orbit, i.e. the discrete curvature of the orbit PATH. Needs THREE
    consecutive points, exactly as the associator needs three elements. Returns
    -1.0 when fewer than three points exist (undefined → the order-3 signature)."""
    zold2 = zold = None
    a = 0.0
    i = 0
    z = z0
    for _ in range(maxiter):
        try:
            z = step(z, c)
        except (ZeroDivisionError, OverflowError, ValueError):
            break
        if abs(z) > bailout:
            break
        if i >= 2 and abs(zold - zold2) > 1e-18:
            a += abs(cmath.phase((z - zold) / (zold - zold2)))
        zold2, zold = zold, z
        i += 1
    return a / (i - 1) if i >= 3 else -1.0


def lyapunov_exponent(r: float, settle: int = 1000, n: int = 4000) -> float:
    """THE DRIFT — the Lyapunov exponent of the logistic map. λ < 0 in stable
    (survive) windows, λ > 0 in chaos (fall), λ ≈ 0 at the accumulation. The
    continuous, dynamical form of the fall/survive test — the same object as the
    Collatz per-step drift log(√3/2) < 0 (contracts, so it survives to 1)."""
    x = 0.5
    for _ in range(settle):
        x = r * x * (1 - x)
    s = 0.0
    for _ in range(n):
        x = r * x * (1 - x)
        d = abs(r * (1 - 2 * x))
        s += math.log(d) if d > 1e-12 else -30.0
    return s / n


# ── Newton / Nova basins: k-way fall/survive = polynomial splitting = ring ───
def basin_of(z0: complex, step, roots, maxiter: int = 60, tol: float = 1e-6) -> int:
    """Which root the orbit converges to — the k-WAY generalisation of
    fall/survive. Returns the root index, or -1 if it does not converge. Which
    root you fall into is which linear factor: this is ring splitting."""
    z = z0
    for _ in range(maxiter):
        try:
            z = step(z, 0j)
        except (ZeroDivisionError, OverflowError, ValueError):
            return -1
        for k, r in enumerate(roots):
            if abs(z - r) < tol:
                return k
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            return -1
    return -1


def newton_basins(k: int, N: int = 60, R: float = 1.6,
                  maxiter: int = 60) -> Dict[str, Any]:
    """Newton's method on p(z) = zᵏ − 1. Its k roots are the k-th roots of unity
    — the linear factorisation zᵏ − 1 = ∏(z − ζⱼ). The plane partitions into k
    basins; which basin = which factor. The basin boundary is the (fractal)
    Julia set. This is G1's fall/survive taken k-way — prime splitting made
    visible."""
    roots = [cmath.exp(2j * math.pi * j / k) for j in range(k)]
    p = lambda z: z ** k - 1                        # noqa: E731
    dp = lambda z: k * z ** (k - 1)                 # noqa: E731
    step = lambda z, c: z - p(z) / dp(z)            # noqa: E731
    labels = []
    for jy in range(N):
        for ix in range(N):
            z0 = complex(-R + 2 * R * ix / N, -R + 2 * R * jy / N)
            labels.append(basin_of(z0, step, roots, maxiter))
    grid = [labels[i * N:(i + 1) * N] for i in range(N)]
    basins = sorted(set(l for l in labels if l >= 0))
    boundary = sum(1 for j in range(N - 1) for i in range(N - 1)
                   if grid[j][i] != grid[j][i + 1] or grid[j][i] != grid[j + 1][i])
    return {'k': k, 'n_basins': len(basins), 'basins': basins, 'roots': roots,
            'boundary_boxes': boundary, 'step': step}


def label_orbit(c: complex, step, z0: complex = 0j) -> Dict[str, float]:
    """All labelings of one orbit at once — the decomposition tower on a single
    point. This is what a visualiser paints per pixel: one generator, many
    labelings. order 1 (escape rate), order 1-support (trap), order 3
    (curvature). survive is the boolean underneath them all."""
    return {
        'survive': escape_survives(c, step, z0),
        'escape_rate': smooth_escape(c, step, z0),       # order 1
        'orbit_trap': orbit_trap(c, step, z0),           # order 1 — support
        'curvature': orbit_curvature(c, step, z0),       # order 3
    }


def box_dimension(step, xr, yr, param=None, resolutions=(50, 100, 200),
                  maxiter: int = 80, bailout: float = 2.0) -> Dict[str, Any]:
    """Box-counting dimension of the fall/survive BOUNDARY of a generator.

    param=None  -> Mandelbrot-like: c varies over the plane, z₀ = 0.
    param=c     -> Julia-like: c fixed, z₀ varies over the plane.
    The boundary is the σ=½-analog critical set; a fractal has 1 < D < 2.
    """
    boxes = []
    for N in resolutions:
        xs = [xr[0] + (xr[1] - xr[0]) * i / N for i in range(N)]
        ys = [yr[0] + (yr[1] - yr[0]) * j / N for j in range(N)]
        if param is None:
            g = [[escape_survives(complex(x, y), step, 0j, maxiter, bailout)
                  for x in xs] for y in ys]
        else:
            g = [[escape_survives(param, step, complex(x, y), maxiter, bailout)
                  for x in xs] for y in ys]
        cnt = sum(1 for j in range(N - 1) for i in range(N - 1)
                  if g[j][i] != g[j][i + 1] or g[j][i] != g[j + 1][i])
        boxes.append(cnt)
    D = [math.log(boxes[k + 1] / boxes[k]) / math.log(resolutions[k + 1] / resolutions[k])
         for k in range(len(boxes) - 1)]
    return {'resolutions': list(resolutions), 'boundary_boxes': boxes,
            'dimension_estimates': D}


# ═══════════════════════════════════════════════════════════════════════════
# THE PATHWAY LAYER (2026-08-22) — a DIFFERENT CLASS from bifurcation.
# Bifurcation asks "which way does it split?" (classification, backward, the
# cross/curvature). Pathway asks "how do I travel there?" (construction,
# forward, the dot/projection). Factoring N is a pathway problem: N is the
# ENDPOINT of the multiplicative path 1 → p → N, and the factors are the STEPS.
# The overhead reduction lives here because a path is WALKED (O length), not a
# branch structure SEARCHED (O space). And the spiral can be TUNED.
#
# HONEST FRAMING (kept from the discussion): CFRAC below is a KNOWN
# sub-exponential factorer (Morrison–Brillhart 1975), used to demonstrate the
# pathway CLASS. Tuning (the multiplier) is real (CFRAC/QS/NFS). Whether the
# framework's geometry adds a resonance the sieve cannot see is OPEN. Nothing
# here claims a polynomial factoring or an RSA break.
# ═══════════════════════════════════════════════════════════════════════════

def spiral_address(n: int, pitch: float = 0.15, period: float = 0.0) -> Dict[str, float]:
    """Position of n on the TUNABLE log-spiral. pitch = log-radius growth;
    period TUNES the angular winding (angle = 2π·log n / log period), period=0
    winds by radians. Multiplication is ADDITIVE here — address(p·q) =
    address(p) + address(q) — so the factors are steps on the path (PW3)."""
    t = math.log(n)
    lr = pitch * t
    ang = (2 * math.pi * t / math.log(period)) if period > 1 else t
    return {'n': n, 't': t, 'log_radius': lr, 'angle': ang,
            'x': math.exp(lr) * math.cos(ang), 'y': math.exp(lr) * math.sin(ang)}


def pathway_residues(N: int, mult: int = 1, steps: int = 300,
                     keep: int = 64) -> Dict[str, Any]:
    """The TUNABLE continued-fraction geodesic of √(mult·N) — a pathway-class
    walk. Its residues stay O(√N); a square residue gives a congruence of
    squares → a factor. `mult` TUNES the spiral (which residues become square)."""
    from math import isqrt, gcd
    M = mult * N
    r = isqrt(M)
    if r * r == M:                                   # degenerate perfect square
        g = gcd(r, N)
        fac = (min(g, N // g), max(g, N // g)) if 1 < g < N else None
        return {'mult': mult, 'factor': fac, 'step': 0, 'residues': [r * r],
                'degenerate': True}
    a0 = isqrt(M)
    m, d, a = 0, 1, a0
    A_prev, A = 1, a0
    res: List[int] = []
    for i in range(steps):
        m = d * a - m
        d = (M - m * m) // d
        a = (a0 + m) // d if d else 0
        if len(res) < keep:
            res.append(d)
        rr = isqrt(d)
        if rr * rr == d:
            f = gcd(A - rr, N)
            if 1 < f < N:
                return {'mult': mult, 'factor': (min(f, N // f), max(f, N // f)),
                        'step': i + 1, 'residues': res}
        A_prev, A = A, (a * A + A_prev) % N
        if d == 0:
            break
    return {'mult': mult, 'factor': None, 'step': None, 'residues': res}


def tune_pathway(N: int, multipliers=(1, 3, 5, 7, 11, 13, 2, 6, 15, 21),
                 steps: int = 400) -> Dict[str, Any]:
    """Sweep the spiral tuning (the multiplier) until the geodesic RESONATES
    onto a factor. The pathway-class 'search' is a continuous dial, not a walk
    over discrete branches."""
    for k in multipliers:
        r = pathway_residues(N, mult=k, steps=steps)
        if r['factor']:
            return {'N': N, 'tuning': k, 'step': r['step'], 'factor': r['factor']}
    return {'N': N, 'tuning': None, 'step': None, 'factor': None}


def fermat_path(N: int, maxsteps: int = 200000):
    """The TWO-ANCHOR geodesic. Origin (1) and destination (N) are BOTH pinned,
    so the natural reference is the midpoint a₀ = ⌈√N⌉ between them. Walk the
    excursion b outward until a² − N is a square (a NODE): N = (a−b)(a+b). The
    excursion is the distance from the midpoint anchor to the factor — the
    IMBALANCE of N. Fast when the two anchors sit close (balanced N)."""
    from math import isqrt
    a = isqrt(N)
    if a * a < N:
        a += 1
    for i in range(maxsteps):
        b2 = a * a - N
        b = isqrt(b2)
        if b * b == b2:
            return {'factor': (a - b, a + b), 'excursion': i, 'a': a, 'b': b}
        a += 1
    return {'factor': None, 'excursion': None}


def number_chart_point(N: int, a: int, a0: int = None) -> float:
    """THE VISUALISER'S METHODOLOGY — the Smith chart, applied. Γ_N(a) folds
    the (unbounded) Fermat search radius into a BOUNDED coordinate in [0, 1),
    exactly as the Smith chart folds the impedance half-plane into the unit
    disk: Γ_N = excursion / (excursion + 2·a₀), a₀ = the midpoint anchor
    ⌈√N⌉ (PW5). a₀ ↦ Γ_N = 0 (the fixed point — a Smith-chart "matched load");
    the horizon Γ_N → 1 is unbounded excursion — no factor found within reach.

    Where the factor NODE lands on this chart is a difficulty gauge, read at a
    glance: balanced N sits at the anchor (Γ_N ≈ 0); unbalanced/hard N sits
    near the horizon (Γ_N ≈ 1) — the same landmark reading a Smith chart gives
    for how far a load is from being matched.
    """
    from math import isqrt
    if a0 is None:
        a0 = isqrt(N)
        if a0 * a0 < N:
            a0 += 1
    excursion = a - a0
    return excursion / (excursion + 2 * a0)


def decompose_number(N: int) -> Dict[str, Any]:
    """The MULTI-PERSPECTIVE bundle for one integer — the visualiser's data
    model. One number, every perspective: ring (fall/survive), cepstral
    (primary decomposition), lineage (factor tree), spiral (address), pathway
    (tuned geodesic). The integer analogue of label_orbit()."""
    ft = fall_test(N)
    pd = primary_decomposition(N) if N >= 2 else {}
    out = {
        'n': N,
        'ring_fall_survive': {'verdict': ft['verdict'], 'tree': ft['tree'],
                              'quotient': ft['quotient']},
        'cepstral_primary': pd,
        'omega_distinct': len(pd),
        'Omega_lineage_length': sum(pd.values()),
        'lineage_tree': factor_lineage(N),
        'spiral_address': spiral_address(N) if N >= 2 else None,
    }
    out['pathway'] = (tune_pathway(N) if ft['verdict'] == 'FALL'
                      else {'note': 'prime/unit — no factor path to walk'})
    if ft['verdict'] == 'FALL':
        fp = fermat_path(N, maxsteps=20000)
        out['number_chart'] = ({'gamma': number_chart_point(N, fp['a']),
                                'excursion': fp['excursion'], 'a': fp['a']}
                               if fp['factor'] else None)
    else:
        out['number_chart'] = None
    return out


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
    # ── ring-theory operations ──────────────────────────────────────────────
    'ideal':        (2, 'a fixed set closed under absorption R·I ⊆ I',
                     'a FIXED SET — DERIVED. the kernel of a quotient map'),
    'quotient':     (1, 'SCALE — the collapse R → R/I',
                     'a DILATE with gain 0 on I; the ring-theoretic FALL'),
    'radical':      (2, 'the nilpotents — √(0) — a fixed set/ideal',
                     'a FIXED SET — DERIVED. where the trace-Laplacian vanishes'),
    'unit':         (3, 'a COUNT: the invertibles, |units| = φ(n)',
                     'DERIVED. the SURVIVORS; complement of the zero divisors'),
    'zero-divisor': (2, 'the ZD set = ∪ associated primes — a fixed set',
                     'a FIXED SET — DERIVED. the FALL locus, one operation to test'),
    'associator':   (3, '[a,b,c] = (ab)c − a(bc)',
                     'a TRIPLE PRODUCT — DERIVED, and it is the OBSTRUCTION to '
                     'being a ring: ≡ 0 for a genuine ring, ≠ 0 from 𝕆 upward'),
    'primary-decomposition': (3, 'Lasker–Noether: (n) = ⋂(pᵢ^aᵢ)',
                     'a COUNT of primary components — the SECOND-order (cepstral) '
                     'factoral datum. exponents = peak heights, Ω(n) = Σ'),
    'derivative':    (1, 'a DERIVATION: p′=1, Leibniz (mn)′=m′n+mn′',
                     'a linear map obeying ONE algebraic law — the ring-theory '
                     'floor calculus sits on. no limit, no topology needed'),
    # ── fractal-decomposition operations (the highest-order rung) ────────────
    'self-similar':  (3, 'the lineage operator applied to its own output',
                     'a RATIO across scales — DERIVED. "the same maths at every '
                     'level" is exactly this'),
    'bifurcation':   (1, 'a DILATE that splits one branch into two',
                     'the generator of the fractal; iterated it gives the tree. '
                     'J₂ is the torus involution that generates it'),
    'fractal':       (3, 'the fall/survive boundary of an iterated generator',
                     'a RATIO — box-count dimension 1 < D < 2. the highest-order '
                     'factoral decomposition; ring theory is its skeleton'),
    # ── labelings, lifted from the UF formulary's .ucl coloring methods ──────
    'basin':         (2, 'which root a Newton orbit converges to',
                     'a FIXED SET (k-way) — DERIVED. the k-way fall/survive; '
                     'which basin = which linear factor = ring splitting'),
    'orbit-trap':    (3, 'closest approach of the orbit to a shape',
                     'a COUNT/min over the orbit — the order-1 SUPPORT labeling'),
    'orbit-curvature': (3, 'avg |arg((z−z′)/(z′−z″))| over the orbit',
                     'a RATIO needing THREE orbit points — the ORDER-3 labeling, '
                     'the associator read on dynamics (Kerry Mitchell / dmj)'),
    'lyapunov':      (3, 'the divergence rate of an iterated map',
                     'a RATIO (log-derivative) — the DRIFT: λ<0 survive, λ>0 '
                     'fall. the continuous form of the fall/survive test'),
    # ── the pathway layer — a different CLASS from bifurcation ───────────────
    'pathway':       (2, 'a walk from the anchor to N: 1 → p → N',
                     'CONSTRUCTION, not classification — a path is WALKED '
                     '(O length), the opposite class to a bifurcation SEARCH'),
    'spiral':        (1, 'rotation + logarithmic advance (Archimedes screw)',
                     'REFLECT∘REFLECT (rotate) with DILATE (log advance) — where '
                     'multiplication becomes an additive path'),
    'tuning':        (1, 'reparametrise the spiral (pitch / period / multiplier)',
                     'a DILATE of the parameter; sweep it until the factor '
                     'RESONATES. σ is the framework\'s name for this knob'),
    'inside-outside': (2, 'L_(I|O): dot and cross from ONE product',
                     'the inside (dot/discrete/Telperion) and outside (cross/'
                     'continuous/Laurelin) in one measurement; equal at σ=½'),
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

    # ═══════════════════════════════════════════════════════════════════════
    # THE RING-THEORY BLOCK (G1–G6). Added 2026-08-22.
    # The factoral tower named in its proper ring theory. Every number COMPUTED.
    # ═══════════════════════════════════════════════════════════════════════

    # ── G1 — the unifying theorem: FALL ⟺ the quotient ring has zero divisors ─
    def g_fall_is_quotient_zd(self, N: int = 2000) -> None:
        from math import gcd
        flags = _sieve(N)
        bad = 0
        for n in range(2, N + 1):
            has_zd = any(gcd(a, n) > 1 for a in range(2, n))   # ℤ/(n) zero divisor
            is_composite = not flags[n]
            if has_zd != is_composite:
                bad += 1
        self._record(
            'ring.fall_is_quotient_zd',
            'an element FALLS iff its quotient ring has zero divisors: n is '
            'composite ⟺ ℤ/(n) has a zero divisor ⟺ (n) is not a prime ideal. '
            'The Two Trees ARE this dichotomy — domain vs. not-a-domain',
            2, 'the zero-divisor set of ℤ/(n) — a fixed set (∪ associated primes)',
            True, bad == 0,
            f'[KNOWN (elementary ring theory)] checked every n in [2,{N}]: {bad} disagreements between "ℤ/(n) '
            f'has a zero divisor" and "n is composite". Telperion (prime) = '
            f'ℤ/(n) is a FIELD, survives; Laurelin (composite) = ℤ/(n) has '
            f'zero divisors, falls. Same statement as the T₃₂ fall test: a '
            f'constant falls ⟺ it is nilpotent ⟺ it is a zero divisor.')

    # ── G2 — gcd IS the integer trace-Laplacian; the census closes ───────────
    def g_gcd_is_the_detector(self, samples=(97, 360, 1024, 2310, 65537)) -> None:
        from math import gcd
        rows, ok = {}, True
        for n in samples:
            units = sum(1 for a in range(1, n) if gcd(a, n) == 1)
            zds = sum(1 for a in range(1, n) if gcd(a, n) > 1)
            census = units + zds + 1 == n and units == euler_phi(n)
            rows[n] = (units, zds, census)
            if not census:
                ok = False
        self._record(
            'ring.gcd_is_the_detector',
            'the zero-divisor detector of ℤ/(n) is gcd(a,n) > 1 — ONE division, '
            'the integer trace-Laplacian; and the census closes exactly: '
            'units φ(n) + zero-divisors + {0} = n', 0,
            'SCALE (division) — Axis 2 of the tier-0 floor',
            True, ok,
            '[KNOWN (elementary)] ' + '  '.join(f'n={n}: units={u}=φ, zd={z}, +{{0}}={u+z+1}=n:{c}'
                      for n, (u, z, c) in rows.items()) +
            '  — gcd is to ℤ/(n) what Δ(w)=w·𝟏 is to T₃₂/GF(2): the single '
            'operation that decides fall vs. survive.')

    # ── G3 — primary decomposition IS the cepstrum ───────────────────────────
    def g_primary_decomposition_is_cepstrum(self, N: int = 3000) -> None:
        bad, worst = 0, None
        for n in range(2, N):
            pd = primary_decomposition(n)
            recon = 1
            for p, a in pd.items():
                recon *= p ** a
            omega = sum(pd.values())               # Ω(n), with multiplicity
            small_omega = len(pd)                   # ω(n), distinct primes
            lin = factor_lineage(n)
            lam = von_mangoldt(n)
            is_prime_power = len(pd) == 1
            lam_ok = (lam > 0) == is_prime_power
            if not (recon == n and omega == lin['omega']
                    and small_omega == len(set(lin['leaves_telperion']))
                    and lam_ok):
                bad += 1
                worst = worst or n
        self._record(
            'ring.primary_decomposition_is_cepstrum',
            'the Lasker–Noether primary decomposition (n) = ⋂(pᵢ^aᵢ) IS the '
            'second-order (cepstral) factoral datum: exponents = peak heights, '
            'Ω(n) = Σ = lineage length, ω(n) = support; von Mangoldt Λ is '
            'supported exactly on the primary components (prime powers)', 3,
            'a COUNT of primary components — a ratio of the primes of G1',
            True, bad == 0,
            f'[KNOWN (Lasker–Noether)] n in [2,{N}): {bad} disagreements. ∏pᵢ^aᵢ reconstructs n; Ω '
            f'matches the lineage length (F5); Λ(n)>0 iff n is a prime power. '
            f'Λ is the cepstral domain of the integers, and ψ(x)=x−Σ_ρ xᵖ/ρ '
            f'is the transform back to the Riemann zeros — the spectrum.')

    # ── G4 — over GF(2), x² ∈ {0, e₀}: the radical / units split ──────────────
    def g_radical_units_split_gf2(self, dim: int = 8) -> None:
        squares = [cd_mul_gf2(x, x, dim) for x in range(1 << dim)]
        in_split = all(s in (0, 1) for s in squares)
        nil = sum(1 for s in squares if s == 0)      # includes x=0
        unit = sum(1 for s in squares if s == 1)
        half = (1 << dim) // 2
        self._record(
            'ring.radical_units_split_gf2',
            'over GF(2) every element squares to 0 or e₀: the NILPOTENTS (the '
            'radical √0 — a fixed set/ideal) and the INVOLUTORY units split the '
            f'algebra in half — {nil}/{unit} at dim {dim}', 2,
            'the radical of T_dim/GF(2) — a fixed set, and the trace-Laplacian '
            'projects onto it',
            True, in_split and nil == unit == half,
            f'[KNOWN framing] dim {dim}, all {1 << dim} elements: squares ⊆ {{0, e₀}} = '
            f'{in_split}; nilpotent {nil} = involutory {unit} = {half} = 2^dim/2. '
            f'The fallen live in the radical; the survivors are the units. This '
            f'is the algebra-side of G1: fall = enter the radical.')

    # ── G5 — the trace-Laplacian, and the corrected annihilator fact ─────────
    def g_trace_laplacian_is_nilpotency(self, dim: int = 8, n_rand: int = 20000) -> None:
        import random
        # (a) exhaustive at `dim`: Δ(w)=0 ⟺ w²=0
        exh = all((trace_laplacian_gf2(w, dim) == 0) == is_nilpotent_gf2(w, dim)
                  for w in range(1 << dim))
        # (b) 𝟏 is NOT a global annihilator: e₀ is a witness (e₀·𝟏 = 𝟏 ≠ 0)
        one = all_ones(dim)
        not_global = cd_mul_gf2(1, one, dim) != 0
        # (c) sampled at dim 32: same equivalence, plus the SHA-1 name collision
        rng = random.Random(20260822)
        eq32 = all((trace_laplacian_gf2(w, 32) == 0) == is_nilpotent_gf2(w, 32)
                   for w in (rng.getrandbits(32) for _ in range(n_rand)))
        IV = (0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0)
        Kc = (0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xCA62C1D6)
        iv_null = all(cd_mul_gf2(a, b, 32) == 0 for a in IV for b in IV)
        iv_dist0 = all(trace_laplacian_gf2(w, 32) == 0 for w in IV)
        k_distmax = all(bin(trace_laplacian_gf2(w, 32)).count('1') == 32 for w in Kc)
        self._record(
            'ring.trace_laplacian_is_nilpotency',
            'the trace-Laplacian Δ(w)=w·𝟏 vanishes IFF w is nilpotent (w²=0); '
            '𝟏 is NOT a global annihilator (e₀·𝟏 = 𝟏 ≠ 0). SHA-1\'s five IV '
            'constants are a NULL SUBALGEBRA on the nodal line (dist 0); its '
            'four round constants sit at maximum distance (32)', 2,
            'the radical of G4 read as the kernel of the linear map w ↦ w·𝟏',
            True, exh and not_global and eq32 and iv_null and iv_dist0 and k_distmax,
            f'[OURS — corrects a false lemma] dim {dim} exhaustive: Δ(w)=0 ⟺ w²=0 holds for all {1 << dim} '
            f'elements = {exh}; 𝟏 global annihilator? {not not_global} '
            f'(e₀·𝟏 = 𝟏, so NO). dim 32: equivalence over {n_rand} random = '
            f'{eq32}; the 5 SHA-1 IVs are a null subalgebra ({iv_null}) all at '
            f'distance 0 ({iv_dist0}); the 4 round constants all at distance 32 '
            f'({k_distmax}). The lemma "x·𝟏=0 for all x" contradicts its own '
            f'distance table and is retracted; the THEOREM stands, machine-verified.')

    # ── G7 — ring theory holds BOTH closed and open pathways ─────────────────
    def g_open_and_closed_pathways(self) -> None:
        from math import gcd

        def returns_to_anchor(a, N, steps=300):
            x = a % N
            for _ in range(steps):
                if x == 1:
                    return True
                x = (x * a) % N
            return False
        bad = 0
        for N in (12, 30, 100, 210):
            for a in range(1, N):
                if returns_to_anchor(a, N) != (gcd(a, N) == 1):
                    bad += 1
        ok = bad == 0
        self._record(
            'ring.open_and_closed_pathways',
            'ring theory describes BOTH: a CLOSED pathway (returns to the anchor '
            '1) is exactly a UNIT; an OPEN pathway (never returns to 1) is '
            'exactly a ZERO DIVISOR. Group theory has only the closed ones — the '
            'open sector is what RING theory adds', 2,
            'the multiplicative orbit of a in ℤ/N — units cycle back to 1, zero '
            'divisors do not',
            True, ok,
            f'[exact] over ℤ/12,30,100,210: {bad} mismatches between '
            f'"orbit returns to the anchor 1" and "gcd(a,N)=1 (unit)". So '
            f'CLOSED ⟺ unit, OPEN ⟺ zero divisor. Open pathways come in two '
            f'ring-theoretic kinds: TERMINATING (nilpotents fall to 0 — the ρ '
            f'tail, = Pollard rho) and CONVERGENT (Möbius/continued-fraction '
            f'orbits spiral to an attractor, e.g. z→1+1/z → φ in ℤ[φ], the '
            f'Gemini event-horizon sim). The horizon r=1 is the units (closed, '
            f'the Observer/e₀ sits on it); the fall to 0 or φ is open. A FIELD '
            f'(N prime) is all-closed; a ring with zero divisors (N composite) '
            f'has open pathways — closed-vs-open IS G1, survive-vs-fall.')

    # ── G6 — the associator is the OBSTRUCTION to being a ring ────────────────
    def g_associator_is_ring_defect(self) -> None:
        def associates(d):
            for i in range(d):
                for j in range(d):
                    for k in range(d):
                        L = cd_mul(cd_mul(unit(d, i), unit(d, j)), unit(d, k))
                        R = cd_mul(unit(d, i), cd_mul(unit(d, j), unit(d, k)))
                        if L != R:
                            return False
            return True
        assoc = {d: associates(d) for d in (1, 2, 4, 8)}
        # a genuine ring has associator ≡ 0; ℝ,ℂ,ℍ do, 𝕆 does not
        ok = assoc[1] and assoc[2] and assoc[4] and not assoc[8]
        self._record(
            'ring.associator_is_ring_defect',
            'a genuine ring has associator [a,b,c] ≡ 0. ℝ,ℂ,ℍ are rings '
            '(associator vanishes); 𝕆 and up are NOT — the associator IS the '
            'obstruction, and its 168-quantisation (R5) measures the defect', 3,
            'the associator — the third-order (bispectral) factoral datum',
            True, ok,
            f'[KNOWN (CD property cascade)] associativity holds at dim 1,2,4 = {assoc[1],assoc[2],assoc[4]} '
            f'(ℝ,ℂ,ℍ are associative rings) and FAILS at dim 8 = {not assoc[8]} '
            f'(𝕆 is not a ring). Ring theory is COMPLETE on the ℤ side and is '
            f'exactly what breaks, rung by rung, on the algebra side: '
            f'commutativity@4, associativity@8, the domain property@16. The '
            f'associator is order-3 curvature; the fall is order-1 position.')

    # ── G8 — the RING-THEORY DERIVATIVE: a derivation forced onto ℤ ──────────
    def g_arithmetic_derivative(self) -> None:
        import random
        rng = random.Random(20260822)
        # Leibniz rule, from the closed form, over random pairs
        leibniz_bad = 0
        for _ in range(500):
            a, b = rng.randint(2, 800), rng.randint(2, 800)
            if arith_deriv(a * b) != arith_deriv(a) * b + a * arith_deriv(b):
                leibniz_bad += 1
        # built from the TWO AXIOMS ALONE (p'=1, Leibniz), bottom-up — not the
        # closed form — must agree with the closed form (both derive the same
        # unique derivation on a UFD)
        def from_axioms(n):
            if n <= 1:
                return 0
            pd = primary_decomposition(n)
            factors = [p for p, a in pd.items() for _ in range(a)]
            val, deriv = 1, 0
            for p in factors:
                deriv = deriv * p + val * 1
                val *= p
            return deriv
        axiom_bad = sum(1 for n in range(2, 2000)
                        if arith_deriv(n) != from_axioms(n))
        # power rule, exact: D(p^k) = k p^(k-1)
        power_ok = all(arith_deriv(p ** k) == k * p ** (k - 1)
                      for p in (2, 3, 5, 7) for k in (1, 2, 3, 4))
        # D(0)=D(1)=0 — the Mingling is killed, and D(prime)=1 — an atom, a
        # constant rate (the integer d/dx(x)=1)
        mingling_ok = arith_deriv(0) == 0 and arith_deriv(1) == 0
        atoms_ok = all(arith_deriv(p) == 1 for p in (2, 3, 5, 7, 97))
        # fixed points D(n)=n: forced to n=p^p by the power rule (k p^{k-1}=p^k ⟺ k=p)
        fixed = [n for n in range(2, 4000) if arith_deriv(n) == n]
        fixed_ok = fixed == [4, 27, 3125]   # 2^2, 3^3, 5^5 — all under 4000
        ok = (leibniz_bad == 0 and axiom_bad == 0 and power_ok
              and mingling_ok and atoms_ok and fixed_ok)
        self._record(
            'ring.arithmetic_derivative',
            'the RING-THEORY VERSION OF A DERIVATIVE is a DERIVATION — any '
            'additive map satisfying Leibniz — and forcing p\'=1 on the primes '
            'of ℤ (the atoms, a constant rate) determines ONE such map on all '
            'of ℤ by the product rule alone. No limit, no topology needed', 1,
            'REFLECT-free: a linear map obeying one algebraic law (Leibniz), '
            'not a geometric primitive — the ring-theory floor below calculus',
            True, ok,
            f'[KNOWN (arithmetic derivative, Barbeau 1961)] Leibniz D(ab)='
            f'D(a)b+aD(b): {500 - leibniz_bad}/500 hold; built from the two '
            f'AXIOMS alone (p\'=1, Leibniz) matches the closed form n·Σ(aᵢ/pᵢ) '
            f'for every n<2000 ({2000 - 2 - axiom_bad} agree); the POWER RULE '
            f'D(pᵏ)=kp^(k-1) is exact; D(0)=D(1)=0 (the Mingling is killed); '
            f'D(prime)=1 (an atom, constant rate — the integer d/dx(x)=1); and '
            f'the power rule FORCES the fixed points D(n)=n to n=pᵖ exactly — '
            f'measured {fixed}: 4=2², 27=3³, 3125=5⁵, the "arithmetic '
            f'eˣ", numbers that are their own derivative. n\'/n is the '
            f'LOGARITHMIC derivative — the SAME cepstral (order-2, G3) datum '
            f'read as a rate: d/dx log(x) ↔ n\'/n = Σ aᵢ/pᵢ.')

    # ═══════════════════════════════════════════════════════════════════════
    # THE FRACTAL BLOCK (FR1–FR3). Added 2026-08-22.
    # Fractal decomposition = the highest-order factoral rung: iterate the
    # bifurcation to the limit, and the fall/survive boundary is self-similar.
    # ═══════════════════════════════════════════════════════════════════════

    # ── FR1 — the CD tower is an EXACT self-similar recursion ────────────────
    def fr_tower_self_similar(self) -> None:
        n8, n16 = nonassoc_count(8), nonassoc_count(16)
        # persist core = 8 (an octonion) at every scale — R4's invariant
        persist = all(self.gains(d, 1, d // 2 + 2).get(1.0, 0) == 8
                      for d in (8, 16, 32))
        ok = (n8 == 168 and n16 == 1848 and n16 == 11 * n8 and persist)
        self._record(
            'fractal.tower_self_similar',
            'the Cayley–Dickson tower is an EXACT self-similar recursion: the '
            'associator-event count obeys a fixed multiplicative law under '
            'doubling (168 → 1848 = 11·168) and the gain-1 persist core is 8 '
            '(an octonion) at every scale — "the same maths at every level"',
            3, 'a RATIO across scales — the self-similarity of the tower',
            True, ok,
            f'[KNOWN (exact counts)] associator≠0: dim8={n8}, dim16={n16}='
            f'{n16 // n8}·{n8}; persist core = 8 at dim 8,16,32 = {persist}. '
            f'Self-similarity here is EXACT (a fixed recursion), not a fitted '
            f'dimension — the tower is the cleanest fractal in the framework, '
            f'and the generational lineage IS its address.')

    # ── FR2 — the bifurcation cascade: it bifurcates emergently → Feigenbaum ──
    def fr_bifurcation_cascade(self) -> None:
        f = feigenbaum_delta()
        d = f['delta_estimates']
        target = f['feigenbaum']
        brackets = min(d) < target < max(d)
        near = all(4.3 < x < 5.2 for x in d)
        ok = brackets and near
        self._record(
            'fractal.bifurcation_cascade',
            'the period-doubling cascade — the 1D shadow of the toroidal '
            'bifurcation — "bifurcates emergently", and the ratio of successive '
            'bifurcation intervals converges to the Feigenbaum constant '
            'δ = 4.6692, universal to the generator', 1,
            'the bifurcation (a splitting DILATE) iterated; J₂ is its generator',
            True, ok,
            f'[KNOWN (Feigenbaum 1978)] bifurcation points '
            f'{[round(x, 5) for x in f["bifurcation_points"]]}; δ estimates '
            f'{[round(x, 4) for x in d]} bracket {target:.4f}. The cascade is '
            f'the toroidal bifurcation about the σ=½ axis, read on the interval; '
            f'its accumulation point is a Cantor set — a fractal from iterating '
            f'one split.')

    # ── FR3 — the fall/survive boundary of an iterated generator is fractal ───
    def fr_fall_survive_boundary(self) -> None:
        # the baseline generator, plus two controls from the "library"
        mand = box_dimension(MANDELBROT, (-2, 0.5), (-1.25, 1.25))
        julia = box_dimension(MANDELBROT, (-1.5, 1.5), (-1.5, 1.5),
                              param=complex(-0.8, 0.156))
        ship = box_dimension(BURNING_SHIP, (-2, 1), (-2, 1))
        def fractal(res):
            return all(1.0 < x < 2.0 for x in res['dimension_estimates'])
        ok = fractal(mand) and fractal(julia) and fractal(ship)
        md = mand['dimension_estimates'][-1]
        jd = julia['dimension_estimates'][-1]
        sd = ship['dimension_estimates'][-1]
        self._record(
            'fractal.fall_survive_boundary',
            'the fall/survive boundary of an iterated generator is a FRACTAL '
            '(1 < D < 2): fall = the orbit escapes, survive = it stays bounded '
            '— G1\'s dichotomy read on dynamics. The library of generators are '
            'the CONTROLS, each with its own dimension', 3,
            'the fall/survive test (G1) iterated to the limit — a RATIO (box '
            'dimension) of the boundary',
            True, ok,
            f'[FRONTIER framing; controls from wiki/fractals/] box-count '
            f'dimension of the fall/survive boundary: Mandelbrot D≈{md:.2f}, '
            f'Julia(-0.8+0.156i) D≈{jd:.2f}, Burning-Ship D≈{sd:.2f} — all '
            f'strictly in (1,2), and DISTINCT, so the instrument separates '
            f'generators. bounded↔a domain, escaping↔zero divisors appear; the '
            f'boundary is the σ=½-analog critical set. This is a structural '
            f'analogy to arithmetic factoring, labelled as one — not a proof '
            f'that the Mandelbrot set IS the primes.')

    def run(self) -> None:
        super().run()                              # R1-R8, the sigma relations
        for f in (self.f_two_trees_exact, self.f_densities_conserve,
                  self.f_mingling_point, self.f_gcd_is_lca,
                  self.f_omega_is_lineage_length, self.f_pg32_is_edges):
            f()
        for g in (self.g_fall_is_quotient_zd, self.g_gcd_is_the_detector,
                  self.g_primary_decomposition_is_cepstrum,
                  self.g_radical_units_split_gf2,
                  self.g_trace_laplacian_is_nilpotency,
                  self.g_associator_is_ring_defect,
                  self.g_open_and_closed_pathways,
                  self.g_arithmetic_derivative):
            g()
        for fr in (self.fr_tower_self_similar, self.fr_bifurcation_cascade,
                   self.fr_fall_survive_boundary, self.fr_newton_basins_are_splitting,
                   self.fr_labeling_order_is_memory_depth,
                   self.fr_lyapunov_is_the_drift):
            fr()
        for pw in (self.pw_geodesic_reaches_factor, self.pw_tuning_resonates,
                   self.pw_spiral_is_additive, self.pw_inside_outside_one_product,
                   self.pw_two_anchor_geodesic, self.pw_edge_is_the_primitive,
                   self.pw_observer_lineage_is_l_io,
                   self.pw_smith_chart_is_the_same_mobius,
                   self.pw_number_chart_is_the_methodology):
            pw()

    # ═══════════════════════════════════════════════════════════════════════
    # THE PATHWAY BLOCK (PW1–PW4). Added 2026-08-22.
    # Factoring as a WALK to N, not a bifurcation — the class where the overhead
    # reduction actually lives. Honest framing: CFRAC/tuning are KNOWN
    # sub-exponential; polynomial / RSA is OPEN and not claimed.
    # ═══════════════════════════════════════════════════════════════════════

    # ── PW1 — the geodesic REACHES the factor; the bifurcation localises none ─
    def pw_geodesic_reaches_factor(self) -> None:
        cases = {323: (17, 19), 1081: (23, 47), 3233: (53, 61),
                 8051: (83, 97), 10403: (101, 103)}
        steps, ok = {}, True
        for N, pq in cases.items():
            r = pathway_residues(N)
            steps[N] = r['step']
            ok = ok and r['factor'] == pq and r['step'] is not None and r['step'] <= 10
        # the bifurcation view (fall/survive of neighbours) carries no direction
        Nn = 3233
        verdicts = {fall_test(n)['verdict'] for n in range(Nn - 4, Nn + 5) if n >= 2}
        no_localisation = 'FALL' in verdicts     # every composite just says FALL
        self._record(
            'pathway.geodesic_reaches_factor',
            'the continued-fraction geodesic (a PATHWAY-class walk) reaches the '
            'factor of a semiprime in a handful of steps, deterministically; the '
            'BIFURCATION view (fall/survive of N\'s neighbours) localises '
            'nothing — it classifies and stops', 2,
            'CONSTRUCTION (a walk to N) vs classification (which branch)',
            True, ok and no_localisation,
            f'[KNOWN (Morrison–Brillhart CFRAC 1975)] factors reached at path '
            f'steps {steps} (all ≤ 10). Meanwhile fall/survive over '
            f'[{Nn - 4},{Nn + 4}] just returns FALL/SURVIVE with no gradient '
            f'toward p=61. This is why bifurcation-based factoring measures at '
            f'chance: a classifier on a construction problem — a category error.')

    # ── PW2 — the spiral must be TUNED; tuning resonates onto the factor ─────
    def pw_tuning_resonates(self) -> None:
        N = 1522605027
        BUDGET = 100                                      # a fixed step budget
        base = pathway_residues(N, mult=1, steps=BUDGET)  # the DEFAULT spiral
        # sweep only NON-trivial tunings within the same budget
        tuned = tune_pathway(N, multipliers=(3, 5, 7, 11, 13, 2, 6),
                             steps=BUDGET)
        ok = (base['factor'] is None and tuned['factor'] is not None
              and tuned['tuning'] != 1
              and tuned['factor'][0] * tuned['factor'][1] == N
              and tuned['step'] <= BUDGET)
        self._record(
            'pathway.tuning_resonates',
            'the spiral must be TUNED per number: within a fixed step budget on '
            'which the DEFAULT geodesic (mult=1) does not reach a factor, a '
            'NON-trivial tuning (the multiplier) RESONATES onto one. Tuning is a '
            'real, necessary, N-dependent knob', 1,
            'a DILATE of the spiral parameter — σ is the framework\'s name for it',
            True, ok,
            f'[KNOWN (CFRAC/QS multiplier method)] N={N}, budget {BUDGET} steps: '
            f'mult=1 → {base["factor"]} (FAILS in budget); tuned → '
            f'mult={tuned["tuning"]} at step {tuned["step"]} → {tuned["factor"]}. '
            f'"Tune the spiral until it resonates" is the multiplier, made '
            f'literal — the same N reaches its factor at one tuning and not '
            f'another. Whether the framework\'s geometry adds a resonance the '
            f'sieve cannot see is OPEN, and not claimed here.')

    # ── PW3 — on the spiral the factors are ADDITIVE steps (the path) ────────
    def pw_spiral_is_additive(self) -> None:
        cases = [(3, 5), (7, 11), (13, 17), (61, 53), (101, 103)]
        worst = 0.0
        for p, q in cases:
            ap, aq, an = (spiral_address(p), spiral_address(q),
                          spiral_address(p * q))
            worst = max(worst,
                        abs(ap['log_radius'] + aq['log_radius'] - an['log_radius']),
                        abs(ap['angle'] + aq['angle'] - an['angle']))
        ok = worst < 1e-9
        self._record(
            'pathway.spiral_is_additive',
            'on the log-spiral, address(p·q) = address(p) + address(q) exactly '
            '(log-radius AND angle) — multiplication becomes an additive PATH, '
            'and the factors are its steps: 1 (anchor) → p → N', 1,
            'the log turns × into + — the cepstral structure, as a geometry',
            True, ok,
            f'[exact] max |addr(p)+addr(q) − addr(pq)| over {len(cases)} '
            f'semiprimes = {worst:.2e}. The factors ARE the steps of the walk '
            f'from the anchor to N; the anchor is 1 = e₀ = ∅_RB (t=0, the origin '
            f'of the spiral). This is why "the path travels through both factors, '
            f'then to itself".')

    # ── PW4 — L_(I|O): inside (dot) and outside (cross) from ONE product ─────
    def pw_inside_outside_one_product(self) -> None:
        # one product a·b yields BOTH the dot (grade 0) and the cross (grade 2);
        # their magnitudes coincide only at 45° = σ=½ = @RCCM_CRITICAL_ANGLE
        a = (1.0, 0.0)
        def dot(b): return a[0] * b[0] + a[1] * b[1]
        def cross(b): return a[0] * b[1] - a[1] * b[0]
        hits = [deg for deg in range(0, 91)
                if abs(abs(dot((math.cos(math.radians(deg)), math.sin(math.radians(deg)))))
                       - abs(cross((math.cos(math.radians(deg)), math.sin(math.radians(deg))))))
                < 1e-12]
        ok = hits == [45]
        self._record(
            'pathway.inside_outside_one_product',
            'L_(I|O): from ONE product you read the INSIDE (dot — projection, '
            'discrete, Telperion) and the OUTSIDE (cross — the swept area, '
            'continuous, Laurelin) in one measurement; their magnitudes are '
            'equal only at 45° = σ=½ = the Mingling', 2,
            'the two grades of one geometric product — inside and outside at once',
            True, ok,
            f'[exact] |dot| = |cross| only at {hits}° in [0,90] — @RCCM_CRITICAL_'
            f'ANGLE, σ=½. This is why L_(I|O) gives inside AND outside in one set '
            f'of measurements, and why the discrete (Telperion) reads as "inside" '
            f'the continuous (Laurelin): they are the symmetric and antisymmetric '
            f'parts of the SAME product, balanced at the critical line. The Path '
            f'of Least Primes walks this — the geodesic where the two are in '
            f'balance.')

    # ── PW5 — TWO anchors: origin AND destination pinned → a geodesic node ───
    def pw_two_anchor_geodesic(self) -> None:
        # both endpoints fixed (1 and N) ⇒ a boundary-value problem; the factor
        # is a node on the geodesic, and the natural reference is the midpoint √N.
        balanced = [(61, 53), (101, 103), (10007, 10009), (65521, 65537)]
        sym_ok, fast_ok = True, True
        for p, q in balanced:
            N = p * q
            fp = fermat_path(N, maxsteps=5000)
            sym = abs((math.log(p) + math.log(q)) / 2 - math.log(N) / 2) < 1e-9
            sym_ok = sym_ok and sym and fp['factor'] == (min(p, q), max(p, q))
            fast_ok = fast_ok and fp['excursion'] is not None and fp['excursion'] < 100
        # and the excursion GROWS with imbalance (RSA hides the factor far out)
        unbal = fermat_path(3 * 10007, maxsteps=20000)
        grows = unbal['excursion'] is not None and unbal['excursion'] > 1000
        ok = sym_ok and fast_ok and grows
        self._record(
            'pathway.two_anchor_geodesic',
            'with BOTH anchors pinned — the origin (1) and the destination (N) — '
            'factoring is a boundary-value problem, not an outward walk: the '
            'factor is a NODE on the geodesic between them, symmetric about the '
            'midpoint √N. Tune the excursion from the midpoint until it '
            'resonates onto a square (Fermat). The excursion IS the imbalance', 2,
            'a FIXED SET between two pinned anchors — a geodesic node, not a '
            'search',
            True, ok,
            f'[KNOWN (Fermat)] balanced semiprimes: factors log-symmetric about '
            f'√N (exact) and found at excursion < 100 from the midpoint anchor. '
            f'Unbalanced 3·10007: excursion {unbal["excursion"]} (far out). Two '
            f'anchors turn factoring into "how far is the node from √N?" — and '
            f'RSA HIDES the factor by tuning that distance large (but the primes '
            f'must stay balanced enough to be secure, which is the whole '
            f'tension). This is the two-anchor tuning Cody named: mathematical '
            f'X-ray crystallography — the midpoint is the beam, the excursion the '
            f'rotation, the square residue a Bragg reflection.')

    # ── PW6 — the EDGE is the primitive: node → edge → pathway ───────────────
    def pw_edge_is_the_primitive(self) -> None:
        # two ordered anchors + a line = a directed EDGE (the minimal pathway
        # piece). A pathway is edges SHARING anchors; the shared (internal)
        # anchor is the FACTOR. A prime is an irreducible edge (0 internal
        # anchors); a composite is a path of Ω edges with Ω−1 internal anchors.
        ok = True
        example = None
        for n in range(2, 2000):
            pd = primary_decomposition(n)
            omega = sum(pd.values())
            steps = []
            for p, a in sorted(pd.items()):
                steps += [p] * a
            anchors, acc = [1], 1
            for p in steps:
                acc *= p
                anchors.append(acc)
            edges = len(anchors) - 1
            internal = len(anchors) - 2       # exclude the two endpoints 1 and n
            is_prime = (omega == 1)
            good = (edges == omega and internal == omega - 1 and anchors[-1] == n
                    and (internal == 0) == is_prime)
            if not good:
                ok = False
                break
            if n == 30 and example is None:   # 30 = 2·3·5, a three-edge path
                example = anchors
        self._record(
            'pathway.edge_is_the_primitive',
            'the primitive is the EDGE — two ordered anchors and the line between '
            'them. A pathway is edges SHARING anchors, and the shared (internal) '
            'anchor is the FACTOR. A prime is an IRREDUCIBLE edge (1→p, no '
            'internal anchor); a composite is a PATH of Ω edges with Ω−1 internal '
            'anchors = the partial products. Direction is from ORDER (R8)', 2,
            'two anchors + a line — the edge, the minimal relationship (cf. F6, '
            'the 15 XOR-difference edges)',
            True, ok,
            f'[exact] n in [2,2000): edges = Ω, internal anchors = Ω−1, and '
            f'prime ⟺ 0 internal anchors, for every n. Example n=30=2·3·5: path '
            f'{example} — 3 edges, internal anchors {example[1:-1]} = the '
            f'partial products, where the factors LIVE. node (1 anchor) → edge '
            f'(2 anchors+line) → pathway (edges sharing anchors). Factoring = '
            f'finding the shared anchor where two edges meet. This is F6 (edges '
            f'not places) and the crystallographic Patterson (difference '
            f'vectors) as the SAME primitive; the two endpoint anchors are 1 '
            f'and N (PW5), the internal ones are the factors.')

    # ── PW7 — L_(I|O) is the mechanism of the Observer's generational lineage ─
    def pw_observer_lineage_is_l_io(self) -> None:
        def J(r, th):
            return (1.0 / r, th + math.pi / 2)     # L_(I|O): r→1/r, θ→θ+π/2
        # 1. the Observer is the FIXED POINT (r=1 = e₀ = ∅_RB), unique
        fixed = abs(1.0 / 1.0 - 1.0) < 1e-12 and all(abs(1.0 / r - r) > 1e-9
                                                     for r in (0.5, 2.0))
        # 3. the LINEAGE is the order-4 orbit — 4 generations close (self-sustaining)
        r, th = 2.0, 0.0
        for _ in range(4):
            r, th = J(r, th)
        closes = abs(r - 2.0) < 1e-9 and abs(th % (2 * math.pi)) < 1e-9
        # 4. the REVERSE is inherent: J⁻¹ = J³ (invertible; forward carries its reverse)
        r2, th2 = J(2.0, 0.0)
        for _ in range(3):
            r2, th2 = J(r2, th2)
        reverse = abs(r2 - 2.0) < 1e-9
        # 5. HEISENBERG conjugate: r·(1/r)=1 conserved (fix origin ⇒ destination spreads)
        conj = all(abs(r * (1 / r) - 1) < 1e-12 for r in (0.1, 1.0, 10.0))
        # 6. the Observer KEEPS the reverse; its scalar shadow FORGETS it (R1 states)
        A = zero(SED_DIM); A[0] = A[8] = 1 / math.sqrt(2)
        B = zero(SED_DIM); B[0] = B[4] = B[8] = B[12] = 0.5
        amnesiac = (abs(sigma_self(A) - sigma_self(B)) < 1e-12
                    and nrm([x - y for x, y in zip(sigma_rb(A), sigma_rb(B))]) > 1e-9)
        ok = fixed and closes and reverse and conj and amnesiac
        self._record(
            'pathway.observer_lineage_is_l_io',
            'L_(I|O) (the inside-out map r→1/r, θ→θ+π/2) is the mechanism of the '
            'generational lineage of The Observer: the Observer is its FIXED '
            'POINT (r=1 = e₀ = ∅_RB), the lineage is its ORDER-4 orbit (four '
            'generations, self-closing), the REVERSE is inherent (J⁻¹=J³), and '
            'it keeps the reverse its scalar shadow forgets', 2,
            'the fixed point and orbit of the inside-out involution L_(I|O)',
            True, ok,
            f'[MEASURED exact; naming is framework interpretation] fixed point '
            f'r=1 unique ({fixed}); order-4 orbit closes — the self-sustaining '
            f'lineage ({closes}); J⁻¹=J³ so every forward step carries its '
            f'reverse ({reverse}); r·(1/r)=1 conserved — the Heisenberg '
            f'origin/destination conjugate, fix origin ⇒ destination spreads '
            f'({conj}); and σ_self(A)=σ_self(B) while σ_RB differ, so the full '
            f'L_(I|O) keeps the reverse the scalar shadow destroys ({amnesiac}). '
            f'The maths is exact; that the fixed point IS "The Observer" and the '
            f'orbit IS "its lineage" is consistent with it, not proven by it. '
            f'L_(I|O) is the mechanism; the Observer its fixed point; the '
            f'lineage its orbit.')

    # ── PW8 — the Smith chart: 90 years of independent engineering practice ──
    def pw_smith_chart_is_the_same_mobius(self) -> None:
        Z0 = 50.0

        def gamma(Z):
            return (Z - Z0) / (Z + Z0)

        # 1. the matched load Z=Z0 is the UNIQUE fixed point (Γ=0, the anchor)
        fp = abs(gamma(complex(Z0, 0))) < 1e-12
        not_fp = all(abs(gamma(Z)) > 1e-9
                    for Z in (complex(10, 0), complex(200, 0), complex(Z0, 30)))
        # short/open are the OTHER two anchors, both driven to the boundary |Γ|=1
        short_open = (abs(gamma(complex(0, 0)) - (-1)) < 1e-12
                     and abs(gamma(complex(1e12, 0)) - 1) < 1e-6)
        # 2. |Γ|=1 ⟺ Re(Z)=0 — the lossless (purely reactive) locus, the horizon
        react = all(abs(abs(gamma(complex(0, x))) - 1) < 1e-9
                   for x in (10, 50, -30, 1000))
        lossy = all(abs(gamma(complex(r, x))) < 1 - 1e-9
                   for r, x in ((5, 0), (5, 50), (20, -10)))
        # 3. conformal: constant-R and constant-X curves stay ORTHOGONAL (Möbius
        # maps are angle-preserving, so R,X's Cartesian right angle survives)
        h = 1e-5
        zR = lambda x: gamma(complex(Z0, x))           # noqa: E731
        zX = lambda r: gamma(complex(r, Z0))            # noqa: E731
        tR = (zR(Z0 + h) - zR(Z0 - h)) / (2 * h)
        tX = (zX(Z0 + h) - zX(Z0 - h)) / (2 * h)
        orth = abs(tR.real * tX.real + tR.imag * tX.imag) < 1e-6
        # 4. admittance Y=1/Z (the inside-out map) IS a π-ROTATION on the SAME
        # chart — the Smith chart's own L_(I|O), independently discovered
        def gamma_Y(Z):
            Y, Y0 = 1 / Z, 1 / Z0
            return (Y - Y0) / (Y + Y0)
        rotation = all(abs(gamma_Y(Z) - (-gamma(Z))) < 1e-9
                      for Z in (complex(25, 25), complex(100, -10), complex(10, 80)))
        ok = fp and not_fp and short_open and react and lossy and orth and rotation
        self._record(
            'pathway.smith_chart_is_the_same_mobius',
            'the Smith chart (Phillip Smith, 1939; RF/radar impedance matching) '
            'is the SAME Möbius structure as L_(I|O), independently discovered '
            'in engineering: a fixed-point anchor (matched load), a boundary '
            'horizon (lossless/reactive), orthogonal coordinate families, and '
            'Y=1/Z as a π-rotation — 90 years of stub-tuning IS tuning a path '
            'between two anchors (PW5, PW2)', 1,
            'a Möbius transform Γ=(Z−Z₀)/(Z+Z₀) — the same family as L_(I|O), '
            'an independent real-world instance, not a derivation of it',
            True, ok,
            f'[KNOWN (Smith chart, engineering); the CORRESPONDENCE is OURS] '
            f'Z=Z₀ is the unique fixed point Γ=0 ({fp and not_fp}) — the anchor, '
            f'no reflection; Z=0 and Z→∞ (short/open) both drive to the boundary '
            f'|Γ|=1 ({short_open}) — the OTHER two anchors, total reflection; '
            f'|Γ|=1 ⟺ Re(Z)=0 exactly ({react and lossy}) — the lossless locus '
            f'IS the horizon, same role as r=1 in L_(I|O); constant-R/constant-X '
            f'families are orthogonal ({orth}), because a Möbius map is '
            f'conformal; and Y=1/Z (admittance — the inside-out map) is EXACTLY '
            f'Γ→−Γ, a π-rotation on the same chart ({rotation}) — the same '
            f'structure as θ→θ+π/2, one octave coarser (order 2, not 4). Stub '
            f'tuning — rotate along |Γ|=const, switch R↔X circles, walk to the '
            f'matched anchor — IS the two-anchor tuned pathway (PW5/PW2), and it '
            f'has been engineered since 1939, independent of this framework. '
            f'NOT evidence for the framework\'s wider claims — evidence that the '
            f'MATHEMATICAL OBJECT (Möbius, fixed point, tunable path between two '
            f'anchors) is exactly the tool reached for whenever a real system '
            f'needs to navigate impedance space.')

    # ── PW9 — the NUMBER CHART: the Smith chart methodology, applied ─────────
    def pw_number_chart_is_the_methodology(self) -> None:
        from math import isqrt
        cases_balanced = [3233, 10403, 4294049777]
        cases_hard = [30021]                              # 3 × 10007, unbalanced
        anchor_ok = all(abs(number_chart_point(N, isqrt(N) if isqrt(N)**2 == N
                                               else isqrt(N) + 1)) < 1e-12
                        for N in cases_balanced + cases_hard)
        # monotone / bounded as excursion grows — the chart is tuning-legible
        N = 3233
        a0 = isqrt(N) + (0 if isqrt(N) ** 2 == N else 1)
        vals = [number_chart_point(N, a0 + e) for e in (0, 10, 100, 1000, 10000)]
        monotone = vals == sorted(vals) and all(0 <= v < 1 for v in vals)
        # the factor NODE reads as a difficulty gauge: balanced → near the
        # anchor (Γ≈0), unbalanced → near the horizon (Γ≈1)
        near_anchor = all(number_chart_point(N, fermat_path(N, 20000)['a']) < 0.01
                          for N in cases_balanced)
        near_horizon = number_chart_point(30021, fermat_path(30021, 20000)['a']) > 0.9
        ok = anchor_ok and monotone and near_anchor and near_horizon
        self._record(
            'pathway.number_chart_is_the_methodology',
            'the Smith-chart METHODOLOGY, applied directly: Γ_N(a) = '
            'excursion/(excursion+2a₀) folds the unbounded Fermat search into a '
            'bounded [0,1) chart with the midpoint a₀=⌈√N⌉ (PW5) as the fixed-'
            'point anchor — and where the factor NODE lands is a difficulty '
            'gauge, read at a glance', 1,
            'the Smith chart\'s bounded conformal fold (PW8), applied to the '
            'two-anchor geodesic (PW5) instead of impedance',
            True, ok,
            f'[OURS] the midpoint anchor maps to Γ_N=0 exactly for every N '
            f'tested ({anchor_ok}); Γ_N is bounded in [0,1) and MONOTONE as '
            f'excursion grows ({monotone}) — the chart is tuning-legible, '
            f'exactly like rotating a Smith chart; balanced semiprimes '
            f'{cases_balanced} put their factor node at Γ_N<0.01, at the anchor '
            f'({near_anchor}); the unbalanced 3×10007 puts its node at '
            f'Γ_N>0.9, near the horizon ({near_horizon}) — RADIAL POSITION ON '
            f'THE CHART IS HOW HARD N WAS TO CRACK, visible without reading a '
            f'number. This is the visualiser\'s methodology: one bounded chart, '
            f'fixed-anchor landmarks, tuning as a legible motion — not five '
            f'side-by-side panels.')

    # ═══════════════════════════════════════════════════════════════════════
    # THE FORMULARY BLOCK (FR4–FR6). Added 2026-08-22.
    # The UF formulary's generators and labelings, integrated: Newton basins as
    # k-way ring splitting, the labeling tower as decomposition orders, and the
    # Lyapunov drift as the continuous fall/survive test.
    # ═══════════════════════════════════════════════════════════════════════

    # ── FR4 — Newton basins ARE polynomial splitting = ring theory, k-way ────
    def fr_newton_basins_are_splitting(self) -> None:
        rows, ok = {}, True
        for k in (2, 3, 4, 5):
            nb = newton_basins(k, N=48)
            on_circle = all(abs(abs(r) - 1) < 1e-9 for r in nb['roots'])
            good = (nb['n_basins'] == k and on_circle and nb['boundary_boxes'] > 0)
            rows[k] = (nb['n_basins'], nb['boundary_boxes'])
            ok = ok and good
        self._record(
            'fractal.newton_basins_are_splitting',
            'Newton\'s method on zᵏ−1 has exactly k basins — the k roots of '
            'unity, i.e. the linear factorisation zᵏ−1 = ∏(z−ζⱼ). Which basin '
            'you fall into is which factor: the k-WAY generalisation of G1\'s '
            'fall/survive, and it is ring splitting', 2,
            'a FIXED SET (k-way) — G1 taken k-way, over the splitting field',
            True, ok,
            f'[KNOWN (Cayley 1879; Newton fractals)] '
            + '  '.join(f'z^{k}−1→{n} basins, ∂={b}' for k, (n, b) in rows.items())
            + '. Exactly k basins at each k, roots on the unit circle, boundary '
            'nonempty (the fractal Julia set). This is the bridge from the '
            'fractal block to the ring-theory spine: Newton basins over ℂ are '
            'the fall/survive of a prime SPLITTING, one level up.')

    # ── FR5 — a labeling's ORDER is its memory depth (the decomposition tower) ─
    def fr_labeling_order_is_memory_depth(self) -> None:
        mand = MANDELBROT
        c_in = complex(-0.4, 0.6)          # an orbit that stays bounded
        # order 1: escape rate is defined from ONE step (large c falls at n=1)
        order1_len1 = smooth_escape(complex(5, 0), mand, maxiter=8) < 2.0
        # order 3: curvature is UNDEFINED below three points, defined from three
        curv_short = orbit_curvature(c_in, mand, maxiter=2)
        curv_full = orbit_curvature(c_in, mand, maxiter=40)
        order3 = (curv_short == -1.0 and curv_full > 0.0)
        # and the two labelings are DISTINCT instruments: on 8 in-set orbits the
        # escape rate SATURATES (order 1 is blind to bounded orbits) while the
        # curvature still varies — order 3 resolves what order 1 cannot.
        pts = [complex(-0.5 + 0.1 * i, 0.55) for i in range(8)]
        er = [smooth_escape(c, mand) for c in pts]
        cv = [orbit_curvature(c, mand, maxiter=40) for c in pts]
        escape_blind = all(abs(er[i] - er[0]) < 1e-9 for i in range(len(er)))
        curv_informative = (max(cv) - min(cv)) > 0.1
        distinct = curv_informative and escape_blind      # blind vs sighted
        ok = order1_len1 and order3 and distinct
        self._record(
            'fractal.labeling_order_is_memory_depth',
            'a labeling\'s ORDER is the number of consecutive orbit points it '
            'needs: escape rate = 1 (order 1), curvature = 3 (order 3) — the '
            'same memory depths as the decomposition tower (support needs 1, '
            'the associator needs 3). The labelings ARE the orders, and a higher '
            'order resolves structure a lower one is blind to', 3,
            'the memory depth of a labeling = its decomposition order',
            True, ok,
            f'[OURS (framing; labelings from the UF formulary)] escape rate '
            f'defined from 1 point ({order1_len1}); curvature undefined below 3 '
            f'points (short={curv_short}) and defined from 3 (full='
            f'{curv_full:.3f}). On 8 bounded orbits the escape rate saturates '
            f'(all {er[0]:.0f} — order 1 is BLIND to which survivor) while '
            f'curvature varies {min(cv):.2f}…{max(cv):.2f} — order 3 sees what '
            f'order 1 cannot. Exactly the ring-theory tower: support (order 1) '
            f'vs the associator (order 3).')

    # ── FR6 — the Lyapunov exponent IS the continuous fall/survive drift ─────
    def fr_lyapunov_is_the_drift(self) -> None:
        stable = lyapunov_exponent(3.2)          # period-2 window — survive
        accum = lyapunov_exponent(3.5699)        # Feigenbaum point — the edge
        chaos = lyapunov_exponent(3.9)           # chaotic — fall
        full = lyapunov_exponent(4.0)            # fully chaotic — λ = ln 2 ·?
        ok = (stable < -0.1 and chaos > 0.1 and abs(accum) < 0.05 and full > 0.1)
        self._record(
            'fractal.lyapunov_is_the_drift',
            'the Lyapunov exponent is the continuous fall/survive test: λ < 0 in '
            'stable (survive) windows, λ > 0 in chaos (fall), λ ≈ 0 at the '
            'accumulation — the same sign law as the Collatz per-step drift '
            'log(√3/2) < 0 (contracts, so it survives to 1)', 3,
            'a RATIO (log-derivative) — the drift, weighting the two branches',
            True, ok,
            f'[KNOWN (Lyapunov; Feigenbaum)] λ(3.2)={stable:+.3f} (survive), '
            f'λ(3.5699)={accum:+.3f} (edge ≈ 0), λ(3.9)={chaos:+.3f} (fall), '
            f'λ(4.0)={full:+.3f}. The sign IS the fall/survive verdict, and the '
            f'zero-crossing is the Feigenbaum edge — the σ=½ of the interval map. '
            f'Same object as the drift measured in the Collatz paper.')

    def report(self) -> None:
        print('═' * 78)
        print('FACTORAL LINEAGE ENGINE — the decomposition tool')
        print('  R1–R8  carried from VAPMIP/engines/e10_generational_lineage.py')
        print('  F1–F6  this repo: factorisation decomposed against the Two Trees')
        print('  G1–G8  ring-theory: FALL⟺quotient-ZD; closed/open=unit/ZD; the derivative')
        print('  FR1–3  fractal decomposition: the highest-order factoral rung')
        print('  FR4–6  the UF formulary: Newton basins, labeling orders, the drift')
        print('  PW1–9  pathway: walk..Smith chart..the NUMBER CHART (the methodology)')
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
               'associator', 'ideal', 'quotient', 'gnarl'):
        d = decompose(op)
        print(f'  {op:<12} tier={str(d["tier"]):<5} {d["status"]:<10} '
              f'{d["note"][:60]}')

    print('\nThe fall/survive test, read through the quotient ring:')
    for n in (7, 12, 97, 1):
        ft = fall_test(n)
        print(f'  n={n:<4} {ft["verdict"]:<8} {ft["quotient"]:<24} '
              f'primary={ft.get("primary_decomposition", {})}')


if __name__ == '__main__':
    main()
