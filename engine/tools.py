"""
SedenionFactoralRelativity.engine.tools
==========================================
Runnable reports over engine.maths. Simplified from ValaQuenta's full
EquationModule/registry contract (h_rb_hat/tools.py's pattern) since this
is a standalone repo, not registered inside ainulindale_engine -- same
spirit (maths.py = pure functions, tools.py = runnable reports), no
framework coupling.

Author:  Claude, at Cody's direction -- 2026-07-17
"""

from .maths import (
    quantized_pieces, pathway_leaf_to_root, pathway_root_system_class,
    pi_x_mod16, equidistribution_control_test,
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
