# Sedenion Factoral Relativity

Recursive factorization, à la Laplacians — same operator, different facet.

## What this is

`H_hat_RB` (the RedBlue Hamiltonian, `ValaQuenta/modules/h_rb_hat/`) has
multiple σ-facets: σ→∞ is the Fermat facet (no rational solutions, the
forbidden zone), σ=½ is the Riemann facet (the critical line, the zeta
zeros). Just as a Laplacian's spectrum looks different depending on the
domain you restrict it to while remaining the same operator, this project
treats **factorization itself as relative to which facet you're standing
at** — not one fixed algebraic test, but a family of them, related by the
same recursive Cayley-Dickson tower construction at different scales.

The Fermat facet already has a working engine:
[`AbrikosovTree/engine/telperion_engine.py`](../AbrikosovTree/engine/telperion_engine.py)
("Telperion" / the Zero Lattice tree). It doesn't search for whether a
number factors — it reads the answer directly off the number's position
in a 9-level Cayley-Dickson tower (ℝ → T_256): a composite's factor pair
exposes as a real zero-divisor collision at k=4 (the sedenion level) and
the number "falls"; a prime has no factor pair to expose, so it survives
the whole walk to k=8. Primes are literally the leaves of this tree —
not a metaphor, `classify_prime()`'s own `fermat_survives` flag is
definitional, not searched for.

**This project's job is the Riemann facet's sibling of that same
mechanism — deliberately named "factoral," not "spectral", to keep it
separate from `UDEO_RSA_DEMO.py`'s Method 3 ("Sedenion Spectral
Relativity," a σ-face *geodesic distance* metric, already tested against
RSA and found at chance).** Factoral relativity isn't about distance
between two points under a metric — it's about which numbers get
extinguished, and which survive, changing with which facet of the same
operator you're standing at.

### On the spelling: "factoral," not "factorial"

Renamed 2026-08-21 (Cody). **Factoral** — *of, or pertaining to, factors*.
The old spelling collided with two things that are not this:

- `n!`, the factorial function, which has nothing to do with the subject;
- `A!` in the `0_RB` context, which `.clauderc_canonical_maths` records
  explicitly as meaning **`A†`, the adjoint — "NOT factorial, do not
  conflate."**

The original naming argument is unchanged and still load-bearing:
*factoral*, not *spectral*, because the target is a discrete fall/survive
condition, not a distance under a metric. The rename only removes the
collision with the exclamation-mark notation.

## The control

Stated plainly, 2026-07-17: **the zeta function is the control.** The
geometric tree is a candidate mechanism, not ground truth. Whatever it
predicts about how primes distribute across N-shapes, root systems, and
fall/survive branches has to be checked against the real, counted order
primes actually grow in — governed by the zeros of the relevant Dirichlet
L-functions (Dirichlet's theorem: primes are asymptotically
equidistributed among the φ(16)=8 residue classes coprime to 16). Same
honest-scoring discipline as every other engine in this framework:
propose, then check against a real control, not another layer of the
same geometry.

## Correction, same day: the tree is a consequence, not the source

`FourthAgePapers/FermatMonster/engine/fermat_monster_engine.py`'s own
docstring states the actual foundational claim — the generalized Fermat
equation (x^l+y^m=z^n, independent exponents) IS the Monster Group + 70
Schellekens siblings (71 holomorphic c=24 VOAs), Cody's "Nightmare
Group" — and explicitly lists the ZD-cascade/leaf-tree mechanism this
project is built on as a **consequence** of that claim, not the bridge
itself. See the wiki page for the full correction. Everything in this
README describing the tree as foundational should be read with that
hierarchy in mind.

## Structure

```
engine/
  maths.py     — quantized pieces (CD tower levels, N-shapes, root systems,
                 ZD constellations, Monster gap) and pathways (leaf-to-root
                 walk, root-system classification), plus the control test
                 (real π(x;16,k) vs Dirichlet equidistribution). Imports
                 telperion_engine.py and h_rb_hat/maths.py directly — no
                 reimplementation of either.
  lineage.py   — THE FACTORAL DECOMPOSITION TOOL. 14 self-checked relations:
                 R1–R8 carried from VAPMIP/engines/e10_generational_lineage.py,
                 F1–F6 this repo's own. stdlib + numpy only; depends on
                 nothing outside this repo, and is imported first and
                 unconditionally by engine/__init__.py for that reason.
  tools.py     — runnable reports over maths.py and lineage.py.
  oscilloscope.py — the two-panel Fermat→Riemann oscilloscope.
wiki/
  Sedenion-Factoral-Relativity.md — fuller write-up, orientation
  (leaf/root, dendritic/tap/clonal root systems), open design questions.
```

