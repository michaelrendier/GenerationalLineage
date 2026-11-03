# 4.7 The fractal block

*Tutorial:* [`13_fractal_block`](../examples/13_fractal_block.py).

The tower's highest-order rung: **a fractal is the higher-order
generational lineage of a toroidal bifurcation, which is the lineage of a
ring, which is the lineage of a circle.**

```python
from engine import escape_survives, box_dimension, lyapunov_exponent, \
    newton_basins, feigenbaum_delta, MANDELBROT, BURNING_SHIP

escape_survives(complex(-0.5, 0.5), MANDELBROT, maxiter=200)
box_dimension(BURNING_SHIP, (-2, 1), (-2, 1))   # {'dimension_estimates': [1.55, 1.56], ...}
lyapunov_exponent(3.5699)                       # ≈-0.004 — the Feigenbaum accumulation point
newton_basins(5, N=48)['n_basins']              # 5 — the 5 linear factors of z⁵−1
```

The library is the control set: any of the 200+ Ultra Fractal formulas in
`wiki/fractals/` of the sibling Ainulindale repository can drive `escape_survives`/`box_dimension`, so
a claimed dimension always has an independent generator to check it against
— Mandelbrot (`D≈1.3`), the Julia set at `−0.8+0.156i` (`D≈1.6`), Burning
Ship (`D≈1.56`): three different, real, checkable dimensions, not one
number asserted.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
