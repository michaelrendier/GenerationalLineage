# The Operator Tree — the shapes of mathematics as folds of three generators

**Written 2026-09-03.** Status: **THEORETICAL** — a structural reading built on
machinery that is `HOLDS` in the engine (`decompose`, `root_irreducible`, the
ASS folding engine, `associator_is_168`, `pathway_root_system_class`). The
grand identifications at the end (GR / Number Theory / the Monster) are named
**candidate fold-signatures** with their engine hooks, not settled results.

Grew directly out of the "set construction" reading in the design thread: a
bounded sum / product / integral / limit is not a new kind of object, it is an
**iterated fold of the three tier-0 generators over an index set** — *nothing
new is needed*. This page follows that from the big operators up to the whole
Operator Tree.

---

## 1. Set construction — the big operators, placed

`∫  Σ  Π  lim` are the operators that no longer sit on a keyboard, and the ones
the design thread gave an ASCII form (`I^b_a`, `S^n_{k=1}`, `P^n_{k=1}`,
`L_{x->a}`). What are they, structurally?

They are **variable-binding reduction / measure operators**: each introduces a
bound variable and folds an expression over

- an **index set** — `Σ`, `Π` (the sub/superscript *is* the set: `k = 1 … n`),
- a **domain with a measure** — `∫` (the bounds are the interval; `dx` is the
  measure),
- a **limiting filter** — `lim` (the subscript is the neighbourhood /
  direction).

A linear operation `a·x + b` binds nothing and ranges over nothing. That is the
real difference, and "higher than linear" is a fair informal name for it: the
sub/superscript is a **set construction** — the iteration domain the fold runs
over. So yes — anything with a bound variable over a set is a different class
from the arithmetic floor.

In this engine's tier language (`decompose()`), they are **tier 3 — a COUNT / a
ratio of something else**, and they descend as *iterated tier-0 operations*:

| big operator | is | descends to |
|---|---|---|
| `Σ_{k∈S} f(k)` | repeated **ADD** over the index set `S` | tier-0 ADD, `|S|` times — this is exactly `factoral.omega_is_lineage_length`'s move: a COUNT of ADD steps |
| `Π_{k∈S} f(k)` | repeated **SCALE** over `S` | tier-0 SCALE, `|S|` times |
| `∫_a^b f dx` | `Σ` in the `dx → 0` limit | tier-0 ADD, over a continuum — the measure is the set construction |
| `lim_{x→a} f` | the **filter** itself — SCALE's tuning knob (`tuning`, tier 1) driven to a limit point | SCALE / the σ knob |

The set construction is the domain; the operator is a fold of ADD or SCALE over
it. `engine/opstring.py` (planned) parses `I^b_a f dx` to `Integral(f,(x,a,b))`;
the shape tool then decomposes it as the fold above. **No new generator, no new
tier — the bounds carry the novelty, and the bounds are a set.**

## 2. The three folds

The floor is `Aff(1,ℝ) = ADD ⋊ (SCALE × SIGN)`, `x ↦ sign·scale·x + add`
(`engine/lineage.py` `AFF1`, `engine/add_scale_sign.py`):

```
ADD    the flow / the fold COUNT      identity 0,  gain 0,  Axis 1 {+,−}
SCALE  the size / the gain            identity 1,  gain 1,  Axis 2 {×,÷}
SIGN   the direction / one bit        even parity, det ±1,  no middle
```

