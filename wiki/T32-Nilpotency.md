# T32 Nilpotency — address = path

`engine/toolsets/t32_nilpotency.py` · line: **both**.

Hyperwebster-style base-97 addressing: an integer address decodes (Horner) to a
digit **path**. A path that ends on a zero step **returns nothing** — it is
**nilpotent** (an extinction; the address is a pure multiple of the top place).

## descend (free)

`descend(address, base=97)` → the digit path, its length, and `nilpotent`
(trailing-zero test). One Horner sweep; `cost = 0`.

```python
from engine import line_descend
line_descend('t32_nilpotency', 97*97*5)   # path [5,0,0], nilpotent True
```

## build_up (work)

`build_up(pattern)` → place digits one at a time to realise a target path; the
address is the Horner value. `cost` = digits placed.

## verify

`{'ok': True}` — `[5,0,0]` is nilpotent, `[3,11]` is not; `build_up` round-trips.
