# 4.9 The factoral spiral — factoral decomposition as chart geometry

*Tutorial:* [`18_factoral_spiral`](../examples/18_factoral_spiral.py).

`PW13`. The visual proof-of-concept is `two_ring_chart_render.py` in this
repository's root. Spectral analysis IS factoral decomposition, using a different notion of
"factor" — an eigendecomposition factors an operator into (eigenvalue,
eigenvector) pairs the same way integer factorisation decomposes N into
primes. `factoral_spiral()` is the generic instrument: point it at ANY
collection with two chosen numeric readings and see the collection's own
factoral/spectral structure as chart geometry — discrete cells ("windows
of order") a caller can render as open bubbles instead of a raw scatter.

```python
# [EXTENDED layer + matplotlib]  writes two PNG files into the current directory
from engine import factoral_spiral, chart_scale_factor, factor_lineage, euler_phi, vigenere_cipher
from engine.tools import report_factoral_spiral_chart, report_crystal_spiral_chart

# generic — point it at anything with two numeric readings (here: the numbers 2..59, by Omega and phi(n)/n):
my_objects = range(2, 60)
report_factoral_spiral_chart(
    my_objects, ring1=lambda n: float(factor_lineage(n)['omega']), ring2=lambda n: euler_phi(n) / n,
    out_path='spiral.png')

# wired directly to PW11's crystallography — a sequence's OWN recovered
# period drives the chart, distance-mod-period vs log2(distance):
ciphertext = vigenere_cipher([ord(c) - 65 for c in "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG" * 8],
                             key=[3, 9, 15, 2, 7], alphabet=26)
report_crystal_spiral_chart(ciphertext, n=3, out_path='crystal_spiral.png')
# -> period recovered exactly (verified on a real period-7 Vigenere test:
#    1142 repeat-distances, 1142/1142 vote support, cells cluster by
#    log-distance since every distance IS a multiple of the true period)
```

`chart_scale_factor(Z, Z0) = |dGamma/dZ|` is the fold's own derivative, in
closed form — the "phase" information a flat `(Re Γ, Im Γ)` reading loses
when a curved conformal map gets flattened into 2D, made into a real,
computable number instead of a qualitative description of it. Checked
against central-difference numerical differentiation, not just algebra:
max relative error `1.55e-09` over 300 random `(Z, Z0)` pairs.

**Honest note on ring choice, kept in the record rather than smoothed
over:** the first attempt at the WordNet demo (`two_ring_chart_render.py`)
fed *raw* relation counts in as the two rings and got a chart that mostly
saturated near `Γ=1` — the Möbius map asymptotes to the boundary for any
large `|Z|`, so a long-tailed raw count collapses almost everything to one
indistinguishable region. Feeding `compress_count()`'s own bounded,
log-quantized output in as the ring values instead — rather than as a
color overlay on the raw scatter — is what actually shows the coarse-
graining as chart geometry. `report_crystal_spiral_chart()` uses the
compressed form by default for exactly this reason.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
