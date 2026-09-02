# Archimedes Screw — the log-pitch of the ladder

`engine/toolsets/archimedes_screw.py` · line: **both**.

The machine (a logarithm) distinct from the medium it lifts. A step from `a` to
`b` is a **pitch** of `ln(b/a)`; the tier boundaries sit at a constant pitch
`ln 2` (the Cayley–Dickson doubling).

## descend (free)

`descend((a, b))` → `pitch = ln(b/a)`, plus `rungs_equiv = pitch / ln 2`. One
log; `cost = 0`. `|pitch| < ln 2` marks a prime-gap-like step.

## build_up (work)

`build_up(height)` — climb `height` natural-log units in rungs of `ln 2`, then
lift the **remainder by hand**. `cost` = rungs climbed; `remainder_by_hand` is
the work the ladder can't do.

## verify

`{'ok': True}` — pitch of `2 → 4` is `ln 2`; climbing `3.5·ln 2` is 3 rungs plus
`0.5·ln 2` by hand.
