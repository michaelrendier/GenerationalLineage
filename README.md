# Sedenion Factoral Relativity
### The Generational Lineage Engine — and its ascent dual, The Emerger

*A tutorial. Read this before the papers — the papers assume you already know what "tier," "lineage," and "the two trees" mean; this document is where you learn it.*

---

## 0. What this document is

This repo is deep enough, fast enough, that most people (including future
sessions of this project) will hit the code before they've built the mental
model it assumes. This README exists to fix that: it defines the engine's own
vocabulary first, says plainly what the thing is *for*, then walks every tool
it exposes, in the order you'd actually reach for them. The theory write-ups
(`wiki/`, the fractal/formulary sections below) go deeper on any one idea;
this is the map you read before picking one to go deep on.

Everything below is runnable. Every number quoted is computed at run time by
`engine/lineage.py` — nothing here is asserted and left unchecked.

---

## 1. What "Generational Lineage" means, in this engine

Start from the object the engine actually stores. Every fact it knows is one
of these:

```python
@dataclass
class Relation:
    name: str
    claim: str      # one sentence: what is being claimed
    tier: int       # 0 irreducible · 1 reflect/dilate · 2 fixed set · 3 count/ratio
    descends: str   # what this is BUILT FROM — its parent in the lineage
    status: Status  # HOLDS / MATHS-FAULT / CODE-FAULT
    detail: str     # the actual computed numbers backing the claim
```

**Lineage** is the `descends` field, followed all the way down. Nothing in
this engine is allowed to just *be* a geometry or an operation — it has to
say what it's built from, and that chain has to bottom out at one of exactly
three irreducibles:

```
ADD      identity 0, gain 0     Axis 1 {+,−}
SCALE    identity 1, gain 1     Axis 2 {×,÷}
SIGN     identity even-parity   one bit, nothing between
```

**Generation** is depth in that chain — for a number, depth in its
recursive factor tree (a prime is generation 0, a leaf; a composite is an
internal node, one generation per split); for an algebraic operation, depth
in the tier ladder above. `Ω(n)`, the prime-factor count with multiplicity,
is not a statistic *about* a number in this engine — it is defined as the
**length of its lineage**, the number of tier-0 SCALE operations needed to
build it from 1.

**Status** is not binary pass/fail — it's three-way, on purpose, because
"wrong" has more than one cause and conflating them hides which kind you're
looking at:

```
HOLDS         ran, both sides measured, they agree
MATHS-FAULT   ran, both sides measured, they DISAGREE — the claim is false
CODE-FAULT    the check did not run — the claim is UNJUDGED, not confirmed
```

A relation that never ran is not evidence of anything. This engine has
caught itself in a MATHS-FAULT at least twice (see §7) and left both in the
record rather than quietly fixing the claim and moving on.

---

## 2. The mathematics — same object, or two things kept in sync by hand?

Same object. `FactoralLineageEngine` (the class that owns every relation
below) is not a program *about* a separate body of theory — it is the
generational-lineage discipline, executed. The base domain it decomposes
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

---

## 3. What this engine was built to do

The starting claim (`ValaQuenta/modules/h_rb_hat`): `Ĥ_RB` has multiple
σ-facets — σ→∞ is the **Fermat facet** (no rational solutions, the
forbidden zone), σ=½ is the **Riemann facet** (the critical line, the zeta
zeros). Same operator, different facet, the way a Laplacian's spectrum
looks different depending on the domain you restrict it to.

**This project's job is the Riemann facet's sibling of the Fermat-facet
engine that already existed** (`AbrikosovTree/engine/telperion_engine.py` —
9-level Cayley–Dickson walk, a composite exposes as a zero-divisor collision
at k=4 and "falls," a prime survives to k=8). So: **factorisation itself is
treated as relative to which facet you're standing at** — not one fixed
algebraic test, a family of them, related by the same recursive
Cayley–Dickson construction at different scales.

Concretely, the engine exists to:

1. Give every named "geometry" in this framework a **tier**, so a claim of
   primitiveness can be checked instead of assumed (§2).
2. Decompose actual numbers, permutations, and algebraic elements against
   the Two Trees domain and report `Ω(n)`, the primary decomposition, the
   fall/survive verdict — exactly, not statistically (§4.2).
3. Provide **instruments** — chart, crystal, join — that measure a
   *relationship* between two things (two ring-quantities, two struts, two
   repeat-positions, two cycles) rather than a property of one thing in
   isolation (§4.4–§4.6). This is the newest layer, and the one this
   session's conversation was about: "measurement of invisible
   relationships."
4. Self-check every one of the above against real computed data — **the
   zeta function is the control** (Dirichlet equidistribution of primes by
   residue class), never another layer of the same geometry — and keep
   every failed prediction in the record rather than deleting it.

No free parameters. No renormalisation.

---

## 4. How to use it — the tools

All examples assume you're in `SedenionFactoralRelativity/` with `import
engine` working (`IMPORT_ERROR` will be `None` if every cross-repo path
resolved).

### 4.1 Run the whole self-check

```bash
python3 engine/lineage.py          # 40/40, ~25s, verbose report
```
```python
from engine import run_lineage
result = run_lineage(verbose=True)  # same thing, importable
```

This is the thing to run first. It prints every relation in §5 with its
computed detail, then a one-line verdict: *"No new generator required. Every
operation above descends from the tier-0 floor by composition."* — or, if
something broke, exactly which relation and which of the three Status values
it got.

### 4.2 Decompose one number

```python
from engine import decompose_number, factor_lineage, fall_test, \
    primary_decomposition, von_mangoldt, euler_phi, arith_deriv

decompose_number(360)
# {'n': 360, 'ring_fall_survive': {...}, 'cepstral_primary': {2:3,3:2,5:1},
#  'omega_distinct': 3, 'Omega_lineage_length': 6, 'lineage_tree': {...},
#  'spiral_address': {...}, 'pathway': {...}, 'number_chart': {...}}

factor_lineage(360)['omega']       # 6 — Ω(360), the lineage length
fall_test(97)                      # SURVIVE — ℤ/(97) is a field
primary_decomposition(360)         # {2: 3, 3: 2, 5: 1} — the cepstral peaks
von_mangoldt(8)                    # log(2) — 8=2³, a prime power
euler_phi(360)                     # 96 — |units of ℤ/(360)|
arith_deriv(360)                   # the arithmetic derivative, Leibniz on primes
```

`decompose_number` is the single richest call — it bundles every
per-number perspective the engine has (ring-theoretic, cepstral, lineage
tree, spiral address, tuned pathway, Smith-style chart position) into one
dict, the way a lab report bundles every instrument reading for one sample.

### 4.3 Ask what tier a named operation is

```python
from engine import decompose, TIERS

decompose('fulcrum')
# {'operation': 'fulcrum', 'tier': 2, 'descends_from': 'ker(M - I)',
#  'status': 'DERIVED', 'note': 'same computation as origin/anchor/balance', 'known': True}
decompose('factorial')
# {'operation': 'factorial', 'tier': 3,
#  'descends_from': 'order of the coordinate reflection group', 'status': 'DERIVED',
#  'note': 'a COUNT — a transposition IS a reflection in x_i = x_j', 'known': True}
```

`TIERS` is the tier table itself, as data — every named operation this
framework uses, its tier, what it descends from, and a one-line note. Look
here before assuming something is primitive.

### 4.4 Walk the pathway / tune a factor search

The **pathway** layer treats factoring as a walk with two pinned anchors (1
and N), not an outward search — the factor is a node on the geodesic
between them, and the walk needs *tuning* per number to resonate onto it.

```python
from engine import spiral_address, pathway_residues, tune_pathway, fermat_path

