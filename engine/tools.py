"""
GenerationalLineage.engine.tools
==========================================
Runnable reports over engine.maths. Simplified from ValaQuenta's full
EquationModule/registry contract (h_rb_hat/tools.py's pattern) since this
is a standalone repo, not registered inside ainulindale_engine -- same
spirit (maths.py = pure functions, tools.py = runnable reports), no
framework coupling.

Author:  Claude, at Cody's direction -- 2026-07-17
"""

import math
import os

from .maths import (
    quantized_pieces, pathway_leaf_to_root, pathway_root_system_class,
    pi_x_mod16, equidistribution_control_test,
)
from .lineage import (
    two_ring_chart, factoral_spiral, chart_scale_factor,
    repeat_distances, infer_period_by_stem_vote,
)


def report_pieces_and_pathways():
    pieces = quantized_pieces()
    print("=" * 74)
    print("  SEDENION FACTORIAL RELATIVITY — quantized inventory")
    print("=" * 74)
    print()
    print("  PIECES:")
    for k, v in pieces.items():
        print(f"    {k:28s} {v}")
    print()
    print("  PATHWAYS, example (p=97, a real prime):")
    walk = pathway_root_system_class(97)
    print(f"    p=97: nshape={walk['nshape']}  root_pathway={walk['root_pathway']}  "
          f"classification={walk['classification']}  fermat_survives={walk['fermat_survives']}")
    print()
    print("  NOTE (caught 2026-07-17): classify_prime() has NO primality check of its")
    print("  own -- it trusts the caller. Feeding it 91=7*13 (composite) still returns")
    print("  fermat_survives=True, silently wrong. Only call it on real primes from")
    print("  prime_sieve(), never on an arbitrary integer.")
    print("=" * 74)


def report_control_test(N: int = 200_000):
    result = equidistribution_control_test(N)
    print("=" * 74)
    print(f"  THE CONTROL — real pi(x;16,k) up to N={result['N']:,}, "
          f"Monster gap vs Niemeier-covered, vs Dirichlet equidistribution")
    print("=" * 74)
    print()
    print(f"  Total primes in the 8 odd classes: {result['total_odd_class_primes']:,}")
    print(f"  Expected per class if equidistributed: {result['expected_per_class_if_equidistributed']:,}")
    print()
    print("  Counts per class:")
    for k, c in result['counts_per_class'].items():
        tag = 'MONSTER GAP' if k in result['monster_gap_shapes'] else 'dendritic'
        print(f"    N-shape {k:2d} ({tag:12s}): {c:,}")
    print()
    print(f"  Chi-square vs uniform (7 dof): {result['chi_square']}")
    print()
    print(f"  Monster gap {result['monster_gap_shapes']}: "
          f"{result['monster_gap_count']:,} vs expected {result['monster_gap_expected']:,} "
          f"({result['monster_gap_deviation_pct']:+.3f}%)")
    print(f"  Dendritic  {result['dendritic_shapes']}: "
          f"{result['dendritic_count']:,} vs expected {result['dendritic_expected']:,} "
          f"({result['dendritic_deviation_pct']:+.3f}%)")
    print("=" * 74)
    return result


if __name__ == "__main__":
    report_pieces_and_pathways()
    print()
    report_control_test()


def report_factoral_lineage(verbose: bool = True):
    """The factoral decomposition tool — 14 relations, tiered and self-checked.

    R1-R8 are carried from VAPMIP/engines/e10_generational_lineage.py; F1-F6 are
    this repo's, applying the same discipline to factorisation itself. Every
    number is COMPUTED at run time -- nothing here is asserted.
    """
    from .lineage import run as _run, factor_lineage, decompose
    result = _run(verbose=verbose)
    if verbose:
        print("\n  FACTORAL DECOMPOSITION -- worked examples:")
        for n in (97, 360, 1024, 1):
            fl = factor_lineage(n)
            print(f"    n={n:<6} {fl['tree_class']:<42} "
                  f"Omega={fl['omega']:<3} generations={fl['generations']:<3} "
                  f"leaves={fl['leaves_telperion']}")
        print("\n  THE FOUR-PART TEST -- worked examples:")
        for op in ('chirality', 'fulcrum', 'dilate', 'add', 'factoral',
                   'leverage', 'gnarl'):
            d = decompose(op)
            print(f"    {op:<12} tier={str(d['tier']):<5} {d['status']:<10} "
                  f"{d['note'][:52]}")
    return result


