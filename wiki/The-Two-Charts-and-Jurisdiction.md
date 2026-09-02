# The Two Charts — continuous and discrete, each in the other's jurisdiction

**Written 2026-09-02.** Status: **THEORETICAL** — a jurisdiction / projection
*reading* in current ("jurisdictional") mathematics, not a new theory. Sibling
to [`Two-Lines-and-Jurisdiction.md`](Two-Lines-and-Jurisdiction.md): the two
*lines* (descent / ascent) restated as two *charts* (continuous / discrete).
Continues, on the GR/QM side, `Ainulindale/wiki/110_qm_in_gr_gr_in_qm.md` and
`Ainulindale/wiki/93_qm_gr_by_tree.md`.

The thread that produced this page, in order: which scaffold for "Now" is more
accurate — a 3-ring Smith chart or an Apollonian gasket with two interior
basins; whether "the continuous sees the discrete / the discrete sees the
continuous" maths properly; that this is Mandelbrot / Julia; a side-eye at
Collatz; and finally, in code — if `class GR` reads `class QM`'s output it can
only see it through `GR` objects. *"parentage in code is the multi-phasic
anchoring… scope is jurisdiction."*

---

## 1. The two charts

Both objects below are the Möbius group `PSL(2,ℂ)` acting on the disk, in two
regimes: **one continuous one-parameter subgroup** (with its invariant pencil of
circles), and **one finitely-generated discrete subgroup** (with its limit set).

### The Smith chart — how the continuous sees the discrete

The Cayley transform `w = (z−1)/(z+1)` is the textbook continuous→discrete
intertwiner:

- von Neumann — an unbounded self-adjoint generator (continuous spectrum; the
  transmission-line operator on ℝ₊) becomes a bounded unitary on the disk;
- Stone's theorem — the one-parameter flow `e^{itA}` becomes powers of a
  rotation; the line's continuous `Γ(x) = Γ₀·e^{−2iβx}` is rotation about the
  chart centre, and you read **discrete** matching elements by intersecting that
  orbit with the constant-R / constant-X pencil.

Its coordinate circles form a **parabolic pencil** — every one tangent at a
*single* point (the open-circuit point at infinity). One boundary contact. This
is the degenerate chart.

### The Apollonian gasket — how the discrete sees the continuous

The gasket is the **limit set** of a discrete (thin, Kleinian) subgroup
`A ⊂ PSL(2,ℂ)` — generators = inversions in four mutually tangent circles.
Countable generating data; uncountable fractal invariant, Hausdorff dimension
`δ ≈ 1.3057`. Patterson–Sullivan theory makes the exchange a **theorem**: that
`δ` is simultaneously

1. the abscissa of convergence of the *discrete* Poincaré series
   `Σ_{g∈A} e^{−s·d(o,go)}`,
2. the exponent of the *continuous* Patterson–Sullivan measure on the gasket,
3. the bottom of the *continuous* Laplace spectrum on the quotient hyperbolic
   3-manifold: `λ₀ = δ(2−δ)` (for `δ > 1`).

Integer Apollonian gaskets are an orbit of `O_f(ℤ)` for the Descartes quadratic
form `f` — `(Σk)² = 2Σk²`, an integer start makes every curvature an integer for
every generation — and *which* integer curvatures appear is the
Bourgain–Kontorovich–Sarnak local–global statement, its density governed by the
continuous `δ`. The discrete/continuous exchange reaches into which whole
numbers are in the picture.

### Verdict on the "Now" scaffold

The gasket-with-two-interior-basins is the more accurate one, for reasons that
are structural, not aesthetic:

| | 3-ring Smith chart | gasket, two interior basins |
|---|---|---|
| where NOW sits | a ring of finite radius — forces an inside/outside asymmetry and concentric cyclicity | the tangency **seam** between two kissing basins — a contact point, not a region; PAST \| FUTURE as the two basins |
| recursion | 3 hand-picked scale bands, no law | intrinsic Descartes curvature ladder — exact integers, a *guarantee* |
| Flattening Syndrome (`project-flattening-syndrome`) | it **is** a flat-circle projection; depth read as radius → false cyclicity, apparent retrocausality | depth carried as curvature *generation*, not radius — resists the flattening |
| group-theoretically | one generator's invariant pencil (parabolic — all tangent at one point) | the *generated* object: a genuine discrete Kleinian subgroup and its limit set |

The `{4:8:4}` lift — NOW(8) ⟂ PAST-FUTURE(8) (`project-oblique-gear`) — lands
cleanly on the two kissing basins: the seam is NOW, the basins are the two
directions of time. Penrose modifiers then only supply what the gasket genuinely
lacks — 5-fold angular / φ phase structure, and (applied to the two basins) a
controlled break of the exact past/future mirror.

## 2. It is one loop, not a mirror

"Continuous sees discrete" and "discrete sees continuous" are **not opposite
arrows between the same two objects.** They compose:

```
continuum --(Cayley / Smith)--> disk --(discrete Kleinian orbit)--> gasket limit set --(δ(2−δ) = λ₀, Patterson–Sullivan)--> continuous spectrum
```

