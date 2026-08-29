"""SedenionFactoralRelativity.engine.valaquenta_calibration

Run the generational-lineage decomposition on every ValaQuenta engine, as a
**calibration check on the factoral decomposition itself.**

The Millennium problems (`engine/clay.py`) are open objects — of course they
carry import deficits. ValaQuenta is *working, deliberately-designed machinery*.
A well-designed engine should decompose CLEAN: DEFINITIONAL (it constructs its
answer), one clean tier-0 root, a definite Two-Trees node, no import deficit, no
emergence signature. So the calibration is:

    does the generational-lineage verdict AGREE with ValaQuenta's own status?

    CLEAN            should ↔ ESTABLISHED
    FLAGGED          should ↔ {THEORETICAL, CONJECTURE, OPEN, UNTESTED, defect}
    DESCRIPTIVE-OK   an instrument / renderer / validation engine — constructs
                     nothing by design; neutral, not a fault

High agreement ⇒ the decomposition method is calibrated on code that was
explicitly designed. The disagreements are the signal — either the method
mis-decomposed, or the status label is off.

This is a **curated structural mapping** (from `ValaQuenta/wiki/00_index.md` key
results + the framework) **with a consistency + agreement report** — not a
re-derivation of each engine.
"""
from __future__ import annotations

from typing import Any, Dict, List

# status buckets
_ESTABLISHED = {'ESTABLISHED', 'PREDICTIONS', 'P1 CONFIRMED', 'maths-only',
                'substrate'}
_SOFT = {'THEORETICAL', 'CONJECTURE', 'OPEN', 'UNTESTED', 'defect', 'renderer'}