## The factoral decomposition tool — `engine/lineage.py`

Added 2026-08-21. The Generational Lineage engine, carried over from
`VAPMIP/engines/e10_generational_lineage.py` so this repo has the
decomposition machinery locally instead of reaching across repos for it.

A decomposition tool is not an accessory here — it *is* the instrument. If
factorisation is relative to which σ-facet you stand at, then the first thing
you need is a way to tell a **primitive** operation from a **derived** one, and
to say what any named "geometry" descends from.

```
python3 engine/lineage.py          # 14/14, ~20s
```

**What it gives this repo that it did not have:**

**1. A domain to decompose against.** The Two Trees partition every integer,
exactly and with no overlap — Telperion = PRIME (defined by what it *cannot* be
decomposed into), Laurelin = COMPOSITE (defined by what it *is* decomposed
into), Mingling = `{0, 1}` (neither, because they are the identities of ADD and
SCALE — which is also *why* neither can be prime). Measured over `[0, 100000]`:

```
2 mingling + 9,592 prime + 90,407 composite = 100,001 = N+1     exact
```

**2. A tier test**, so a named geometry can be shown derived rather than assumed
primitive. Four questions asked in order (`decompose()`):

```
chirality  → t3 DERIVED    a count: the parity of a reflection count
fulcrum    → t2 DERIVED    a fixed set: ker(M − I), same computation as
                           origin / anchor / balance — one object, four names
dilate     → t1            primitive at t1, and INDEPENDENT of reflect
add        → t0 PRIMITIVE  irreducible; identity 0
leverage   → t3            a COROLLARY, not a geometry — it needs rigidity
                           added; remove that and the fulcrum survives while
                           leverage does not
gnarl      → UNPLACED      the emergence signal, not a licence to invent a tier
```

**3. `factor_lineage(n)`** — the generational lineage of a factorisation.
Generation = depth in the recursive factor tree; a prime is a leaf, a composite
an internal node. `Ω(n)` is not a statistic *about* `n` — it is the **length of
its lineage**, the number of tier-0 SCALE operations that build `n` from the
multiplicative identity. Verified over `[2, 3000)` with zero disagreements.

**4. `gcd` as the lowest common ancestor**, measured over 20,000 random pairs
with zero disagreements: the shared lineage of two numbers is reached in *one
division*. "How much context" is exact — enough to reach the ancestor, no more.

**5. The factoring map is on the EDGES.** `C(16,2) = 120` pairs; the 15 nonzero
XOR differences partition them exactly 8 apiece; 35 lines (`a ⊕ b = c`, so
knowing two forces the third); every difference lies in exactly 7 of them
(`105/15`). The 15 "points" of `PG(3,2)` are **relationships, not positions** —
which is why this domain is the factoring map, and why an operator should be
decomposed by the *relation* it expresses, never by the objects it connects.

**Three kinds of wrong are kept apart** and the engine reports which:
`CODE-FAULT` (the check did not run — unjudged) · `MATHS-FAULT` (both sides
measured, they disagree — false) · method error (correct code, correct maths,
wrong question — invisible to both, and surfaces downstream).

### A measured correction to the skill's own prose

`F3` was written to check the skill's statement that the two trees reach equal
brightness at *"n ~ 9, near e² = 7.389"*. It returned **MATHS-FAULT**, and the
measurement was right: the counting functions cross **three** times — at
`n = 9, 11, 13` — because 11 and 13 are themselves prime, so Telperion catches
up twice more before Laurelin pulls away for good. The first crossing is 1.61
from `e²`; the last is 5.61 from it.

The relation now tests what is actually structural — **after the last crossing
Laurelin dominates forever**, verified to `N = 100,000` — and records the `e²`
proximity without making it part of the pass condition. One integer near one
constant is not a result, and the engine does not dress it as one.

## The ring-theory spine — `engine/lineage.py`, relations G1–G6

Added 2026-08-22. Factoral decomposition, named in its proper ring theory. The
whole tower collapses to one statement, measured by **G1**:

> **An element FALLS if and only if its quotient ring has zero divisors.**