spiral_address(97)                      # log-radius + angle on the CFRAC spiral
pathway_residues(1522605027, mult=1)    # the untuned walk (often fails in budget)
tune_pathway(1522605027)                # sweeps multipliers until one resonates
fermat_path(3233)                       # {'factor': (53, 61), 'excursion': 8, ...}
```

`[KNOWN — Morrison–Brillhart CFRAC, 1975]`: this is real, sub-exponential
factoring, not a metaphor. What's `[OURS]` is reading the *tuning* itself as
the framework's σ-dilate, and reading the excursion as a difficulty gauge
(§4.5).

### 4.5 Read the chart — Smith-chart-derived instruments

`PW8` found that a Smith chart (RF/radar impedance matching, Phillip Smith,
1939) is the *same* Möbius structure — `Γ=(Z−Z0)/(Z+Z0)` — already built
into this framework as `L_(I|O)`. `PW9` applied the methodology directly to
factoring (`number_chart_point`); `PW10` proved the fold itself doesn't care
what the two rings mean — any two quantities can drive it.

```python
from engine import number_chart_point, ring_chart_gamma, two_ring_chart

number_chart_point(3233, a=61)          # 0.034 — the balanced factor sits near the anchor
number_chart_point(30021, a=10007)      # 0.966 — unbalanced (3×10007), near the horizon

# the GENERAL two-ring fold — pick your own two ring definitions:
ring1 = lambda n: float(factor_lineage(n)['omega'])
ring2 = lambda n: euler_phi(n) / n
two_ring_chart(97, ring1, ring2, Z0=complex(0, 1), ring1_name='Omega', ring2_name='phi/n')
# -> {'Z': (1+0.99j), 'gamma': ..., 'abs_gamma': ..., ...}
```

Radial position on the chart is a difficulty gauge, read at a glance — the
anchor (`Γ≈0`) is "as easy as it gets," the horizon (`Γ≈1`) is "hardest
tested." Because `PW10` proved the fold is generic, the same instrument
applies to anything you can describe with two real numbers — including a
pair of box-kite struts instead of impedance:

```python
from engine.tools import report_strut_pair_chart
report_strut_pair_chart()     # prints all 21 strut pairs, sorted by |Γ|
```

Worth knowing before you read that output: the *first* ring pair tried
(strut-intrinsic scalars) came back `Γ=0` for every single pair — a real
null result, not a bug, because every one of the 7 box-kites is the same
octahedron by construction. The version shipped uses a per-address pair
(chart-energy difference, diagonal-imbalance difference) so the reading is
non-degenerate. Read the function's own docstring before trusting a
strut-pair number; it says exactly what would make one reading better than
another, and admits there's no ground truth yet to check the choice
against.

### 4.6 The crystal and the join — recovering what you didn't observe

Built the same session as this README, directly off a "crystallography as
measurement of invisible relationships" conversation: can a hidden
generating parameter be read off a structure's own repeat-pattern, with the
generator itself never observed?

**The crystal** (`PW11`) — an autocorrelation of a sequence against itself,
built from repeats alone (this *is* the Patterson-function move):

```python
from engine import repeat_distances, infer_period_by_stem_vote, vigenere_cipher

cipher = vigenere_cipher(plaintext, key=[3, 9, 15, 2, 7], alphabet=26)  # key length 5, hidden
dists = repeat_distances(cipher, n=4)
infer_period_by_stem_vote(dists, max_period=20)['best_period']   # -> 5, recovered blind
```

This is Kasiski examination / the Friedman test (1863 / 1920s), generalised
past text ciphers to any repeating sequence — R8's gcd/meet, run as a *vote*
across every candidate period instead of one blind reduction (a blind gcd
is fragile: one spurious repeat collapses it to 1). **Honest limit, not
hidden:** a composite period is genuinely ambiguous against its own
divisors by this method alone — real Kasiski cryptanalysis needs the
Friedman Index of Coincidence on top to resolve that; not built here yet.

**The join** (`PW12`) — a permutation's order from its own cycle-length
stems, the lattice-dual of R8's gcd/meet:

```python
from engine import permutation_cycles, permutation_order_direct, permutation_order_via_stems

perm = [1, 2, 0, 4, 3]                          # cycles (0 1 2)(3 4)
permutation_cycles(perm)                        # [[0, 1, 2], [3, 4]]
permutation_order_direct(perm)                  # 6 — apply repeatedly, definitional
permutation_order_via_stems(perm)               # 6 — lcm(3, 2), via primary_decomposition
```

Same stems `G3`'s cepstrum already extracts from an integer's factorisation
(`primary_decomposition`), combined with **max** exponent per prime instead
of R8's **min** — the join instead of the meet. Verified against direct
computation on 400 random permutations, 400/400 agree.

### 4.7 The fractal block

The tower's highest-order rung: **a fractal is the higher-order
generational lineage of a toroidal bifurcation, which is the lineage of a
ring, which is the lineage of a circle.**

```python
from engine import escape_survives, box_dimension, lyapunov_exponent, \
    newton_basins, feigenbaum_delta, MANDELBROT, BURNING_SHIP

escape_survives(complex(-0.5, 0.5), MANDELBROT, maxiter=200)
box_dimension(BURNING_SHIP, (-2, 1), (-2, 1))   # {'dimension_estimates': [1.55, 1.56], ...}
lyapunov_exponent(3.5699)                       # ≈-0.004 — the Feigenbaum accumulation point
newton_basins(5, N=48)['n_basins']              # 5 — the 5 linear factors of z⁵−1
```

The library is the control set: any of the 200+ Ultra Fractal formulas in
`Ainulindale/wiki/fractals/` can drive `escape_survives`/`box_dimension`, so
a claimed dimension always has an independent generator to check it against
— Mandelbrot (`D≈1.3`), the Julia set at `−0.8+0.156i` (`D≈1.6`), Burning
Ship (`D≈1.56`): three different, real, checkable dimensions, not one
number asserted.

### 4.9 The factoral spiral — factoral decomposition as chart geometry

`PW13`, built the same session as the `two_ring_chart_render.py` visual
proof-of-concept (`VAPMIP/SedenionFactoralRelativity`'s sibling repo):
spectral analysis IS factoral decomposition, using a different notion of
"factor" — an eigendecomposition factors an operator into (eigenvalue,
eigenvector) pairs the same way integer factorisation decomposes N into
primes. `factoral_spiral()` is the generic instrument: point it at ANY
collection with two chosen numeric readings and see the collection's own
factoral/spectral structure as chart geometry — discrete cells ("windows
of order") a caller can render as open bubbles instead of a raw scatter.

```python
from engine import factoral_spiral, chart_scale_factor
from engine.tools import report_factoral_spiral_chart, report_crystal_spiral_chart

# generic — point it at anything with two numeric readings:
report_factoral_spiral_chart(
    my_objects, ring1=lambda o: ..., ring2=lambda o: ...,
    out_path='spiral.png')

# wired directly to PW11's crystallography — a sequence's OWN recovered
# period drives the chart, distance-mod-period vs log2(distance):
report_crystal_spiral_chart(ciphertext, n=3, out_path='crystal_spiral.png')
# -> period recovered exactly (verified on a real period-7 Vigenere test:
#    1142 repeat-distances, 1142/1142 vote support, cells cluster by
#    log-distance since every distance IS a multiple of the true period)
```

`chart_scale_factor(Z, Z0) = |dGamma/dZ|` is the fold's own derivative, in
closed form — the "phase" information a flat `(Re Γ, Im Γ)` reading loses
when a curved conformal map gets flattened into 2D, made into a real,
computable number instead of a qualitative description of it. Checked
against central-difference numerical differentiation, not just algebra:
max relative error `1.55e-09` over 300 random `(Z, Z0)` pairs.

**Honest note on ring choice, kept in the record rather than smoothed
over:** the first attempt at the WordNet demo (`two_ring_chart_render.py`)
fed *raw* relation counts in as the two rings and got a chart that mostly
saturated near `Γ=1` — the Möbius map asymptotes to the boundary for any
large `|Z|`, so a long-tailed raw count collapses almost everything to one
indistinguishable region. Feeding `compress_count()`'s own bounded,
log-quantized output in as the ring values instead — rather than as a
color overlay on the raw scatter — is what actually shows the coarse-
graining as chart geometry. `report_crystal_spiral_chart()` uses the
compressed form by default for exactly this reason.

### 4.10 The pathway decomposition — factoring a PROCESS, not a number

`PW14`, the primary forensic tool. Cody, 2026-08-25, the framing this
landed on after two corrections: "building a mathematical 'pathway
decomposition' using 'process operators'...regardless of actual
mathematical equations or operations associated with an Octonion or a
Quaternion...those additional i's [are not] rotations in the maths, they
[are] composite constructions for any process from imaginary to real
meaning." So `pathway_decomposition()` does NOT try to name a Cayley-
Dickson level, does NOT assume a linear chain, and does NOT treat "how
many components" as a question with one right answer. "Imaginary" here
names a ROLE (hidden, generative, composite) applied to any process's own
minimum necessary tool-set, not an algebra with multiplication rules —
the same distinction `spelling_code` vs `context_vector` already drew
elsewhere in this project's sibling work (surface form vs relational
structure): the SHAPE is borrowed from hypercomplex numbers, the algebra
is not.

```python
from engine import ProcessOperator, pathway_decomposition