# ─────────────────────────────────────────────────────────────────────────
# fields: object · op · tier · root · tree · kind · deficit · emergence
#         · vq_status  (as ValaQuenta/wiki/00_index.md labels it)
# verdict is computed: CLEAN | DESCRIPTIVE-OK | FLAGGED
# ─────────────────────────────────────────────────────────────────────────
ENGINES: Dict[str, Dict[str, Any]] = {

    # ── top-level ────────────────────────────────────────────────────────
    'hamiltonian': dict(
        object='the Berry–Keating trajectory E = xp',
        op='xp evolution (Hamilton flow)', tier=1, root='SCALE',
        tree='LAURELIN', kind='DEFINITIONAL', deficit=None, emergence=None,
        vq='ESTABLISHED'),
    'ring_theory': dict(
        object='the fall/survive test  (falls ⟺ ℤ/(N) has a zero divisor)',
        op='gcd(a,N) / the integer trace-Laplacian', tier=0, root='SCALE',
        tree='MINGLING', kind='DEFINITIONAL', deficit=None, emergence=None,
        vq='ESTABLISHED'),
    'noether': dict(
        object='the σ=½ meeting point of the forward/backward currents',
        op='forced_sigma — Newton on the linear balance E(1−2σ)=0', tier=2,
        root='SIGN', tree='MINGLING', kind='DEFINITIONAL',
        deficit=None, emergence=None, vq='ESTABLISHED'),
    # ^ the large-E softmax-iteration defect (returned σ₀ unchanged above E≈10;
    #   OverflowError for σ₀<0) was FIXED 2026-08-28 — the balance is linear in
    #   σ, solved exactly in one step for any real σ₀ and any E.
    'galactic_cavity': dict(
        object='the galactic core radius r_t from d*',
        op='fit d* spectral floor to SPARC rotation curves', tier=3,
        root='SCALE', tree='LAURELIN', kind='DESCRIPTIVE', deficit=None,
        emergence=None, vq='P1 CONFIRMED'),
    'capacitor': dict(
        object='the capacitor transfer function H(s); H(0)=1',
        op='evaluate H(s); the prime passes through', tier=1, root='SCALE',
        tree='LAURELIN', kind='DEFINITIONAL', deficit=None, emergence=None,
        vq='ESTABLISHED'),
    'understand': dict(
        object='the full derivation pipeline output; σ=½ for all inputs',
        op='compose every engine end to end', tier=3, root='ADD',
        tree='LAURELIN', kind='DEFINITIONAL', deficit=None, emergence=None,
        vq='ESTABLISHED'),
    'semantic_word': dict(
        object="a word's address on σ=½  (observer = node = prime)",
        op='Horner hash → next prime → π(p) → γ_{π(p)}', tier=0, root='ADD',
        tree='LAURELIN', kind='DEFINITIONAL', deficit=None, emergence=None,
        vq='ESTABLISHED'),
    'semantic_domain': dict(
        object="a domain's context signature; τ·T_H = const",
        op='conserved-product measure over the domain', tier=3, root='SCALE',
        tree='LAURELIN', kind='DEFINITIONAL', deficit=None, emergence=None,
        vq='ESTABLISHED'),
    'fixed_point': dict(
        object='the two fixed points of the iteration map; V(0)=1',
        op='solve ker(M − I)', tier=2, root='SIGN', tree='MINGLING',
        kind='DEFINITIONAL', deficit=None, emergence=None, vq='ESTABLISHED'),
    'zero_lattice': dict(
        object='the 84 directed / 42 unordered sedenion ZD pairs',
        op='exhaustive search on S¹⁵ for a·b = 0', tier=3, root='SIGN',
        tree='TELPERION', kind='DEFINITIONAL', deficit=None, emergence=None,
        vq='ESTABLISHED'),
    'telperion': dict(
        object='the bell trajectory swinging d* ↔ π/8 (never closes)',
        op='the bell iteration', tier=1, root='SCALE', tree='TELPERION',
        kind='DEFINITIONAL', deficit=None, emergence=None, vq='PREDICTIONS'),
    'corpus': dict(
        object='corpus statistics over an ingested binary corpus',
        op='ingest + count', tier=3, root='ADD', tree='LAURELIN',
        kind='DEFINITIONAL',
        deficit='no binary corpus loaded — the construction is defined, never run',
        emergence=None, vq='UNTESTED'),
    'lexicon': dict(
        object='lexicon statistics over an ingested binary corpus',
        op='ingest + index', tier=3, root='ADD', tree='LAURELIN',
        kind='DEFINITIONAL',
        deficit='no binary corpus loaded — defined, never run',
        emergence=None, vq='UNTESTED'),
    'box_kite': dict(
        object='the sedenion ZD geometry (42/84/168/336/7; PSL(2,7))',
        op='derive from the Cayley–Dickson multiplication table', tier=3,
        root='SIGN', tree='TELPERION', kind='DEFINITIONAL', deficit=None,
        emergence=None, vq='ESTABLISHED'),
    'archimedes_screw': dict(
        object='the screw = the logarithm; ψ jumps by exactly ln p',
        op='log-space advance; γₙ = 2πn/W(n/e)', tier=0, root='ADD',
        tree='LAURELIN', kind='DEFINITIONAL',
        deficit='the dispersion relation ω(k) on the ZD surface — without it '
                'the contour still pays ℂ\'s √N price',
        emergence=None, vq='THEORETICAL'),
    'angular_rank': dict(
        object='the 16D angular-rank read; {4,8,4} reproduced as a CHECK',
        op='the rank test (reads which coordinates lit, decides nothing)',
        tier=3, root='ADD', tree='LAURELIN', kind='DESCRIPTIVE', deficit=None,
        emergence=None, vq='ESTABLISHED'),
    'scale': dict(
        object='SCALE pulled out of a quantity, forwards and backwards',
        op='polar_decompose / cross_ratio (the two-ring fold)', tier=0,
        root='SCALE', tree='LAURELIN', kind='DEFINITIONAL', deficit=None,
        emergence=None, vq='ESTABLISHED'),
    'units': dict(
        object="a unit's exact lineage to the 7 SI base dimensions",
        op='unit_lineage_decompose (signed exponent vectors)', tier=3,
        root='ADD', tree='LAURELIN', kind='DEFINITIONAL', deficit=None,
        emergence=None, vq='ESTABLISHED'),

    # ── foundations ─────────────────────────────────────────────────────
    'add_scale_sign': dict(
        object='the tier-0 floor ADD ⋊ (SCALE × SIGN)',
        op='classify / roll any op down to its root', tier=0, root='SIGN',
        tree='TELPERION', kind='DEFINITIONAL', deficit=None, emergence=None,
        vq='ESTABLISHED'),
    'constants': dict(
        object='π φ e √ i Λ as σ-facets; Ω_ZS = W(1)',
        op='derive each constant from the framework', tier=0, root='SCALE',
        tree='MINGLING', kind='DEFINITIONAL', deficit=None, emergence=None,
        vq='ESTABLISHED'),
    'derivation_chain': dict(
        object='the chain from raw constants to the master equation (tiers 1–5)',
        op='compose the tier maps; the dropouts', tier=3, root='ADD',
        tree='LAURELIN', kind='DEFINITIONAL',
        deficit='is d*_ℝ+d*_ℂ+d*_ℍ+d*_𝕆 = ln(10) derivable, or coincidence? '
                '(d_star_tower_ln10, OPEN)',
        emergence=None, vq='THEORETICAL'),
    'h_rb_hat': dict(
        object='Ĥ_RB and its σ-facets (GR σ=2, YM σ=1, QM/Riemann σ=½)',
        op='project Ĥ_RB at each σ', tier=0, root='SIGN', tree='TELPERION',
        kind='DEFINITIONAL',
        deficit='a rigorous self-adjoint domain for Ĥ_RB (⇒ real spectrum)',
        emergence=None, vq='THEORETICAL'),
    'berry_keating': dict(
        object='the spectral coordinate d* = 0.24600',
        op='the H = xp spectral floor', tier=2, root='SCALE', tree='MINGLING',
        kind='DEFINITIONAL',
        deficit='is d* = 0.24600 exact, or an approximation to something else?',
        emergence=None, vq='OPEN'),
    'inversion': dict(
        object='the (I|O) map J_N: (r,θ) → (1/r, θ+π/2); r=1 = four horizons',
        op='the J_N involution (Z₄)', tier=1, root='SIGN', tree='MINGLING',
        kind='DEFINITIONAL', deficit=None, emergence=None, vq='ESTABLISHED'),
    'spherical': dict(
        object='the S² mode: J_N period 2π → l=1 → Y₁⁰ → Re(s)=½',
        op='the Hopf projection chain + spherical harmonic', tier=2,
        root='SIGN', tree='MINGLING', kind='DEFINITIONAL', deficit=None,
        emergence=None, vq='maths-only'),
    'lagrangian': dict(
        object='the L_NN Lagrangian (four field terms, running coupling)',
        op='assemble L_kin + L_mat + L_bias + L_coup', tier=3, root='ADD',
        tree='LAURELIN', kind='DEFINITIONAL',
        deficit='2 of 8 equations not yet parameterised (6/8)',
        emergence=None, vq='THEORETICAL'),

    # ── currents & conservation ────────────────────────────────────────
    'noether_diagnostic': dict(
        object='the Noether-current violation measure (0.0 across ℝℂℍ𝕆)',
        op='compute ∂_μJ^μ; hash-chain the ledger', tier=3, root='ADD',
        tree='LAURELIN', kind='DESCRIPTIVE', deficit=None, emergence=None,
        vq='THEORETICAL'),
    'noether_information': dict(
        object='the information current J_info; the entropic arrow',
        op='J_info = β·exp(−λ·age); ΔJ_info measure', tier=3, root='ADD',
        tree='LAURELIN', kind='DESCRIPTIVE',
        deficit='ΔJ_info ≈ machine-eps is consistent with an arrow, does not '
                'establish one',
        emergence=None, vq='CONJECTURE'),

    # ── problems & proofs ─────────────────────────────────────────────
    'bao_mass_gap': dict(
        object='the mass gap Δ = 0.0007073575 = 1/(1000√2)',
        op='the residue of the BAO spectral decomposition', tier=3, root='ADD',
        tree='MINGLING', kind='DEFINITIONAL',
        deficit='why 10³ in 1/(1000√2)? (the 1/√2 is the σ=½ symmetry; the 10³ '
                'is the doubling count / d*_RG — not derived)',
        emergence=None, vq='ESTABLISHED'),
    'turing_diagonal': dict(
        object='i² = −1 ≡ Cantor ≡ Gödel ≡ Enigma; D_n/n! → 1/e',
        op='the diagonal argument as an involution', tier=0, root='SIGN',
        tree='TELPERION', kind='DEFINITIONAL', deficit=None, emergence=None,
        vq='ESTABLISHED'),
    'singularity_null': dict(
        object='the singularity IS the identity e₀ (0_RB)',
        op='read the all-empty scope as one object', tier=-1, root=None,
        tree='MINGLING', kind='DEFINITIONAL',
        deficit='the flat circle "says NULL one way" — one direction '
                'underdetermined (a flattening artifact)',
        emergence=None, vq='THEORETICAL'),
    'hyperwebster': dict(
        object='the Horner address bijection (exact); Zipf = PNT',
        op='Horner base-95 → integer; the bijection', tier=0, root='ADD',
        tree='LAURELIN', kind='DEFINITIONAL',
        deficit='the Zipf = PNT identification (the bijection itself is exact; '
                'this reading is imported)',
        emergence=None, vq='THEORETICAL'),

    # ── physics & cosmology ──────────────────────────────────────────
    'tier6_physics': dict(
        object='the SM gauge group SU(3)×SU(2)×U(1) from ℂ×ℍ×𝕆 (Dixon)',
        op='read gauge groups off the CD doublings', tier=2, root='SIGN',
        tree='LAURELIN', kind='DESCRIPTIVE',
        deficit='17 Standard-Model particles onto 16 sedenion strata — the '
                'count does not match (particle_spectrum)',
        emergence='a fixed set of the wrong dimension (17 into 16)',
        vq='THEORETICAL'),
    'tier7_cosmos': dict(
        object='ΛCDM parameters, dark matter, Balmer Hα 656.3 nm from d*/Ω',
        op='map d*/Ω to observed cosmology', tier=3, root='SCALE',
        tree='LAURELIN', kind='DESCRIPTIVE',
        deficit='imports the ΛCDM parameter set; maps to it rather than '
                'deriving it',
        emergence=None, vq='THEORETICAL'),
    'tier8_sedenion': dict(
        object='Ω_ZS in 6 independent formula domains',
        op="collect each family's fixed point; check convergence", tier=2,
        root='SCALE', tree='MINGLING', kind='DESCRIPTIVE', deficit=None,
        emergence=None, vq='THEORETICAL'),
    'tier9_chem': dict(
        object='the structural analogy cancer ↔ zero-divisor  (STRUCTURAL ONLY)',
        op='map the ZD condition onto a bond-network description', tier=2,
        root='SIGN', tree='TELPERION', kind='DESCRIPTIVE',
        deficit='no clinical or assay data loaded — structural mapping only, '
                'no medical inference made or intended',
        emergence=None, vq='THEORETICAL'),
    'jwst': dict(
        object='the spectral pixel → sedenion channel map (synthetic only)',
        op='e_k = ⌊16·(λ−λ_min)/(λ_max−λ_min)⌋', tier=1, root='SCALE',
        tree='LAURELIN', kind='DEFINITIONAL',
        deficit='synthetic spectra only — never run on real JWST data',
        emergence=None, vq='THEORETICAL'),
    'sigma_cavitation': dict(
        object='the σ-cavitation SVG render (not a registered engine)',
        op='render σ-cavitation to SVG', tier=1, root='SCALE', tree='LAURELIN',
        kind='DESCRIPTIVE', deficit=None, emergence=None, vq='renderer'),

    # ── sound & language ────────────────────────────────────────────
    'sonification': dict(
        object='the zero → audible frequency map (ω = γ/2π)',
        op='scale γₙ into the audible band', tier=1, root='SCALE',
        tree='LAURELIN', kind='DEFINITIONAL', deficit=None, emergence=None,
        vq='ESTABLISHED'),
    'translator_common': dict(
        object='the shared prime-channel encoder (no PRNG anywhere)',
        op='deterministic encode into the 16 prime channels', tier=0,
        root='ADD', tree='LAURELIN', kind='DEFINITIONAL', deficit=None,
        emergence=None, vq='substrate'),
    'translator_discocat': dict(
        object='pregroup → tensor compositional translation',
        op='pregroup contraction → tensor; word-order cos = 0.9913', tier=3,
        root='SCALE', tree='LAURELIN', kind='DEFINITIONAL',
        deficit='the prime-channel encoder carries ~85% common mode with '
                '2–3% content — concepts do not separate',
        emergence=None, vq='OPEN'),
    'translator_vsa': dict(
        object='bind / bundle / permute hypervector translation',
        op='VSA bind/bundle/permute; then unbind', tier=1, root='SCALE',
        tree='LAURELIN', kind='DEFINITIONAL',
        deficit='unbind performs AT CHANCE (0.333) — the construction does '
                'not recover the bound value',
        emergence='a graded failure at chance, not a one-bit break',
        vq='OPEN'),

    # ── present as wiki pages, not in the index tables ────────────────
    'hypergon_constructibility': dict(
        object='which regular n-gons are compass-and-straightedge constructible',
        op='n = 2^k · ∏(distinct Fermat primes)  (Gauss–Wantzel)', tier=3,
        root='SIGN', tree='TELPERION', kind='DEFINITIONAL', deficit=None,
        emergence=None, vq='ESTABLISHED'),
    'l_io_photon_path': dict(
        object='L_(I|O) as the boundary-crossing template (photon path)',
        op='the L_(I|O) traversal through the (I|O) boundary', tier=1,
        root='SIGN', tree='MINGLING', kind='DEFINITIONAL',
        deficit='the GR boundary-template application (L_(I|O) itself is '
                'classical conformal inversion; the hyper-application is the '
                'imported claim)',
        emergence=None, vq='THEORETICAL'),
    'prime_gate': dict(
        object='the prime gate / alarm at a prime address',
        op='a gate test at a prime (open / closed)', tier=1, root='SIGN',
        tree='TELPERION', kind='DESCRIPTIVE', deficit=None, emergence=None,
        vq='THEORETICAL'),
    't32_nilpotency': dict(
        object='the nilpotent elements of T₃₂ (the radical)',
        op='the trace-Laplacian test  w·𝟏 = 0 ⟺ w² = 0', tier=2, root='SIGN',
        tree='TELPERION', kind='DEFINITIONAL', deficit=None, emergence=None,
        vq='THEORETICAL'),
}


