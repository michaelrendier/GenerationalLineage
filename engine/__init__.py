"""SedenionFactoralRelativity.engine

The FACTORAL DECOMPOSITION TOOL (`lineage`) is imported FIRST and
unconditionally: it is stdlib + numpy only and depends on nothing outside this
repo, so it must stay usable even when the cross-repo Fermat-facet imports are
unavailable. `maths`/`tools` reach into AbrikosovTree, ValaQuenta and
TuringStack; if any of those has moved, the decomposition tool still works and
the failure is reported through `IMPORT_ERROR` rather than taking the whole
package down.
"""

from .lineage import (
    FactoralLineageEngine, GenerationalLineageEngine, Relation, Status,
    run as run_lineage, decompose, factor_lineage, two_trees, TIERS,
    root_irreducible, ROOT_OF, AFF1,
    sieve_lineage, sieve_recurrence,
    cd_mul, unit, sigma_self, sigma_rb, sigma_rb_independent,
    # ring-theory machinery (2026-08-22)
    cd_mul_gf2, all_ones, trace_laplacian_gf2, is_nilpotent_gf2,
    primary_decomposition, von_mangoldt, euler_phi,
    quotient_zero_divisors, fall_test, arith_deriv,
    # fractal decomposition (2026-08-22)
    nonassoc_count, feigenbaum_delta, escape_survives, box_dimension,
    MANDELBROT, BURNING_SHIP,
    smooth_escape, orbit_trap, orbit_curvature, lyapunov_exponent,
    basin_of, newton_basins, label_orbit,
    # the pathway layer (2026-08-22)
    spiral_address, pathway_residues, tune_pathway, decompose_number,
    fermat_path, number_chart_point,
    # the two-ring chart (2026-08-23) -- the Smith-chart fold, generalised
    ring_chart_gamma, two_ring_chart, chart_scale_factor, factoral_spiral, ProcessOperator, pathway_decomposition, cross_ratio,
    SI_BASE, unit_vector, unit_mul, unit_div, unit_lineage_decompose,
    # the crystal + the join (2026-08-23) -- unseen periods from repeat-
    # structure alone (Kasiski/Friedman), and a permutation's order as the
    # lcm/join dual of R8's gcd/meet
    repeat_distances, infer_period_by_stem_vote, vigenere_cipher,
    permutation_cycles, permutation_order_direct, permutation_order_via_stems,
)

from .bio import (
    TOWER_LEVELS, tower,
    molecular_decomposition, dna_decomposition,
    protein_folding_decomposition, genome_decomposition,
)

from .clay import (
    CLAY, generational_lineage_of, clay_lineage_report, check_consistency,
    descriptive_or_definitional, import_deficit,
)

from .spectral import (
    dft, idft, power_spectrum, spectral_lines, reconstruct, spectral_residue,
    autocorrelation, dominant_period, spectral_decompose,
)

from .add_scale_sign import (
    ASS, ASSWord, compose as ass_compose, word as ass_word,
    fast_inverse_sqrt, fisr_word, reduces_everything,
    CAMSHAFT, BRACKET as ASS_BRACKET,
)

from .valaquenta_calibration import (
    ENGINES as VQ_ENGINES, calibration_report, lineage_of as vq_lineage_of,
    wiki_block as vq_wiki_block, decompose_h_rb_hat, shape_diff_navier_stokes, decompose_the_lineage_engine,
)

IMPORT_ERROR = None
try:
    from .tools import (
        report_pieces_and_pathways, report_control_test,
        report_factoral_lineage, report_strut_pair_chart,
    )
    from .maths import (
        quantized_pieces, pathway_leaf_to_root, pathway_root_system_class,
        pi_x_mod16, equidistribution_control_test,
    )
except ImportError as _exc:                       # pragma: no cover
    IMPORT_ERROR = _exc

__all__ = [
    'IMPORT_ERROR',
    # reports
    'report_pieces_and_pathways', 'report_control_test',
    'report_factoral_lineage', 'report_strut_pair_chart',
    # the Fermat-facet inventory and the control
    'quantized_pieces', 'pathway_leaf_to_root', 'pathway_root_system_class',
    'pi_x_mod16', 'equidistribution_control_test',
    # the factoral decomposition tool
    'FactoralLineageEngine', 'GenerationalLineageEngine', 'Relation', 'Status',
    'run_lineage', 'decompose', 'factor_lineage', 'two_trees', 'TIERS',
    'root_irreducible', 'ROOT_OF', 'AFF1',
    'sieve_lineage', 'sieve_recurrence',
    # the biological factoral tower (STUB — structural only, no medical inference)
    'TOWER_LEVELS', 'tower', 'molecular_decomposition', 'dna_decomposition',
    'protein_folding_decomposition', 'genome_decomposition',
    # the generational lineage of the seven Clay Millennium Problems
    'CLAY', 'generational_lineage_of', 'clay_lineage_report', 'check_consistency',
    'descriptive_or_definitional', 'import_deficit',
    # general spectral decomposition (NOT sedenion-specific) — factoring wavelengths
    'dft', 'idft', 'power_spectrum', 'spectral_lines', 'reconstruct',
    'spectral_residue', 'autocorrelation', 'dominant_period', 'spectral_decompose',
    # the ADD:SCALE:SIGN datatype AS AN ENGINE — the tier-0 floor as a value type;
    # the fast inverse square root as its canonical worked example
    'ASS', 'ASSWord', 'ass_compose', 'ass_word', 'fast_inverse_sqrt', 'fisr_word',
    'reduces_everything', 'CAMSHAFT', 'ASS_BRACKET',
    # the ValaQuenta calibration — generational lineage of every VQ engine
    'VQ_ENGINES', 'calibration_report', 'vq_lineage_of', 'vq_wiki_block', 'decompose_h_rb_hat', 'shape_diff_navier_stokes', 'decompose_the_lineage_engine',
    'cd_mul', 'unit', 'sigma_self', 'sigma_rb', 'sigma_rb_independent',
    'cd_mul_gf2', 'all_ones', 'trace_laplacian_gf2', 'is_nilpotent_gf2',
    'primary_decomposition', 'von_mangoldt', 'euler_phi',
    'quotient_zero_divisors', 'fall_test', 'arith_deriv',
    'nonassoc_count', 'feigenbaum_delta', 'escape_survives', 'box_dimension',
    'MANDELBROT', 'BURNING_SHIP',
    'smooth_escape', 'orbit_trap', 'orbit_curvature', 'lyapunov_exponent',
    'basin_of', 'newton_basins', 'label_orbit',
    'spiral_address', 'pathway_residues', 'tune_pathway', 'decompose_number',
    'fermat_path', 'number_chart_point',
    'ring_chart_gamma', 'two_ring_chart', 'chart_scale_factor', 'factoral_spiral', 'ProcessOperator', 'pathway_decomposition', 'cross_ratio',
    'SI_BASE', 'unit_vector', 'unit_mul', 'unit_div', 'unit_lineage_decompose',
    'repeat_distances', 'infer_period_by_stem_vote', 'vigenere_cipher',
    'permutation_cycles', 'permutation_order_direct', 'permutation_order_via_stems',
]
