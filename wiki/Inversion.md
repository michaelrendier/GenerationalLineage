# Inversion — the map between the jurisdictions

`engine/toolsets/inversion.py` · line: **both**.

`J_N : (r, θ) → (1/r, θ + π/2)`. Descent named in ascent terms, and back, is
`J_N`. It is an involution **up to a quarter turn**: four applications return to
identity; two give a point inversion `(r, θ+π)` — same `r`, opposite direction,
**not** home. That "twice is not home" is the extinction-order ≠ rebirth-order
fact in one operator.

## descend (free)

`descend((r, θ))` → one application of `J_N`. Singular at `r = 0` (the
zero-divisor locus). `cost = 0`.

## build_up (work)

`build_up((r, θ))` → apply `J_N` until the point returns to itself; reports the
orbit and `cost = period = 4` — the cost of a full round trip between descent
and ascent. `half_way_is_home` is `False`.

## verify

`{'ok': True}` — `J_N` sends `r=2` to `0.5`; `J_N⁴ = id`, `J_N² ≠ id`.
