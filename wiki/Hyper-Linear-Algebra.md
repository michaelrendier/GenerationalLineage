# 4.17 The hyper-linear algebra decomposition  `[TUTORIAL — multiplication as a regular representation]`

`engine/toolsets/hyper_linear.py` · *Tutorial:* [`29_hyper_linear`](../examples/29_hyper_linear.py). Notebook:
[`notebooks/01_hyper_linear_algebra_decomposition.ipynb`](../notebooks/01_hyper_linear_algebra_decomposition.ipynb)
(executed, real captured output). Sedenion-side companion (sibling repository):
`SedenionSpectralRelativity/hyper_linear_bridge.py`.

`a*b` read as a regular-representation matrix: every row of the schoolbook
addition matrix is exactly ONE tier-0 SCALE op (`L_d`, multiply by that
digit of `b`) composed with a shift (`T^r` — also just SCALE, by the base).
`ADD` enters exactly once, summing the rows. `TIERS['hyper-linear']` in
`engine/lineage.py` records this: descends from SCALE alone, nothing above
tier 0 is needed until the final sum.

```python
from engine.toolsets import hyper_linear as hl
from engine.lines import AscentNotFree

d = hl.descend(1546854629, 7283619945)
d['rows']                  # one dict per digit: {row, digit, operator: "L_d o T^r", spills}
d['n_spilling_rows']       # 4 — rows whose partial product ran to an 11th digit
d['dft_reconstruction_exact']   # True — reuses engine.spectral.dft, the convolution theorem

try:
    hl.build_up({'product': d['product']})          # raises AscentNotFree —
except AscentNotFree as e:                          # the bare product under-determines
    e.owed                                          # which rows spilled; that recovery
                                                    # is exactly as hard as factoring it
hl.build_up({'product': d['product'], 'a': 1546854629})   # -> free again: one division
                                                            # recovers b, then the spill
                                                            # pattern reads straight off it
```

*Reading:* the DECOMPOSITION line is genuinely free here — no toolset in
this engine needs less than `hyper_linear` does per row. The EMERGER line
is the honest surprise: "which rows had 11 digits" looks like it should be
readable off the 20-digit answer alone, and it provably is not — recovering
it from the bare product is the same hardness class as factoring the
product, and `build_up` refuses rather than pretend otherwise. Supplying
either factor (not both) collapses the ascent back to free. Verified
against `a=1546854629, b=7283619945` (the worked example used throughout):
product exact, DFT reconstruction exact, 4 spilling rows, refusal on the
bare product, and full recovery from one factor — all checked live in
`verify()`.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