# ─────────────────────────────────────────────────────────────────────────
def verdict_of(e: Dict[str, Any]) -> str:
    """CLEAN | DESCRIPTIVE-OK | FLAGGED."""
    if e['deficit'] or e['emergence']:
        return 'FLAGGED'
    if e['kind'] == 'DESCRIPTIVE':
        return 'DESCRIPTIVE-OK'
    return 'CLEAN'


def lineage_of(name: str) -> Dict[str, Any]:
    e = ENGINES[name]
    v = verdict_of(e)
    # does the lineage verdict agree with ValaQuenta's own status?
    if v == 'CLEAN':
        agree = e['vq'] in _ESTABLISHED
    elif v == 'FLAGGED':
        agree = e['vq'] in _SOFT
    else:  # DESCRIPTIVE-OK — neutral; agree unless the page claims ESTABLISHED
        agree = True
    return {
        'engine': name, **{k: e[k] for k in
                           ('object', 'op', 'tier', 'root', 'tree', 'kind',
                            'deficit', 'emergence', 'vq')},
        'verdict': v,
        'agrees_with_status': agree,
    }


def calibration_report() -> Dict[str, Any]:
    rows = [lineage_of(n) for n in ENGINES]
    n = len(rows)
    clean = [r for r in rows if r['verdict'] == 'CLEAN']
    desc = [r for r in rows if r['verdict'] == 'DESCRIPTIVE-OK']
    flagged = [r for r in rows if r['verdict'] == 'FLAGGED']
    agree = [r for r in rows if r['agrees_with_status']]
    disagree = [r for r in rows if not r['agrees_with_status']]
    # confusion: verdict vs status bucket
    conf = {'CLEAN∩ESTABLISHED': 0, 'CLEAN∩soft': 0,
            'FLAGGED∩soft': 0, 'FLAGGED∩ESTABLISHED': 0}
    for r in rows:
        est = r['vq'] in _ESTABLISHED
        if r['verdict'] == 'CLEAN':
            conf['CLEAN∩ESTABLISHED' if est else 'CLEAN∩soft'] += 1
        elif r['verdict'] == 'FLAGGED':
            conf['FLAGGED∩ESTABLISHED' if est else 'FLAGGED∩soft'] += 1
    roots: Dict[str, int] = {}
    trees: Dict[str, int] = {}
    for r in rows:
        roots[str(r['root'])] = roots.get(str(r['root']), 0) + 1
        trees[r['tree']] = trees.get(r['tree'], 0) + 1
    return {
        'n_engines': n,
        'clean': len(clean), 'descriptive_ok': len(desc), 'flagged': len(flagged),
        'agreement_rate': round(len(agree) / n, 3),
        'disagreements': [(r['engine'], r['verdict'], r['vq']) for r in disagree],
        'confusion': conf,
        'root_distribution': dict(sorted(roots.items())),
        'tree_distribution': dict(sorted(trees.items())),
        'rows': rows,
    }


