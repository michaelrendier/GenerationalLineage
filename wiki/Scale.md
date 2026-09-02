# Scale — the multiplicative generator

`engine/toolsets/scale.py` · line: **both** · `SCALE` of the tier-0 floor `Aff(1,ℝ)`.

## descend (free)

`descend(value, reference=1.0)` → `scale = value / reference`. One division; also
returns `ln_scale` and `sign`. `cost = 0`.

```python
from engine import line_descend
line_descend('scale', 15.0, reference=3.0)   # {'scale': 5.0, 'sign': 1, 'cost': 0, ...}
```

## build_up (work)

`build_up({'x': x, 'y': y}, probes=[(x2, y2), …])` recovers `s` (and `a`) for the
map `x → s·x + a`. **One `(x, y)` pair is undetermined** — the ADD term is free —
so with a single reading it raises `AscentNotFree("a second (x, y) reading")`.
With two independent probes it returns `{'scale', 'add', 'cost': n_probes}`.

```python
from engine import line_build_up
line_build_up('scale', {'x': 2.0, 'y': 9.0}, probes=[(5.0, 21.0)])   # s=4, a=1 (y = 4x+1)
```

## the two charts — what SCALE looks like to each jurisdiction

Not two orthogonal Smith charts. **A Smith chart orthogonal to an Apollonian
gasket.** `charts(s)` reads a scale ratio in both jurisdictions at once — still
the free reading, both are single-pass:

| chart | jurisdiction | reading | ruler |
|---|---|---|---|
| **Smith chart** | `GR()` — continuous | `Γ = (s−1)/(s+1)` on the unit disk; exact local scale factor `|dΓ/ds| = 2/(s+1)²` (the flattening artifact) | conformal, gap-free |
| **Apollonian gasket** | `QM()` — discrete | `s` on the integer curvature ladder of the bounded gasket (Descartes 1643, seed `(-1,2,2,3)`): nearest rung, bracketing rungs, BFS generation depth, gaps | integer curvature ladder, tangency-packed |

```python
from engine import line_descend
line_descend('scale', 10.0, reference=4.0, chart=True)['charts']   # s = 2.5
# {'continuous': {'gamma': 0.4286, 'local_scale_factor': 0.1633, ...},
#  'discrete':   {'nearest_curvature': 2, 'bracket': (2, 3), 'generation': 0, ...},
#  'orthogonal': True,
#  'tilt': 'matter/energy is the tilt between the continuous and discrete axes ...',
#  'shared_axis': 'artifact — both rulers are monotone in ln(s); ...'}
```

`sedenion_locus_orthogonality()` runs both charts across the sedenion locus
split by the Two Trees (lower octonion `1..7`, the tree holding `e₀` the anchor;
upper octonion `8..15`, pure imaginary). The continuous order and the discrete
order of the indices **coincide on both trees**, so the apparent shared axis is
returned as `METHOD` — an artifact of two charts both monotone in `ln(s)`, with
`GR`/`QM` attached by hand — **not** an emergent axis at this layer. A later pass
may chase it further. Full context: [`The-Two-Charts-and-Jurisdiction.md`](The-Two-Charts-and-Jurisdiction.md).

## verify

`{'ok': True}` — descend of 15/3 = 5; build_up recovers `y = 4x + 1`; a lone
`(x, y)` is refused; `(Σk)² = 2Σk²` holds to 0 on the gasket seed; an integer
seed stays integer (`6, 11, 14, 15, 18, 23` all present); the Smith fold
round-trips; the sedenion-locus orders coincide (artifact verdict).
