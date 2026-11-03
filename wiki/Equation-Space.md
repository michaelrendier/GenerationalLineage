# 4.18 The Equation Space Engine — steering by a collapse function's own gradient

`engine/toolsets/equation_space.py` · *Tutorial:* [`30_equation_space`](../examples/30_equation_space.py). Notebook:
[`notebooks/02_equation_space.ipynb`](../notebooks/02_equation_space.ipynb).
Sedenion-side companion (sibling repository): `SedenionSpectralRelativity/equation_space_engine.py`.

A `rho(s) >= 0` — a continuous "distance to the interesting locus"
function — turns a discrete membership test ("is s special") into
something you can take a gradient of. `descend()` reads `rho` and its
gradient at one point, free. `build_up()` walks from a start point to
`rho=0` by gradient descent, cost = steps, and genuinely refuses
(`AscentNotFree`) if the walk stalls or the locus isn't reachable in
budget — the same shape as every other toolset's ascent.

Two diagnostics beyond the basic contract: `classify_singularity()` —
is the locus a **fold** (`rho` falls off linearly on both sides, an A2
caustic, a genuine structural collapse) or a **smooth minimum**
(quadratic falloff, `rho` just happens to get small)? — and
`steering_correlation()` — does an independent, cheap compass signal
(computed with no reference to `rho` at all) predict `|grad(rho)|`, the
actual expensive steering direction?

```python
from engine.toolsets import equation_space as eqs

eqs.descend(0.5+0.1j)                    # rho and its gradient at one point — free
result = eqs.build_up({'start': 0.5+0.1j})   # walk to rho=0 — cost=19 steps, converges
eqs.classify_singularity(result['s'])    # is_fold_caustic: True
eqs.steering_correlation(eqs._gamma_curvature)   # pearson ~0.97
```

*Reading:* the built-in `rho` is Smith's own `Gamma(s)=(s-1)/(s+1)`
(`scale.py`, extended here to complex `s`), distance to the diagonal ray
`{c(1+i)}`. Its zero locus, found here by pure gradient descent with no
sedenion machinery at all, is `center=i, radius=sqrt(2)` — matching, to
within tolerance, the same circle found independently via an actual
sedenion zero-divisor construction (`prime_gauge_sedenion.py` in the
sibling SedenionSpectralRelativity repository). Two unrelated methods, same
answer — the closest thing here to an independent cross-check of that
earlier result.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
