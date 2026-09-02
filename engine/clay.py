"""GenerationalLineage.engine.clay

The generational lineage of the seven Clay Millennium Problems, each read as a
*decomposed object* / structural mapping — to confirm or confound current
understanding.

This is a **curated structural mapping with a consistency checker**, not a claim
to have derived any of the conjectures. Each entry states the problem's central
object, its central operation, where that operation lands on the tier-0 floor
(ADD / SCALE / SIGN — see `add_scale_sign` / `root_irreducible`), where the
object sits on the Two Trees, whether the object is DEFINITIONAL (carries a
construction of its own answer) or DESCRIPTIVE (references a set/quantity it does
not construct), and — for the open ones — the single piece its lineage cannot
derive from the floor. `check_consistency()` verifies the internal invariants;
`clay_lineage_report()` runs all seven with Poincaré as the control.

Two new factoring methods are introduced here and documented in the README
tutorial:
  * ``descriptive_or_definitional`` — does the object build its answer, or
    import it?
  * ``import_deficit`` — the one tier-0-underivable piece; ``None`` iff solved.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    from .lineage import decompose, root_irreducible          # in-package
except ImportError:                                            # pragma: no cover
    from lineage import decompose, root_irreducible


# ═══════════════════════════════════════════════════════════════════════════
# Two new factoring methods
# ═══════════════════════════════════════════════════════════════════════════

def descriptive_or_definitional(constructs_its_answer: bool,
                                imported_symbol: Optional[str]) -> Dict[str, Any]:
    """Classify an object by whether it carries a construction of its own answer.

    DEFINITIONAL — a procedure that produces the answer (the Sieve produces the
        primes; Ricci flow produces the diffeomorphism). Remove nothing and it
        still computes.
    DESCRIPTIVE — it references a set or quantity it does not build (ζ references
        its zeros; an L-function references its order of vanishing). It needs
        that piece supplied from outside.

    A problem whose central object is DESCRIPTIVE is open until the missing
    DEFINITIONAL construction is supplied — that construction IS the solution.
    """
    kind = 'DEFINITIONAL' if constructs_its_answer else 'DESCRIPTIVE'
    return {
        'kind': kind,
        'imported': None if kind == 'DEFINITIONAL' else imported_symbol,
        'note': ('builds its answer; nothing imported' if kind == 'DEFINITIONAL'
                 else f'imports {imported_symbol!r} — the piece the lineage '
                      f'cannot derive from ADD/SCALE/SIGN'),
    }


def import_deficit(problem: Dict[str, Any]) -> Optional[str]:
    """The single piece the problem's generational lineage cannot derive from
    the tier-0 floor. ``None`` iff the problem is solved (its central tool is
    definitional). For the open six this string *is* the open problem."""
    return problem.get('deficit')


# ═══════════════════════════════════════════════════════════════════════════
# The seven, as a structural mapping
# ═══════════════════════════════════════════════════════════════════════════
# Fields per entry:
#   object       — the thing the problem is about
#   central_op   — the tool / operation it turns on
#   op_known     — a name `decompose()` already places, or None
#   tier, root   — where central_op lands on the tier-0 floor
#   tree         — Two Trees placement (TELPERION irreducible / LAURELIN
#                  composite / MINGLING the identities' balance line)
#   builds       — does the central tool construct the answer?  (bool)
#   deficit      — the one imported / underivable piece   (None iff solved)
#   emergence    — which skill-§5 emergence signature fires, if any
#   verdict      — CONTROL / CONFIRM (fits the pattern) / CONFOUND (reframes it)
#   bone         — the one-line structural reading

CLAY: Dict[str, Dict[str, Any]] = {

    'poincare': {
        'clay_number': 7, 'name': 'Poincaré Conjecture', 'status': 'SOLVED',
        'object': 'a simply-connected closed 3-manifold M³ — is M³ ≅ S³?',
        'central_op': 'Ricci flow with surgery  (∂g/∂t = −2 Ric, cut at singularities)',
        'op_known': None,
        'tier': 1, 'root': 'SCALE',
        'tree': 'TELPERION',   # S³ = the irreducible closed 3-manifold (trivial π₁)
        'builds': True,
        'deficit': None,
        'emergence': None,
        'verdict': 'CONTROL',
        'bone': 'the tool is DEFINITIONAL: Ricci flow *constructs* the '
                'diffeomorphism to S³; nothing is imported; the lineage '
                'terminates — every simply-connected closed 3-manifold flows '
                'to the round S³. Solved because the tool builds the answer.',
    },

    'riemann': {
        'clay_number': 1, 'name': 'Riemann Hypothesis', 'status': 'OPEN',
        'object': 'the non-trivial zeros of ζ(s) — do they all lie on Re(s)=½?',
        'central_op': 'analytic continuation + the explicit formula '
                      'ψ(x) = x − Σ_ρ x^ρ/ρ − …',
        'op_known': None,
        'tier': 2, 'root': 'SIGN',   # the zeros = nodal set of a reflection-symmetric field
        'tree': 'MINGLING',          # the zeros sit on σ=½, the balance line; the primes are TELPERION
        'builds': False,
        'deficit': 'the locus of the imported zero set {ρ} — i.e. C1 / the '
                   'Berry–Keating self-adjointness step. ζ describes the zeros; '
                   'the Sieve (definitional) would place them.',
        'emergence': 'a fixed set (the nodal line) whose dimension must be shown '
                     'to equal the reflection\'s fixed set — not yet shown',
        'verdict': 'CONFIRM',
        'bone': 'ζ is DESCRIPTIVE — every operation it performs is on the floor '
                '(∏=SCALE, Σlog=ADD, s↔1−s=SIGN, σ=SCALE knob) EXCEPT the sum '
                'over zeros, a set it does not build. That one import is the '
                'whole of RH. The Two Trees partition (a zero-gradient harmonic '
                'field) gives a construction-side route to the same nodal line.',
    },

    'yang_mills': {
        'clay_number': 2, 'name': 'Yang–Mills Existence and Mass Gap', 'status': 'OPEN',
        'object': 'the mass gap Δ>0 — the least energy of a non-vacuum state; '
                  'and existence of the 4-D quantum theory',
        'central_op': 'the spectral infimum above the vacuum (a difference of '
                      'eigenvalues); non-abelian self-interaction [A_μ,A_ν]',
        'op_known': None,
        'tier': 3, 'root': 'ADD',    # a gap = a difference; existence half is tier-2 (a floor)
        'tree': 'MINGLING',          # Δ is the spacing of the identities: vacuum → first excited
        'builds': False,
        'deficit': 'the 10³ factor in GAP = Ω_ZS − d*·ln10 ≈ 1/(1000√2). The '
                   '1/√2 is the σ=½ symmetry (SIGN); the 10³ = the count of '
                   'Cayley–Dickson doublings / d*_RG — not derived from first '
                   'principles.',
        'emergence': 'a graded quantity (the gap magnitude) sitting where the '
                     'sign structure is one bit — the magnitude is the un-named part',
        'verdict': 'CONFIRM',
        'bone': 'Δ>0 is structurally forced — the vacuum and the first excited '
                'state cannot coincide because the identities are separated at '
                'the Mingling. What is imported is one scalar factor (10³), '
                'exactly the way RH imports one set.',
    },

    'navier_stokes': {
        'clay_number': 3, 'name': 'Navier–Stokes Existence and Smoothness', 'status': 'OPEN',
        'object': 'global-in-time smoothness of 3-D incompressible flow — or a '
                  'finite-time singularity',
        'central_op': 'advection u·∇u (self-SCALE, gain>1 threat) + diffusion '
                      'νΔu (ADD, the Laplacian average) + incompressibility '
                      '∇·u=0 (a constraint = COROLLARY)',
        'op_known': None,
        'tier': 1, 'root': 'SCALE',  # "does a length blow up" → needs DILATE
        'tree': 'LAURELIN',          # the real projection; the Blue/Telperion half is dropped
        'builds': False,
        'deficit': 'the discarded imaginary / Blue channel. NS = Yang–Mills '
                   'with i → 0; the construction (restore i, show the apparent '
                   'blow-up is a bounded 90° rotation into the Blue half) is '
                   'not done — see Ainulindale/wiki/106.',
        'emergence': 'THE canonical §5 signature — a quantity (the velocity '
                     'gradient) that changes length without bound where only '
                     'isometries were in play',
        'verdict': 'CONFOUND',
        'bone': 'the singularity is read as a coordinate artifact of dropping '
                'the Blue channel: a SIGN rotation (r↔1/r, θ→θ+π/2) misread as '
                'unbounded SCALE. R̂†=B̂ ⇒ the Noether current can only rotate, '
                'not be destroyed. Confounds "maybe it blows up" — the blow-up '
                'is the shadow of a discarded half.',
    },

    'p_vs_np': {
        'clay_number': 4, 'name': 'P vs NP', 'status': 'OPEN',
        'object': 'is every quickly-checkable problem quickly-solvable? '
                  '(search ≟ verification)',
        'central_op': 'verification (one forward pass = ADD) vs search '
                      '(a bifurcation tree = tier-1 SCALE); J_red (forward) vs '
                      'J_blue (reverse), adjoint but not isomorphic',
        'op_known': 'bifurcation',
        'tier': 3, 'root': 'ADD',    # comparing two growth rates = a ratio/difference
        'tree': 'LAURELIN',          # verify = check a given decomposition; search = find the TELPERION one
        'builds': False,             # the framework offers a mechanism, but the bridge is unproven — imported
        'deficit': 'the bridge: proving "adjoint ≠ isomorphic in the sedenion" '
                   '⇒ "P ≠ NP as a complexity statement". A THEORETICAL step, '
                   'not a reduction.',
        'emergence': None,
        'verdict': 'CONFIRM',
        'bone': 'verification is J_red (forward, cheap); search is J_blue '
                '(reverse). In a non-commutative algebra the reverse traversal '
                'is NOT the forward one — it carries information forward does '
                'not. So P ≠ NP structurally: the adjoint costs more. Confirms '
                'the expected answer, with a mechanism.',
    },

    'hodge': {
        'clay_number': 5, 'name': 'Hodge Conjecture', 'status': 'OPEN',
        'object': 'is every rational Hodge class of type (p,p) a rational '
                  'combination of classes of algebraic subvarieties?',
        'central_op': 'the Hodge decomposition Hⁿ = ⊕ H^{p,q} (splitting into '
                      'reflection eigen-subspaces = tier-2 SIGN) + the cycle '
                      'class map (subvarieties → cohomology = an ADD-sublattice)',
        'op_known': None,
        'tier': 3, 'root': 'SIGN',   # surjectivity onto a reflection-fixed set
        'tree': 'LAURELIN',          # algebraic cycles are built from subvarieties
        'builds': False,
        'deficit': 'the missing cycles — a construction that produces an '
                   'algebraic cycle for every Hodge class (or a proof that none '
                   'beyond the known ones is needed).',
        'emergence': 'a fixed set of possibly the wrong dimension — H^{p,p}(ℚ) '
                     'may exceed the span of algebraic cycles; the conjecture '
                     'asserts the dimensions match',
        'verdict': 'CONFOUND',
        'bone': 'the lineage reads Hodge as the claim "the TELPERION set at '
                'type (p,p) is empty — there is no Hodge class that cannot be '
                'built from cycles". That is the *opposite* shape to RH, where '
                'the irreducibles (the primes) are the entire point. Hodge is '
                'an emptiness claim about an irreducible set.',
    },

    'bsd': {
        'clay_number': 6, 'name': 'Birch and Swinnerton-Dyer', 'status': 'OPEN',
        'object': 'for an elliptic curve E/ℚ: does rank E(ℚ) = ord_{s=1} L(E,s)? '
                  '(algebraic rank ≟ analytic rank)',
        'central_op': 'rank = count of free generators of E(ℚ) ≅ ℤ^r (tier-3 '
                      'ADD); ord_{s=1} L = multiplicity of a zero (tier-3 ADD)',
        'op_known': None,
        'tier': 3, 'root': 'ADD',
        'tree': 'MINGLING',          # two counts meeting at one value; known only for r ≤ 1
        'builds': False,
        'deficit': 'the r ≥ 2 construction — a map between analytic rank and r '
                   'independent rational points, general r (known: r = 0, 1 — '
                   'Gross–Zagier, Kolyvagin).',
        'emergence': 'a collision that unpacks where the encoder should have '
                     'made it impossible — two unrelated machineries (algebraic '
                     'count, analytic count) conjectured to always agree',
        'verdict': 'CONFIRM',
        'bone': 'BSD is the RH descriptive-vs-definitional split localised to '
                'one curve: the L-function (descriptive) vs the rank '
                '(definitional, count the generators). Same pattern, one object.',
    },
}

_ORDER = ['poincare', 'riemann', 'yang_mills', 'navier_stokes',
          'p_vs_np', 'hodge', 'bsd']


# ═══════════════════════════════════════════════════════════════════════════
# The lineage of one problem, and the consistency check
# ═══════════════════════════════════════════════════════════════════════════

def generational_lineage_of(key: str) -> Dict[str, Any]:
    """Return the generational-lineage decomposition of one Clay problem."""
    p = CLAY[key]
    dd = descriptive_or_definitional(p['builds'], p['deficit'])
    placed = decompose(p['op_known']) if p.get('op_known') else None
    root_walk = (root_irreducible(p['op_known']).get('root_path')
                 if p.get('op_known') else None)
    return {
        'key': key,
        'clay_number': p['clay_number'],
        'name': p['name'],
        'status': p['status'],
        'object': p['object'],
        'central_operation': p['central_op'],
        'tier': p['tier'],
        'root': p['root'],
        'two_trees': p['tree'],
        'kind': dd['kind'],
        'import_deficit': import_deficit(p),
        'emergence_signature': p['emergence'],
        'verdict': p['verdict'],
        'bone': p['bone'],
        'engine_placement': placed,      # None unless central_op is a known op
        'root_path': root_walk,
    }


def check_consistency() -> Dict[str, Any]:
    """Verify the internal invariants of the mapping:
      I1  SOLVED ⟺ builds ⟺ import_deficit is None      (the control invariant)
      I2  root ∈ {ADD, SCALE, SIGN}
      I3  tier ∈ {1, 2, 3}
      I4  every OPEN problem names exactly one import_deficit string
      I5  a stated emergence signature ⇒ the problem is OPEN
    """
    fails: List[str] = []
    for k in _ORDER:
        p = CLAY[k]
        solved = p['status'] == 'SOLVED'
        if solved != p['builds'] or solved != (p['deficit'] is None):
            fails.append(f'{k}: I1 (SOLVED⟺builds⟺no-deficit) broken')
        if p['root'] not in ('ADD', 'SCALE', 'SIGN'):
            fails.append(f'{k}: I2 bad root {p["root"]!r}')
        if p['tier'] not in (1, 2, 3):
            fails.append(f'{k}: I3 bad tier {p["tier"]!r}')
        if not solved and not (isinstance(p['deficit'], str) and p['deficit']):
            fails.append(f'{k}: I4 open problem with no import_deficit')
        if p['emergence'] and solved:
            fails.append(f'{k}: I5 emergence signature on a solved problem')
    return {'holds': not fails, 'failures': fails,
            'checked': len(_ORDER), 'invariants': ['I1', 'I2', 'I3', 'I4', 'I5']}


def clay_lineage_report() -> Dict[str, Any]:
    """Run the generational lineage on all seven. Poincaré is the control."""
    rows = [generational_lineage_of(k) for k in _ORDER]
    cons = check_consistency()
    control = next(r for r in rows if r['status'] == 'SOLVED')
    open_ = [r for r in rows if r['status'] == 'OPEN']
    bone = (
        "Run the generational lineage on all seven. Poincaré — the one that is "
        "SOLVED — is the only one whose central tool is DEFINITIONAL (Ricci "
        "flow constructs the diffeomorphism; nothing imported) and whose "
        "lineage terminates with no deficit. Every OPEN problem has a "
        "DESCRIPTIVE central object that imports exactly one piece its lineage "
        "cannot derive from ADD/SCALE/SIGN — and that imported piece IS the "
        "open problem:\n"
        + "\n".join(f"  · {r['name']}: {r['import_deficit']}" for r in open_)
        + "\n\nA problem is open exactly when it is DESCRIBED but not "
          "CONSTRUCTED. Solving it means supplying the one missing construction."
    )
    return {
        'rows': rows,
        'control': control['name'],
        'consistency': cons,
        'confirm': [r['name'] for r in open_ if r['verdict'] == 'CONFIRM'],
        'confound': [r['name'] for r in open_ if r['verdict'] == 'CONFOUND'],
        'bone': bone,
    }


def _fmt_table(rows: List[Dict[str, Any]]) -> str:
    head = f"{'#':>2}  {'problem':<34} {'status':<7} {'tier':>4} {'root':<6} " \
           f"{'two-trees':<10} {'kind':<12} {'verdict':<9}"
    line = "-" * len(head)
    out = [head, line]
    for r in rows:
        out.append(f"{r['clay_number']:>2}  {r['name']:<34} {r['status']:<7} "
                   f"{r['tier']:>4} {r['root']:<6} {r['two_trees']:<10} "
                   f"{r['kind']:<12} {r['verdict']:<9}")
    return "\n".join(out)


if __name__ == '__main__':
    rep = clay_lineage_report()
    print("=" * 78)
    print("GENERATIONAL LINEAGE — THE SEVEN CLAY MILLENNIUM PROBLEMS")
    print("=" * 78)
    print(_fmt_table(rep['rows']))
    print()
    c = rep['consistency']
    print(f"consistency: {'HOLDS' if c['holds'] else 'FAILS'} "
          f"({', '.join(c['invariants'])} over {c['checked']} problems)")
    if c['failures']:
        for f in c['failures']:
            print("  !", f)
    print(f"control: {rep['control']}")
    print(f"fits the pattern (CONFIRM): {', '.join(rep['confirm'])}")
    print(f"reframes it (CONFOUND):     {', '.join(rep['confound'])}")
    print()
    for r in rep['rows']:
        print(f"── [{r['clay_number']}] {r['name']}  ({r['status']}) "
              f"{'— CONTROL' if r['verdict'] == 'CONTROL' else ''}")
        print(f"   object     : {r['object']}")
        print(f"   central op : {r['central_operation']}")
        print(f"   floor      : tier {r['tier']}, root {r['root']}, "
              f"{r['two_trees']}, {r['kind']}")
        if r['import_deficit']:
            print(f"   IMPORTS    : {r['import_deficit']}")
        if r['emergence_signature']:
            print(f"   emergence  : {r['emergence_signature']}")
        print(f"   bone       : {r['bone']}")
        print()
    print("=" * 78)
    print("THE BONE")
    print("=" * 78)
    print(rep['bone'])