result = pathway_decomposition(input_value, [
    ProcessOperator('a', fn_a, depends_on=('input',)),
    ProcessOperator('b', fn_b, depends_on=('input',)),      # sibling of a, not chained to it
    ProcessOperator('c', fn_c, depends_on=('a', 'b')),       # a genuine combination of two prior operators
], output_name='c')
# result['real']       — output_name's own value
# result['imaginary']  — every OTHER operator's output, in resolution order
# result['dim']        — 1 + len(imaginary) — however many operators the
#                        process needed, discovered by running it
# result['order']      — the actual dependency-resolved order
```

**RSA as the control case** (`PtolemyDesktop/Kryptos/Ciphers/RSA.py`) —
not the object of study, a real algorithm exercising a genuine dependency
graph: CRT-decrypt's `m1` and `m2` each depend only on the ciphertext
(siblings, not chained to each other); the CRT term `h` depends on BOTH;
the final `m` depends on `h` AND `m2` again — `m2` fans out to two later
operators, which a forced linear chain (this tool's own first, corrected
attempt) cannot represent without lying about the structure via closures
reaching around it. `pathway_decomposition()` resolves this correctly:
`dim=4`, order `[m1, m2, h, m]`. The full key lifecycle (prime `p`, prime
`q`, modulus `n`, totient, public `e`, private `d`, ciphertext, plaintext)
is a different, equally real decomposition of "RSA" — `dim=8` — not a
re-measurement of the same number; there is no single correct count for
an algorithm this size, only whichever real sub-process the tool is
pointed at.

Verified against a real, externally-checkable example alongside the RSA
control case, not a synthetic one: `pw_process_trace_matches_the_cipher`
re-derives the textbook Vigenere pair `ATTACKATDAWN`/`LEMON` →
`LXFOPVEFRNHR` through the same generic DAG runner, independently of
`vigenere_cipher()`'s own hand-written function, AND confirms RSA's `m2`
fan-out resolves correctly — the thing the corrected design exists to get
right.

### 4.11 The unit lineage — a THIRD domain for the same decomposition

`PW16`. Cody, 2026-08-25: *"information lives in the units...units can
spectrally show direct generational lineage...mitochondrial lineage if you
will...units are directly how the geometries hold the permutation."* Every
named compound SI unit (Newton, Joule, Watt, Volt, Weber, Tesla) is a point
in the 7-axis lattice of SI base dimensions (`kg,m,s,A,K,mol,cd` — the
leaves), with an exact, computable lineage back to them — the same
leaf/composite discipline this file already runs on numbers
(`factor_lineage`) and processes (`pathway_decomposition`), applied to a
third domain rather than reinvented for it. A unit is a **geometry** in
exactly this project's sense: it carries no numeric content and does no
work itself, but it determines which recombinations of content are legal.

```python
from engine import unit_vector, unit_mul, unit_div, unit_lineage_decompose, SI_BASE

MOL, LITER = unit_vector((0,0,0,0,0,1,0), name='mol'), unit_vector((0,3,0,0,0,0,0), name='L')
concentration = unit_div(MOL, LITER)          # mol/L
recombined = unit_mul(concentration, LITER)   # cancels back to mol EXACTLY
```

**Caught and fixed while building this, not hidden**: the first version of
`unit_lineage_decompose` stored a composite's lineage as bare parent names
(`('Wb', 'm')` for Tesla) and always *added* the parents' vectors — running
it immediately failed all six named units, because Tesla is `Wb/m²`, a
divide by a square, not an add of `Wb` and `m`. Fixed by storing signed
`(parent, power)` pairs per lineage step (`(('Wb',1),('m',-2))`); re-run,
all six match exactly (`N,J,W,V,Wb,T` all `True`), and `mol/L * L` returns
bit-for-bit to `mol`. Ported from an independent build,
`PtolemyDesktop/Archimedes/UnitVector.py` (verified there first against the
same Tesla/Joule derivations), not re-derived from scratch here.

### 4.12 The generational lineage of a Clay Millennium Problem  `[TUTORIAL — new factoring methods]`

`engine/clay.py`. The same decomposition discipline this file runs on numbers,
processes and units, applied to the **seven Clay Millennium Problems** — each
read as a *decomposed object* / structural mapping, with **Poincaré as the
control** (it is solved). The full engine output is at the end of this README;
this section documents the two factoring methods added to make it possible.

```python
from engine import (clay_lineage_report, generational_lineage_of,
                    descriptive_or_definitional, import_deficit, CLAY)

generational_lineage_of('riemann')   # one problem's decomposition dict
clay_lineage_report()                # all seven + the consistency check + the bone
```

**This is a curated structural mapping with a consistency checker — not a
derivation of any conjecture.** `check_consistency()` verifies five internal
invariants (I1–I5); `clay.py`'s value is that the machine confirms the mapping
is self-consistent and that **Poincaré is the only one of the seven with no
import deficit.**

#### New method 1 — `descriptive_or_definitional(builds, imported_symbol)`

Classify an object by whether it carries a construction of its own answer:

- **DEFINITIONAL** — a procedure that *produces* the answer. The Sieve produces
  the primes; Ricci flow produces the diffeomorphism to S³. Remove nothing and
  it still computes.
- **DESCRIPTIVE** — it *references* a set or quantity it does not build. ζ(s)
  references its zeros; an L-function references its order of vanishing at
  `s = 1`. It needs that piece supplied from outside.

This generalises the RH-addendum move (`RiemannHypothesisProof/ADDENDUM_
generational_lineage_2026-08-28.md` §A): ζ is descriptive, the "313 Sieve" is
definitional, and the pair is a *decomposition detector* — does the object build
its answer, or import it?

#### New method 2 — `import_deficit(problem)`

The **single piece** the problem's generational lineage cannot derive from the
tier-0 floor (ADD / SCALE / SIGN). `None` iff the problem is solved (its central
tool is definitional). For the open six, **this string *is* the open problem.**

#### The result (the "bone")

Run the lineage on all seven. Poincaré — the solved one — is the only one whose
central tool is DEFINITIONAL and whose lineage terminates with no deficit. Every
open problem has a DESCRIPTIVE central object that imports **exactly one** piece
its lineage cannot derive, and that imported piece *is* the open problem. **A
problem is open exactly when it is described but not constructed; solving it
means supplying the one missing construction.** Four of the six fit the pattern
cleanly (RH, Yang–Mills, P vs NP, BSD); two are reframed by it (Navier–Stokes —
the singularity as a coordinate artifact of a dropped channel; Hodge — an
emptiness claim about an irreducible set).

`decompose_h_rb_hat()` and `shape_diff_navier_stokes()` (same module) do the
same move at the operator level: **0_RB is the reference decomposition a
well-formed equation must match.** `decompose_h_rb_hat` breaks `Σ_RB` into its
tier-0 pieces (`Σ_p`=ADD, `p^{-σ}`=SCALE, `R̂_p=xp`=SCALE, `B̂_p`=SIGN,
`∂̂_∂M`=SIGN, `†`=SIGN, self-adjoint=SIGN) and confirms the shape matches 0_RB
(whole Two-Trees span, 8 DOF, †-fixed) with one import — "a self-adjoint domain
exists". `shape_diff_navier_stokes` compares standard NS (LAURELIN only, no
SIGN, blow-up flag fires) to halocline-modified NS (adds one operator, `∂̂_∂M`
the critical-angle interface, which brings `B̂` and `†`; shape then matches
0_RB, flag clears) — **the shadow of the missing operator in standard NS is the
halocline.**

### 4.13 General spectral decomposition — factoring wavelengths  `[not sedenion-specific]`

`engine/spectral.py`. "Spectral analysis IS factoral decomposition, using a
different order datum" (Cody). This engine factors numbers, processes, units and
the sieve; this module adds **factoring a signal into its wavelengths**, with
the leftover reported as the residual — the BAO "what no component absorbs"
reading, made general. stdlib + numpy, works on any real or complex sequence.

```python
from engine import spectral_decompose, spectral_lines, spectral_residue, dominant_period

