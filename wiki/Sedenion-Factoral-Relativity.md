# Sedenion Factoral Relativity

Session origin: 2026-07-17, arising directly out of the SHA-1-first UDEO
session (see `TuringStack`'s `.clauderc_context_1` entry) and Cody's own
tree/root vocabulary for navigating the Cayley-Dickson tower.

## The core move: factorization is relative to which facet you stand at

`H_hat_RB` is one operator with multiple σ-facets (`h_rb_hat/maths.py`):

| σ | Facet | Character |
|---|---|---|
| 0.0 | Fermat (forbidden zone) | no rational solutions — discrete, algebraic |
| 0.5 | Riemann (critical line) | the zeta zeros — continuous, spectral |
| 1.0 | Yang-Mills | gauge |
| 2.0 | General Relativity | curved |

Fermat's facet already has a real, working, already-built mechanism —
the Zero Lattice tree (`telperion_engine.py`). This project's premise:
the same recursive Cayley-Dickson construction, applied at the Riemann
facet instead, should produce its own "extinction" mechanism — not a
metric (already tried, at chance — see Method 3 below), but a genuine
structural fall/survive condition, the way Fermat's facet has one.

**Why "factoral," not "spectral":** `UDEO_RSA_DEMO.py`'s Method 3
("Sedenion Spectral Relativity") already exists and already has a
result — a σ-face geodesic-distance metric, tested against RSA's (e,d),
AT CHANCE. Naming this new work "spectral" would risk quietly reusing
that already-failed mechanism under a new name. "Factoral" names the
actual target precisely: not distance under a metric, but which numbers
get extinguished and which survive — a discrete fall/no-fall condition,
same shape as Fermat's, different facet.

**Why "factoral," not "factorial":** renamed 2026-08-21 (Cody), repo
and directory together. *Factoral* — of, or pertaining to, factors. The
old spelling collided with `n!` (nothing to do with the subject) and,
worse, with `A!` in the `0_RB` context, which
`.clauderc_canonical_maths` records explicitly as meaning **`A†`, the
adjoint — "NOT factorial, do not conflate."** The naming *argument*
above is unchanged and still load-bearing; only the collision is gone.

## Correction: the foundational claim is the Nightmare Group, not the tree

Added 2026-07-17, same session, after Cody named and pointed at
`FourthAgePapers/FermatMonster/engine/fermat_monster_engine.py` directly.
Everything above and below this section had been implicitly treating the
Zero Lattice tree (`telperion_engine.py`) as the load-bearing object.
It isn't. Grounded straight from that engine's own docstring:

**The one claim:** *"The Generalized N-Shape Fermat Equation (x^l + y^m
= z^n for all exponent configurations) IS the Monster Group and its 70
Schellekens siblings — the 71 holomorphic c=24 VOAs are the complete map
of Fermat N-shapes in 𝕊."* This is the *generalized* Fermat equation —
independent exponents l, m, n on each term, across every configuration —
not the classic same-exponent FLT (aⁿ+bⁿ=cⁿ). Cody's own name for this
unification: **the Nightmare Group** (playing on `telperion_engine.py`'s
own "Fermat's Nightmare (FLT via ZD cascade)").

**The chain** ("Fermat Defines. Riemann Fires."): generalized Fermat
carves out a forbidden zone; what survives the exclusion is prime.
Niemeier Coxeter numbers h mod 16 cover 13 N-shapes. The 3-shape gap
{1,11,15} is a proven theorem — no A/D/E root system reaches it. The
Monster fills exactly that gap via five Moonshine primes {17,11,59,31,47}.
71 VOAs total = 24 lattice (23 Niemeier + Leech) + 47 non-lattice.
Generalized Fermat across all N-shapes and the 71 VOAs are claimed
**identical**, not merely related.

**The reframe:** the engine's own docstring lists the ZD-cascade/leaf-tree
mechanism — everything this project is built on — under *"Consequences
(now understood as CONSEQUENCES not the bridge)"*, alongside FLT
extinction, the Frey curve mapping, and j-coefficient parity. The tree is
not the foundational object. The Monster/71-VOA identity is. The
leaf/root walk, the dendritic/tap/clonal root-system classification, the
Dirichlet-equidistribution control test — all of it is one consequence
among several of the Nightmare Group claim, not the claim itself. Read
everything below with that hierarchy in mind: this project has so far
been instrumenting a downstream effect, not the source.

