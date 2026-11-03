# 4.8 The reports

*Tutorial:* [`90_extended_fermat_facet`](../examples/90_extended_fermat_facet.py) (Extended layer).

```python
# [EXTENDED layer for the engine.tools reports; report_emergence and report_ping are Core]
from engine.tools import report_pieces_and_pathways, report_control_test, \
    report_factoral_lineage, report_strut_pair_chart

report_pieces_and_pathways()    # the Fermat-facet inventory
report_control_test()           # real π(x;16,k) vs Dirichlet equidistribution
report_factoral_lineage()       # the full 44-relation run, plus worked examples
report_strut_pair_chart()       # §4.5's box-kite application
# §4.9 — report_factoral_spiral_chart(objs, ring1, ring2) and report_crystal_spiral_chart(seq) take
# arguments; see the worked calls in §4.9 above.

from engine import report_emergence
report_emergence()              # §4.14 — the ascent dual; bracketing & firing order

from engine import report_ping
report_ping(3233)               # §4.15 — the Emerger–Lineage unification / regime classifier
```

`engine/oscilloscope.py` (Extended layer) renders the two-panel Fermat→Riemann SVG
(`python3 engine/oscilloscope.py <N>`, which writes `factorial_oscilloscope.svg` into the repository root) — "Fermat Defines. Riemann Fires.":
the Fermat panel is the prompt (which N-shape, which root-system pathway),
the Riemann panel is the response (real prime-density deviation from
Dirichlet equidistribution), a dashed connector line linking one number's
channel across both.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
