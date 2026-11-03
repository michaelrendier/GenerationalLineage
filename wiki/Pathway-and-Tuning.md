# 4.4 Walk the pathway / tune a factor search

*Tutorial:* [`17_pathway_and_tuning`](../examples/17_pathway_and_tuning.py).

The **pathway** layer treats factoring as a walk with two pinned anchors (1
and N), not an outward search — the factor is a node on the geodesic
between them, and the walk needs *tuning* per number to resonate onto it.

```python
from engine import spiral_address, pathway_residues, tune_pathway, fermat_path

spiral_address(97)                      # log-radius + angle on the CFRAC spiral
pathway_residues(1451951, mult=1)['factor']   # None — the untuned walk finds nothing in budget
tune_pathway(1451951)                   # {'tuning': 3, 'step': 86, 'factor': (1009, 1439)} — multiplier 3 resonates
fermat_path(3233)                       # {'factor': (53, 61), 'excursion': 0, ...} — balanced: at the anchor
fermat_path(1234007)                    # {'factor': (1009, 1223), 'excursion': 5, ...} — less balanced, further out
```

`[KNOWN — Morrison–Brillhart CFRAC, 1975]`: this is real, sub-exponential
factoring, not a metaphor. What's `[OURS]` is reading the *tuning* itself as
the framework's σ-dilate, and reading the excursion as a difficulty gauge
(§4.5).

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