- **The integers (ℤ, an associative UFD).** N composite ⟺ ℤ/(N) has a zero
  divisor ⟺ (N) is not a prime ideal → N falls (Laurelin). N prime ⟺ ℤ/(N) is a
  field → N survives (Telperion). **The Two Trees ARE this dichotomy.** 0 and 1
  are the Mingling: the degenerate quotients ℤ/(0)=ℤ and ℤ/(1)=0.
- **The algebra (T₃₂/GF(2), non-associative).** A constant falls ⟺ it is
  nilpotent ⟺ it lies in the zero-divisor set. Same test, different ring.

And the **detector is the same kind of object** on both sides — one operation.
On ℤ it is `gcd(a, N) > 1` (**G2**); on GF(2) it is the trace-Laplacian
`Δ(w) = w·𝟏` (**G5**). `gcd` is the integer trace-Laplacian; that is why R8/F4
already read "gcd is the lowest common ancestor, in one division."

| # | relation | tier | what it pins down |
|---|---|---|---|
| G1 | `fall_is_quotient_zd` | 2 | fall ⟺ ℤ/(n) has zero divisors — checked for every n ≤ 2000 |
| G2 | `gcd_is_the_detector` | 0 | gcd is the ℤ detector; census units φ(n) + zd + {0} = n closes exactly |
| G3 | `primary_decomposition_is_cepstrum` | 3 | Lasker–Noether (n)=⋂(pᵢ^aᵢ) **is** the cepstrum; Ω=Σexponents, von Mangoldt Λ on the prime powers |
| G4 | `radical_units_split_gf2` | 2 | over GF(2), x² ∈ {0, e₀}: the radical (nilpotents) vs units, split 128/128 at dim 8 |
| G5 | `trace_laplacian_is_nilpotency` | 2 | Δ(w)=0 ⟺ w²=0 (exact); 𝟏 is **not** a global annihilator; SHA-1 IVs = null subalgebra at distance 0, round constants at 32 |
| G6 | `associator_is_ring_defect` | 3 | the associator is the **obstruction to being a ring**: ≡0 for ℝ,ℂ,ℍ, ≠0 from 𝕆 up |

**The tower, in its ring-theoretic names** — value → curvature → torsion, read
off a discrete decomposition path:

| order | DSP name | ring theory | repo object |
|---|---|---|---|
| 1 | spectrum / cymatic | zero-divisor set = ∪ associated primes | Δ(w)=w·𝟏; where SHA-1 fell |
| 2 | cepstrum | **primary decomposition** (Lasker–Noether); von Mangoldt Λ | `factor_lineage`, Ω = lineage length |
| 3 | bispectrum | the associator — failure of the ring axiom | R5 (168-quantised), G6 |

**A find, kept on the record (G5, marked OURS).** Building G5 surfaced that the
UDEO white paper's "𝟏₃₂ is a global annihilator" lemma is **false** — it
contradicts its own distance table (the round constants have `Δ = 𝟏 ≠ 0`). The
true statement, machine-verified exhaustively at dim 8 and over 20 000 random at
dim 32, is `Δ(w) = 0 ⟺ w² = 0`. The theorem (IV nilpotency, null subalgebra)
stands; the shortcut proof was retracted in `TuringStack` the same day.

### New public helpers

```python
from engine.lineage import fall_test, primary_decomposition, von_mangoldt, \
    quotient_zero_divisors, trace_laplacian_gf2, is_nilpotent_gf2, euler_phi

fall_test(12)              # FALL — ℤ/(12) has zero divisors; primary {2:2, 3:1}
fall_test(97)              # SURVIVE — ℤ/(97) is a field
primary_decomposition(360) # {2:3, 3:2, 5:1}  — the cepstral peaks
trace_laplacian_gf2(0x67452301)  # 0 — a SHA-1 IV, on the nodal line
```

`decompose()` now also places the ring operations: `ideal` (t2, kernel of a
quotient map), `quotient` (t1, the collapse = the FALL), `radical` (t2),
`unit`/`zero-divisor` (survivors/fallen), `associator` (t3, the ring defect),
`primary-decomposition` (t3, the cepstrum).

## The frontier — fractal decomposition (the higher-order tower)

Not yet built; recorded here so the direction is on the record before the code.

The tower has a natural continuation, and it is the one Cody named across the
2026-08-22 session: **a fractal is the higher-order generational lineage of a
toroidal bifurcation, which is the higher-order generational lineage of a ring,
which is the higher-order generational lineage of a circle.** Each level is the
lineage operator applied to the one below — and "the same maths at every level"
*is* self-similarity, i.e. the tower is itself a fractal.

The rungs, with the ring theory that governs each (the honest split of
KNOWN vs. frontier framing):