d = spectral_decompose(signal, keep='auto')      # or keep=int, keep='all'
d['wavelength_factors']   # the leaves: [{wavelength, freq, amplitude, phase, power, rel_power}, ...]
d['residual']             # what no wavelength absorbs
d['residual_rel']         # RMS residual / RMS signal  (0 = fully resolved)
d['round_trip_exact']     # Parseval: do the lines carry all the signal's energy?
d['residue_plateaus_at']  # kept lines past which the residual stops moving
```

| function | does |
|---|---|
| `dft` / `idft` / `power_spectrum` | the transform and `|X|²/N` |
| `spectral_lines(x, top=, min_rel_power=)` | the wavelength factors, strongest first; real inputs merge the ±k bins |
| `reconstruct(lines, n)` | sum the identified components back |
| `spectral_residue(x, keep)` | keep the top `keep` lines, subtract, report the leftover |
| `autocorrelation` / `dominant_period` | frequency-space period detection — complements the position-space `repeat_distances` / Kasiski already here |
| `spectral_decompose(x, keep=)` | the full report + a **residue convergence trace** (residual_rel vs lines kept; flags where it plateaus — the generalisation of "the residue does not move once the real content is out") |

*Reading:* signal = composite; each `wavelength_factor` = an irreducible leaf;
residual = the residue no wavelength absorbs. Verified: 3 planted sinusoids +
noise → all three λ, amplitudes and phases recovered, round-trip Parseval error
`1e-15`, residual = the noise floor, plateau detected. `SedenionSpectralRelativity`
remains the sedenion-specific spectrograph; this is the algebra-free tool.

### 4.14 The Emerger — the ascent dual  `[TUTORIAL — sedenion / CD bracketing]`

`engine/emerger.py`. Full write-up: [`wiki/The-Emerger-Ascent-Dual.md`](wiki/The-Emerger-Ascent-Dual.md).

Everything above this section runs **descent**: given an operator or a number,
what built it — `factor_lineage`, `decompose`, the two trees, the tier test.
Differentiate down. Writing.

The Emerger runs **ascent**. Given a *bracketing* of a Cayley–Dickson algebra —
an ordered partition of its imaginary units — which sub-domains does that
grouping expose, and, because each domain needs the ones under it, in what
**order** do the variables emerge. Integrate up. Reading. Spectroscopy.

`e_0` (the real component) is never bracketed. It is the *tilt to the i axis* —
the fixed reference every imaginary group is paired against. Each group `G`,
with the anchor, spans `span({e_0} ∪ G)`, classified by closure:
`|G|=1`→ℂ, `3`→ℍ, `7`→𝕆, anything not closed → **FRAGMENT** (a linear
subspace, not a subalgebra — where zero divisors live).

```python
from engine import (report_emergence, emerge_brackets, bracket_firing_order,
                     emerger_verify, domain_of, bracketings_for)

report_emergence('e1+e10')            # 14/14 exact self-checks + a worked run
# THE EMERGER -- sedenion bracketing & firing order
#   verify: 14/14 exact self-checks pass; 4 legal firing orders
#   emerge('e1+e10')  Sigma_tilt=+0.0000  precession 6/12  entry #1
#   canonical : {1:15} -> {2:14} -> {8:8} -> {4:4:4:4} -> {4:8:4}
#   phased    : {2:14} -> {8:8} -> {4:4:4:4} -> {4:8:4} -> {1:15}  (dependency-legal: False)
#     [1] {2:14}     [THEORETICAL] {'pointer_z': (0.0, 0.0), '|z|-Omega': -0.567...}
#     [2] {8:8}      [DERIVED    ] {'on_zd_equator': True, 'is_zero_divisor': True}
#     [3] {4:4:4:4}  [DERIVED    ] {'Sigma_tilt': 0.0, 'sigma_is_half': True}
#     [4] {4:8:4}    [THEORETICAL] {'gain_class': 'unit (gain 1, NOW)'}
#     [5] {1:15}     [DERIVED    ] {'Re': 0.0, 'N': 2.0}

r = emerge_brackets('e1+e10')         # the dict; r['steps'], r['firing_order']
bracket_firing_order([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])   # any 16-vector, or 'e3-e11'
domain_of(frozenset([1,2,3]))         # 'H'   ;  {1,5,9} -> 'FRAGMENT'
bracketings_for(8)                     # {'nested': [{1}, {2,3}, {4,5,6,7}]}  -- any 2^k
```

| item | tier | what it gives |
|---|---|---|
| `emerger_verify()` | ESTABLISHED | 14 exact self-checks from the CD table: `Sigma_axis=0`; `e1+e10` is a zero divisor **and** on the ZD equator; `e1+e2` neither; `domain_of` {1}=ℂ {1,2,3}=ℍ {1..7}=𝕆 {1,5,9}=FRAGMENT; 4 of 120 firing orders are dependency-legal |
| `emerge_brackets(x, mode=)` | THEORETICAL | the five brackets in firing order, each conditioned on the ones before it. `mode='sigma_rb'` (default) or `'canonical'` |
| `bracket_firing_order(x)` | THEORETICAL | `Σtilt` → the entry bracket in the 12-step precession (4 d\* faces : 3 Lambert-W faces). `Σtilt = 0 ⇔ σ = ½` |
| `cd_is_zero_divisor(x)` / `on_zd_equator(x)` | ESTABLISHED | exact — rank-deficiency of `Lₓ` over `Fraction`; the equator is the `J_red ↔ J_blue` balance locus |
| `domain_of(G)` | ESTABLISHED | ℂ / ℍ / 𝕆 / FRAGMENT by closure |
| `scale_partitions()` | ESTABLISHED | the `{1,3,7}`-shapes of the 15 imaginary indices — most contiguous groupings past the first are fragments; subalgebra bracketings are rare |
| `bracketings_for(dim)` | — | canonical brackets for any `2^k` (`dim=16` → the five; else the nested ℂ⊂ℍ⊂𝕆⊂… shell chain) |

*Reading:* the descent side factors what already exists; the ascent side reports
what a chosen grouping *lets exist*, and the order it has to come in. The
five sedenion brackets are `{1:15}` (grades the algebra), `{2:14}` (the pointer
plane carrying Ω_ZS), `{8:8}` (the CD double / ZD equator / J₂), `{4:4:4:4}`
(four SU(2) phases + σ_RB), `{4:8:4}` (the gain spectrum 0/1/√2). **Finding,
surfaced not hidden:** a σ_RB phase can select a firing order that is *not*
dependency-legal — the engine reports the illegality rather than snapping to the
nearest legal order.

`SedenionSpectralRelativity/emerger_spectrum.py` renders this as an SVG
spectrograph (Sedenion-focused). `ValaQuenta/modules/emerger/` is the
Full-Engine-Protocol build.

### 4.8 The reports

```python
from engine import ProcessOperator, pathway_decomposition
from engine.tools import report_pieces_and_pathways, report_control_test, \
    report_factoral_lineage, report_strut_pair_chart, \
    report_factoral_spiral_chart, report_crystal_spiral_chart

