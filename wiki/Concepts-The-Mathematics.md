# 2. The mathematics — same object, or two things kept in sync by hand?

Same object. `FactoralLineageEngine` — the class that runs every relation
below; it extends `GenerationalLineageEngine`, which owns the inherited R-series — is not a program *about* a separate body of
theory: it is the generational-lineage discipline, executed. The base domain it decomposes
against is exact and total:

```
TELPERION   PRIME       defined by what it CANNOT be decomposed into
LAURELIN    COMPOSITE   defined by what it IS decomposed into
MINGLING    0 and 1     neither — the identities of ADD and SCALE
```

Measured over `[0, 100000]`: `2 + 9,592 + 90,407 = 100,001` — every integer,
zero overlap, zero remainder (`F1`, below). Every other relation in the
engine is a further decomposition *inside* this domain, checked against it
the same way F1 checked the domain itself: propose, then measure, then
report which of the three Status values came back. There is no separate
"real math" this code approximates — when a relation says `HOLDS`, that is
the mathematics, not a report on it.

The four-question tier test any named operation goes through, in order:

1. **Is it a count or ratio of something else?** → tier 3, DERIVED.
2. **Is it a fixed set?** → tier 2, DERIVED.
3. **Does it change length?** → needs DILATE. **Preserve length?** →
   reachable from REFLECT.
4. **Does it need an added constraint to exist?** → a COROLLARY, not a
   geometry (e.g. `leverage` needs rigidity; remove rigidity and the
   `fulcrum` survives, `leverage` doesn't).

Only what survives all four is a candidate primitive. `decompose(op_name)`
runs this test and hands back the tier — see §4.3.

## 2a. Two lines — and why their maths differs by direction

The engine runs in two directions, and they are **not the same computation run
backwards**. They are two jurisdictions:

```
DECOMPOSITION LINE   descent   "what built this"       anchor: engine/lineage.py
EMERGER LINE         ascent    "what does this build"   anchor: engine/emerger.py
```

> *The extinction order is not the rebirth order. Extinction is free; rebirth
> requires work.*

**Descent is the deductive sieve of Eratosthenes** — mark the multiples, read
off what is left. Single pass, no search, no stored tape. It is
forward-propagating: the direction the maths is *built* to go. On any toolset,
`descend()` costs nothing (`free = True`, `cost = 0`).

**Ascent is induction** — to rebuild an object you must *choose*: which
bracketing, which firing order (4 legal of 120), which pitch to climb, which
pencil factors a relation into two. Choice is work. On any toolset, `build_up()`
searches or needs an added constraint, and reports a `cost`; a descent-only
toolset *refuses* and names what the caller owes.

One direction is an **adjoint** of the other, not a companion — and the adjoint
is the one that costs. (When GR looks at QM it describes QM in GR's terms;
when QM looks at GR it sees GR in QM's terms — same object, two jurisdictions,
one way free and the other paid.) `engine/toolsets/inversion.py` (`J_N`) is the
map between them: apply it four times and you are home; twice and you are
point-inverted, *not* home — the "orders are not the same" fact in one operator.

See §4.16 for the toolsets, `engine/lines.py` for the registry, the [Tools Reference](Tools-Reference.md) for every tool
defined, and `python3 -m engine --lines` for the roster printed.

## 2b. The two charts — continuous and discrete, each in the other's jurisdiction

The two lines have a geometric restatement worth keeping here, before the tutorial
proper, because it is the same asymmetry in a different vocabulary.

**The Smith chart is how the continuous sees the discrete.** The Cayley transform
`w = (z−1)/(z+1)` is the textbook continuous→discrete intertwiner (von Neumann: an
unbounded self-adjoint generator becomes a bounded unitary; Stone's theorem turns
a one-parameter flow into a circle rotation you can stroboscope). Its coordinate
circles are a *parabolic pencil* — all tangent at one point. The degenerate chart.

**The Apollonian gasket is how the discrete sees the continuous.** It is the limit
set of a discrete (thin, Kleinian) subgroup of `PSL(2,ℂ)`: countable generating
data, uncountable fractal invariant. Patterson–Sullivan theory makes the exchange
a theorem — the Hausdorff dimension `δ` is at once the abscissa of a *discrete*
orbit sum and the bottom of a *continuous* Laplace spectrum, `λ₀ = δ(2−δ)`. The
integer gasket is an `O_f(ℤ)` orbit of the Descartes form — the discreteness
reaches into which whole numbers appear (Bourgain–Kontorovich–Sarnak).

Both are `PSL(2,ℂ)` on the disk — one continuous one-parameter subgroup with its
invariant pencil, one finitely-generated discrete subgroup with its limit set.
They are **not mirror images.** They compose into one loop:

```
continuum --(Cayley / Smith)--> disk --(discrete Kleinian orbit)--> gasket limit set --(δ(2−δ)=λ₀)--> continuous spectrum
```

The Cayley leg is a genuine isomorphism — its "discreteness" is the observer's
chosen grid, a reparametrisation (**descent: free**). The gasket leg is an
*emergence* — genuinely discrete group, genuinely continuous invariant, no
observer choice (**ascent: work**). The §2a free/paid split, one row up in
abstraction.

`Mandelbrot ↔ Julia` is this exact duality one polynomial degree higher —
parameter space vs dynamical space — and the statement that the two are columns of
one table is **Sullivan's dictionary** (Kleinian groups ↔ rational maps). Where it
breaks is informative: a Möbius family has no critical point, so it does not
bifurcate, so there is no fractal "Mandelbrot boundary" in impedance space — the
Smith chart is `M` with its bifurcation set contracted to a point.

**In code:** if `class GR` reads output from `class QM`, it receives it only
through `GR` types — `GR.observe(qm) : QM.State → GR.StressEnergy`, i.e.
`⟨ψ|T̂_μν|ψ⟩`, a forgetful functor whose kernel (relative phase, the which-path
superposition of the source, the entanglement partition) is exactly what "gravity
gives up on." **Scope is jurisdiction; parentage** — the `class Physics` neither
theory subclasses — **is the anchor** (`e₀`, the reference the Emerger never
brackets). Writing `Physics → {GR, QM}` is the free descent nobody can perform,
because the parent is not there; building `Physics` up from the two children is
quantum gravity, the work direction. `GR.observe(QM)` is a pushforward (forward,
cheap); recovering the `QM.State` behind a given `T_μν` is a fiber (a whole
preimage class, no stored tape, uphill) — "the adjoint is the one that costs."

Full treatment, with the Collatz case and the conversation it came from:
[`wiki/The-Two-Charts-and-Jurisdiction.md`](The-Two-Charts-and-Jurisdiction.md).

*Provenance.* The Cayley transform and the Smith chart, von Neumann's and Stone's theorems, Patterson–Sullivan theory,
Bourgain–Kontorovich–Sarnak and Sullivan's dictionary are **ESTABLISHED** mathematics. Reading them together as the free/paid split of
§2a is **OURS**. The `GR`/`QM` paragraph is an illustration of the idea in code, not code in this repository (no `class GR` or
`class QM` exists here), and its claim about quantum gravity is **THEORETICAL**.

*Part of the [Manual](README.md) of the [Generational Lineage Engine](../README.md). Section numbers (§) are kept from the engine's original single-file tutorial so earlier citations stay valid.*