Engine's own epistemic stance, unchanged and worth repeating here:
*"Engine derives; does not prove. No renormalization. Failed predictions
stay in data."*

## Orientation inside the tree: leaf, root, and three kinds of roots

Corrected mid-session (Claude had this backwards initially): **k=0 (ℝ,
"The Unit") is the leaf. The root is T_256 AND ABOVE — k≥8, not a single
point at k=8.** Asymmetric on purpose: the leaf is exact and singular
(ℝ, dim=1, the one base case the recursion bottoms out at); the root is
a region, not a point, because — Cody, 2026-07-17 — "the root becomes
indistinguishable from contents around T_256": past that dimension the
tower's own structure (per the T_n/GF(2) Frobenius theorem, `paper.tex`)
saturates — every element is nilpotent or involutory, no third option —
so any further doubling (T_512, T_1024, ...) adds dimension without
adding new distinguishable structure at the boundary. The leaf end
narrows to a point; the root end diffuses into an indistinguishable
mass. Read as a recursion
tree, not a botanical one — the Cayley-Dickson construction doubles
outward from ℝ (T_256 = CD(T_128,T_128) = ... = CD(ℝ,ℝ) iterated), so
k=0 is the base case where the recursion terminates (the leaf, in the
CS sense — `CayleyDickson.multiply()`'s own `if dim==1: return...` base
case), and k=8 is the top-level construction (the root).
`prime_tower_path()` already walks leaf → root (k=0 → k=8); a composite
falls off that walk at k=4 when its factor pair exposes as a zero-divisor
collision; a prime completes the walk.

Three kinds of "root system" beneath that walk, grounded in
`FourthAgePapers/FermatMonster/engine/fermat_monster_engine.py`:

- **Dendritic roots** — the 23 non-Leech Niemeier lattices, each built
  from a genuine A/D/E-type root system (literal branching Dynkin
  diagrams for D/E), each covering specific N-shapes via its Coxeter
  number h mod 16.
- **Tap root** — the Leech lattice, `LEECH_SHAPE=0`, the one Niemeier
  lattice with *no* root system of its own ("no roots, identity shape"
  — the code's own words). The center axis the other 23 are all cut
  relative to, not one of the branches.
- **Clonal roots** — primes sharing the same h/N-shape aren't
  independently rooted; they converge onto the *same* underlying
  root-system pathway, the way a clonal colony (Pando) presents as many
  trunks sharing one root system underground. A prime's identity as a
  leaf is inseparable from which colony (root-system class) it belongs
  to.

## Quantized pieces and pathways (v1, `engine/maths.py`)

**Pieces:** 9 CD tower levels; 16 N-shapes (8 in `PRIME_SECTOR`, 1
`LEECH_SHAPE`, 3-shape `NIEMEIER_GAP` {1,11,15} — the Monster gap,
unreachable by any A/D/E root system); 24 Niemeier lattices (23 rooted +
Leech); 12 canonical `ZD_CONSTELLATIONS_ODD` 4-tuples; 20 real Riemann
zeros on file (`RIEMANN_ZEROS`, LMFDB/Odlyzko, `h_rb_hat/maths.py`).

**Pathways:** leaf-to-root walk (`prime_tower_path`); the fall branch at
k=4; the clonal branch (shared root-system convergence); the gap-filling
branch (Monster + 70 sibling VOAs cover what no root system reaches).

## The control: the zeta function, stated explicitly

Cody, 2026-07-17: *"the Zeta Function is the Control...it is the
authoritative maths for the order the primes grow."* Concretely:
Dirichlet's theorem — primes are asymptotically equidistributed among
the φ(16)=8 classes coprime to 16 — is itself a consequence of the
non-vanishing of Dirichlet L-functions on the critical line (GRH
territory), i.e. real zeta/L-function structure, not tree geometry.
`telperion_engine.py`'s own module docstring already names the exact
quantity that connects the two — *"Oscillations in π(x;16,k) are driven
by zeros of Dirichlet L-functions L(s,χ). These zeros ARE the spectral
nodes of the Zero Tree"* — but nothing wired that statement to real data
until this project.

**First honest test run (N=200,000):** does the Monster gap {1,11,15}
show a real density deviation from equidistribution — evidence the gap
shapes are structurally special in actual prime counts, not just in the
tree's own classification? Chi-square = 0.38 (7 dof). Gap deviation
−0.083%, dendritic deviation +0.050%. **No detectable signal.** Real
primes don't currently show any density anomaly correlated with the
tree's own gap/dendritic split, at this scale. Recorded, not deleted —
failed predictions stay in the record.

## Open design question — not yet built

The actual Riemann-facet "fall" condition. Fermat's fall is exact and
structural: a composite's factor pair collides as a real zero-divisor at
k=4. What is the Riemann-facet analog — what, structurally, would a
prime's own relationship to the real zeta zeros (not the P1 hash-index
proxy) cause it to "fall" against? Candidates not yet evaluated:
proximity between a prime's some derived quantity and a zero height
γ_n; a prime's contribution to the explicit-formula oscillation term
Li(x^ρ) crossing some threshold; something else entirely. This has to
be defined precisely — the same way "zero-divisor collision" is a
precise, computable condition — before it's a testable engine, not an
analogy.

