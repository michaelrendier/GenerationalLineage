"""
SedenionFactoralRelativity.engine.ping
=======================================
THE EMERGER-LINEAGE UNIFICATION  --  ping 0 from a modulus.

    "can we ping 0 from a Modulus?"                -- Cody, 2026-09-01
    "using the RSA hardness counter-operators ... will it draw a path
     from modulus to 0 along a bifurcation?"

Two structural hop axes, merged:

    OPERATOR HOP   (descent -- Generational Lineage / lineage.py)
        the RSA HARDNESS COUNTER-OPERATORS. One per hardness, each also a
        point on TuringStack/references/logistic_bifurcation_RSA.png v2:
          Fermat            <-  p ~ q          (the pitchfork)
          trial division    <-  q small        (the floor branch)
          Pollard p-1       <-  p-1 smooth
          Williams p+1      <-  p+1 smooth
          ECM               <-  a mid-size factor
          Wiener (CF e/N)   <-  d small        (needs the public exponent e)
          Coppersmith/LLL   <-  half the bits of p known   (stub -- note only)
          batch GCD         <-  a shared prime across a corpus
          GNFS / Shor       <-  none of the above          (the floor)

    BRACKET HOP    (ascent -- The Emerger / emerger.py)
        bracket N's 16-vector embedding five ways in sigma_RB firing order.
        Needs NO factors -- it runs free on any modulus.

`ping(N)` hops through the counter-operators permutatively (all orders, to a
budget). It returns 0_RB -- i.e. factors N -- IFF N sits in one broken
regime. For a properly generated RSA modulus none fire and it returns the
GNFS/Shor floor. The bracket-hop structural map comes back either way.

THE COUNTER-OPERATOR LAPLACIAN.  `counter_operator_laplacian()` builds the
graph of counter-operators (edge = "counters an adjacent regime" or "can hand
off to"), returns L = D - A, its spectrum, and the Fiedler cut. L is
SYMMETRIC, so its spectrum is permutation-invariant: **the verdict is
order-independent; only the schedule (which probes fire before the one that
works) is order-sensitive.** An order-independent Laplacian is a CLASSIFIER,
not a pathfinder -- it tells you which regime, never the factorisation.

THE FLAT DIAGRAM.  The bifurcation diagram is a 2-D projection. On it, N's
column shows ~pi(sqrt N)^2 apparent p x q meetings; exactly ONE is a real
crossing (pq = N), the rest are PASSES (two prime branches overlapping in
projection, pq != N). The distinguishing coordinate is the projected-out
DEPTH -- the product value, equivalently ln(q/p), the palindrome centre, the
erased coordinate. Reconstructing depth for the apparent crossings IS the
operator hop = factoring. `flat_diagram_depth_note(N)` states this per N.

stdlib + numpy.  Every number is CALCULATED and reproducible.
"""
from __future__ import annotations

import math
import random
from fractions import Fraction
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

try:
    from .lineage import factor_lineage
except Exception:                                   # noqa: BLE001
    factor_lineage = None
try:
    from .emerger import emerge, coerce_vec
except Exception:                                   # noqa: BLE001
    emerge = coerce_vec = None


# ======================================================================
#  small number theory
# ======================================================================

