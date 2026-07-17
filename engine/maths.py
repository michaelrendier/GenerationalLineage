"""
SedenionFactorialRelativity.engine.maths
==========================================
Core pieces and pathways for the Fermat facet of H_hat_RB (the Zero
Lattice tree, `AbrikosovTree/engine/telperion_engine.py`), plus the first
honest control test against the Riemann facet — real prime counts by
residue class, checked against Dirichlet equidistribution, which is what
the zeta zeros of L(s,chi) actually govern (see module docstring in
telperion_engine.py: "Oscillations in pi(x;16,k) are driven by zeros of
Dirichlet L-functions L(s,chi). These zeros ARE the spectral nodes of the
Zero Tree" -- stated there, never wired to real data until this file).

NOT a new mechanism reimplemented from scratch: this module IMPORTS the
real telperion_engine.py and h_rb_hat/maths.py code directly. Nothing
here duplicates their logic.

THE CONTROL, stated plainly (Cody, 2026-07-17): "the Zeta Function is the
Control. it is the authoritative maths for the order the primes grow."
Concretely: Dirichlet's theorem on primes in arithmetic progressions says
primes are asymptotically equidistributed among the phi(16)=8 residue
classes coprime to 16 -- {1,3,5,7,9,11,13,15}. That equidistribution is
itself governed by the zeros of the relevant Dirichlet L-functions (GRH
territory). So: does the geometric tree's own structural grouping of
those 8 classes (5 Niemeier-covered "dendritic" shapes vs the 3-shape
Monster gap {1,11,15}) show any real, honest deviation from that
equidistributed control in actual prime counts -- or is the geometric
grouping invisible to the real density, the same AT-CHANCE question every
other engine this session was held to?

STATUS: v1. This wires up the real inventory and runs ONE honest test
(Monster-gap density vs non-gap density, against Dirichlet
equidistribution). It does NOT yet implement a full "Riemann N-Holes"
read-off condition -- that design question (what, structurally, would a
prime's OWN zeta-zero relationship "fall" against, the way a composite's
factor pair falls at k=4) is still open, flagged honestly, not glossed
over.

Author:  Claude, at Cody's direction -- 2026-07-17
White Hat. No free parameters. Failed predictions stay in the record.
"""

import os
import sys
import math
from typing import Dict, List, Any

# ── Reach the real, existing engines directly -- no reimplementation ──────────

_THEPLACE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_ABRIKOSOV_ENGINE = os.path.join(_THEPLACE, 'AbrikosovTree', 'engine')
_H_RB_HAT_MODULE = os.path.join(_THEPLACE, 'AinulindaleBAK', 'ValaQuenta', 'modules', 'h_rb_hat')
# telperion_engine.py's OWN _FERMAT_DIR computation assumes it is nested one
# directory deeper than it actually is (expects .../FourthAgePapers/AbrikosovTree/
# engine/, but it actually lives at ThePlace/AbrikosovTree/engine/ directly) --
# a pre-existing path bug in that file, not touched here. Inserting the real
# location ourselves so the import resolves regardless.
_FERMAT_MONSTER_ENGINE = os.path.join(_THEPLACE, 'FourthAgePapers', 'FermatMonster', 'engine')
_TURINGSTACK = os.path.join(_THEPLACE, 'TuringStack')
sys.path.insert(0, _ABRIKOSOV_ENGINE)
sys.path.insert(0, _H_RB_HAT_MODULE)
sys.path.insert(0, _FERMAT_MONSTER_ENGINE)
sys.path.insert(0, _TURINGSTACK)

from telperion_engine import (  # noqa: E402
    prime_sieve, classify_prime, cd_level_data, full_tower, prime_tower_path,
    N_LEVELS, FIRST_ZD_LEVEL, PRIME_SECTOR, NIEMEIER_GAP, LEECH_SHAPE,
    ZD_CONSTELLATIONS_ODD, MOONSHINE_PRIMES, CD_NAMES,
)
from maths import RIEMANN_ZEROS, SIGMA_CRITICAL, SIGMA_FORBIDDEN  # noqa: E402  (h_rb_hat/maths.py)
from udeo_poc import CayleyDickson  # noqa: E402