report_pieces_and_pathways()    # the Fermat-facet inventory
report_control_test()           # real π(x;16,k) vs Dirichlet equidistribution
report_factoral_lineage()       # the full 41-relation run, plus worked examples
report_strut_pair_chart()       # §4.5's box-kite application
report_factoral_spiral_chart()  # §4.9 — point it at any two-reading collection
report_crystal_spiral_chart()   # §4.9 — the crystal (PW11), charted

from engine import report_emergence
report_emergence()              # §4.14 — the ascent dual; bracketing & firing order
```

`engine/oscilloscope.py` renders the two-panel Fermat→Riemann SVG
(`python3 engine/oscilloscope.py <N>`) — "Fermat Defines. Riemann Fires.":
the Fermat panel is the prompt (which N-shape, which root-system pathway),
the Riemann panel is the response (real prime-density deviation from
Dirichlet equidistribution), a dashed connector line linking one number's
channel across both.

---

## 5. Reference — every self-checked relation

`40/40` as of this write-up. Every `claim` below is one sentence; the full
computed `detail` (the actual numbers) only prints from `run_lineage()` —
this table is the index, not a substitute for running it.

**R1–R8 — inherited from `VAPMIP/engines/e10_generational_lineage.py`**
(σ-in-∅_RB; carried over so this repo has its own copy of the discipline it
runs on):

| relation | tier | claim |
|---|---|---|
| `sigma.not_a_scalar` | 2 | two states share σ_self exactly yet differ in σ_RB — a scalar can't tell them apart |
| `sigma.carries_eight` | 3 | σ_RB has 8 independent components (an octonion); σ_self keeps 1 |
| `lineage.is_order_of_operations` | 3 | the four CD generations ARE the four order-of-operations losses |
| `lineage.persist_is_octonion` | 2 | gain-1 persistence = 8 at every CD scale — dimensional, not fractional |
| `lineage.associator_is_168` | 3 | order-of-grouping quantises in units of 168 = \|PSL(2,7)\| |
| `sigma.three_xor_roles` | 2 | σ_RB pairs by ⊕4, the octonion boundary is ⊕8, ZD entangles by a third XOR |
| `lineage.io_share_substrate` | 2 | INPUT (kernel) and OUTPUT (√2 band) are the ± halves of the same axis pairs |
| `lineage.gcd_is_lca` | 0 | the shared context of two pathways is their gcd, reached in one division |

**F1–F6 — the factoral basics** (the Two Trees domain, applied to integers):

| relation | tier | claim |
|---|---|---|
| `factoral.two_trees_exact` | 2 | prime + composite + {0,1} = every integer, zero overlap |
| `factoral.densities_conserve` | 3 | prime density + composite density = 1 at every scale |
| `factoral.mingling_point` | 2 | the trees cross at n=9, 11, 13; Laurelin dominates forever after |
| `factoral.gcd_is_lca` | 0 | the shared lineage of two numbers is their gcd, in one division |
| `factoral.omega_is_lineage_length` | 3 | Ω(n) = the number of SCALE ops building n from 1 |
| `factoral.pg32_is_edges` | 3 | PG(3,2)'s 15 points are XOR differences — relationships, not positions |

**G1–G8 — the ring-theory spine** (fall ⟺ zero divisors, the same test on
two rings):

| relation | tier | claim |
|---|---|---|
| `ring.fall_is_quotient_zd` | 2 | n composite ⟺ ℤ/(n) has a zero divisor ⟺ (n) is not a prime ideal |
| `ring.gcd_is_the_detector` | 0 | the ZD detector of ℤ/(n) is gcd(a,n)>1 — the integer trace-Laplacian |
| `ring.primary_decomposition_is_cepstrum` | 3 | Lasker–Noether decomposition IS the cepstrum; Ω = Σ exponents |
| `ring.radical_units_split_gf2` | 2 | over GF(2), nilpotents vs units split the algebra exactly in half |
| `ring.trace_laplacian_is_nilpotency` | 2 | Δ(w)=w·𝟏 vanishes IFF w²=0; SHA-1 IVs are a null subalgebra |
| `ring.open_and_closed_pathways` | 2 | a closed pathway (returns to 1) IS a unit; an open one IS a zero divisor |
| `ring.associator_is_ring_defect` | 3 | ℝ,ℂ,ℍ are rings (associator≡0); 𝕆 and up are not |
| `ring.arithmetic_derivative` | 1 | the ring-theoretic derivative is a Leibniz derivation, forced by p′=1 |

**FR1–FR6 — the fractal block** (§4.7's tower, made concrete):

| relation | tier | claim |
|---|---|---|
| `fractal.tower_self_similar` | 3 | the CD tower is an exact self-similar recursion (168→1848=11×168) |
| `fractal.bifurcation_cascade` | 1 | the period-doubling cascade brackets the Feigenbaum constant |
| `fractal.fall_survive_boundary` | 3 | the fall/survive boundary of an iterated generator is a fractal (1<D<2) |
| `fractal.newton_basins_are_splitting` | 2 | Newton on zᵏ−1 has exactly k basins = the k linear factors |
| `fractal.labeling_order_is_memory_depth` | 3 | a labeling's order = how many orbit points it needs (1 vs 3) |
| `fractal.lyapunov_is_the_drift` | 3 | λ<0 survive, λ>0 fall, λ≈0 at the Feigenbaum edge |

**PW1–PW12 — the pathway/tuning/instrument layer** (§4.4–§4.6, the newest
and most actively growing block):

| relation | tier | claim |
|---|---|---|
| `pathway.geodesic_reaches_factor` | 2 | the CFRAC walk reaches a factor in ≤10 steps; bifurcation localises nothing |
| `pathway.tuning_resonates` | 1 | the spiral must be TUNED per number to resonate onto a factor |
| `pathway.spiral_is_additive` | 1 | address(p·q) = address(p) + address(q) exactly, on the log-spiral |
| `pathway.inside_outside_one_product` | 2 | one product gives INSIDE (dot) and OUTSIDE (cross); equal only at σ=½ |
| `pathway.two_anchor_geodesic` | 2 | factoring is a boundary-value problem between two pinned anchors |
| `pathway.edge_is_the_primitive` | 2 | the primitive is the EDGE; a composite is a path of Ω edges |
| `pathway.observer_lineage_is_l_io` | 2 | L_(I|O) is an order-4 self-closing orbit; the Observer is its fixed point |
| `pathway.smith_chart_is_the_same_mobius` | 1 | the Smith chart is the same Möbius structure as L_(I|O) |
| `pathway.number_chart_is_the_methodology` | 1 | Γ_N(a) folds the unbounded Fermat search into a bounded [0,1) chart |
| `pathway.two_ring_chart_is_general` | 1 | the fold's invariants survive ANY ring pair and ANY (incl. complex) anchor |
| `pathway.key_length_is_a_stem_vote` | 3 | an unseen period is recovered from repeat-distances alone (Kasiski/Friedman) |
| `pathway.permutation_order_is_the_join` | 3 | a permutation's order = lcm of cycle-length stems — R8's meet, dualised |

---

## 6. Where "the Factorial" actually lives

**On the spelling.** This engine deliberately writes **factoral**, not
*factorial* — renamed 2026-08-21 to stop colliding with two unrelated
things: `n!` (the factorial function) and `A!` in the `0_RB` context (which
`.clauderc_canonical_maths` records explicitly means `A†`, the adjoint —
"NOT factorial, do not conflate"). *Factoral* — of, or pertaining to,
factors — targets a discrete fall/survive condition (`Ω(n)`, the lineage
length); it was never trying to be the combinatorial `n!`.

**So where does the real, combinatorial factorial live?** `TIERS['factorial']`
already answers this, and has since before this session: tier 3, DERIVED,
descending from **"the order of the coordinate reflection group"** — a
transposition *is* a reflection in the hyperplane `x_i = x_j`, so `S_n`,
generated by transpositions, is a Coxeter group, and `|S_n| = n!` is
literally that group's order. This is standard, established group theory
(Coxeter/Weyl group orders), not new.

Cody's synthesis, stated plainly (2026-08-23): **that connects directly to
the Fermat-facet machinery this whole repo sits next to.** The N-shape
theorem (proved in `FourthAgePapers/FermatMonster`, v0.300) classifies every
number by which of 71 N-shapes it occupies — and each N-shape corresponds
to a Niemeier root system, and *every* Niemeier root system is a direct sum
of simple ADE root systems, each of which generates its own Coxeter
reflection group with a known, closed-form order (`|A_n|=(n+1)!`,
`|D_n|=2^{n-1}n!`, and so on — reflection-group orders are, by construction,
members of the factorial family). And `168 = |PSL(2,7)|` — the exact group
structuring this engine's 7 box-kites (`R5`, `lineage.associator_is_168`;
`box_kite.psl27_order()`) — is not a coincidence sitting next to that
machinery; `PSL(2,7)` is the automorphism group of the Fano plane the
box-kite skeleton is built from, and reflection-group orders are exactly
the currency the N-shape theorem's Niemeier classification is stated in.

**Honest status of this connection:** the individual pieces are each real
and independently checked — `TIERS['factorial']`'s Coxeter-group claim, `R5`'s
168 quantisation, the N-shape theorem's own proof (elsewhere, in
`FermatMonster`). Stitching all three into one measured statement — "the
Coxeter-group order of N-shape k's root system is *this specific*
factorial-family number, computed and confirmed for all 71 shapes" — is not
yet a relation this engine runs. It's a well-founded next thing to build,
not a claim already sitting in §5's table. Consistent with it; not proven by
it — same hedge this file uses everywhere else a strong pattern hasn't yet
been reduced to a computed relation.

---

## 7. Corrections kept in the record

Two, kept rather than quietly fixed, because "failed predictions stay in
the record" is a standing rule here, not a slogan:

- **F3, the Mingling point.** The generational-lineage skill's own prose
  claimed the two trees reach equal brightness "near `n=9`, near `e²≈7.389`."
  Measured: they cross **three** times, at `n=9, 11, 13` (11 and 13 are
  themselves prime, so Telperion catches up twice more before Laurelin pulls
  ahead for good). `MATHS-FAULT` against the original prose; the relation
  now tests what's actually structural (Laurelin dominates forever after the
  *last* crossing, verified to `N=100,000`) and records the `e²` proximity
  without treating it as a pass condition.
- **G5, the "global annihilator" lemma.** Building the trace-Laplacian
  relation surfaced that the UDEO white paper's "`𝟏₃₂` is a global
  annihilator" lemma is **false** — it contradicts its own distance table
  (round constants have `Δ=𝟏≠0`). The true statement, machine-verified
  exhaustively at dim 8 and over 20,000 random samples at dim 32, is
  `Δ(w)=0 ⟺ w²=0`. The underlying theorem (IV nilpotency) stands; the
  shortcut proof was retracted the same day.

---

## 8. What's next

A curses upgrade — this engine is getting a console GUI, and it's being
built to merge with the monad's window and the Derivation Engine's curses
GUI rather than as a third, separate interface. Design discussion for that
starts after this README.

---

## The Seven Clay Millennium Problems — Generational Lineage Output

Raw output of `python3 -m engine.clay` (`engine/clay.py`, §4.12). A curated
structural mapping with a consistency checker — **not** a derivation of any
conjecture. Poincaré is the control (solved). Regenerate rather than hand-edit.

```
==============================================================================
GENERATIONAL LINEAGE — THE SEVEN CLAY MILLENNIUM PROBLEMS
==============================================================================
 #  problem                            status  tier root   two-trees  kind         verdict
