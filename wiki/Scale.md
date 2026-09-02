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

## verify

`{'ok': True}` — descend of 15/3 = 5; build_up recovers `y = 4x + 1`; a lone
`(x, y)` is refused.