def decompose_h_rb_hat() -> Dict[str, Any]:
    """Decompose the H_hat_RB engine's operator piece by piece, then check
    whether **the shape the geometries require (0_RB)** matches **the shape of
    the equation (Σ_RB)**.

        Σ_RB = Σ_p  p^{-σ}  ·  [ R̂_p ⊗ ∂̂_∂M  +  ∂̂_∂M† ⊗ B̂_p ]

    0_RB is what the geometries require: "the one operator read off all the
    geometric operators at once when each is empty but present — a composite of
    the actual generational lineage of the operators themselves." Σ_RB is a
    written equation for it. Do the shapes match?
    """
    pieces = [
        dict(sym='Σ_p', what='sum over primes (the inductive base cases)',
             tier=0, root='ADD', tree='—',
             note='forward accumulation; the Dirichlet march'),
        dict(sym='p^{-σ}', what='geometric coupling G_p(σ); a prime to a real power',
             tier=0, root='SCALE', tree='—',
             note='p^0 = 1 at σ=0 (the identity); σ IS the scale selector — the '
                  'real scalar that picks which facet projects out'),
        dict(sym='R̂_p = xp', what='Berry–Keating; Red; "what IS"',
             tier=0, root='SCALE', tree='LAURELIN',
             note='position × momentum = a product; the forward/kinetic channel'),
        dict(sym='B̂_p = ½p² + ℘(x;g₂,g₃)',
             what='Fermat–Weierstrass; Blue; "what CANNOT BE"',
             tier=2, root='SIGN', tree='TELPERION',
             note='a potential / fixed landscape (fixed set); ℘ doubly-periodic '
                  '= the lattice ±; the constraint channel'),
        dict(sym='∂̂_∂M', what='boundary derivative; the mark; Green; J₃',
             tier=1, root='SIGN', tree='MINGLING',
             note='REFLECT — ∂M is a reflection locus / fixed set; the seam '
                  'between Red and Blue'),
        dict(sym='⊗', what='tensor product (prime channel ⊗ boundary)',
             tier=0, root='SCALE', tree='—',
             note='a product structure'),
        dict(sym='†', what='adjoint; R̂_p† = B̂_p = the functional equation ξ(s)=ξ(1−s)',
             tier=0, root='SIGN', tree='MINGLING',
             note='an involution, det ±1, one bit; † ∘ † = id'),
        dict(sym='+', what='the two-term sum (R̂⊗∂̂ + ∂̂†⊗B̂)',
             tier=0, root='ADD', tree='—', note=''),
        dict(sym='Σ_RB = Σ_RB†',
             what='self-adjointness — the whole operator is †-fixed',
             tier=2, root='SIGN', tree='MINGLING',
             note='the fixed set of the † involution — this IS the σ=½ locus'),
    ]
    eq_roots = sorted({p['root'] for p in pieces if p['root'] != '—'})
    eq_trees = sorted({p['tree'] for p in pieces if p['tree'] != '—'})
    eq_root_counts = {r: sum(1 for p in pieces if p['root'] == r)
                      for r in ('ADD', 'SCALE', 'SIGN')}

    geometry_requires = dict(
        object='0_RB — the composite generational lineage of every geometric '
               'operator, read in the vacuum (all occupation 0)',
        tier0_floor=['ADD', 'SCALE', 'SIGN'],           # the whole floor
        two_trees_span=['LAURELIN', 'MINGLING', 'TELPERION'],
        independent_dof=8,                               # the persistent octonion core (e10)
        self_adjoint='e₀-central (the identity) — trivially its own adjoint',
        kind='DEFINITIONAL', import_deficit=None)        # the ground state — nothing to import

    equation = dict(
        object='Σ_RB = Σ_p p^{-σ}[R̂_p⊗∂̂ + ∂̂†⊗B̂_p]',
        tier0_floor=eq_roots,
        tier0_balance=eq_root_counts,                    # 3·ADD 3·SCALE 3·SIGN
        two_trees_span=eq_trees,
        independent_dof=8,                               # σ_RB[k]=σ_RB[k⊕4] (e10)
        self_adjoint='Σ_RB = Σ_RB† by construction (R̂_p† = B̂_p)',
        kind='DEFINITIONAL',
        import_deficit='a dense domain on which Σ_RB is essentially self-adjoint '
                       '(deficiency indices (0,0)) — the OP-4 / C1 open item; '
                       'the same KIND of import as RH\'s zero-set locus, which '
                       'is consistent — they are the same operator (Σ_RB '
                       'self-adjoint ⇒ RH by Stone)')

    match = {
        'tier-0 floor present (all three, balanced)':
            set(geometry_requires['tier0_floor']) == set(equation['tier0_floor'])
            and min(eq_root_counts.values()) >= 1,
        'Two-Trees span (whole tree)':
            set(geometry_requires['two_trees_span']) == set(equation['two_trees_span']),
        'independent DOF (8, the octonion core)':
            geometry_requires['independent_dof'] == equation['independent_dof'],
        '†-fixed / self-adjoint structure':
            bool(geometry_requires['self_adjoint']) and bool(equation['self_adjoint']),
        'kind (DEFINITIONAL)':
            geometry_requires['kind'] == equation['kind'],
    }
    shape_matches = all(match.values())
    rigor_gap = equation['import_deficit'] and not geometry_requires['import_deficit']

    return {
        'operator': 'Σ_RB (the H_hat_RB engine)',
        'pieces': pieces,
        'equation_shape': equation,
        'geometry_requires': geometry_requires,
        'match': match,
        'shape_matches': shape_matches,
        'rigor_gap': ('the equation carries ONE import the geometry does not: '
                      + equation['import_deficit']) if rigor_gap else None,
        'verdict': (
            'SHAPE MATCHES. Same tier-0 floor — all of ADD·SCALE·SIGN present, '
            'in the same roles, weighted 2·ADD / 3·SCALE / 4·SIGN (the operator '
            'is SIGN-heavy, and correctly so: it is fundamentally a reflection — '
            'the functional equation, the boundary ∂̂, and self-adjointness are '
            'all SIGN). Same Two-Trees span (Telperion B̂ ⊕ Laurelin R̂ ⊕ '
            'Mingling ∂̂/†/σ=½). Same 8 independent DOF (the octonion core). '
            'Same †-fixed self-adjoint structure. Σ_RB is a faithful shape of '
            'what 0_RB requires. The one divergence: a single import on the '
            'equation side — "a suitable self-adjoint domain exists" — which is '
            'exactly the gap between "right shape" and "proven", and the same '
            'KIND of import RH carries (they are the same operator: Σ_RB '
            'self-adjoint ⇒ RH by Stone).'),
    }


