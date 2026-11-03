# 4.3 Ask what tier a named operation is

*Tutorial:* [`04_tier_test`](../examples/04_tier_test.py).

```python
from engine import decompose, TIERS

decompose('fulcrum')
# {'operation': 'fulcrum', 'tier': 2, 'descends_from': 'ker(M - I)', 'status': 'DERIVED',
#  'root': 'SIGN', 'note': 'same computation as origin/anchor/balance', 'known': True}
decompose('factorial')
# {'operation': 'factorial', 'tier': 3,
#  'descends_from': 'order of the coordinate reflection group', 'status': 'DERIVED',
#  'root': 'SIGN', 'note': 'a COUNT — a transposition IS a reflection in x_i = x_j', 'known': True}
```

`TIERS` is the tier table itself, as data — every named operation this
framework uses, its tier, what it descends from, and a one-line note; `decompose()` adds the tier-0 `root` it rolls down to. Look
here before assuming something is primitive.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