# ══════════════════════════════════════════════════════════════════════════
# ROOT-REGION SATURATION — does the nilpotent (zero) outcome start to
# DOMINATE the involutory (e0) outcome soon past T_256, and if so, at what
# rate? Cody, 2026-07-17: "not at t_256, but soon after the dominant
# appearance in the root is zeros...it's a xeno's paradoxical halfing...
# the bifurcation tree branches" -- testing whether the GAP to full
# nilpotent dominance (1 - nilpotent_fraction) halves at each dimension
# doubling (each bifurcation level), the way Zeno's paradox halves the
# remaining distance at each step.
# ══════════════════════════════════════════════════════════════════════════

import random as _random


def nilpotent_fraction_at_dim(dim: int, n_samples: int = 30, seed: int = 20260717) -> float:
    """Fraction of random dim-bit integers, embedded in T_dim/GF(2), that
    are nilpotent (x^2=0) rather than involutory (x^2=e0). Reuses
    CayleyDickson('gf2') unchanged from udeo_poc.py -- the same exact
    Frobenius-theorem machinery, no reimplementation."""
    cd = CayleyDickson(dim, 'gf2')
    rng = _random.Random(seed + dim)
    nilp = 0
    for _ in range(n_samples):
        bits = [rng.randint(0, 1) for _ in range(dim)]
        sq = cd.multiply(bits, bits)
        if cd.is_zero(sq):
            nilp += 1
    return nilp / n_samples


def root_region_saturation(dims: List[int] = None, n_samples: int = 30) -> List[Dict[str, Any]]:
    """Nilpotent fraction at increasing CD dimensions past T_256, and the
    'gap' (1 - fraction) at each, to check the halving-at-each-doubling
    conjecture directly against real numbers."""
    if dims is None:
        dims = [256, 512, 1024, 2048]
    rows = []
    prev_gap = None
    for d in dims:
        frac = nilpotent_fraction_at_dim(d, n_samples)
        gap = 1.0 - frac
        ratio = (gap / prev_gap) if prev_gap and prev_gap > 0 else None
        rows.append({'dim': d, 'nilpotent_fraction': round(frac, 4),
                      'gap_to_full_dominance': round(gap, 4),
                      'gap_ratio_vs_prev_dim': round(ratio, 4) if ratio is not None else None})
        prev_gap = gap
    return rows


# ══════════════════════════════════════════════════════════════════════════
# QUANTIZED PIECES — the discrete inventory, "below ground"
# ══════════════════════════════════════════════════════════════════════════

def quantized_pieces() -> Dict[str, Any]:
    """The finite, countable structural objects in play. Nothing computed
    here -- this is the inventory, read directly off the imported engines."""
    return {
        'cd_tower_levels': N_LEVELS,                       # 9, k=0..8
        'leaf_level':       0,                              # ℝ, "The Unit" -- exact, singular
        'root_level_start': 8,                              # T_256 AND ABOVE (k>=8) -- a
                                                              # region, not a point: structure
                                                              # saturates past here (Frobenius
                                                              # theorem), further doubling adds
                                                              # no new distinguishable boundary
        'first_zd_level':   FIRST_ZD_LEVEL,                 # 4, 𝕊 -- Fermat extinction threshold
        'n_shapes':         16,                              # p mod 16
        'prime_sector':     sorted(PRIME_SECTOR),           # 8 odd N-shapes
        'niemeier_gap':     sorted(NIEMEIER_GAP),           # {1,11,15} -- Monster gap
        'leech_shape':      LEECH_SHAPE,                    # 0 -- tap root, no root system
        'dendritic_shapes': sorted(PRIME_SECTOR - NIEMEIER_GAP),  # {3,5,7,9,13} -- Niemeier-covered
        'zd_constellations_odd': ZD_CONSTELLATIONS_ODD,     # 12 canonical 4-tuples
        'n_riemann_zeros_on_file': len(RIEMANN_ZEROS),      # 20, LMFDB/Odlyzko
        'sigma_critical_h_rb_hat': SIGMA_CRITICAL,          # 0.5 -- Riemann facet, global scale
        'sigma_forbidden_h_rb_hat': SIGMA_FORBIDDEN,        # 0.0 -- Fermat facet, global scale
    }


# ══════════════════════════════════════════════════════════════════════════
# QUANTIZED PATHWAYS — the discrete routes through the pieces
# ══════════════════════════════════════════════════════════════════════════

def pathway_leaf_to_root(p: int) -> Dict[str, Any]:
    """The one walk that already exists end to end: a prime's real
    9-level path from k=0 (leaf) to k=8 (root), reused unchanged from
    telperion_engine.py."""
    return prime_tower_path(p)