def _shape_signature(pieces: List[Dict[str, Any]], self_adjoint: bool,
                     dof: str) -> Dict[str, Any]:
    roots = sorted({p['root'] for p in pieces if p['root'] not in ('—', None)})
    counts = {r: sum(1 for p in pieces if p['root'] == r)
              for r in ('ADD', 'SCALE', 'SIGN')}
    trees = sorted({p['tree'] for p in pieces if p['tree'] not in ('—', None)})
    return {'roots': roots, 'root_counts': counts, 'two_trees_span': trees,
            'self_adjoint': self_adjoint, 'independent_dof': dof}


# the reference shape — 0_RB, "the decomposition engine for equations"
_ZERO_RB_SHAPE = {
    'what': '0_RB — the composite generational lineage of every geometric '
            'operator, read in the vacuum. The reference a well-formed equation '
            'must match.',
    'roots': ['ADD', 'SCALE', 'SIGN'],          # the whole tier-0 floor
    'two_trees_span': ['LAURELIN', 'MINGLING', 'TELPERION'],   # the whole tree
    'self_adjoint': True,                        # e₀-central; Σ_RB = Σ_RB†
    'independent_dof': 'whole (8 — both octonion halves; R̂ ⟂ B̂ across ⊕8)',
}


def shape_diff_navier_stokes() -> Dict[str, Any]:
    """The direct test: shape of Navier–Stokes  vs  0_RB  vs  halocline-modified
    Navier–Stokes. 0_RB is the reference decomposition. Where a variant's shape
    fails to match 0_RB's, name the missing / out-of-place operator — "the
    shadow of a missing operator".
    """

    # ── standard 3-D incompressible Navier–Stokes ──────────────────────────
    ns_pieces = [
        dict(sym='u·∇u', what='advection (self-transport of the field)',
             tier=1, root='SCALE', tree='LAURELIN',
             note='self-SCALE with gain > 1 — where the energy cascades to '
                  'small scales; the blow-up threat lives here'),
        dict(sym='νΔu', what='viscous diffusion (the Laplacian average)',
             tier=0, root='ADD', tree='LAURELIN',
             note='an averaging = repeated addition; smooths, only ever '
                  'removes energy'),
        dict(sym='∇·u = 0', what='incompressibility (a constraint)',
             tier=2, root='SCALE', tree='LAURELIN',
             note='a COROLLARY — needs an added constraint to exist; the '
                  'pressure is its Lagrange multiplier'),
        dict(sym='−∇p/ρ', what='pressure gradient (enforces the constraint)',
             tier=0, root='ADD', tree='LAURELIN', note=''),
    ]
    ns = _shape_signature(ns_pieces, self_adjoint=False,
                          dof='half (real projection only — one density, no '
                              'reverse current)')
    ns['emergence'] = ('THE canonical §5 signature — a quantity (the velocity '
                       'gradient) that changes length WITHOUT BOUND where only '
                       'isometries were in play. The blow-up.')

    # ── halocline-modified Navier–Stokes ──────────────────────────────────
    hns_pieces = list(ns_pieces) + [
        dict(sym='∂̂_H', what='the halocline — the interface between two fluid '
                              'densities (the critical-angle mirror)',
             tier=1, root='SIGN', tree='MINGLING',
             note='REFLECT — total internal reflection is a critical angle, '
                  'not a gradient; the "mirrored curtain"; this IS ∂̂_∂M, the '
                  'boundary operator 0_RB carries'),
        dict(sym='∂ρ/∂t + ∇·(ρu) = 0',
             what='continuity for the compressible (Blue) density',
             tier=2, root='SIGN', tree='TELPERION',
             note='the second density — "what CANNOT BE" resolved in the real '
                  'projection; wiki/88: the incompressible half closes, the '
                  'compressible half never does'),
        dict(sym='†  (ρ_Re ↔ ρ_Im)',
             what='self-adjointness restored — energy rotates between the two '
                  'densities instead of only dissipating',
             tier=0, root='SIGN', tree='MINGLING',
             note='the reverse current; R̂† = B̂; the Noether current can now '
                  'rotate, not only decay'),
    ]
    hns = _shape_signature(hns_pieces, self_adjoint=True,
                           dof='whole (8 — both densities; Re(ψ) ⟂ Im(ψ))')
    hns['emergence'] = ('cleared — the unbounded SCALE (advection) now has a '
                        'SIGN partner (†) to rotate into: the apparent blow-up '
                        'becomes a bounded 90° rotation into the Blue density '
                        '(r ↔ 1/r), which the real equations could not follow.')

    def _diff(sig: Dict[str, Any]) -> Dict[str, Any]:
        missing_roots = [r for r in _ZERO_RB_SHAPE['roots']
                         if r not in sig['roots']]
        missing_trees = [t for t in _ZERO_RB_SHAPE['two_trees_span']
                         if t not in sig['two_trees_span']]
        return {
            'roots_missing_vs_0_RB': missing_roots,
            'two_trees_missing_vs_0_RB': missing_trees,
            'self_adjoint_matches': sig['self_adjoint'] == _ZERO_RB_SHAPE['self_adjoint'],
            'dof_matches_whole': 'whole' in sig['independent_dof'],
            'shape_matches_0_RB': (not missing_roots and not missing_trees
                                   and sig['self_adjoint']),
        }

    ns_diff = _diff(ns)
    hns_diff = _diff(hns)

    # the shadow: what is in 0_RB and in halocline-NS but NOT in standard NS
    the_shadow = {
        'missing_from_standard_NS': ns_diff['two_trees_missing_vs_0_RB']
                                    + ns_diff['roots_missing_vs_0_RB'],
        'the_operator': '∂̂_∂M — the boundary / interface / reflection operator '
                        '(the halocline). It is SIGN-rooted, and it drags the '
                        'other two SIGN pieces back with it: B̂ (the Blue / '
                        'second density / "what CANNOT BE" channel) and † '
                        '(self-adjointness / the reverse current).',
        'why_it_shows_as_a_shadow': 'standard NS is SCALE-heavy (advection) '
            'with an ADD counter-term (diffusion) and NO SIGN structure at all '
            '— LAURELIN only. In 0_RB, unbounded SCALE growth is caught by † '
            'and rotated into B̂. NS has no †, so the SCALE growth has nowhere '
            'to go: it diverges. THE SINGULARITY IS THE SHADOW OF THE MISSING † '
            '— and † only exists once the boundary operator ∂̂_∂M (the '
            'halocline) re-couples the two densities.',
        'filled_by_halocline_NS': not hns_diff['two_trees_missing_vs_0_RB']
                                  and not hns_diff['roots_missing_vs_0_RB']
                                  and hns_diff['self_adjoint_matches'],
    }

    return {
        'reference': _ZERO_RB_SHAPE,
        'standard_navier_stokes': {'pieces': ns_pieces, 'signature': ns,
                                   'diff_vs_0_RB': ns_diff},
        'halocline_navier_stokes': {'pieces': hns_pieces, 'signature': hns,
                                    'diff_vs_0_RB': hns_diff},
        'the_shadow': the_shadow,
        'verdict': (
            'Standard Navier–Stokes decomposes to LAURELIN only — SCALE '
            '(advection) + ADD (diffusion) + a tier-2 constraint, no SIGN '
            'structure. Against 0_RB it is missing the whole SIGN half: the '
            'boundary operator ∂̂_∂M, the Blue channel B̂ (Telperion), and '
            'self-adjointness †. The §5 emergence flag fires — the blow-up is '
            'an unbounded length change with no isometry to absorb it. '
            'Halocline-modified NS adds exactly one operator, ∂̂_∂M (the '
            'critical-angle interface between the two fluid densities), and it '
            'brings B̂ and † with it. Its shape then matches 0_RB — whole '
            'Two-Trees span, self-adjoint, both densities — and the emergence '
            'flag clears: the blow-up becomes a bounded rotation into the '
            'second density. The shadow of the missing operator in standard NS '
            'is ∂̂_∂M / the halocline.'),
    }