- **Circle → ring.** Partition the circle into `n` points → the `n`-th roots of
  unity → the **cyclotomic ring ℤ[ζₙ]**. The circle's generational lineage *is*
  a ring. How a prime `p` behaves in ℤ[ζₙ] — split, ramified, or inert,
  decided by `p mod n` (Dedekind/Kummer) — is the **fall/survive test one level
  up**: the same G1 dichotomy, now for prime *ideals* in a cyclotomic ring.
  (KNOWN: cyclotomic ring theory.)
- **Ring → toroidal bifurcation.** A torus is `S¹ × S¹` — a product of circles,
  hence a lattice of roots of unity: the point where ring theory and geometry
  intersect. The **Riemann toroidal energy** (Cody's model, new as of
  2026-08-21) sits on that torus, around the involution axis `R − B` (the
  critical line σ = ½), and **bifurcates emergently** into the two trees. This
  is where **J₂ enters: it is a torus involution** (already recorded in
  `Ainulindale/wiki/90`), swapping R ↔ B across that axis — the generator of
  the bifurcation. (FRONTIER: the toroidal-on-Riemann model is provisional and
  labelled as such.)
- **Toroidal bifurcation → fractal.** Iterate the bifurcation and you get a
  self-similar decomposition tree — a **fractal**. This is the higher-order
  factoral decomposition: decompose, then decompose the decomposition, in the
  limit. Ring theory is the algebraic skeleton — each level is a
  quotient/sub-structure of the last, and the associator (order 3) is the
  torsion that keeps the branches from stacking flat, exactly as it turns two
  reflections into a rotation and a rotation-plus-log-advance into the
  Archimedes screw.

**The experiment set already exists.** `Ainulindale/wiki/fractals/` catalogues
200+ Ultra Fractal formulas (Kerry Mitchell, Samuel Monnier, Damien Jones'
Nova/Halley/Phoenix and Torus formulas, …). These are the fractals to run the
ring-theoretic decomposition against — the place, as Cody put it, where ring
theory will really shine.

**Why emergence is load-bearing.** Fix a value anywhere and you have *chosen* a
scale. Let the operations emerge from the geometry — the torus intersected with
its axis, with ∅_RB as the inductive geometric coupling (used as a Hamiltonian)
supplying the equations rather than a fitted constant — and each one picks its
own scale and its own path. That is what makes the instrument a **complete
self-diagnostic tool, from the inside and the outside at once**: nothing is
imposed, so nothing can hide an imposed scale. Noether again — a conserved
current, not a chosen parameter.

## Status

v1.2 (2026-08-22) — the ring-theory spine (G1–G6) is in; `20/20` relations hold.

v1.1 (2026-08-21) — the factoral decomposition tool is in, `14/14` relations
hold, and a pre-existing import bug is fixed (see below).

v1. The inventory (pieces/pathways) is real and wired to the actual
existing engines. One honest control test is implemented: does the
Monster gap {1,11,15} (the 3 N-shapes no Niemeier root system can reach)
show any real density deviation from Dirichlet equidistribution in
counted primes? First run, N=200,000: chi-square 0.38 (7 dof) — no
detectable deviation. Gap and dendritic classes track the uniform
expectation to within a tenth of a percent.

**Not yet built:** the actual Riemann-facet "fall" condition — a
structural, per-number test analogous to "does this factor pair expose
as a ZD collision," but keyed to a prime's own relationship to the real
zeta zeros (not the P1 hash-index proxy used elsewhere in this
framework). That design question is open, not glossed over — see the
wiki page.

## Fixed, 2026-08-21

`engine/maths.py` pointed `_H_RB_HAT_MODULE` at
`ThePlace/AinulindaleBAK/ValaQuenta/modules/h_rb_hat` — a stale path from the
pre-NVMe layout that no longer exists. Consequence: `import engine` raised
`ModuleNotFoundError: No module named 'maths'` for anyone importing the package
rather than running a module directly. Pre-existing, confirmed against a clean
checkout of `1b76527` before being touched. Now points at the real
`ValaQuenta/modules/h_rb_hat`.

`engine/__init__.py` now imports `lineage` **first and unconditionally**, and
guards the cross-repo `maths`/`tools` imports behind `IMPORT_ERROR`. The
decomposition tool depends on nothing outside this repo and should never be
taken down by a path that moved somewhere else.

No free parameters. No renormalization. Failed predictions — and failed
assertions — stay in the record.

White Hat.