The Smith chart is the first leg; the gasket is the middle; the
dimension = spectral-gap identity closes it back to the continuum.

The correction to the symmetry — and it is the same correction as §2a of the
README:

| leg | what it is | this engine's line |
|---|---|---|
| Cayley / Smith | a genuine isomorphism (half-plane ≅ disk); the "discreteness" is the *observer's chosen grid* — a reparametrisation | **descent** — the sieve, single pass, `free = True` |
| gasket / Patterson–Sullivan | an **emergence** — genuinely discrete group, genuinely continuous invariant, no observer choice | **ascent** — choice of generators / firing order, reports a `cost` |

Unitary equivalence vs a limit. One free, one paid. *The extinction order is not
the rebirth order.*

## 3. Mandelbrot / Julia — the same duality one degree up

Not a metaphor. It is the parameter-space / dynamical-space duality for a
degree-2 family, and the formal statement that it is the same table is
**Sullivan's dictionary** (Kleinian groups ↔ rational maps).

| | degree 1 (Möbius) | degree 2 (quadratic) |
|---|---|---|
| state-space object | gasket = Kleinian limit set `Λ(A)` | Julia set `J(c)` |
| parameter-space chart | Smith chart (Cayley uniformisation) | Douady–Hubbard exterior chart `Φ : ℂ∖M → ℂ∖D̄` |
| conformal density | Patterson–Sullivan measure, exponent `δ` | measure of maximal entropy on `J` |
| dimension = analytic quantity | `δ(2−δ) = λ₀` (Sullivan) | Bowen's formula: `dim J(c)` = zero of the pressure `P(−s·log\|f′\|)`; real-analytic on hyperbolic components (Ruelle) |