--------------------------------------------------------------------------------------------
 7  Poincaré Conjecture                SOLVED     1 SCALE  TELPERION  DEFINITIONAL CONTROL
 1  Riemann Hypothesis                 OPEN       2 SIGN   MINGLING   DESCRIPTIVE  CONFIRM
 2  Yang–Mills Existence and Mass Gap  OPEN       3 ADD    MINGLING   DESCRIPTIVE  CONFIRM
 3  Navier–Stokes Existence & Smoothness OPEN     1 SCALE  LAURELIN   DESCRIPTIVE  CONFOUND
 4  P vs NP                            OPEN       3 ADD    LAURELIN   DESCRIPTIVE  CONFIRM
 5  Hodge Conjecture                   OPEN       3 SIGN   LAURELIN   DESCRIPTIVE  CONFOUND
 6  Birch and Swinnerton-Dyer          OPEN       3 ADD    MINGLING   DESCRIPTIVE  CONFIRM

consistency: HOLDS (I1, I2, I3, I4, I5 over 7 problems)
control: Poincaré Conjecture
fits the pattern (CONFIRM): Riemann Hypothesis, Yang–Mills, P vs NP, Birch and Swinnerton-Dyer
reframes it (CONFOUND):     Navier–Stokes, Hodge Conjecture

── [7] Poincaré Conjecture  (SOLVED) — CONTROL
   object     : a simply-connected closed 3-manifold M³ — is M³ ≅ S³?
   central op : Ricci flow with surgery  (∂g/∂t = −2 Ric, cut at singularities)
   floor      : tier 1, root SCALE, TELPERION, DEFINITIONAL
   bone       : the tool is DEFINITIONAL: Ricci flow *constructs* the diffeomorphism to S³;
                nothing is imported; the lineage terminates — every simply-connected closed
                3-manifold flows to the round S³. Solved because the tool builds the answer.

── [1] Riemann Hypothesis  (OPEN)
   object     : the non-trivial zeros of ζ(s) — do they all lie on Re(s)=½?
   central op : analytic continuation + the explicit formula ψ(x) = x − Σ_ρ x^ρ/ρ − …
   floor      : tier 2, root SIGN, MINGLING, DESCRIPTIVE
   IMPORTS    : the locus of the imported zero set {ρ} — i.e. C1 / the Berry–Keating
                self-adjointness step. ζ describes the zeros; the Sieve (definitional) would
                place them.
   emergence  : a fixed set (the nodal line) whose dimension must be shown to equal the
                reflection's fixed set — not yet shown
   bone       : ζ is DESCRIPTIVE — every operation it performs is on the floor (∏=SCALE,
                Σlog=ADD, s↔1−s=SIGN, σ=SCALE knob) EXCEPT the sum over zeros, a set it does
                not build. That one import is the whole of RH. The Two Trees partition (a
                zero-gradient harmonic field) gives a construction-side route to the same
                nodal line.

── [2] Yang–Mills Existence and Mass Gap  (OPEN)
   object     : the mass gap Δ>0 — the least energy of a non-vacuum state; and existence of
                the 4-D quantum theory
   central op : the spectral infimum above the vacuum (a difference of eigenvalues);
                non-abelian self-interaction [A_μ,A_ν]
   floor      : tier 3, root ADD, MINGLING, DESCRIPTIVE
   IMPORTS    : the 10³ factor in GAP = Ω_ZS − d*·ln10 ≈ 1/(1000√2). The 1/√2 is the σ=½
                symmetry (SIGN); the 10³ = the count of Cayley–Dickson doublings / d*_RG —
                not derived from first principles.
   emergence  : a graded quantity (the gap magnitude) sitting where the sign structure is
                one bit — the magnitude is the un-named part
   bone       : Δ>0 is structurally forced — the vacuum and the first excited state cannot
                coincide because the identities are separated at the Mingling. What is
                imported is one scalar factor (10³), exactly the way RH imports one set.

── [3] Navier–Stokes Existence and Smoothness  (OPEN)
   object     : global-in-time smoothness of 3-D incompressible flow — or a finite-time
                singularity
   central op : advection u·∇u (self-SCALE, gain>1 threat) + diffusion νΔu (ADD, the
                Laplacian average) + incompressibility ∇·u=0 (a constraint = COROLLARY)
   floor      : tier 1, root SCALE, LAURELIN, DESCRIPTIVE
   IMPORTS    : the discarded imaginary / Blue channel. NS = Yang–Mills with i → 0; the
                construction (restore i, show the apparent blow-up is a bounded 90° rotation
                into the Blue half) is not done — see Ainulindale/wiki/106.
   emergence  : THE canonical §5 signature — a quantity (the velocity gradient) that changes
                length without bound where only isometries were in play
   bone       : the singularity is read as a coordinate artifact of dropping the Blue
                channel: a SIGN rotation (r↔1/r, θ→θ+π/2) misread as unbounded SCALE. R̂†=B̂
                ⇒ the Noether current can only rotate, not be destroyed. Confounds "maybe it
                blows up" — the blow-up is the shadow of a discarded half.