def _load_box_kite_maths():
    """Reach ValaQuenta/modules/box_kite/maths.py DIRECTLY, by file path --
    not via `import box_kite`, which pulls in box_kite/tools.py's
    `from ...engine.registry import ...` (a relative import that only
    resolves inside the full ainulindale_engine package tree). maths.py
    itself needs only stdlib (math, typing), so loading it standalone is
    exact -- no framework coupling, same discipline as engine/maths.py's
    guarded reach into h_rb_hat, one level more careful because box_kite's
    OWN package __init__ is not safe to trigger from here."""
    import importlib.util
    _THEPLACE = os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    path = os.path.join(_THEPLACE, 'ValaQuenta', 'modules', 'box_kite', 'maths.py')
    spec = importlib.util.spec_from_file_location('_box_kite_maths', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def report_strut_pair_chart(v=None, verbose: bool = True):
    """THE STRUT-PAIR CHART -- the two-ring chart (lineage.two_ring_chart,
    PW10) applied to a box-kite strut pair (ValaQuenta's
    box_kite/maths.py), instead of impedance.

    FIRST TRIED, AND WORTH RECORDING: strut-INTRINSIC scalars (mean
    skeleton share, mean associator defect per strut) turn out IDENTICAL
    across all 7 struts -- every box-kite is combinatorially the same
    octahedron by construction (README: chart_spectrum is {0,4,4,4,6,6} for
    every strut). Folding two constants gives Γ=0 for all 21 pairs: a real,
    honest null result, not a bug -- structural symmetry between struts is
    invisible to strut-only summaries. To get a non-degenerate pair-wise
    READING you need something that is NOT symmetric under the struts'
    own PSL(2,7) relabelling, which is exactly what a specific object (an
    address) supplies: two struts read differently for a fixed v even
    though the struts are isomorphic to each other.

    So the two rings here are v-DEPENDENT, using box_kite's own chart_of()
    machinery per strut:

        ring1 = CHART ENERGY        chart_projection(v)[s] − [t]:
                                     how much MORE of v's energy strut s
                                     carries than strut t
        ring2 = DIAGONAL IMBALANCE  mean |d+|−|d−| imbalance over strut s's
                                     6 Assessors, minus strut t's -- how
                                     much more one-sided v's overlap is

    v defaults to a SYNTHETIC test vector (a mixed direction touching a few
    basis indices) if none is passed -- labelled synthetic because it is:
    this is a demonstration of the instrument, not a reading of a real
    monad address. Pass a real 16-vector (e.g. from
    VAPMIP/monad_sedenion_addresses.pkl) to get one.

    Anchor Z0 is the MEAN (ring1, ring2) over all 21 pairs -- data-derived,
    not chosen -- so a pair's |Γ| reads as how far ITS coupling, under v,
    sits from the typical pair's, on both axes at once.

    DESCRIPTIVE, not self-tested: PW10 verifies the FOLD is generic (holds
    for any ring pair, any anchor); it does not and cannot verify that
    chart-energy/diagonal-imbalance is the RIGHT pair of rings for struts,
    because there is no independent ground truth to check that choice
    against -- same caveat box_kite.address_census() already carries
    ("descriptive only ... nothing scored against an expectation"). A
    different ring pair is exactly the kind of question this instrument is
    FOR asking; the chart itself does not change, only what feeds it.
    """
    bk = _load_box_kite_maths()
    struts = list(range(1, 8))
    if v is None:
        v = bk.basis_vector((0.7, 1), (0.5, 2), (0.9, 9), (0.3, 12), (0.4, 15))

    ce = bk.chart_projection(v)
    coords = bk.assessor_coordinates(v)
    kites = bk.box_kites()
    imbalance_by_strut = {
        s: sum(coords[(a, b)]['imbalance'] for a, b in kites[s]) / 6
        for s in struts
    }

    pairs = [(s, t) for s in struts for t in struts if s < t]
    raw = {(s, t): (ce[s] - ce[t], imbalance_by_strut[s] - imbalance_by_strut[t])
           for s, t in pairs}
    Z0 = complex(sum(r[0] for r in raw.values()) / len(raw),
                 sum(r[1] for r in raw.values()) / len(raw))

    def ring1(pair): return raw[pair][0]
    def ring2(pair): return raw[pair][1]

    readings = {pair: two_ring_chart(pair, ring1, ring2, Z0,
                                     'chart_energy_diff', 'diagonal_imbalance_diff')
                for pair in pairs}
    if verbose:
        print("=" * 74)
        print("  THE STRUT-PAIR CHART -- box-kite struts on the two-ring fold")
        print("=" * 74)
        print(f"  v = {[round(c, 2) for c in v]}  (synthetic test vector)")
        print(f"  anchor Z0 = {Z0:.3f}  (mean chart-energy-diff, mean "
              f"diagonal-imbalance-diff over {len(pairs)} pairs)")
        print()
        for (s, t), r in sorted(readings.items(), key=lambda kv: kv[1]['abs_gamma']):
            print(f"    struts ({s},{t}): Z={r['Z']:.3f}  "
                  f"Γ={r['gamma']:.3f}  |Γ|={r['abs_gamma']:.3f}")
        print()
        print("  |Γ| near 0 = this pair's v-coupling sits near the 21-pair average")
        print("  on both axes at once; |Γ| can exceed 1 here (unlike impedance,")
        print("  ring1/ring2 are UNSIGNED-DIFFERENCE quantities, not confined to a")
        print("  half-plane, so the fold is not guaranteed inside the unit disk --")
        print("  expected, not a bug). DESCRIPTIVE -- see docstring; strut-")
        print("  intrinsic (v-free) ring choices gave Γ=0 for every pair instead.")
        print("=" * 74)
    return readings


# ── THE FACTORAL SPIRAL — point this at any two-reading collection ─────────
# Cody, 2026-08-25: "this should be a tool in the generational lineage
# engine...spectral analysis IS factoral decomposition using different
# 'factors'...can be directly used by the crystallography portion of the
# engine showing live mathematical structure underlying whatever it's
# pointed at." report_factoral_spiral_chart() is the generic instrument
# (lineage.factoral_spiral, PW13); report_crystal_spiral_chart() below
# wires it specifically to PW11's crystallography (repeat_distances /
# infer_period_by_stem_vote), so a sequence's own recovered period drives
# the chart instead of an arbitrary anchor.

def report_factoral_spiral_chart(objs, ring1, ring2, Z0=None,
                                 ring1_name: str = 'ring1', ring2_name: str = 'ring2',
                                 out_path=None, verbose: bool = True):
    """Run factoral_spiral() over `objs` and (if matplotlib is available)
    render the "open bubbles" chart: one translucent, open-edged circle per
    distinct integer cell (round(ring1), round(ring2)), sized by how many
    objects land there — the discrete "windows of order" as shapes, not a
    raw scatter. Falls back to a text-only report if matplotlib isn't
    importable — never a hard dependency of the engine itself."""
    if Z0 is None:
        vals1 = [ring1(o) for o in objs]
        vals2 = [ring2(o) for o in objs]
        Z0 = complex(sum(vals1) / len(vals1), sum(vals2) / len(vals2)) if objs else complex(1, 0)

    spiral = factoral_spiral(objs, ring1, ring2, Z0, ring1_name, ring2_name)
    cells = spiral['cells']

    if verbose:
        print("=" * 74)
        print("  THE FACTORAL SPIRAL — factoral/spectral decomposition, as chart geometry")
        print("=" * 74)
        print(f"  {len(objs)} objects, anchor Z0={Z0:.3f}, "
              f"rings=({ring1_name}, {ring2_name})")
        print(f"  {len(cells)} distinct cells (windows of order):")
        for key, idxs in sorted(cells.items(), key=lambda kv: -len(kv[1]))[:12]:
            print(f"    cell {key}: {len(idxs)} objects")
        print("=" * 74)

    if out_path:
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
        except ImportError:
            if verbose:
                print("  [matplotlib not available — skipping render, report above stands]")
            return spiral

        fig, ax = plt.subplots(figsize=(8, 8), dpi=160, facecolor='#0a0a12')
        ax.set_facecolor('#0a0a12')
        boundary_pts = [complex(math.cos(t), math.sin(t))
                        for t in [i * 2 * math.pi / 400 for i in range(401)]]
        ax.plot([p.real for p in boundary_pts], [p.imag for p in boundary_pts],
               color='#888888', lw=1.0)

        max_count = max((len(v) for v in cells.values()), default=1)
        for (r1, r2), idxs in cells.items():
            Z = complex(r1, r2)
            from .lineage import ring_chart_gamma
            G = ring_chart_gamma(Z, Z0)
            radius = 0.02 + 0.10 * (len(idxs) / max_count) ** 0.5
            circle = plt.Circle((G.real, G.imag), radius, fill=False,
                                edgecolor='#7fd4ff', linewidth=1.3, alpha=0.8)
            ax.add_patch(circle)
            ax.scatter([G.real], [G.imag], s=6, color='#ffd014', alpha=0.9)

        ax.set_xlim(-1.05, 1.05); ax.set_ylim(-1.05, 1.05)
        ax.set_aspect('equal')
        ax.set_title(f"Factoral spiral: {len(objs)} objects, {len(cells)} open bubbles\n"
                    f"({ring1_name}, {ring2_name}) — bubble size = population",
                    color='#dddddd', fontsize=10.5)
        ax.tick_params(colors='#888888', labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor('#444444')
        fig.tight_layout()
        fig.savefig(out_path, facecolor=fig.get_facecolor())
        if verbose:
            print(f"  Saved {out_path}")

    return spiral


def report_crystal_spiral_chart(seq, n: int = 3, max_period: int = 20,
                                out_path=None, verbose: bool = True):
    """PW11's crystallography (repeat_distances / infer_period_by_stem_vote)
    run through the factoral spiral: each REPEAT DISTANCE is one object,
    ring1 = distance mod the sequence's OWN recovered period (its residue
    class — the period made visible as chart position, not just a printed
    number), ring2 = log2(distance+1) (the same compress_count-style log
    quantization used elsewhere in this project, so long-range repeats
    don't saturate the chart the way raw counts did on the first attempt
    at this — see VAPMIP's two_ring_chart_render.py for that honest
    failure and its fix, ported here as the default rather than repeated)."""
    distances = repeat_distances(seq, n)
    if not distances:
        if verbose:
            print("  no repeated n-grams found — nothing to chart")
        return None
    vote = infer_period_by_stem_vote(distances, max_period)
    period = vote['best_period'] or 1

    def ring1(d):
        return float(d % period)

    def ring2(d):
        return math.log2(d + 1)

    if verbose:
        print(f"  crystal: {len(distances)} repeat-distances, "
              f"recovered period={period} (vote support "
              f"{vote['votes'].get(period, 0)}/{len(distances)})")

    return report_factoral_spiral_chart(
        distances, ring1, ring2, Z0=complex(period / 2.0, 1.0),
        ring1_name=f'distance mod {period}', ring2_name='log2(distance+1)',
        out_path=out_path, verbose=verbose)


def report_add_scale_sign(x: float = 0.15625):
    """The ADD:SCALE:SIGN datatype as an engine in the decomposer suite,
    with the fast inverse square root as the worked example."""
    from .add_scale_sign import ASS, compose, fisr_word, CAMSHAFT, BRACKET
    print("=" * 74)
    print("  ADD:SCALE:SIGN  —  the tier-0 floor as a value type")
    print("=" * 74)
    T = compose(ASS.SIGN(-1), ASS.SCALE(3.0), ASS.ADD(4.0))
    print(f"\n  T = SIGN(-1) ∘ SCALE(3) ∘ ADD(4)  =  {T}")
    print(f"    camshaft {CAMSHAFT}   {BRACKET}")
    print(f"    round-trip (~T∘T)(x)=x : "
          f"{all(abs((~T)(T(v)) - v) < 1e-12 for v in (-2.0, 0.0, 7.5))}")
    w = T.lineage('chrono')
    print(f"    u = {w.u_total():.6g}   Γ = {w.gamma():.6g}   "
          f"firing defect (g-1)ln s = {w.firing_defect():+.6g}")
    print(f"    chrono: {w.as_equation()}")
    print(f"    zeta  : {T.lineage('zeta').as_equation()}")
    print(f"    smith : {T.to_smith()['notation']}")
    print(f"\n  FAST INVERSE SQUARE ROOT  (0x5f3759df)  —  ADD:SCALE:SIGN in log2:")
    for k, v in fisr_word(x).items():
        print(f"    {k:28s} {v}")
    print()
