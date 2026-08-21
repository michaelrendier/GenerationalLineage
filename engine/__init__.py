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
    cd_mul, unit, sigma_self, sigma_rb, sigma_rb_independent,
)

IMPORT_ERROR = None
try:
    from .tools import (
        report_pieces_and_pathways, report_control_test,
        report_factoral_lineage,
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
    'report_factoral_lineage',
    # the Fermat-facet inventory and the control
    'quantized_pieces', 'pathway_leaf_to_root', 'pathway_root_system_class',
    'pi_x_mod16', 'equidistribution_control_test',
    # the factoral decomposition tool
    'FactoralLineageEngine', 'GenerationalLineageEngine', 'Relation', 'Status',
    'run_lineage', 'decompose', 'factor_lineage', 'two_trees', 'TIERS',
    'cd_mul', 'unit', 'sigma_self', 'sigma_rb', 'sigma_rb_independent',
]