def pathway_root_system_class(p: int) -> Dict[str, Any]:
    """Which root-system pathway (dendritic / tap / gap) a prime's
    N-shape converges onto -- the 'clonal' grouping."""
    cls = classify_prime(p)
    ns = cls['nshape']
    if ns == LEECH_SHAPE:
        branch = 'tap_root'         # Leech -- no root system, the center axis
    elif ns in NIEMEIER_GAP:
        branch = 'monster_gap'      # {1,11,15} -- unreachable by A/D/E, filled by Monster+siblings
    elif ns in PRIME_SECTOR:
        branch = 'dendritic'        # Niemeier A/D/E-type root system
    else:
        branch = 'even_niemeier'
    cls['root_pathway'] = branch
    return cls


# ══════════════════════════════════════════════════════════════════════════
# THE CONTROL — real prime counts by residue class, vs Dirichlet equidistribution
# ══════════════════════════════════════════════════════════════════════════

def pi_x_mod16(N: int) -> Dict[int, int]:
    """Real, counted pi(x;16,k) for every residue class k in [0,16), primes
    up to N. This is the actual data the zeta zeros of L(s,chi) govern --
    not a hash, not an embedding, an exact sieve count."""
    primes = prime_sieve(N)
    counts = {k: 0 for k in range(16)}
    for p in primes:
        counts[p % 16] += 1
    return counts


def equidistribution_control_test(N: int = 200_000) -> Dict[str, Any]:
    """
    THE CONTROL TEST. Dirichlet's theorem: primes are asymptotically
    equidistributed among the phi(16)=8 classes coprime to 16 -- each of
    {1,3,5,7,9,11,13,15} should carry ~1/8 of all primes as N grows. That
    equidistribution IS the zeta-governed order Cody named as the control.

    Question: does the geometric tree's own grouping -- the 3-shape
    Monster gap {1,11,15} (unreachable by any Niemeier root system) vs the
    5-shape Niemeier-covered set {3,5,7,9,13} -- show any REAL deviation
    from equidistribution in actual counted primes? If the gap shapes are
    structurally special (per the tree's own claim, they're the shapes
    'not even regular algebraic structure can describe'), a real density
    difference there would be the first honest signal. If not, the
    geometric distinction is invisible to the real order primes grow in,
    the same AT-CHANCE finding as everywhere else this session.
    """
    counts = pi_x_mod16(N)
    odd_classes = sorted(PRIME_SECTOR)
    total_odd = sum(counts[k] for k in odd_classes)
    expected_per_class = total_odd / len(odd_classes)

    gap_count = sum(counts[k] for k in NIEMEIER_GAP)
    dendritic_count = sum(counts[k] for k in (PRIME_SECTOR - NIEMEIER_GAP))
    expected_gap = expected_per_class * len(NIEMEIER_GAP)
    expected_dendritic = expected_per_class * len(PRIME_SECTOR - NIEMEIER_GAP)

    # Pearson chi-square across all 8 odd classes vs uniform (Dirichlet) expectation
    chi_sq = sum((counts[k] - expected_per_class) ** 2 / expected_per_class for k in odd_classes)
    dof = len(odd_classes) - 1  # 7

    gap_deviation_pct = 100.0 * (gap_count - expected_gap) / expected_gap if expected_gap else 0.0
    dendritic_deviation_pct = (100.0 * (dendritic_count - expected_dendritic) / expected_dendritic
                                if expected_dendritic else 0.0)

    return {
        'N': N,
        'total_odd_class_primes': total_odd,
        'counts_per_class': {k: counts[k] for k in odd_classes},
        'expected_per_class_if_equidistributed': round(expected_per_class, 2),
        'chi_square': round(chi_sq, 4),
        'degrees_of_freedom': dof,
        'monster_gap_shapes': sorted(NIEMEIER_GAP),
        'monster_gap_count': gap_count,
        'monster_gap_expected': round(expected_gap, 2),
        'monster_gap_deviation_pct': round(gap_deviation_pct, 3),
        'dendritic_shapes': sorted(PRIME_SECTOR - NIEMEIER_GAP),
        'dendritic_count': dendritic_count,
        'dendritic_expected': round(expected_dendritic, 2),
        'dendritic_deviation_pct': round(dendritic_deviation_pct, 3),
    }