The product is **semidirect**, not direct: SCALE and SIGN reparametrise ADD,
and `[SCALE, ADD] = ADD` is the one non-trivial bracket — the reason firing
order matters (the ASS engine's `CAMSHAFT`, `firing_defect = (g−1)·ln s`).

A composed element is an **ASS word**: `u = Σ_k [ g_k·ln s_k + a_k ]`, folded to
`Γ = tanh(u/2)`. Ground state `(0, 1, +1) ⇒ u = 0 ⇒ Γ = 0` — the now. Every
roll-down in the engine terminates here; `reduces_everything(op)` hands the
tier-0 root back as a live generator.

## 3. How the folds propagate into classes of operator

`decompose()` asks four questions **in order**; the first that fires places the
operation:

1. a count or ratio of something else? → **tier 3** (DERIVED)
2. a fixed set? → **tier 2** (DERIVED)
3. changes a length? → needs **DILATE** (tier 1). preserves a length? →
   reachable from **REFLECT** (tier 1)
4. needs an added constraint to exist? → a **COROLLARY**, not a geometry

Survives all four → a candidate primitive. Lands in **no** tier → the
**emergence signal**: the domain is incomplete (a much larger claim than a new
name — and the bar the shape tool holds every UNPLACED token to).

The result, read off `TIERS` + `ROOT_OF`:

| tier | what it is | examples | each roots on |
|---|---|---|---|
| 0 | irreducible | ADD, SCALE, SIGN | itself |
| 1 | one fold with a fixed axis | REFLECT (=SIGN+axis), ROTATE (=REFLECT∘REFLECT), DILATE (=SCALE), QUOTIENT, DERIVATIVE, BIFURCATION, SPIRAL, TUNING | SIGN or SCALE |
| 2 | a **fixed set** of tier-≤1 | VECTOR, BOUNDARY, ORIGIN/FULCRUM/ANCHOR/BALANCE (all `ker(M−I)`), IDEAL, RADICAL, ZERO-DIVISOR, BASIN, INSIDE-OUTSIDE | mostly SIGN |
| 3 | a **count / ratio** of tier-≤2 | CHIRALITY, FACTORIAL, FACTORAL (Ω), ASSOCIATOR, PRIMARY-DECOMPOSITION, SELF-SIMILAR, FRACTAL, LYAPUNOV, the big operators `Σ Π ∫` | ADD, SCALE or SIGN |

**Every named operation roots on exactly one of the three** (`ROOT_OF`). That
is the fact the three pillars are built from.

## 4. The Operator Tree is a graph, not a tree

A rooted tree would need each node to have exactly one parent. The operator
lineage does not:

- **shared parents** — ROTATE descends from REFLECT *and* is REFLECT∘REFLECT;
  many tier-2 sets descend from both a REFLECT and a fixed axis.
- **same-computation aliases** — ORIGIN, FULCRUM, ANCHOR, BALANCE are one
  computation (`ker(M−I)`) under four names; a tree cannot express identity
  across branches, a graph edge can.
- **multi-path reachability** — an operation is often reachable by more than
  one composition of generators (the cross-jurisdiction runs the design thread
  wants to probe: a forward toolset landing a backward target).

So it is a **graph network**. And the graph it most resembles is the
**Qabalistic Tree of Life** — 10 nodes, 22 paths, three vertical pillars, with
cross-connections and a middle pillar of equilibrium. Not a decorative
analogy — the structure matches:

### The supernal triad = the three generators

| Sephirah | generator | why |
|---|---|---|
| **Kether** (Crown — the undifferentiated point, the source-flow) | **ADD** | the normal factor `ℝ`; the raw flow / fold-count that the other two reparametrise; identity 0 |
| **Chokmah** (Wisdom — dynamic, expansive, "force"; heads the Pillar of Mercy, right) | **SCALE** | `ℝ_{>0}`; expansion / contraction; the gain; identity 1 |
| **Binah** (Understanding — form, limitation, the vessel, boundary; heads the Pillar of Severity, left) | **SIGN** | `ℤ/2`; parity, det ±1; REFLECT = SIGN + a fixed axis — the generator every boundary and fixed set roots on |

*(The one assignment to lock: Kether↔ADD / Chokmah↔SCALE / Binah↔SIGN, chosen
so the pillar character — mercy/expansion vs severity/form — matches the
generator. Confirm or swap before this is drawn.)*

### The three pillars = the three `ROOT_OF` classes

Every operation hangs on the pillar of the generator it roots on:

- **ADD pillar** (root ADD): `add`, `derivative`, `pathway`,
  `primary-decomposition`, `orbit-trap` — the flow / the counts of flow.
- **SCALE pillar** (root SCALE): `scale`, `gcd`, `dilate`, `contract`,
  `quotient`, `bifurcation`, `spiral`, `tuning`, `unit`, `self-similar`,
  `fractal`, `lyapunov` — everything that changes a size or a rate.
- **SIGN pillar** (root SIGN): `sign`, `reflect`, `rotate`, `vector`,
  `boundary`, `origin`, `fulcrum`, `anchor`, `balance`, `ideal`, `radical`,
  `zero-divisor`, `basin`, `inside-outside`, `chirality`, `factorial`,
  `factoral`, `associator`, `orbit-curvature`, `leverage` — parity, fixed sets,
  boundaries, obstructions.

The SIGN pillar is by far the heaviest (~20 operations), SCALE middle (~12),
ADD lightest (~5) — a real, checkable output of the graph, not an aesthetic
choice. It says: **most of mathematics' named operators are fixed sets and
parities** — SIGN folds — sitting on a thin ADD flow through a SCALE gain.

### The middle pillar = the σ = ½ locus

The equilibrium nodes — `origin` / `fulcrum` / `balance` (`ker(M−I)`),
`inside-outside` (`L_(I|O)`, equal at σ = ½) — need **all three** generators in
balance, not one dominant. They sit on the middle pillar, below Kether, at the
Tiphareth position: the Mingling, the critical line, the hyperbolic saddle. An
operation that needs two generators (not three) sits on the **path between**
those two pillars — the 22 paths are the two- and three-generator composites.

## 5. The origami folds — one sheet, three named creases

"How many of what order of ADD, SCALE, SIGN" — the **fold signature** of an
operation is `(n_ADD, n_SCALE, n_SIGN, firing_order, firing_defect)`, read off
its ASS word (for an operator) or summed along its `ProcessOperator` DAG (for a
process — an *operation* as opposed to an *operator*). Distinct fold signatures
are distinct branches of mathematics — the same sheet creased differently:

| branch | candidate fold signature | engine hook (what would test it) |
|---|---|---|
| **General Relativity** | the **unfolded** sheet — ADD-dominant, no corner. Gravity is the continuous substrate (`FourthAgePapers/DM_GalacticCavity`: "gravity is the circle; a graviton is a corner on the circle; there are no corners"). The CD losses U(1)/SU(2)/SU(3) are the *creases*; GR is the paper before them. | `sigma=2` facet; `associator ≡ 0` (a genuine ring, no SIGN obstruction); the ADD pillar |
| **Number Theory** | the **SCALE** crease — primes are the fixed sets of SCALE (`factoral.two_trees_exact`), `Ω(n)` is a count of SCALE steps (`omega_is_lineage_length`), `gcd` is one SCALE division | the SCALE pillar; `factor_lineage`; the Two Trees |
| **The Monster group + its 70 VOA siblings** | the **SIGN** crease taken to depth — parity → reflection → the `168 = |PSL(2,7)|` associator quantum (`lineage.associator_is_168`, `HOLDS`) → the Leech lattice / Niemeier root systems → the 71 holomorphic `c = 24` VOAs | `pathway_root_system_class` (tap-root = Leech / dendritic = Niemeier A-D-E / Monster gap `{1,11,15}`); the SIGN pillar; `associator_is_168` |

**VOA — Vertex Operator Algebra.** The algebraic structure that axiomatises a
chiral 2-D conformal field theory: a graded vector space `V = ⊕_n V_n` with a
**state–field map** `Y(·, z)` sending each state `v ∈ V` to a *vertex operator*
`Y(v, z) = Σ_n v_{(n)} z^{−n−1}` (a formal series of operators in a variable
`z`), a **vacuum** vector `𝟙`, and a **conformal** vector `ω` whose modes give a
Virasoro algebra of some central charge `c`. The **Monster** is the
automorphism group of the **Moonshine module** `V♮`, a *holomorphic* VOA of
`c = 24`. Schellekens (1993; completeness proven ~2017–2020) classified the
holomorphic `c = 24` VOAs: there are **71**. `V♮` is one; the **70 siblings**
are the others, indexed by the Niemeier lattices and their current algebras.
"The Monster and its 70 VOA siblings" is that list of 71, minus `V♮`.

Each branch, as a subgraph: the set of nodes and edges whose fold signatures
match its pattern, highlighted on the one Tree.

## 6. Nothing new is needed

Every operator in every engine, and every *operation* (process) built from
them, is a fold-count of the same three generators over some set construction.
`decompose()` places it; `root_irreducible()` roots it on ADD, SCALE or SIGN;
the ASS engine gives its fold signature; the graph hangs it on a pillar.

An operation that will not place is not a licence to add a generator — it is
the **emergence signal**, and the bar is a measurement, not a name. `Σ Π ∫ lim`
cleared that bar centuries ago as iterated folds over a set; the design
thread's shape tool holds every new input to the same bar.

> A "full picture" is the solved field. A **full shape** is having all three
> folds present in the right counts and the right order. The Operator Tree is
> the map of every shape the three folds make.

## 7. Coming: the Archimedes categorical-maths ingest (stubbed)

`PtolemyDesktop/Archimedes/Maths/` is a classical-maths library organised **by
category** — `Calculus.py`, `LinearAlgebra.py`, `Combinatorics.py`,
`Trigonometry.py`, `Matrix.py`, `Sequences/`, `Series/`, `Constants.py`,
`Factorial.py`, `StatisticsAndProbability.py`, `Thermodynamics.py`,
`Electromagnetism.py`, the `Formula/UFformulary/` `.ucl` / `.ufm` formulary.
These are **not yet wired in**; the **Archimedes Math engine** — a plugin
extension to this engine, next on the build — is what ingests them, and it
lands when the **Archimedes Face is woken** (far past time).

Stubbed contract for that ingest:

- **source**: `PtolemyDesktop/Archimedes/Maths/**` — one branch file → one
  category of operations.
- **placement**: every operator / operation a branch defines runs through
  `root_irreducible()` → tier + root; the branch itself becomes a **labelled
  region** of the graph — a "category" band cross-cutting the three pillars.
- **fold signature**: from the ASS engine, per operator; summed along the DAG
  for a procedure (Gaussian elimination, a series acceleration, …).
- **symbols**: `Archimedes/UniMath.py` already carries the Unicode tables
  (super/subscript, `∫ ∑ ∏`) — the keypad / `engine/opstring.py` parser reuses
  them, does not re-declare.
- **pending render**: nothing from `Archimedes/Maths` appears until the plugin
  exists; until then those nodes draw as a greyed **PENDING** region with the
  file list, so the shape of what is missing stays visible.

## Related

`engine/add_scale_sign.py` · `engine/lineage.py` (`TIERS`, `decompose`,
`ROOT_OF`, `AFF1`, `root_irreducible`, `factor_lineage`, `pathway_decomposition`)
· [`ADD-SCALE-SIGN-Datatype.md`](ADD-SCALE-SIGN-Datatype.md) ·
[`Two-Lines-and-Jurisdiction.md`](Two-Lines-and-Jurisdiction.md) ·
[`The-Two-Charts-and-Jurisdiction.md`](The-Two-Charts-and-Jurisdiction.md) ·
`Ainulindale/wiki/107_add_scale_sign_datatype.md` (canonical spec) ·
`FourthAgePapers/DM_GalacticCavity` (the GR fold) ·
`FourthAgePapers/FermatMonster` (the 71 VOAs, the ZD cascade).