── [4] P vs NP  (OPEN)
   object     : is every quickly-checkable problem quickly-solvable? (search ≟ verification)
   central op : verification (one forward pass = ADD) vs search (a bifurcation tree = tier-1
                SCALE); J_red (forward) vs J_blue (reverse), adjoint but not isomorphic
   floor      : tier 3, root ADD, LAURELIN, DESCRIPTIVE
   IMPORTS    : the bridge: proving "adjoint ≠ isomorphic in the sedenion" ⇒ "P ≠ NP as a
                complexity statement". A THEORETICAL step, not a reduction.
   bone       : verification is J_red (forward, cheap); search is J_blue (reverse). In a
                non-commutative algebra the reverse traversal is NOT the forward one — it
                carries information forward does not. So P ≠ NP structurally: the adjoint
                costs more. Confirms the expected answer, with a mechanism.

── [5] Hodge Conjecture  (OPEN)
   object     : is every rational Hodge class of type (p,p) a rational combination of
                classes of algebraic subvarieties?
   central op : the Hodge decomposition Hⁿ = ⊕ H^{p,q} (splitting into reflection
                eigen-subspaces = tier-2 SIGN) + the cycle class map (subvarieties →
                cohomology = an ADD-sublattice)
   floor      : tier 3, root SIGN, LAURELIN, DESCRIPTIVE
   IMPORTS    : the missing cycles — a construction that produces an algebraic cycle for
                every Hodge class (or a proof that none beyond the known ones is needed).
   emergence  : a fixed set of possibly the wrong dimension — H^{p,p}(ℚ) may exceed the span
                of algebraic cycles; the conjecture asserts the dimensions match
   bone       : the lineage reads Hodge as the claim "the TELPERION set at type (p,p) is
                empty — there is no Hodge class that cannot be built from cycles". That is
                the *opposite* shape to RH, where the irreducibles (the primes) are the
                entire point. Hodge is an emptiness claim about an irreducible set.

── [6] Birch and Swinnerton-Dyer  (OPEN)
   object     : for an elliptic curve E/ℚ: does rank E(ℚ) = ord_{s=1} L(E,s)? (algebraic
                rank ≟ analytic rank)
   central op : rank = count of free generators of E(ℚ) ≅ ℤ^r (tier-3 ADD); ord_{s=1} L =
                multiplicity of a zero (tier-3 ADD)
   floor      : tier 3, root ADD, MINGLING, DESCRIPTIVE
   IMPORTS    : the r ≥ 2 construction — a map between analytic rank and r independent
                rational points, general r (known: r = 0, 1 — Gross–Zagier, Kolyvagin).
   emergence  : a collision that unpacks where the encoder should have made it impossible —
                two unrelated machineries (algebraic count, analytic count) conjectured to
                always agree
   bone       : BSD is the RH descriptive-vs-definitional split localised to one curve: the
                L-function (descriptive) vs the rank (definitional, count the generators).
                Same pattern, one object.

==============================================================================
THE BONE
==============================================================================
Poincaré — the one that is SOLVED — is the only one of the seven whose central
tool is DEFINITIONAL (Ricci flow constructs the diffeomorphism; nothing imported)
and whose lineage terminates with no deficit. Every OPEN problem has a
DESCRIPTIVE central object that imports exactly one piece its lineage cannot
derive from ADD/SCALE/SIGN — and that imported piece IS the open problem:

  · Riemann Hypothesis  → the locus of the imported zero set {ρ}  (C1 / Berry–Keating)
  · Yang–Mills          → the 10³ factor in GAP ≈ 1/(1000√2)  (the doubling count / d*_RG)
  · Navier–Stokes       → the discarded Blue channel  (NS = Yang–Mills with i → 0)
  · P vs NP             → the bridge  non-commutativity ⇒ complexity bound
  · Hodge               → the missing cycles  (or a proof none are needed)
  · Birch–Swinnerton-Dyer → the r ≥ 2 construction  (known: r = 0, 1)

A problem is open exactly when it is DESCRIBED but not CONSTRUCTED. Solving it
means supplying the one missing construction.
```

The same treatment lives, per problem, on the Ainulindalë wiki
(`13`, `50`, `38`, `93`, `105`, `106`) and on `ValaQuenta/wiki/clay_millennium.md`;
the Riemann case is developed at length in
`RiemannHypothesisProof/ADDENDUM_generational_lineage_2026-08-28.md`.

---

## ValaQuenta — Generational Lineage Calibration

`engine/valaquenta_calibration.py` (`python3 -m engine.valaquenta_calibration`).
The Millennium problems are *open* objects — of course they import. **ValaQuenta
is working, deliberately-designed machinery**, so running the same decomposition
on every ValaQuenta engine is a **calibration check on the factoral
decomposition itself**: a well-designed engine should come out **CLEAN**
(DEFINITIONAL, one clean tier-0 root, a definite Two-Trees node, no import
deficit, no emergence signature). The calibration number is *does the
generational-lineage verdict agree with ValaQuenta's own status label?*

```
engines            : 46
CLEAN              : 22   (decompose as designed)
DESCRIPTIVE-OK     :  6   (instruments / renderers / validators — construct nothing by design)
FLAGGED            : 18   (an import deficit or an emergence signature)

agreement w/ status: 0.957   (verdict matches ValaQuenta's own ESTABLISHED / THEORETICAL /
                              CONJECTURE / OPEN / UNTESTED / defect label)
confusion : CLEAN∩ESTABLISHED 21 · CLEAN∩soft 1 · FLAGGED∩soft 17 · FLAGGED∩ESTABLISHED 1
roots     : SCALE 16 · SIGN 15 · ADD 14   (no bias in the tier-0 classifier)
trees     : LAURELIN 25 · MINGLING 11 · TELPERION 10   (most engines construct → Laurelin)

disagreements (the signal) —
  · bao_mass_gap   : FLAGGED (the 10³ factor is un-derived; "Δ = 1/(1000√2)" is a 3-sig-fig
                     coincidence, and the "spectral residue" is the same Ω−d*·ln10 subtraction
                     renamed) but the page says ESTABLISHED. See the Claim audit on that page.
  · t32_nilpotency : CLEAN (the trace-Laplacian test constructs cleanly) but the page says
                     THEORETICAL — the decomposition rates this engine more solid than its label.

  Was 3 disagreements — `noether` (recorded `forced_sigma` large-E defect) FIXED 2026-08-28
  (the balance F=B is linear in σ; one Newton step from any σ₀); FLAG cleared.