def _is_probable_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _primes_upto(b: int) -> List[int]:
    if b < 2:
        return []
    sieve = bytearray([1]) * (b + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(b ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [i for i in range(2, b + 1) if sieve[i]]


def _split(n: int, d: int) -> Optional[Tuple[int, int]]:
    if d and 1 < d < n and n % d == 0:
        return (d, n // d) if d <= n // d else (n // d, d)
    return None


# ======================================================================
#  the RSA-hardness counter-operators
# ======================================================================

def op_trial_division(N: int, B: int = 1 << 20, **_) -> Dict[str, Any]:
    """<- q small.  The floor branch of the bifurcation."""
    for p in _primes_upto(min(B, math.isqrt(N) + 1)):
        if N % p == 0:
            return {'fired': True, 'factors': _split(N, p), 'work': p,
                    'regime': 'q small (trial-divisible)'}
    return {'fired': False, 'work': B}


def op_fermat(N: int, k: int = 1 << 16, **_) -> Dict[str, Any]:
    """<- p ~ q.  The pitchfork (r = 3).  N = a^2 - b^2."""
    a = math.isqrt(N)
    if a * a < N:
        a += 1
    for i in range(k):
        b2 = a * a - N
        b = math.isqrt(b2)
        if b * b == b2:
            return {'fired': True, 'factors': _split(N, a - b), 'work': i + 1,
                    'regime': 'p ~ q (Fermat: |p-q| small)'}
        a += 1
    return {'fired': False, 'work': k}


def op_pollard_p_minus_1(N: int, B: int = 100000, **_) -> Dict[str, Any]:
    """<- p-1 smooth.  gcd(a^(k!) - 1, N)."""
    a = 2
    for p in _primes_upto(B):
        pk = p
        while pk * p <= B:
            pk *= p
        a = pow(a, pk, N)
        g = math.gcd(a - 1, N)
        if 1 < g < N:
            return {'fired': True, 'factors': _split(N, g), 'work': p,
                    'regime': 'p-1 smooth (Pollard p-1)'}
        if g == N:
            break
    return {'fired': False, 'work': B}


def op_williams_p_plus_1(N: int, B: int = 50000, **_) -> Dict[str, Any]:
    """<- p+1 smooth.  Lucas sequence V_k."""
    for A in (3, 5, 7, 9):
        v0, v1 = 2, A % N
        for p in _primes_upto(B):
            pk = p
            while pk * p <= B:
                pk *= p
            # Lucas-V ladder for multiplier pk
            m = pk
            x, y = v0, v1
            bits = bin(m)[2:]
            u, w = 2, A % N
            for bit in bits:
                if bit == '1':
                    u = (u * w - A) % N
                    w = (w * w - 2) % N
                else:
                    w = (u * w - A) % N
                    u = (u * u - 2) % N
            g = math.gcd(u - 2, N)
            if 1 < g < N:
                return {'fired': True, 'factors': _split(N, g), 'work': p,
                        'regime': 'p+1 smooth (Williams p+1)'}
            if g == N:
                break
    return {'fired': False, 'work': B}


def op_ecm(N: int, curves: int = 60, B1: int = 20000, seed: int = 1, **_) -> Dict[str, Any]:
    """<- a mid-size factor.  Minimal Lenstra ECM (stage 1)."""
    rng = random.Random(seed)
    primes = _primes_upto(B1)

    def add(P, Q, a, n):
        if P is None:
            return Q
        if Q is None:
            return P
        (x1, y1), (x2, y2) = P, Q
        if x1 == x2 and (y1 + y2) % n == 0:
            return None
        if P != Q:
            num, den = (y2 - y1) % n, (x2 - x1) % n
        else:
            num, den = (3 * x1 * x1 + a) % n, (2 * y1) % n
        g = math.gcd(den, n)
        if g > 1:
            raise ValueError(g)
        m = num * pow(den, -1, n) % n
        x3 = (m * m - x1 - x2) % n
        y3 = (m * (x1 - x3) - y1) % n
        return (x3, y3)

    def mul(k, P, a, n):
        R, Q = None, P
        while k:
            if k & 1:
                R = add(R, Q, a, n)
            Q = add(Q, Q, a, n)
            k >>= 1
        return R

    for c in range(curves):
        x0, y0, a = rng.randrange(N), rng.randrange(N), rng.randrange(N)
        P = (x0, y0)
        try:
            for p in primes:
                pk = p
                while pk * p <= B1:
                    pk *= p
                P = mul(pk, P, a, N)
                if P is None:
                    break
        except ValueError as gv:
            g = int(gv.args[0])
            if 1 < g < N:
                return {'fired': True, 'factors': _split(N, g), 'work': c + 1,
                        'regime': 'mid-size factor (ECM)'}
    return {'fired': False, 'work': curves}


def op_wiener(N: int, e: Optional[int] = None, **_) -> Dict[str, Any]:
    """<- d small.  Continued fraction of e/N (needs the public exponent)."""
    if e is None:
        return {'fired': False, 'work': 0, 'note': 'needs the public exponent e'}
    # convergents of e/N
    a, b = e, N
    conv = []
    p0, p1, q0, q1 = 0, 1, 1, 0
    while b:
        q = a // b
        a, b = b, a - q * b
        p0, p1 = p1, q * p1 + p0
        q0, q1 = q1, q * q1 + q0
        k, dg = p1, q1                        # e*dg = 1 + k*phi
        if k == 0:
            continue
        if (e * dg - 1) % k:
            continue
        phi = (e * dg - 1) // k
        s = N - phi + 1                       # p + q
        disc = s * s - 4 * N
        if disc >= 0:
            t = math.isqrt(disc)
            if t * t == disc and (s + t) % 2 == 0:
                p = (s + t) // 2
                r = _split(N, p)
                if r:
                    return {'fired': True, 'factors': r, 'work': len(conv) + 1,
                            'regime': 'd small (Wiener / continued fractions)'}
        conv.append(q)
    return {'fired': False, 'work': len(conv)}


def op_batch_gcd(N: int, corpus: Optional[List[int]] = None, **_) -> Dict[str, Any]:
    """<- a shared prime across keys (poor RNG)."""
    if not corpus:
        return {'fired': False, 'work': 0, 'note': 'needs a corpus of moduli'}
    for M in corpus:
        if M == N:
            continue
        g = math.gcd(N, M)
        if 1 < g < N:
            return {'fired': True, 'factors': _split(N, g), 'work': 1,
                    'regime': 'shared prime (batch GCD)'}
    return {'fired': False, 'work': len(corpus)}


def op_coppersmith(N: int, known_high_bits: Optional[int] = None, **_) -> Dict[str, Any]:
    """<- half the high bits of p known.  STUB -- note only (needs LLL)."""
    return {'fired': False, 'work': 0,
            'note': 'Coppersmith/LLL: recovers p from ~half its bits; not '
                    'implemented here. Needs a lattice-reduction backend.'}


# name -> (callable, hardness countered, bifurcation point, cost class)
COUNTER_OPS: List[Tuple[str, Any, str, str, str]] = [
    ('trial_division', op_trial_division, 'q small', 'floor branch', 'O(spf N)'),
    ('fermat',         op_fermat,         'p ~ q',   'pitchfork r=3', 'O(|p-q|^2/N^{1/2})'),
    ('pollard_p_minus_1', op_pollard_p_minus_1, 'p-1 smooth', 'window (smooth tangency)', 'O(B log B)'),
    ('williams_p_plus_1', op_williams_p_plus_1, 'p+1 smooth', 'window (smooth tangency)', 'O(B log B)'),
    ('ecm',            op_ecm,            'mid-size factor', 'small-x branch', 'L_p[1/2]'),
    ('wiener',         op_wiener,         'd small', 'off-diagram (key structure)', 'O(log N)'),
    ('batch_gcd',      op_batch_gcd,      'shared prime', 'off-diagram (RNG failure)', 'O(#corpus)'),
    ('coppersmith',    op_coppersmith,    'leaked bits of p', 'window entry tangency', 'poly (LLL)'),
]

FLOOR_MARKERS = [
    ('gnfs', 'none of the above', 'chaotic bulk', 'L_N[1/3] (sub-exponential)'),
    ('shor', 'none of the above', 'the rotation number', 'poly (quantum)'),
]


# ======================================================================
#  ping
# ======================================================================

def ping(N: int, e: Optional[int] = None, corpus: Optional[List[int]] = None,
         order: Optional[List[str]] = None, budget: int = 1 << 18,
         verbose: bool = False) -> Dict[str, Any]:
    """
    Hop through the RSA-hardness counter-operators.  Returns:
        factored   : bool
        factors    : (p, q) or None
        regime     : which hardness applied, or 'floor -- GNFS/Shor only'
        path       : the ops tried, in order, with per-op work
        bracket_map: the Emerger bracket-hop structural map of N (free)
        laplacian  : the counter-operator Laplacian summary (order-independent)
    """
    ops = {name: fn for name, fn, *_ in COUNTER_OPS}
    seq = order or [name for name, *_ in COUNTER_OPS]
    path, factored, factors, regime = [], False, None, None
    for name in seq:
        fn = ops.get(name)
        if fn is None:
            continue
        r = fn(N, e=e, corpus=corpus, B=min(budget, 1 << 20))
        path.append({'op': name, 'fired': r.get('fired', False),
                     'work': r.get('work'), 'note': r.get('note')})
        if verbose:
            print(f"  {name:20s} fired={r.get('fired')}  work={r.get('work')}"
                  f"  {r.get('note') or ''}")
        if r.get('fired'):
            factored, factors, regime = True, r.get('factors'), r.get('regime')
            break
    if not factored:
        regime = 'floor -- GNFS (L_N[1/3]) or Shor (quantum) only'

    return {
        'N': N,
        'factored': factored,
        'factors': factors,
        'regime': regime,
        'path': path,
        'bracket_map': _bracket_map(N),
        'laplacian': counter_operator_laplacian(),
        'flat_diagram_depth': flat_diagram_depth_note(N),
    }


def _bracket_map(N: int) -> Dict[str, Any]:
    """The Emerger bracket-hop -- runs free on N's embedding, no factors."""
    if emerge is None:
        return {'available': False, 'note': 'emerger not importable'}
    dim = 16
    v = [0.0] * dim
    v[N % dim] += 1.0
    v[(N * 7 + 3) % dim] += 0.5
    n = math.sqrt(sum(c * c for c in v)) or 1.0
    v = [Fraction(round(c / n, 9)).limit_denominator(10 ** 6) for c in v]
    r = emerge(v, mode='sigma_rb')
    fo = r['firing_order']
    return {
        'available': True,
        'embedding_note': 'illustrative map_int_to_hypercomplex(N); not a Hyperwebster address',
        'firing_order': fo['order'],
        'Sigma_tilt': fo['Sigma_tilt'],
        'steps': [{'bracket': s['bracket'],
                   'on_zd_equator': s.get('on_zd_equator'),
                   'is_zero_divisor': s.get('is_zero_divisor'),
                   'gain_class': s.get('gain_class')}
                  for s in r['steps']],
    }


# ======================================================================
#  the counter-operator Laplacian
# ======================================================================

# adjacency: two ops are joined if they counter neighbouring regimes or one
# can hand off to the other. Symmetric by construction.
_ADJ = [
    ('trial_division', 'ecm'),
    ('trial_division', 'fermat'),          # the two endpoint degeneracies
    ('fermat', 'coppersmith'),             # both are "close / partial" attacks
    ('pollard_p_minus_1', 'williams_p_plus_1'),
    ('pollard_p_minus_1', 'ecm'),
    ('williams_p_plus_1', 'ecm'),
    ('ecm', 'gnfs'),                        # ecm hands off to the floor
    ('coppersmith', 'gnfs'),
    ('wiener', 'coppersmith'),             # both use the key's own structure
    ('wiener', 'batch_gcd'),               # both: the key's ecosystem betrays it
    ('gnfs', 'shor'),                      # the two floor methods
]

# The FIRST bifurcation of the cascade -- the r=3 pitchfork, period-1 -> period-2
# -- IS the +/- (SIGN) distinction: the sheet, +-sqrt(N), the sign-locked factor
# sets {+p,+q} / {-p,-q}. That is why Fermat lives there: N = a^2 - b^2 is the
# difference-of-squares, the +- structure itself.
FIRST_BIFURCATION = {
    'event': 'r = 3 pitchfork (period-1 -> period-2)',
    'is': 'the +/- (SIGN) distinction',
    'meaning': 'the sheet / +-sqrt(N) / the sign-locked sets {+p,+q} and {-p,-q}',
    'counter_operator_here': 'fermat (N = a^2 - b^2, the difference of squares)',
}


def counter_operator_laplacian() -> Dict[str, Any]:
    names = [n for n, *_ in COUNTER_OPS] + [m for m, *_ in FLOOR_MARKERS]
    idx = {n: i for i, n in enumerate(names)}
    n = len(names)
    A = np.zeros((n, n))
    for u, v in _ADJ:
        if u in idx and v in idx:
            A[idx[u], idx[v]] = A[idx[v], idx[u]] = 1.0
    D = np.diag(A.sum(1))
    L = D - A
    w = np.sort(np.linalg.eigvalsh(L))
    # Fiedler vector -> the cut between cheap regimes and the floor
    _, vecs = np.linalg.eigh(L)
    fiedler = vecs[:, 1]
    cheap = [names[i] for i in range(n) if fiedler[i] < 0]
    floor = [names[i] for i in range(n) if fiedler[i] >= 0]
    return {
        'nodes': names,
        'eigenvalues': [round(float(x), 4) for x in w],
        'connected': bool(abs(w[1]) > 1e-9),
        'algebraic_connectivity': round(float(w[1]), 4),
        'symmetric': bool(np.allclose(L, L.T)),
        'order_independent': True,
        'first_bifurcation': FIRST_BIFURCATION,
        'fiedler_cut': {'cheap_regimes': cheap, 'floor': floor},
        'reading': (
            'L is symmetric -> its spectrum is permutation-invariant -> the '
            'regime VERDICT is order-independent; only the SCHEDULE (which '
            'probes fire before the one that works) is order-sensitive. An '
            'order-independent Laplacian is a CLASSIFIER, not a pathfinder: it '
            'names the regime, never the factorisation.'
        ),
    }


# ======================================================================
#  the flat-diagram depth
# ======================================================================

def flat_diagram_depth_note(N: int) -> Dict[str, Any]:
    root = math.isqrt(N)
    approx_pi = root // max(1, int(math.log(root))) if root > 2 else 1
    apparent = approx_pi * (approx_pi + 1) // 2
    return {
        'apparent_pxq_crossings_near_N_column': apparent,
        'real_crossings': 1,
        'passes': apparent - 1,
        'distinguishing_coordinate': 'the projected-out DEPTH = the product '
                                     'value, equivalently ln(q/p) (the '
                                     'palindrome centre, the erased coordinate)',
        'reading': (
            'The bifurcation diagram is a 2-D projection. On it, N\'s column '
            f'has ~{apparent} apparent p x q meetings; exactly ONE is a real '
            'crossing (pq = N), the rest are PASSES -- two prime branches '
            'overlapping in projection with pq != N. Distinguishing cross from '
            'pass needs the depth coordinate; reconstructing it for the '
            'apparent crossings IS the operator hop = factoring. The flatness '
            'carries a TON of information out of view.'
        ),
    }


# ======================================================================
#  the Emerger-Lineage unification -- both hop axes at once
# ======================================================================

def emerger_lineage_unify(N: int, verbose: bool = True) -> Dict[str, Any]:
    """
    Walk BOTH structural axes for N:
      operator hop (descent)  -- factor_lineage(N): the Two-Trees / tier
                                 decomposition, N -> its prime leaves -> 0_RB.
      bracket  hop (ascent)   -- the Emerger map of N's embedding.
    For a KNOWN composite this returns the shortest hop-path modulus -> 0_RB
    (release each prime: SCALE-down; then the Mingling). For an unknown N the
    bracket map is free and the operator hop degenerates to `ping`.
    """
    out: Dict[str, Any] = {'N': N}

    if factor_lineage is not None:
        fl = factor_lineage(N)
        out['operator_hop'] = {
            'tree_class': fl.get('tree_class'),
            'omega_distinct': fl.get('omega') or fl.get('omega_distinct'),
            'generations': fl.get('generations') or fl.get('Omega_lineage_length'),
            'leaves_telperion': fl.get('leaves_telperion'),
            'path_to_0RB': '  ->  '.join(
                [f'divide out {p}' for p in _prime_leaves(N)] + ['1 (SCALE identity)', '0_RB (Mingling)']),
        }
    out['bracket_hop'] = _bracket_map(N)
    out['ping'] = {k: ping(N)[k] for k in ('factored', 'regime', 'path')}
    out['flat_diagram_depth'] = flat_diagram_depth_note(N)

    if verbose:
        print(f"THE EMERGER-LINEAGE UNIFICATION  --  N = {N}")
        oh = out.get('operator_hop', {})
        print(f"  operator hop (descent): {oh.get('tree_class')}  "
              f"omega={oh.get('omega_distinct')}  gens={oh.get('generations')}")
        print(f"    modulus -> 0_RB:  {oh.get('path_to_0RB')}")
        bh = out['bracket_hop']
        if bh.get('available'):
            print(f"  bracket hop (ascent):  firing {' -> '.join(bh['firing_order'])}"
                  f"   Sigma_tilt={bh['Sigma_tilt']:+.4f}")
        print(f"  ping regime: {out['ping']['regime']}")
        print(f"  flat-diagram depth: ~{out['flat_diagram_depth']['passes']} passes, "
              f"1 real crossing")
    return out


def _prime_leaves(n: int) -> List[int]:
    leaves, d = [], 2
    while d * d <= n:
        while n % d == 0:
            leaves.append(d)
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        leaves.append(n)
    return leaves


def report_ping(N: int = 3233, e: Optional[int] = None) -> Dict[str, Any]:
    """Worked example, FD report_* house style.  3233 = 61 * 53 (RSA-toy)."""
    print(f"  PING  --  N = {N}" + (f"   e = {e}" if e else ""))
    r = ping(N, e=e, verbose=True)
    print(f"\n  regime: {r['regime']}")
    print(f"  factors: {r['factors']}")
    lap = r['laplacian']
    print(f"  counter-operator Laplacian: {len(lap['nodes'])} nodes, "
          f"lambda_2 = {lap['algebraic_connectivity']}, "
          f"symmetric={lap['symmetric']} -> order-independent VERDICT")
    print(f"  Fiedler cut -- cheap: {lap['fiedler_cut']['cheap_regimes']}")
    print(f"               floor: {lap['fiedler_cut']['floor']}")
    fd = r['flat_diagram_depth']
    print(f"  flat diagram: ~{fd['passes']} passes vs 1 real crossing near N's column")
    return r