The parameter-chart leg is the **same electrostatic construction** in both: put a
charge on the excluded region, take equipotentials + field lines as the working
grid. Smith chart's constant-R / constant-X circles are the field of a 2-D
dipole; `M`'s external rays are the field of `M` as a charged conductor. In the
quadratic case the shared skeleton is the **angle-doubling map** `θ ↦ 2θ` on
`ℝ/ℤ`, running identically in parameter space (`M`'s rays) and dynamical space
(`J(c)`'s rays); Tan Lei's theorem then says `M` is asymptotically similar to
`J(c)` at Misiurewicz points.

**Where it breaks — the informative break.** Möbius maps have no critical point,
so the mechanism that *defines* `M` (critical orbit decides connectivity;
hyperbolic components; MLC) has no degree-1 analogue. A Möbius family does not
bifurcate → there is **no fractal "Mandelbrot boundary" in impedance space**. The
Smith chart is `M` with its bifurcation set contracted to a point — exactly the
"Smith chart = the degenerate case" of §1.

**Two flavours of "discrete."** Mandelbrot/Julia's discrete side is *symbolic*
(kneading sequences, Hubbard trees, the shift on `{0,1}^ℕ`); the
integer-Apollonian side is a genuine ℤ-lattice (number theory). The analogy
pairs the *dynamics*, not the number theory.

## 4. The Collatz side-eye

The complex Collatz map (Letherman–Schleicher–Wood, 1999) has honest Fatou /
Julia sets, and the conjecture reduces to: *do all the integer orbits sit in one
basin, or is a stray cycle / divergent orbit hiding in the Julia set?* Every
iteration scheme throws that parameter/orbit shadow — including the uncrackable
one.

The engine's version of the same open question: **does every quantum orbit land
in the classical-geometry basin, or do some sit where the mean-field
description has no connected picture to offer?** Semiclassical breakdown *is*
"an orbit outside `M`."

## 5. In code — scope is jurisdiction, parentage is anchoring

If `class GR` consumes output from `class QM`, it can only receive it through
`GR` types.

```
GR.observe(qm) : QM.State -> GR.StressEnergy          # = ⟨ψ| T̂_μν |ψ⟩
```

It **cannot** return a `QM.State` — GR has no such type. This is a **forgetful
functor with a nonempty kernel**: relative phase, the which-path superposition
of the source, the entanglement partition among subsystems with equal local
energy — all in the kernel. "Gravity doesn't break, it gives up" = the kernel is
nonempty and widens as source coherence grows. It is the `|z|²` step — the one
operation with no adjoint (`generational-lineage` §7b;
`Ainulindale/wiki/110`).

The reverse call is type-locked too: `QM` takes `GR.metric` as a `const g_μν`
parameter it may read but not mutate — QFT on curved spacetime. **Each class sees
the other only as an instance of one of its own classes. Neither is a subtype of
the other.**

### scope = jurisdiction

Not lexical scope — the **category of admissible sources**. Diffeomorphism
invariance + the equivalence principle force gravity to couple only to the
symmetric conserved rank-2 tensor, so the boundary is not
encapsulation-by-convention (no reflection, no duck-typing escape hatch) — it is
closer to a fixed bus width. And the adapter is not canonical: `⟨T_μν⟩` in
curved space is defined only up to a finite set of renormalisation constants
(Wald's axioms) — `GR.observe` ships with config flags. In the UFT reading a
jurisdiction is a **band in `u = ln x`** (`Ainulindale/wiki/110`); same
statement.

### parentage = multi-phasic anchoring

There is no `class Physics` in the standard library with `GR` and `QM` as
subclasses. If there were, a `Physics&` reference would hold either and dispatch
on the shared interface. Absent it, you get **peer-to-peer marshalling** — a
hand-written adapter each way — not inheritance.

The missing common parent is the **anchor**: `e₀`, the tilt reference *"never
bracketed… the fixed reference each imaginary group is paired against"*
([`The-Emerger-Ascent-Dual.md`](The-Emerger-Ascent-Dual.md)). "Multi-phasic"
because the anchor is precisely what every phase group is measured against; take
`e₀` out of the room and the two trees go maximally active and asymmetric
(`Ainulindale/wiki/93` §3).

- **Decomposition line** — `Physics → {GR, QM}`, descent, **FREE** — is the one
  nobody can write, because the parent is not there to descend *from*.
- **Emerger line** — build `Physics` up from the two children — is **quantum
  gravity**, the **WORK** direction.
- `GR.observe(QM)` is a **pushforward** (a function — forward, cheap);
  recovering the `QM.State` behind a given `T_μν` is a **fiber** (a whole
  preimage class, no stored tape, uphill). Exactly
  [`Two-Lines-and-Jurisdiction.md`](Two-Lines-and-Jurisdiction.md)'s "the
  adjoint is the one that costs."

## 6. Mapping back to the engine

| this conversation | this engine |
|---|---|
| Smith chart — continuous→discrete, Cayley transform | **decomposition line** — reparametrisation, sieve, `free = True` |
| Apollonian gasket — discrete→continuous, Patterson–Sullivan | **Emerger line** — emergence, choice of generators, reports a `cost` |
| one loop through `PSL(2,ℂ)`, not a mirror | descent ≠ ascent run backwards — two jurisdictions |
| Mandelbrot ↔ Julia (Sullivan's dictionary) | parameter space ↔ dynamical space — same object, two charts |
| the informative break: Möbius doesn't bifurcate | the degenerate case — one generator's invariant pencil |
| Collatz: do all orbits reach one basin? | do all quanta land in the classical-geometry basin? |
| `GR.observe(qm) → GR.StressEnergy`, kernel ≠ ∅ | the `|z|²` step — the one operation with **no adjoint** |
| scope = category of admissible sources | jurisdiction = a band in `u = ln x` |
| parentage = the missing `class Physics` | the anchor `e₀` the Emerger never brackets |

## 7. Honest boundaries

- **Textbook, cited as-is:** the Cayley transform and von Neumann / Stone;
  Sullivan's dictionary; Patterson–Sullivan theory and `λ₀ = δ(2−δ)`; the
  Descartes circle theorem and the Apollonian group as `O_f(ℤ)`;
  Bourgain–Kontorovich–Sarnak; Douady–Hubbard connectivity of `M`; Tan Lei
  similarity; Bowen's formula and Ruelle analyticity; Wald's renormalisation
  axioms for `⟨T_μν⟩`; semiclassical gravity `G_μν = 8πG⟨T̂_μν⟩` and its known
  sub-seam breakdown; the complex Collatz map's Fatou / Julia sets
  (Letherman–Schleicher–Wood).
- **The reading laid on top:** the "continuous sees discrete / discrete sees
  continuous" assignment; the gasket-with-two-basins as the "Now" scaffold; the
  single loop; and the mapping of all of it onto this engine's two lines and
  onto `class GR` / `class QM`. No quantum-gravity theory is claimed — this is a
  reading of the seam, the same posture as `Ainulindale/wiki/110`.

## In the engine

`engine/toolsets/scale.py` carries this as code: `charts(s)` reads a scale ratio
in **both** jurisdictions at once — `continuous` (the Smith fold `Γ = (s−1)/(s+1)`
+ exact `|dΓ/ds|`) and `discrete` (`s` on the integer Apollonian curvature ladder,
Descartes seed `(-1,2,2,3)`, with generation depth). `sedenion_locus_orthogonality()`
runs both across the Two Trees split and returns the `METHOD` verdict — the shared
axis is an artifact of two monotone charts, not an emergent one at this layer.
See [`Scale.md`](Scale.md).

## Related

[`Two-Lines-and-Jurisdiction.md`](Two-Lines-and-Jurisdiction.md) ·
[`The-Emerger-Ascent-Dual.md`](The-Emerger-Ascent-Dual.md) ·
[`The-Generational-Lineage-Engine.md`](The-Generational-Lineage-Engine.md) §4.5
(the Smith-chart-derived instruments), §4.9 (the factoral spiral as chart
geometry) · `Ainulindale/wiki/110_qm_in_gr_gr_in_qm.md`,
`Ainulindale/wiki/93_qm_gr_by_tree.md`, `Ainulindale/wiki/47_the_two_trees.md` ·
`project-flattening-syndrome`, `project-oblique-gear`,
`project-scalar-context-paper`.