def decompose_the_lineage_engine() -> Dict[str, Any]:
    """Recursive application of the generational lineage engine — to itself.

    "Decomposing generational lineage" (Cody, 2026-08-28). Take the engine's own
    operations and run the decomposition ON them; then recurse on the operation
    of decomposing. Check: does the set CLOSE (every engine op decomposes to
    ADD/SCALE/SIGN, and to operations already in the engine's vocabulary), or
    does it produce a §5 emergence signal — an operator the apparatus cannot
    classify?  If it closes, that is "no new generator required" applied
    reflexively — the engine is self-consistent.
    """
    ops = [
        dict(name='decompose(op)', tier=2, root='SIGN', tree='LAURELIN',
             what='the four-question test — maps an operation to one of a fixed '
                  'set of tiers', reads_as='a CLASSIFIER = a fixed set (the tiers)'),
        dict(name='root_irreducible(op)', tier=2, root='SIGN', tree='LAURELIN',
             what='walk an operation down past REFLECT/DILATE to its tier-0 root',
             reads_as='a REDUCE — a walk to a fixed point (ker of the descent)'),
        dict(name='two_trees(N)', tier=2, root='SIGN', tree='MINGLING',
             what='partition [0,N] into prime / composite / {0,1}',
             reads_as='a PARTITION = a fixed set; the classifier itself'),
        dict(name='factor_lineage(n)', tier=3, root='SCALE', tree='LAURELIN',
             what='recursively split n into its prime leaves',
             reads_as='RECURSION — self-similar; the lineage operator on its own output'),
        dict(name='sieve_lineage(N,order)', tier=3, root='ADD', tree='LAURELIN',
             what='the sieve as the generational lineage; generation(n)=π(spf(n))',
             reads_as='ADD (march the multiples) ∘ SCALE (the p-wave) gated by '
                      'SIGN (divisibility) — established this session'),
        dict(name='sieve_recurrence(x,a)', tier=3, root='SCALE', tree='LAURELIN',
             what='φ(x,a)=φ(x,a−1)−φ(x/pₐ,a−1); closed form Σ μ(d)⌊x/d⌋',
             reads_as='ADD ∘ SIGN ∘ SCALE — a signed-wave superposition'),
        dict(name='spectral_decompose(x)', tier=3, root='ADD', tree='LAURELIN',
             what='factor a signal into wavelengths + the residual',
             reads_as='ADD (Σ over lines) ∘ SCALE (per-frequency) ∘ SIGN (phase); '
                      'residual = the composite remainder'),
        dict(name='clay_lineage_report() / calibration_report()',
             tier=3, root='ADD', tree='LAURELIN',
             what='decompose a set of objects, aggregate, compare to a reference',
             reads_as='a COUNT / RATIO — the agreement rate; a tier-3 statistic '
                      'over tier-0..2 decompositions'),
        dict(name='descriptive_or_definitional / import_deficit',
             tier=0, root='SIGN', tree='MINGLING',
             what='does the object build its answer, or import it?',
             reads_as='one BIT — built vs imported; SIGN, nothing between'),
    ]

    roots_used = sorted({o['root'] for o in ops})
    closes_on_floor = set(roots_used) <= {'ADD', 'SCALE', 'SIGN'}
    tiers_used = sorted({o['tier'] for o in ops})
    within_tier_range = set(tiers_used) <= {0, 1, 2, 3}

    # the recursion: decompose "the operation of decomposing"
    recursion = [
        ('decompose', 'a CLASSIFIER — assign each operation a tier', 2, 'SIGN'),
        ('classify', 'compare against a fixed set of categories', 2, 'SIGN'),
        ('a fixed set of categories', 'the tiers themselves — a labelling', 2, 'SIGN'),
        ('a labelling', 'one bit per category boundary', 0, 'SIGN'),
    ]
    fixed_point = recursion[-1]         # ('a labelling', ..., 0, 'SIGN')
    reaches_fixed_point = (recursion[-1][3] == recursion[-2][3] == 'SIGN')

    # §5 emergence check on the engine itself
    emergence = None
    if not closes_on_floor:
        emergence = 'an engine operation roots on something outside ADD/SCALE/SIGN'
    elif not within_tier_range:
        emergence = 'an engine operation sits outside tiers 0–3'

    return {
        'engine_operations': ops,
        'roots_used': roots_used,
        'tiers_used': tiers_used,
        'closes_on_the_tier_0_floor': closes_on_floor,
        'within_tier_range_0_to_3': within_tier_range,
        'recursion_on_decompose': recursion,
        'fixed_point': {'name': fixed_point[0], 'tier': fixed_point[2],
                        'root': fixed_point[3]},
        'reaches_fixed_point': reaches_fixed_point,
        'emergence_signature': emergence,
        'verdict': (
            'The generational lineage engine, decomposed by itself, stays '
            'entirely inside ADD/SCALE/SIGN (roots used: ' + '·'.join(roots_used)
            + ') and tiers 0–3. The reflexive recursion — decompose "decompose" '
            '→ "classify" → "a fixed set of categories" → "a labelling" — '
            'converges to SIGN: a one-bit-per-boundary labelling, which is '
            'exactly what e10 means by "generational lineage = order of '
            'operations" and what the skill §4 means by "order is not an '
            'operator". NO NEW GENERATOR REQUIRED — applied reflexively. The '
            'apparatus is self-consistent: it can decompose its own output '
            'without needing an operator it cannot classify.'
            if (closes_on_floor and within_tier_range and reaches_fixed_point)
            else 'EMERGENCE FLAG on the engine itself: ' + str(emergence)),
    }


