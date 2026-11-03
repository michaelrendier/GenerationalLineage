# 4.2 Decompose one number

*Tutorial:* [`03_decompose_a_number`](../examples/03_decompose_a_number.py).

```python
from engine import decompose_number, factor_lineage, fall_test, \
    primary_decomposition, von_mangoldt, euler_phi, arith_deriv

decompose_number(360)
# {'n': 360, 'ring_fall_survive': {...}, 'cepstral_primary': {2: 3, 3: 2, 5: 1},
#  'omega_distinct': 3, 'Omega_lineage_length': 6, 'lineage_tree': {...},
#  'spiral_address': {...}, 'pathway': {...}, 'number_chart': {...}}

factor_lineage(360)['omega']       # 6 — Ω(360), the lineage length
fall_test(97)['verdict']           # 'SURVIVE' — ℤ/(97) is a field
primary_decomposition(360)         # {2: 3, 3: 2, 5: 1} — the cepstral peaks
von_mangoldt(8)                    # 0.693… = log 2 — 8 = 2³, a prime power
euler_phi(360)                     # 96 — |units of ℤ/(360)|
arith_deriv(360)                   # 852 — the arithmetic derivative, Leibniz on primes
```

`decompose_number` is the single richest call — it bundles every
per-number perspective the engine has (ring-theoretic, cepstral, lineage
tree, spiral address, tuned pathway, Smith-style chart position) into one
dict, the way a lab report bundles every instrument reading for one sample.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