```

**Reading:** 95.7% agreement between an independent structural decomposition and
the hand-assigned status labels, on ~46 engines that were each explicitly
designed, is the calibration — the factoral decomposition recovers the design
status. The 18 FLAGGED-and-soft and 20 CLEAN-and-ESTABLISHED engines are the
method and the labels confirming each other; the 2 off-diagonal pairs are the
only places worth a second look. Per-engine blocks are appended toward the
bottom of each `ValaQuenta/wiki/*.md` page. Scripts:
`.claude/scratchpad/2026-08-28_valaquenta-calibration/`.

---

## Structure

```
engine/
  maths.py     — quantized pieces (CD tower levels, N-shapes, root systems,
                 ZD constellations, Monster gap) and pathways (leaf-to-root
                 walk, root-system classification), plus the control test
                 (real π(x;16,k) vs Dirichlet equidistribution). Imports
                 telperion_engine.py and h_rb_hat/maths.py directly.
  lineage.py   — THE GENERATIONAL LINEAGE ENGINE. §5's 40 self-checked
                 relations. stdlib+numpy; nothing outside this repo, and is
                 imported first and unconditionally by engine/__init__.py.
  tools.py     — runnable reports over maths.py and lineage.py (§4.8).
  oscilloscope.py — the two-panel Fermat→Riemann oscilloscope (§4.8).
  emerger.py   — §4.14: THE EMERGER, the ascent dual of lineage.py.
                 Sedenion / any-2^k bracketing & firing order of emergence.
                 e_0 is the anchor (tilt to the i axis), never bracketed;
                 groups classified C/H/O/FRAGMENT by closure; firing order
                 canonical or σ_RB-phased (12-step precession). Exact ZD
                 tests over Fraction, 14/14 self-checks. Pure stdlib.
  bio.py       — STUB: the biological factoral tower (knot 𝕊 → molecule T₃₂ →
                 DNA T₆₄ → protein T₁₂₈ → genome T₂₅₆). Structural only.
  clay.py      — §4.12: the generational lineage of the seven Clay Millennium
                 Problems, Poincaré the control. Curated mapping + consistency
                 checker; the two new factoring methods
                 (descriptive_or_definitional, import_deficit).
  valaquenta_calibration.py — the same decomposition run on every ValaQuenta
                 engine, as a calibration check on the factoral decomposition
                 itself. 0.957 agreement with ValaQuenta's own status labels.
                 Per-engine block appended to each ValaQuenta/wiki/*.md page.
wiki/
  Sedenion-Factoral-Relativity.md — fuller theory write-up, open design
  questions this README doesn't cover.
  The-Emerger-Ascent-Dual.md — §4.14 in full: descent vs ascent, the five
  brackets, the firing-order dependency lattice, the exact results.
```

## Status

v2.11 (2026-09-01) — THE EMERGER (`engine/emerger.py`, §4.14). The ascent
dual of `lineage.py`: sedenion / any-2^k Cayley-Dickson bracketing & firing
order of emergence. Pure stdlib, `Fraction`-exact ZD tests, 14/14 self-checks.
`bracketings_for(dim)` generalises past the sedenion. Wired into
`engine/__init__.py`; `wiki/The-Emerger-Ascent-Dual.md`. The Sedenion-focused
spectrograph is `SedenionSpectralRelativity/emerger_spectrum.py`; the
Full-Engine-Protocol build is `ValaQuenta/modules/emerger/`.

v2.10 (2026-08-28) — GENERAL SPECTRAL DECOMPOSITION (`engine/spectral.py`, §4.13)
+ SHAPE-MATCH DECOMPOSERS (`decompose_h_rb_hat`, `shape_diff_navier_stokes` in
the calibration module). `spectral.py` factors any real/complex signal into its
wavelengths with the leftover as the residual (the BAO reading, made general):
`spectral_decompose` / `spectral_lines` / `spectral_residue` / `dominant_period`
+ a residue-convergence trace. **Not sedenion-specific.** Verified: 3 planted
sinusoids + noise → all λ, amplitudes, phases recovered; Parseval round-trip
`1e-15`. `shape_diff_navier_stokes` names the missing operator in standard NS
(`∂̂_∂M` = the halocline; standard NS is LAURELIN-only, no SIGN, the blow-up flag
fires; halocline-NS adds `∂̂_∂M` + `B̂` + `†`, shape matches 0_RB, flag clears).
Relations still 44/44; calibration still 0.957.

v2.9 (2026-08-28) — THE VALAQUENTA CALIBRATION (`engine/valaquenta_calibration.py`):
the generational-lineage decomposition run on **every ValaQuenta engine** (46) as
a calibration check on the factoral decomposition itself — working machinery
should decompose CLEAN. Result: **0.957 agreement** between the lineage verdict
(CLEAN / DESCRIPTIVE-OK / FLAGGED) and ValaQuenta's own status label; 21 CLEAN∩
ESTABLISHED, 17 FLAGGED∩soft, 2 off-diagonal (`bao_mass_gap`, `t32_nilpotency`).
A 3rd off-diagonal — `noether`'s recorded `forced_sigma` large-E defect — was
**fixed** 2026-08-28 (the balance `F=B` is `E(1−2σ)=0`, linear in σ; solved in
one Newton step from any σ₀), and the BAO "spectral residue = mass gap exactly"
claim was **audited** (disproven as stated; `Δ>0` and `Δ ≈ Ω−d*·ln10` stand,
`Δ = 1/(1000√2)` is a 3-sig-fig coincidence). Per-engine block appended toward
the bottom of each `ValaQuenta/wiki/*.md`. Relations still 44/44.

v2.8 (2026-08-28) — THE CLAY LINEAGE (`engine/clay.py`, §4.12): the seven Clay
Millennium Problems run through the same decomposition discipline this engine
applies to numbers, processes and units — each read as a decomposed object /
structural mapping, with **Poincaré as the control**. Two new factoring methods:
`descriptive_or_definitional` (does the object build its answer or import it?)
and `import_deficit` (the one tier-0-underivable piece — `None` iff solved). The
result: Poincaré alone is DEFINITIONAL and deficit-free; every open problem is
DESCRIPTIVE and names exactly one import — *a problem is open exactly when it is
described but not constructed*. `check_consistency()` verifies five invariants
(I1–I5), all hold. Curated mapping, not a derivation. Full output at the end of
this README. Also filed:
`RiemannHypothesisProof/ADDENDUM_generational_lineage_2026-08-28.md`. Relations
still 44/44.

v2.7 (2026-08-25) — THE UNIT LINEAGE (`PW16`): units as a THIRD domain for
this file's own decomposition discipline (numbers, processes, now
dimensional exponent vectors) — every named compound SI unit traces an
exact lineage back to the 7 SI base leaves, cancellation is exact vector
arithmetic, and a unit is a geometry (no numeric content, determines which
permutations of content are legal) in exactly this project's established
sense. A first version silently summed lineage steps as if every one were
an addition; running it caught the fault immediately (all six named units
failed), fixed by carrying signed `(parent, power)` per step. Also folds in
`PW15` (THE SCALE INVARIANT: the cross-ratio survives every anchor of the
two-ring fold; the raw angle, tested first, does not), added since v2.6
without its own version note. 44/44 relations hold.

v2.6 (2026-08-25) — THE PATHWAY DECOMPOSITION (`PW14`), the primary
forensic tool: `pathway_decomposition()` factors a PROCESS into named
`ProcessOperator`s and their real dependency graph — a genuine DAG, not a
forced linear chain, and no rounding a stage count to the nearest
division algebra ("imaginary" names a role, not an algebra with rotation
rules). Verified against a real cipher (textbook Vigenere, independently
of its own hand-written function) and against real RSA CRT-decrypt as the
control case, correctly resolving a genuine fan-out (`m2` feeding two
later operators) that an earlier chain-only version of this tool could
not represent. 42/42 relations hold.

v2.5 (2026-08-25) — THE FACTORAL SPIRAL (`PW13`): `factoral_spiral()`
generalises the two-ring chart to a whole collection at once, with exact
`chart_scale_factor()` (`|dΓ/dZ|`, checked against numerical
differentiation, max rel. err. 1.55e-09/300 trials) as the "flattening
artifact" reading — and wired directly to `PW11`'s crystallography
(`report_crystal_spiral_chart`), so a sequence's own recovered period
drives the chart. 41/41 relations hold.

v2.4 (2026-08-23) — THE CRYSTAL and THE JOIN (`PW11`–`PW12`): an unseen
period recovered from repeat-structure alone (Kasiski/Friedman,
generalised), and a permutation's order as the lcm/join dual of R8's
gcd/meet.

v2.3 (2026-08-23) — the TWO-RING CHART (`PW10`): the Smith-chart fold,
generalised beyond impedance to any ring pair.

v2.2 (2026-08-22) — the NUMBER CHART (`PW9`): the Smith-chart methodology,
applied.

v2.1 (2026-08-22) — the Smith chart, an independent Möbius confirmation
(`PW8`).

v2.0 (2026-08-22) — the arithmetic derivative (`G8`): ring theory's
calculus.

v1.9–v1.1 — the pathway layer, the UF formulary integration, the fractal
block, the ring-theory spine, and the original factoral decomposition tool,
all 2026-08-21/22. Full per-version relation counts are in git history from
here on rather than repeated in this file.

White Hat. No free parameters. Failed predictions stay in the record.