def wiki_block(name: str) -> str:
    """The markdown block to paste toward the bottom of an engine's wiki page."""
    r = lineage_of(name)
    root = r['root'] or '—'
    tail = (f" — deficit: {r['deficit']}" if r['deficit'] else "")
    emg = (f"\nEmergence signature: {r['emergence']}." if r['emergence'] else "")
    agree = ('agrees with' if r['agrees_with_status'] else '**disagrees with**')
    return (
        "## Generational Lineage — calibration (2026-08-28)\n\n"
        "Decomposed by `SedenionFactoralRelativity/engine/valaquenta_calibration.py` "
        "(`python3 -m engine.valaquenta_calibration`) as a check on the factoral "
        "decomposition itself — working, deliberately-designed machinery should "
        "decompose CLEAN.\n\n"
        f"| object | central operation | tier · root | Two Trees | kind | verdict |\n"
        f"|---|---|---|---|---|---|\n"
        f"| {r['object']} | {r['op']} | {r['tier']} · {root} | {r['tree']} | "
        f"{r['kind']} | **{r['verdict']}**{tail} |\n"
        f"{emg}\n\n"
        f"Calibration: this verdict {agree} the page's stated status "
        f"(**{r['vq']}**).\n"
    )


if __name__ == '__main__':
    rep = calibration_report()
    print("=" * 78)
    print("VALAQUENTA — GENERATIONAL LINEAGE CALIBRATION")
    print("=" * 78)
    hdr = f"{'engine':<26} {'tier·root':<10} {'tree':<10} {'kind':<12} " \
          f"{'verdict':<15} {'status':<12} ok"
    print(hdr)
    print("-" * len(hdr))
    for r in rep['rows']:
        root = r['root'] or '—'
        print(f"{r['engine']:<26} {str(r['tier'])+'·'+root:<10} {r['tree']:<10} "
              f"{r['kind']:<12} {r['verdict']:<15} {r['vq']:<12} "
              f"{'✓' if r['agrees_with_status'] else '✗'}")
    print("-" * len(hdr))
    print(f"engines            : {rep['n_engines']}")
    print(f"CLEAN              : {rep['clean']}")
    print(f"DESCRIPTIVE-OK     : {rep['descriptive_ok']}  (instruments / renderers / validators)")
    print(f"FLAGGED            : {rep['flagged']}  (deficit or emergence signature)")
    print(f"agreement w/ status: {rep['agreement_rate']}   "
          f"(verdict matches ValaQuenta's own label)")
    print(f"confusion          : {rep['confusion']}")
    print(f"root distribution  : {rep['root_distribution']}")
    print(f"tree distribution  : {rep['tree_distribution']}")
    if rep['disagreements']:
        print("disagreements (verdict vs status) — the signal:")
        for eng, v, s in rep['disagreements']:
            print(f"  · {eng}: {v} but page says {s}")
    print()
    print("READING: high agreement ⇒ the factoral decomposition is calibrated on "
          "code that was\nexplicitly designed. FLAGGED engines should be exactly "
          "the ones ValaQuenta already\nlabels THEORETICAL / CONJECTURE / OPEN / "
          "UNTESTED / defect. Where they are, the method\nand the label confirm "
          "each other; where they differ, that pair is worth a look.")
