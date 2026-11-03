# 4.5 Read the chart — Smith-chart-derived instruments

*Tutorial:* [`11_two_ring_chart`](../examples/11_two_ring_chart.py).

`PW8` found that a Smith chart (RF/radar impedance matching, Phillip Smith,
1939) is the *same* Möbius structure — `Γ=(Z−Z0)/(Z+Z0)` — already built
into this framework as `L_(I|O)`. `PW9` applied the methodology directly to
factoring (`number_chart_point`); `PW10` proved the fold itself doesn't care
what the two rings mean — any two quantities can drive it.

```python
from engine import number_chart_point, ring_chart_gamma, two_ring_chart, factor_lineage, euler_phi

number_chart_point(3233, a=61)          # 0.034 — the balanced factor sits near the anchor
number_chart_point(30021, a=10007)      # 0.966 — unbalanced (3×10007), near the horizon

# the GENERAL two-ring fold — pick your own two ring definitions:
ring1 = lambda n: float(factor_lineage(n)['omega'])
ring2 = lambda n: euler_phi(n) / n
two_ring_chart(97, ring1, ring2, Z0=complex(0, 1), ring1_name='Omega', ring2_name='phi/n')
# -> {'Z': (1+0.99j), 'gamma': ..., 'abs_gamma': ..., ...}
```

Radial position on the chart is a difficulty gauge, read at a glance — the
anchor (`Γ≈0`) is "as easy as it gets," the horizon (`Γ≈1`) is "hardest
tested." Because `PW10` proved the fold is generic, the same instrument
applies to anything you can describe with two real numbers — including a
pair of box-kite struts instead of impedance:

```python
# [EXTENDED layer]
from engine.tools import report_strut_pair_chart
report_strut_pair_chart()     # prints all 21 strut pairs, sorted by |Γ|
```

Worth knowing before you read that output: the *first* ring pair tried
(strut-intrinsic scalars) came back `Γ=0` for every single pair — a real
null result, not a bug, because every one of the 7 box-kites is the same
octahedron by construction. The version shipped uses a per-address pair
(chart-energy difference, diagonal-imbalance difference) so the reading is
non-degenerate. Read the function's own docstring before trusting a
strut-pair number; it says exactly what would make one reading better than
another, and admits there's no ground truth yet to check the choice
against.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