## On the way back out

Cody, mid-session: *"on the way back out of this rabbit hole, we will
use the negative maths all the way back."* Parked for when the Riemann
facet's fall condition is actually built — `facet_fermat()`'s own
framing (FLT as the *negative* facet of H_hat_RB, "not a projection of
what the operator produces") is the likely anchor for what "negative
maths" means here, not yet connected further.


## The factoral decomposition tool — `engine/lineage.py`

Added 2026-08-21, at Cody's direction, carried over from
`VAPMIP/engines/e10_generational_lineage.py` ("the anatomy of σ in ∅_RB",
2026-08-20) so this repo holds the decomposition machinery locally rather
than reaching across repos for it.

**Why it belongs here rather than staying in VAPMIP.** This repo's whole
premise is that factorisation is *relative to which σ-facet of `0_RB` you
stand at*. A decomposition tool is therefore not an accessory — it is the
instrument. Before you can ask which numbers a facet extinguishes, you
need a way to say what any given operation *descends from*, and whether a
named "geometry" is primitive or merely a count of something below it.

`14/14` relations hold. `R1–R8` are the VAPMIP engine's σ relations,
carried verbatim and re-measured here — not paraphrased, not re-derived.
`F1–F6` are this repo's.

| | relation | tier | what it measures |
|---|---|---|---|
| F1 | `two_trees_exact` | 2 | Telperion + Laurelin + Mingling = every integer, zero overlap |
| F2 | `densities_conserve` | 3 | the two densities sum to 1 at every scale |
| F3 | `mingling_point` | 2 | the crossings, and Laurelin's permanent dominance after them |
| F4 | `gcd_is_lca` | 0 | shared lineage = gcd = lowest common ancestor, in one division |
| F5 | `omega_is_lineage_length` | 3 | `Ω(n)` **is** the lineage length, not a statistic about it |
| F6 | `pg32_is_edges` | 3 | the 15 are relationships, not positions; each factors 7 ways |

### The domain: what the Two Trees actually partition

    TELPERION   PRIME       defined by what it CANNOT be decomposed into
    LAURELIN    COMPOSITE   defined by what it IS decomposed into
    MINGLING    0 and 1     neither — the identities of ADD and SCALE

Measured over `[0, 100000]`: `2 + 9,592 + 90,407 = 100,001 = N+1`, exact,
zero overlap. **0 and 1 are on neither tree because they are the
identities of the first two tier-0 primitives** — which is also the
reason neither can be prime. Not a convention; a consequence.

### The tier floor

    tier 3   chirality, factorial, factoral, leverage, balance
             ← COUNTS and RATIOS of the layer below
    tier 2   vector, boundary, origin, fulcrum / anchor / balance
             ← FIXED SETS, and products of reflect × scale
    tier 1   reflect, rotate, contract / dilate   ← I − 2uuᵀ; gains {0, 1, √2}
    tier 0   ADD (identity 0) · SCALE (identity 1) · SIGN (one bit)

`decompose(name)` asks the four questions in order and the first to fire
decides. An operation that lands in **no** tier is not a discovery — it
is the emergence signal, and per §5 of the skill, claiming a genuinely
new generator needs a far better measurement than a name.

### The factoring map is on the EDGES, not the places

`F6` is the relation that most directly earns this tool its place in this
repo. Sixteen placeholders give `C(16,2) = 120` pairs; the 15 nonzero XOR
differences partition those 120 **exactly 8 apiece**; there are 35 lines
(`a ⊕ b = c`, so knowing two forces the third); and every difference lies
in exactly 7 of them (`105 / 15 = 7`) — the seven ways to **factor one
relation into two others**.

So the 15 "points" of `PG(3,2)` are *relationships*, not positions, and
`e₀` is not a point at all: in the edge reading it is the **root**, the
node that owns no edge and does no work. When decomposing an operator
here, decompose the **relation** it expresses — never the objects it
connects.

### A measured correction to the skill's own prose

`F3` was written to check the generational-lineage skill's statement that
the two trees reach equal brightness at *"n ~ 9, near e² = 7.389"*. It
came back **MATHS-FAULT**, and the measurement was right: the counting
functions cross **three** times — `n = 9, 11, 13` — because 11 and 13 are
themselves prime, so Telperion catches up twice more before Laurelin
pulls away for good.

The first crossing is 1.61 from `e²`. The **last** is 5.61 from it. So
the `e²` proximity, such as it is, holds for the first of three and not
for the Mingling as a whole.

The relation now tests what is actually structural — *after the last
crossing Laurelin dominates forever*, verified to `N = 100,000` — and
records the `e²` distance without making it part of the pass condition.
One integer near one constant is not a result and is not dressed as one.
**The skill's prose should be read as approximate here.**

### Usage

```python
from engine.lineage import run, decompose, factor_lineage, two_trees

run()                    # all 14 relations, tiered and self-checked
decompose('chirality')   # → tier 3, DERIVED: a count of reflection parity
decompose('gnarl')       # → UNPLACED: the emergence signal
factor_lineage(360)      # → Ω=6, generations=5, leaves [2,2,2,3,3,5]
two_trees(100_000)       # → the exact partition, measured
```

`engine/__init__.py` imports `lineage` **first and unconditionally** —
it is stdlib + numpy only and depends on nothing outside this repo, so it
stays usable even when the cross-repo Fermat-facet imports are not. Those
are guarded behind `IMPORT_ERROR` rather than being allowed to take the
package down.

### Open, for this tool

- **The `mingling_point` band.** Three crossings is measured; *why* the
  band is `[9, 13]` rather than a single point is not derived.
- **The tier table is a lookup, not a decision procedure.** `decompose()`
  returns `UNPLACED` for anything not already in `TIERS`. It cannot yet
  *derive* a tier for a new operation from its behaviour — it can only
  tell you that the domain does not contain it. That is honest, and it is
  also the obvious next piece of work.

---

## The ring-theory spine (relations G1–G6, added 2026-08-22)

Cody, 2026-08-22: *"where is ring theory in all this."* The answer: it was here
the whole time, named in signal-processing and geometry. Put it back on top and
the tower collapses to one statement.

### The unifying theorem — an element falls iff its quotient ring has zero divisors

    ℤ side (associative UFD — classical ring theory is COMPLETE):
        N composite  ⟺  ℤ/(N) has a zero divisor  ⟺  (N) not a prime ideal   → FALL
        N prime      ⟺  ℤ/(N) is a field                                     → SURVIVE
        N ∈ {0,1}    ⟺  the degenerate quotients ℤ/(0)=ℤ, ℤ/(1)=0            → MINGLING

    algebra side (T₃₂/GF(2) — NON-associative, ring axioms break rung by rung):
        w falls  ⟺  w is nilpotent  ⟺  w ∈ the zero-divisor set (∪ associated primes)

**The Two Trees ARE this dichotomy** — a domain vs. not-a-domain. And the
*detector* is the same kind of object on both sides, one operation:

    ℤ    :  gcd(a, N) > 1          — the integer trace-Laplacian
    GF(2):  Δ(w) = w · 𝟏           — Δ(w)=0 ⟺ w²=0

That is why R8/F4 already said "gcd is the lowest common ancestor, in one
division": gcd is to ℤ/(N) exactly what Δ is to T₃₂/GF(2).

### The three orders, in their proper names

| order | DSP name | ring theory | what it reads |
|---|---|---|---|
| 1 | spectrum / cymatic | zero-divisor set = ∪ associated primes | which primes are present — the SUPPORT (ω); where SHA-1 fell |
| 2 | cepstrum | **primary decomposition** (Lasker–Noether), von Mangoldt Λ | the EXPONENTS — multiplicity (Ω), the lineage length |
| 3 | bispectrum | the **associator** — failure of the ring axiom | the ORDERING / coupling; ≡0 for a ring, ≠0 from 𝕆 up |

The cepstrum rung is not an analogy: `log n = Σ aᵢ log pᵢ` turns the product into
a sum, and the von Mangoldt function Λ(n) — supported exactly on prime powers,
weight log p — is the cepstral domain of the integers. The explicit formula
`ψ(x) = x − Σ_ρ xᵖ/ρ` is the transform back to the Riemann zeros ρ, which are the
first-order **spectrum** (Berry–Keating). Value → curvature → torsion.

### The two rings are different in kind

Ring theory is **complete** on the ℤ side and is **exactly what breaks**, rung by
rung, on the algebra side: commutativity dies at ℍ, associativity at 𝕆, the
domain property at 𝕊. Factoral decomposition is the *projection* of the first
into the second; the zero-divisor locus is where "factorisation is non-trivial"
lands under that projection; and the **associator is the precise obstruction to
𝕊 being a ring at all** (G6). The white paper's own §2.5 already calls it
curvature — the associator is the torsion a genuine ring does not have.

### A find, kept on the record (G5, OURS)

Building G5 surfaced that the UDEO white paper's *"𝟏₃₂ is a global annihilator
(x·𝟏 = 0 for every x)"* lemma is **false** and contradicts its own distance
table — the round constants have `Δ(K) = 𝟏 ≠ 0` (distance 32). The correct,
machine-verified statement is `Δ(w) = 0 ⟺ w² = 0` (nilpotency), exhaustive at
dim 8 and over 20 000 random at dim 32. The theorem stands (IV nilpotency, null
subalgebra — not "ideal", since the algebra is non-associative); the shortcut
proof was retracted in `TuringStack` the same day. A MATHS-FAULT the harness was
built to catch, caught.

---

## The frontier — fractal decomposition

Recorded before the code, per the discipline. Cody's chain across the session:

> **a circle → (higher generational lineage) → a ring → a toroidal bifurcation
> → a fractal.** Each level is the lineage operator applied to the one below;
> "the same maths at every level" is self-similarity, so the tower is itself a
> fractal.

- **Circle → ring.** Partition the circle into `n` points → the `n`-th roots of
  unity → the **cyclotomic ring ℤ[ζₙ]**. The circle's lineage *is* a ring. How a
  prime `p` splits / ramifies / stays inert in ℤ[ζₙ], decided by `p mod n`
  (Dedekind–Kummer), is the fall/survive test one level up — G1 for prime
  *ideals*. This is the exact, KNOWN reason "the partitions of the circle" and
  "the ways of factorising them" are ring theory.
- **Ring → toroidal bifurcation.** A torus is `S¹ × S¹`, a product of circles —
  the intersection of ring theory and geometry. The **Riemann toroidal energy**
  (Cody's model, new 2026-08-21) sits on that torus around the involution axis
  `R − B` (σ = ½) and **bifurcates emergently** into the two trees. **J₂ is the
  torus involution** (`wiki/90`) swapping R ↔ B — the generator of the
  bifurcation. FRONTIER, labelled provisional.
- **Toroidal bifurcation → fractal.** Iterating the bifurcation gives a
  self-similar decomposition tree. Ring theory is its algebraic skeleton: every
  level a quotient/sub-structure of the last, the associator the torsion that
  stops the branches stacking flat (two reflections → a rotation;
  rotation + log advance → the Archimedes screw).

**The experiment set exists:** `Ainulindale/wiki/fractals/` — 200+ Ultra Fractal
formulas (Mitchell, Monnier, Jones' Nova/Halley/Phoenix/Torus, …). The place to
run the ring-theoretic decomposition, and where ring theory is expected to shine.

**Why emergence is load-bearing.** Fix a value anywhere and you have *chosen* a
scale. Let the operations emerge from the geometry — the torus ∩ its axis, with
∅_RB as the inductive geometric coupling used as a Hamiltonian supplying the
equations — and each picks its own scale and path. That is what makes it a
complete self-diagnostic tool, inside and outside at once: nothing imposed, so
no imposed scale can hide. Noether again — a conserved current, not a fitted
parameter.
