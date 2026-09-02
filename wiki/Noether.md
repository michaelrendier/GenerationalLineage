# Noether — the invariant the domain conserves

`engine/toolsets/noether.py` · line: **both**.

The two trees counter-rotate: along any decomposition the red current and the
blue current trade, and their sum is fixed. `J_red + J_blue = const`.

## descend (free)

`descend(readings)` — `readings` is a list of `(j_red, j_blue)` pairs taken
along a descent. Checks the sum held (within `tol`). One pass; `cost = 0`.

## build_up (work)

`build_up(orders, total)` — `orders` is a list of candidate emergence orders,
each a sequence of per-step red-current increments. Keeps those whose running
sum stays in `[0, total]` and ends at `total`. `cost` = orders scanned. This is
the conservation law **filtering the legal ascent set**.

## verify

`{'ok': True}` — a constant-sum synthetic conserves, a drifting one does not; the
filter keeps only the order that respects the total.
