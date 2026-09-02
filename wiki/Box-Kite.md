# Box-Kite — the domain geometry

`engine/toolsets/box_kite.py` · line: **both**.

16 Cayley–Dickson placeholders `e0..e15`. The 15 nonzero XOR differences between
them are the **edges** — kinds of relation, not places. A **line** is three
relations that compose: `a ^ b = c`. A **pencil** is the 7 ways to factor one
relation into two others.

## descend (free)

`descend((i, j))` → `edge = i ^ j` (one XOR) and the lines that edge lies on.
`cost = 0`.

```python
from engine import line_descend
line_descend('box_kite', (3, 10))   # {'edge': 9, 'is_edge': True, 'lines': [...]}
```

## build_up (work)

`build_up(edge)` → the **7 pencils** of that edge: unordered `{f, g}`, both
nonzero, `f ^ g == edge`. `cost` = pairs scanned.

## verify

`{'ok': True}` — every edge has exactly 7 pencils; `C(16,2) = 120 = 15 edges × 8
pairs`.
