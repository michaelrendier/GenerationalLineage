# The Two Lines — and jurisdiction

`engine/lines.py`

The Generational Lineage engine runs in two directions. They are **not one
computation run backwards.** They are two jurisdictions.

| line | direction | question | anchor | cost |
|---|---|---|---|---|
| **decomposition** | descent | "what built this" | `engine/lineage.py` | **free** |
| **emerger** | ascent | "what does this build" | `engine/emerger.py` | **work** |

> The extinction order is not the rebirth order. Extinction is free; rebirth
> requires work.

## Descent is free

The deductive sieve of Eratosthenes: mark the multiples, read off what is left.
Single pass, no search, no stored tape — forward-propagating, the direction the
maths is built to go. `descend()` on any toolset returns `free = True`,
`cost = 0`.

## Ascent is work

Induction. To rebuild an object you must **choose** — which bracketing, which
firing order (4 legal of 120), which pitch to climb, which pencil factors a
relation into two. Choice is work. `build_up()` searches or needs an added
constraint and reports a `cost`; a descent-only toolset raises `AscentNotFree`
and names what the caller owes.

## The adjoint, not the companion

One direction is the **adjoint** of the other, and the adjoint is the one that
costs. When GR looks at QM it describes QM in GR's terms; when QM looks at GR it
sees GR in QM's terms — the same object, two jurisdictions, one way free and the
other paid. Back-propagating weights is not free; forward-propagating instinct
with a jurisdictional desire is built in.

`engine/toolsets/inversion.py` (`J_N : (r,θ) → (1/r, θ+π/2)`) is the map between
them. Apply it four times and you are home; twice and you are point-inverted,
**not** home — "the orders are not the same" in one operator.

## The contract

Every toolset in `engine/toolsets/` (and `add_scale_sign.py`, `oscilloscope.py`):

    NAME        str
    LINE        "decomposition" | "emerger" | "both"
    descend(x, **k)       -> dict   (free=True, cost=0)
    build_up(target, **k) -> dict   (free=False, cost=<steps>) or raises AscentNotFree
    verify()             -> dict   (ok=<bool>)

`engine/lines.py`: `describe_lines()`, `verify_all()`, `descend(name, …)`,
`build_up(name, …)`, `DECOMPOSITION_LINE`, `EMERGER_LINE`, `TOOLSETS`.

Per-toolset pages: [Scale](Scale.md) · [Units](Units-and-the-Equation-Index.md) ·
[Box-Kite](Box-Kite.md) · [Noether](Noether.md) ·
[Archimedes-Screw](Archimedes-Screw.md) · [Inversion](Inversion.md) ·
[T32-Nilpotency](T32-Nilpotency.md) ·
[ADD:SCALE:SIGN](ADD-SCALE-SIGN-Datatype.md).
